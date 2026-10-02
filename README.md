# deekayen.meshchat

[![CI](https://github.com/deekayen/ansible-role-meshchat/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-meshchat/actions/workflows/ci.yml) [![Ansible Galaxy](https://img.shields.io/badge/galaxy-deekayen.meshchat-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/deekayen/meshchat/) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive) ![BSD 3-Clause license](https://img.shields.io/badge/license-BSD%203--Clause-blue)

An Ansible role that installs [Trevor Paskett's mesh chat](http://www.trevorsbench.com/meshchat-messaging-for-mesh-networks/) on a Debian-family host, so it can serve the chat to an [AREDN](https://www.arednmesh.org/) mesh network. It installs Apache, installs the mesh chat package, and points the mesh chat CGI configuration at a zone and an AREDN node.

The role installs `apache2` and `curl` with apt, then installs `meshchat_1.02_all.deb` straight from this repository's `main` branch on GitHub. It then sets three lines in `/usr/lib/cgi-bin/meshchatconfig.pm`: `$pi_zone`, `$local_meshchat_node`, and `$meshchat_path` (always `/var/www/meshchat`).

## Requirements

- ansible-core 2.15 or newer on the controller.
- A Debian-family target. `tasks/assert.yml` fails the play when `ansible_facts.os_family` is not `Debian`.
- Outbound HTTPS from the target to `github.com` to download the package.
- A current apt cache on the target. The role does not refresh it; run `apt update` or an `ansible.builtin.apt` `update_cache` task first, as the example below does.
- Privilege escalation on the target. Run the play with `become: true`; the role installs packages and edits a file under `/usr/lib/cgi-bin`.

## Supported platforms

From `meta/main.yml`, and each one runs through Molecule in CI:

| Platform | Versions |
| --- | --- |
| Debian | 12 (bookworm), 13 (trixie) |
| Ubuntu | 22.04 (jammy), 24.04 (noble), 26.04 (resolute) |

## Installation

From Ansible Galaxy:

```bash
ansible-galaxy role install deekayen.meshchat
```

Or pin it in `requirements.yml`:

```yaml
---
roles:
  - name: deekayen.meshchat
    src: https://github.com/deekayen/ansible-role-meshchat.git
    scm: git
    version: main
```

```bash
ansible-galaxy role install -r requirements.yml
```

## Role variables

| Variable | Default | Description |
| --- | --- | --- |
| `pi_zone` | `MeshChat` | Mesh chat zone name, written to `our $pi_zone`. |
| `local_meshchat_node` | `localnode` | AREDN node that hosts the mesh chat service, written to `our $local_meshchat_node`. Set it to the node's name. |

Both values land inside single-quoted Perl strings, so `tasks/assert.yml` requires each to be non-empty and free of single quotes and backslashes. The package URL, `meshchat_deb`, is an internal value in `vars/main.yml`.

## Behavior

- The `Enable apache2.` handler sets the `apache2` service to start at boot. It runs only when the apt task installs `apache2` or `curl`, and it does not start or restart Apache.

## Dependencies

None.

## Example playbook

```yaml
---
- name: Install mesh chat for the local AREDN mesh.
  hosts: aredn_meshchat
  become: true

  pre_tasks:
    - name: Update the apt cache.
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 600

  roles:
    - role: deekayen.meshchat
      vars:
        local_meshchat_node: N0CALL-OMNI-1
```

`N0CALL-OMNI-1` is a placeholder; use the node name of your AREDN node.

## Known issues

- `tasks/main.yml:16-18` downloads this repository's own deb from the `raw/main` URL in `vars/main.yml:3` and never uses the copy in `files/meshchat_1.02_all.deb` that ships with the role. The target needs access to `github.com`, and installing a pinned release such as `1.1.0` still installs whatever deb is on `main`.
- `meshchat_deb` is in `vars/main.yml`, and the [variable precedence list](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence) puts role vars above inventory, `group_vars`, and play `vars`. To point the install at a mirror, set `meshchat_deb` as a role parameter directly on the `roles:` entry, or pass it with `-e`.

## Development

CI runs on every push to `main` and every pull request (see `.github/workflows/ci.yml`):

1. Lint: `ansible-lint --profile production` and `flake8 molecule/`.
2. Molecule: converge, idempotence, and testinfra verification in Docker against each distribution in the table above. `converge.yml` refreshes the apt cache in `pre_tasks` and sets `local_meshchat_node: N0CALL-TEST`.

To run the same checks locally with Docker available:

```bash
pip3 install ansible-core ansible-lint flake8 molecule "molecule-plugins[docker]" docker pytest-testinfra
ansible-lint --profile production
flake8 molecule/
MOLECULE_DISTRO=ubuntu2204 molecule test
```

`MOLECULE_DISTRO` selects a `geerlingguy/docker-<distro>-ansible` image. The values CI uses are `ubuntu2204`, `ubuntu2404`, `ubuntu2604`, `debian12`, and `debian13`. Set one of them explicitly, since `molecule.yml` falls back to `rockylinux9`, which the Debian assert rejects. The testinfra checks in `molecule/default/tests/test_default.py` confirm that `apache2`, `curl`, and `meshchat` are installed, `apache2` is enabled, and `meshchatconfig.pm` contains the three expected lines.

The repository also has a `.pre-commit-config.yaml`; run `pre-commit run --all-files` before pushing.

### Repository layout

| Path | Purpose |
| --- | --- |
| `tasks/main.yml` | Package installs and the three `meshchatconfig.pm` edits. |
| `tasks/assert.yml` | Debian check and input validation, tagged `always`. |
| `handlers/main.yml` | Enables `apache2` at boot. |
| `defaults/main.yml` | Every user-facing variable. |
| `vars/main.yml` | The package download URL. |
| `files/meshchat_1.02_all.deb` | Copy of the mesh chat package, stored in Git LFS. See [Known issues](#known-issues). |
| `molecule/default/` | Molecule scenario: `prepare.yml`, `converge.yml`, and testinfra tests. |
| `.github/workflows/` | `ci.yml` for lint and Molecule, `release.yml` for Galaxy import. |

## Releases

Pushing a git tag runs `.github/workflows/release.yml`, which imports the tagged commit into Ansible Galaxy as `deekayen.meshchat`. The import needs a `GALAXY_API_KEY` repository or organization secret.

## License

BSD 3-Clause. See [LICENSE](LICENSE).

## Author

[David Norman](https://github.com/deekayen), N4DKN. Sponsorship links are in [.github/FUNDING.yml](.github/FUNDING.yml).

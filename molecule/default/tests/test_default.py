import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dependencies_installed(host):
    assert host.package("apache2").is_installed
    assert host.package("curl").is_installed


def test_dependencies_service(host):
    assert host.service("apache2").is_enabled


def test_meshchat_files(host):
    assert host.file("/usr/lib/cgi-bin/meshchatconfig.pm").exists

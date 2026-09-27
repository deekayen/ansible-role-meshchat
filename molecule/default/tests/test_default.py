"""Testinfra checks for the mesh chat role."""

import pytest

CONFIG = "/usr/lib/cgi-bin/meshchatconfig.pm"


@pytest.mark.parametrize("name", ["apache2", "curl", "meshchat"])
def test_packages_installed(host, name):
    assert host.package(name).is_installed


def test_apache_enabled(host):
    assert host.service("apache2").is_enabled


@pytest.mark.parametrize(
    "line",
    [
        "our $pi_zone = 'MeshChat';",
        "our $local_meshchat_node = 'N0CALL-TEST';",
        "our $meshchat_path = '/var/www/meshchat';",
    ],
)
def test_config_lines(host, line):
    assert line in host.file(CONFIG).content_string.splitlines()

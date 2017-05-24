import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('omero-server')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'


@pytest.mark.parametrize("name", ["omero-server", "omero-web", "nginx"])
def test_services_running_and_enabled(Service, name):
    service = Service(name)
    assert service.is_running
    assert service.is_enabled


def test_postgres_not_installed(Service):
    service = Service('postgresql-9.6')
    assert not service.is_running
    assert not service.is_enabled


def test_omero_login(Command, Sudo):
    with Sudo('omero-server'):
        Command.check_output(
            '%s login -C -s localhost -u root -w omero' % OMERO)

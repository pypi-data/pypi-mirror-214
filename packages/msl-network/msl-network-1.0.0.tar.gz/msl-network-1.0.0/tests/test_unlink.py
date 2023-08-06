import threading

import pytest

import conftest
from msl.examples.network import Echo
from msl.network import LinkedClient
from msl.network import connect
from msl.network.manager import run_services


def test_unlink_client_max1():

    manager = conftest.Manager(Echo, max_clients=1)

    cxn1 = connect(**manager.kwargs)
    cxn2 = connect(**manager.kwargs)

    link1 = cxn1.link('Echo')
    assert repr(link1).startswith("<Link with Echo[")
    assert link1.service_name == 'Echo'
    assert link1.echo(1, x=2) == [[1], {'x': 2}]

    # the same Client can re-link to the same Service
    link1b = cxn1.link('Echo')
    assert link1b is not link1
    assert link1b.service_name == 'Echo'
    assert link1b.echo(1, x=2) == [[1], {'x': 2}]

    # another Client cannot link
    with pytest.raises(RuntimeError, match=r'The maximum number of Clients are already linked'):
        cxn2.link('Echo')

    link1.unlink()
    assert repr(link1).startswith("<Un-Linked from Echo[")
    assert link1._client is None
    with pytest.raises(AttributeError, match=r"Cannot access 'echo' since the link has been broken"):
        link1.echo(1)

    # another Client can now link
    link2 = cxn2.link('Echo')
    assert link2.service_name == 'Echo'
    assert link2.echo(1, x=2) == [[1], {'x': 2}]

    link2.unlink()
    assert link2._client is None
    with pytest.raises(AttributeError, match=r"Cannot access 'echo' since the link has been broken"):
        link2.echo(1)

    # un-linking multiple times is okay
    for i in range(20):
        link2.unlink()
        link2.disconnect()  # an alias for unlink

    manager.shutdown(connection=cxn1)

    # shutting down the manager using cxn1 will also disconnect cxn2
    assert not cxn1.is_connected()
    assert not cxn2.is_connected()


def test_unlink_client_max10():

    manager = conftest.Manager(Echo, max_clients=10)

    clients = [connect(**manager.kwargs) for _ in range(10)]
    links = [client.link('Echo') for client in clients]
    for link in links:
        assert link.service_name == 'Echo'
        assert link.echo(1, x=2) == [[1], {'x': 2}]

    cxn = connect(**manager.kwargs)

    # another Client cannot link
    with pytest.raises(RuntimeError, match=r'The maximum number of Clients are already linked'):
        cxn.link('Echo')

    links[0].unlink()
    assert links[0]._client is None
    with pytest.raises(AttributeError, match=r"Cannot access 'echo' since the link has been broken"):
        links[0].echo(1)

    # another Client can now link
    link2 = cxn.link('Echo')
    assert link2.service_name == 'Echo'
    assert link2.echo(1, x=2) == [[1], {'x': 2}]

    link2.unlink()
    assert link2._client is None
    with pytest.raises(AttributeError, match=r"Cannot access 'echo' since the link has been broken"):
        link2.echo(1)

    manager.shutdown(connection=cxn)

    # shutting down the manager using cxn will also disconnect all clients
    for client in clients:
        assert not client.is_connected()


def test_unlink_linkedclient_max10():

    class ShutdownableEcho(Echo):

        def __init__(self):
            super(ShutdownableEcho, self).__init__(max_clients=10)

        def shutdown_service(self):
            pass

    port = conftest.Manager.get_available_port()

    run_thread = threading.Thread(
        target=run_services,
        args=(ShutdownableEcho(),),
        kwargs={'port': port, 'log_file': conftest.Manager.log_file}
    )
    run_thread.start()

    # wait for the Manager to be running
    conftest.Manager.wait_start(port, 'Cannot connect to manager')

    linked_clients = [LinkedClient('ShutdownableEcho', port=port, name='foobar%d' % i) for i in range(10)]

    for i, link in enumerate(linked_clients):
        assert link.service_name == 'ShutdownableEcho'
        assert link.name == 'foobar%d' % i
        assert link.echo(1, x=2) == [[1], {'x': 2}]

    # creating another LinkedClient is not allowed
    with pytest.raises(RuntimeError, match=r'The maximum number of Clients are already linked'):
        LinkedClient('ShutdownableEcho', port=port, name='foobar10')

    linked_clients[0].unlink()
    assert linked_clients[0]._link is None
    with pytest.raises(AttributeError, match=r"Cannot access 'echo' since the link has been broken"):
        linked_clients[0].echo(1)

    # another LinkedClient can now be created
    link2 = LinkedClient('ShutdownableEcho', port=port, name='foobar10')
    assert link2.service_name == 'ShutdownableEcho'
    assert link2.name == 'foobar10'
    assert link2.echo(1, x=2) == [[1], {'x': 2}]
    assert repr(link2).startswith('<Link[name=foobar10]')
    link2.unlink()
    assert link2._link is None
    assert repr(link2).startswith('<Un-Linked[name=foobar10]')
    with pytest.raises(AttributeError, match=r"Cannot access 'echo' since the link has been broken"):
        link2.echo(1)

    # un-linking the LinkedClient multiple times is okay
    for i in range(20):
        link2.unlink()
    link2.disconnect()  # a linkedClient can disconnect the Client via self._client

    # shutdown the ShutdownableEcho Service and disconnect the LinkedClient
    # from the Manager, the second item in the LinkedClient list is still linked
    # and can therefore still send requests
    assert linked_clients[1].service_name == 'ShutdownableEcho'
    assert linked_clients[1].name == 'foobar1'
    assert linked_clients[1].echo(1, x=2) == [[1], {'x': 2}]
    linked_clients[1].shutdown_service()
    linked_clients[1].disconnect()

    # this LinkedClient was already unlinked but calling disconnect should not raise an error
    linked_clients[0].disconnect()

    # once the ShutdownableEcho shuts down, the Manager also automatically shuts down
    # since the ShutdownableEcho was started using the run_services() function
    for client in linked_clients[2:]:
        client.disconnect()  # can still disconnect
        client.disconnect()  # even multiple times
        client.disconnect()
        client.disconnect()
        client.disconnect()

    # the `run_services` function will block the unittests forever if a
    # LinkedClient does not shut down ShutdownableEcho
    run_thread.join()

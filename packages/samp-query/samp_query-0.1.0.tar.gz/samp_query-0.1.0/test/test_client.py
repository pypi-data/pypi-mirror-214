from samp_query import Client


async def test_connect() -> None:
    client = Client('tms-server.com', 7777)
    assert client.ip == 'tms-server.com'
    assert client.port == 7777
    assert client.rcon_password is None
    assert not client._socket
    assert not client.prefix

    await client.connect()

    assert client.ip == '192.168.0.1'  # FIXME: Resolver
    assert client._socket
    assert client.prefix

    client._socket.close()  # FIXME: Automatic somehow

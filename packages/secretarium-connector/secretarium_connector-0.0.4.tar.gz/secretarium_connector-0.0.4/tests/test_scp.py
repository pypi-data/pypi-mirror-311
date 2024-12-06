import asyncio
from secretarium_connector import SCP, Key

async def test_scp():

    print(f"TEST: Starting tests")
    key = await Key.createKey()
    scp = SCP()

    # context = await scp.connect("wss://gimli4.node.secretarium.org:9430", key)
    context = await scp.connect("wss://klave-dev.secretarium.org", key)
    tx = context.newTx("wasm-manager", "list-app", None, {
        "key": "value"
    })
    
    print(f"TEST: Registering listeners")

    tx.onError(lambda message: print(f"LMB Error: {message}"))
    tx.onResult(lambda message: print(f"LMB Result 1: {message}"))
    tx.onResult(lambda message: print(f"LMB Result 2: {message}"))

    print(f"TEST: Sending data")

    await tx.send()
    # asyncio.as_completed([tx.send()])

    print(f"TEST: Waiting for results")

asyncio.run(test_scp())
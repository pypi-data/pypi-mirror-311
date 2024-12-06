import asyncio
from clients.kucoin import KuCoin
from clients.bybit import Bybit


async def kucoin_test_api(exchange: KuCoin):
    print(await exchange.request(
        path="/api/v1/market/stats",
        params={"symbol": "BTC-USDT"}
    ))
    print(await exchange.request(
        method="POST",
        path="/api/v1/orders/test",
        signed=True,
        data={
            "clientOid": "123",
            "symbol": "BTC-USDT",
            "side": "buy",
            "type": "market",
            "funds": "5"
        }
    ))


async def bybit_test_api(exchange: Bybit):
    print(await exchange.request(
        path="/v5/market/tickers",
        params={
            "category": "spot",
            "symbol": "BTCUSDT"
        }
    ))
    print(await exchange.request(
        path="/v5/account/info",
        signed=True
    ))


async def main():
    exchange = KuCoin()
    # exchange = KuCoin(
    #     api_key="66d3241512f9dd0001388d27",
    #     secret="6f951c6e-7015-4050-845a-19239bf9b1c9",
    #     passphrase="kilopkilop"
    # )
    # exchange = Bybit(
    #     api_key="nXNzKoSTs8DCk7X7Bd",
    #     secret="wByVmG6TGJCFo3z5KHVJZz9va6crcOjyqHjZ"
    # )
    # exchange = Bybit(
    #     api_key="G6zWBrUPaPA7nVaIgN",
    #     private_key="/Users/ren3104/Documents/Projects/GitHub/pycryptoex/test_space/private_rsa.key"
    # )
    async with exchange:
        ...

        ws = await exchange.create_websocket_stream()
        await ws.start()

        async def _handler(data):
            print(data)

        try:
            # asyncio.ensure_future(ws.restart())

            await ws.subscribe_callback("/market/candles:BTC-USDT_1min", _handler)

            await asyncio.sleep(5)

            await ws.stop()

            await asyncio.sleep(1)

            print(await exchange.request(
                path="/api/v1/market/stats",
                params={"symbol": "BTC-USDT"}
            ))

            while not ws.closed:
                await asyncio.sleep(0.1)
        finally:
            await ws.stop()



        # for _ in range(10):
        #     await exchange.request("/api/v1/market/stats?symbol=BTC-USDT")


asyncio.run(main())

from vulcan import Keystore
from vulcan import Account
from vulcan import Vulcan
import json
import asyncio

async def main():
    #tworzenie klucza (przez dostep zdalny na dzienniku UONET)
    keystore = await Keystore.create(device_model="Vulcan API")
    #zmienne przepisane z panelu Dostep Zdalny w dzienniku UONET
    token = '3S1KFFD'
    symbol = 'opole'
    pin = '355482'
    #rejestrowanie konta(urządzenia) w dzienniku UONET !!!TY WPISZ SWOJE!!!
    account = await Account.register(keystore, token, symbol, pin)
    #zapisywanie klucza w pliku json 
    with open("keystore.json", "w") as f:
        f.write(keystore.as_json)
    #zapisywanie informacji o koncie w pliku json 
    with open("account.json", "w") as f:
        f.write(account.as_json)

#wykonanie funkcji
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
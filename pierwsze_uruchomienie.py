from vulcan import Keystore
from vulcan import Account
from vulcan import Vulcan
import json
import asyncio
import os


async def main():
    os.system('cls')
    # próbuje cos zrobic, niewazne
    login_list = []
    f = open("data/uonet_pass.txt", "r")
    for line in f:
        login_line = str(line)
        removed_suffix = login_line.removesuffix("\n")
        if removed_suffix != ' ':
            login_list.append(removed_suffix)
        # print(line, end="")
    # print(login_list)
    # tworzenie klucza (przez dostep zdalny na dzienniku UONET)
    keystore = await Keystore.create(device_model="Vulcan API")
    # zmienne przepisane z panelu Dostep Zdalny w dzienniku UONET
    token = login_list[0]
    symbol = login_list[1]
    pin = login_list[2]
    # rejestrowanie konta(urządzenia) w dzienniku UONET !!!TY WPISZ SWOJE!!!
    account = await Account.register(keystore, token, symbol, pin)
    # zapisywanie klucza w pliku json
    with open("keystore.json", "w") as f:
        f.write(keystore.as_json)
    # zapisywanie informacji o koncie w pliku json
    with open("account.json", "w") as f:
        f.write(account.as_json)

# wykonanie funkcji
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

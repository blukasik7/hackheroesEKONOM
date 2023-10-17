from vulcan import *
import asyncio


#wczytywanie danych o koncie ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\Users\lukas\Desktop\VULCAN API\account.json") as f:
    account = Account.load(f.read())
#wczytywanie klucza ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\Users\lukas\Desktop\VULCAN API\keystore.json") as f:
    keystore = Keystore.load(f.read())


async def main():
    client = Vulcan(keystore, account)
    await client.select_student()

    print(client.student)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

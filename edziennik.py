from vulcan import *
import asyncio
import vulcan
from datetime import datetime
import os

# wczytywanie danych o koncie ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\account.json") as f:
    account = Account.load(f.read())
# wczytywanie klucza ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\keystore.json") as f:
    keystore = Keystore.load(f.read())


async def main():
    # czysci terminal za kazdym razem
    os.system('cls')
    # tworzenie obiektu Vulcan
    client = Vulcan(keystore, account)
    await client.select_student()

    # ustala obecną date
    present = datetime.now()

    # pobiera info o sprawdzianach do zmiennej
    exam = await client.data.get_exams()
    # pusta lista na tematy sprawdzianów
    exam_list = []

    async for ex_info in exam:
        # kod odpowiedzialny za dodawanie tylko tych sprawdzianow, ktorych jeszcze nie bylo
        str_date_deadline = str(ex_info.deadline)
        dtt_date_deadline = datetime.strptime(
            str_date_deadline, '%Y-%m-%d %H:%M:%S')

        if (present <= dtt_date_deadline):
            exam_topic = str(ex_info.topic)

            exam_list.append(exam_topic)

    print(exam_list)
    print(len(exam_list))
    #dodaje tylko pierwszy element listy do HTMLA a ma dodawać wszystkie
    def print_loop(list: list):
        list_length = len(list)
        for i in range(0, list_length):
            list_str = str(list[i])
            return [list_str]

    print(print_loop(exam_list))

    html_template = "<!DOCTYPE html> <html><head><meta charset="+'"UTF-8">' + \
        "</head><body>" + str(print_loop(exam_list)) + "</body> </html>"
    web_doc = open('website.html', "w", encoding="utf-8")
    web_doc.write(html_template)
    await client.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

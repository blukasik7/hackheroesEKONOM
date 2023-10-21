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

    # próba odczytywania tematów lekcji z dnia poprzedniego
    lessons = await client.data.get_lessons()
    async for lesson in lessons:

        print(lesson.event)
        print(lesson.subject.name)

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

            exam_list.append(exam_topic+'\n')

    # zwraca wartosc wszystkich indeksow z listy

    def return_all(list: list):
        return ''.join(map(str, list))

    print(return_all(exam_list))
    all_exams = return_all(exam_list)

    exam_doc = open('exams.txt', "w", encoding="utf-8")
    exam_doc.write(all_exams)
    await client.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

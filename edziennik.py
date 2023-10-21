from vulcan import *
import asyncio
import vulcan
import datetime
import os
import timedelta
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
    # print(client.student.unit)
    # ustala obecną i wczorajsza date
    present = datetime.datetime.today()
    yesterday = present - datetime.timedelta(days=1)

    lessons_topics_list = []
    # pobiera frekwencję i przedmioty z dnia poprzedniego a następnie tematy lekcji
    attendance = await client.data.get_attendance(date_from=yesterday)
    async for attend in attendance:
        lessons_topics_list.append(attend.topic)
        # print(attend.subject.name +' : ' + attend.topic)

    # pobiera imie i nazwisko ucznia
    name = client.student.full_name
    print(name)
    name_doc = open('data/name.txt', 'w', encoding="utf-8")
    name_doc.write(name)
    name_doc.close()
    # próba odczytywania tematów lekcji z dnia poprzedniego
    # lessons = await client.data.get_lessons(date_from=yesterday)
    # async for lesson in lessons:
    #
    #   print(lesson.subject.name)
    # pobiera info o sprawdzianach do zmiennej
    exam = await client.data.get_exams()
    # pusta lista na tematy sprawdzianów
    exam_list = []

    async for ex_info in exam:
        # kod odpowiedzialny za dodawanie tylko tych sprawdzianow, ktorych jeszcze nie bylo
        str_exam_deadline = str(ex_info.deadline)
        exam_deadline = datetime.datetime.strptime(
            str_exam_deadline, '%Y-%m-%d %H:%M:%S')

        if (present <= exam_deadline):
            exam_topic = str(ex_info.topic)

            exam_list.append(exam_topic+'\n')

    # zwraca wartosc wszystkich indeksow z listy

    def return_all(list: list):
        return ''.join(map(str, list))

    print(return_all(exam_list))
    all_exams = return_all(exam_list)

    exam_doc = open('data/exams.txt', "w", encoding="utf-8")
    exam_doc.write(all_exams)
    exam_doc.close()
    await client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

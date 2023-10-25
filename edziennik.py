from vulcan import *
import asyncio
import vulcan
import datetime
import os
import timedelta
import g4f
import os.path
# wczytywanie danych o koncie ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\account.json") as f:
    account = Account.load(f.read())
# wczytywanie klucza ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\keystore.json") as f:
    keystore = Keystore.load(f.read())

def check_exist(file_name):
    if os.path.exists(file_name):
        return True;
    else:
        return False;
    
def return_all(list: list):
    return '\n'.join(map(str, list))
def remove_special(string:str):
    string = string.replace('"', '')
    string = string.replace('/', "")
    string = string.replace("!", "")
    string = string.replace('*', "")
    string = string.replace('%', "")
    string = string.replace('(', "")
    string = string.replace(')', "")
    string = string.replace('^', "")
    string = string.replace('#', "")
    string = string.replace('$', "")
    string = string.replace('@', "")
    return string

async def main():
    # czysci terminal za kazdym razem
    os.system('cls')

    # tworzenie obiektu Vulcan
    client = Vulcan(keystore, account)
    await client.select_student()
    # print(client.student.unit)
    # ustala daty
    present = datetime.datetime.today()
    yesterday = present - datetime.timedelta(days=1)
    twodago = present - datetime.timedelta(days=2)

    lessons_topics_list = []

    # pobiera frekwencję i przedmioty z dnia poprzedniego a następnie tematy lekcji
    attendance = await client.data.get_attendance(date_from=present)
    async for attend in attendance:
        lessons_topics_list.append(attend.topic)
        # print(attend.subject.name +' : ' + attend.topic)
    lessons_doc = open('data/todays_lessons.txt', 'w', encoding="utf-8")
    if (return_all(lessons_topics_list) != ""):
        lessons_doc.write(return_all(lessons_topics_list)+'\n')
        lessons = (return_all(lessons_topics_list)+'\n')

    else:
        lessons_doc.write("Dzisiaj nie ma lekcji! Ciesz się dniem wolnym =)")

    # pobiera imie i nazwisko ucznia
    name = client.student.full_name
    print(name)
    name_doc = open('data/name.txt', 'w', encoding="utf-8")
    name_doc.write(name)
    name_doc.close()

    exam = await client.data.get_exams()
    # pusta lista na tematy sprawdzianów
    global exam_list
    exam_list = []

    async for ex_info in exam:
        # kod odpowiedzialny za dodawanie tylko tych sprawdzianow, ktorych jeszcze nie bylo
        str_exam_deadline = str(ex_info.deadline)
        exam_deadline = datetime.datetime.strptime(
            str_exam_deadline, '%Y-%m-%d %H:%M:%S')

        if (present <= exam_deadline):
            exam_topic = str(ex_info.topic)
            exam_topic = remove_special(exam_topic)
            exam_list.append(exam_topic)

    print(return_all(exam_list))
    all_exams = return_all(exam_list)

    exam_doc = open('data/exams.txt', "w", encoding="utf-8")
    exam_doc.write(all_exams)
    exam_doc.close()

    html_template = '<!DOCTYPE html>\
                        <html>\
                        <head>\
                            <meta charset="utf-8">\
                        </head>\
                        <body>\
                            <p>'+all_exams+'  </p>\
                        </body>\
                        </html>'

    html = open('website.html', 'w', encoding="utf-8")
    html.write(html_template)

    await client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # GENEROWANIE NOTATEK

    _providers = [
        g4f.Provider.GptGo,
        # g4f.Provider.You
    ]
    
    async def run_provider(provider: g4f.Provider.BaseProvider):
        for i in range (len(exam_list)):
            if not(check_exist("notes/"+str(exam_list[i])+'.txt')):
                try:
                    response = await g4f.ChatCompletion.create_async(
                        model=g4f.models.gpt_35_turbo,
                        messages=[
                            {"role": "user", "content": "Wygeneruj notatkę dzięki której uczeń przygotuje się na sprawdzian z tematu:" + exam_list[i] + "."}],
                        provider=provider
                    )
                    print(response)
                    with open("notes/"+str(exam_list[i])+'.txt', 'w', encoding="utf-8") as plik:
                        plik.write(str(response))
                except Exception as e:
                    print(f"{provider.__name__}:", e)
            else:
                print("Notatka już istnieje!")

    async def run_all():
        calls = [
            run_provider(provider) for provider in _providers
        ]
        await asyncio.gather(*calls)

    asyncio.run(run_all())
    print('___________________________________koniec__________________________________________________')

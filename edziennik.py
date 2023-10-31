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
        return True
    else:
        return False


def return_all(list: list):
    return '\n'.join(map(str, list))


def remove_special(string):
    specials_list = ['"', '#', '%', '&', '*', ':', '<', '>', '?']
    for i in range(len(specials_list)):
        string = string.replace(specials_list[i], "")

    return str(string)


def generate_objects(list):
    obj_sum = ""
    for i in range(len(list)):

        path = exam_list[i]+'''.html'''
        obj = '''<object
            data="notes/'''+str(path)+'''"
            style="width: 100%; height: 100%;display:none"
             id='''+chr(65+i)+'''
            >
            </object>'''

        obj_sum += str(obj)
    return str(obj_sum)

def generate_topic_paragraph(list:list):
    p_ids = [
        "pierwszy",
        "drugi",
        "trzeci",
        "czwarty",
        "piaty",
        "szosty",
        "siodmy",
        "osmy",
      ];
    paragraphs =""
    for i in range(len(list)):
        topic = exam_list[i]
        paragraph = '''<p style="display:none;" id="'''+p_ids[i]+'''">'''+str(topic)+'''</p>'''
        paragraphs+=paragraph
    return str(paragraphs)

async def main():
    # czysci terminal za kazdym razem
    os.system('cls')

    # tworzenie obiektu Vulcan
    client = Vulcan(keystore, account)
    await client.select_student()
    student = await client.select_student()
    # print(client.student.unit)
    # ustala daty
    present = datetime.datetime.today()
    yesterday = present - datetime.timedelta(days=1)
    twodago = present - datetime.timedelta(days=2)

    lessons_topics_list = []

    # attendance = await client.data.get_attendance();
    # async for attend in attendance:
    #    print(attend.topic)
    lessons = await client.data.get_lessons(date_from=yesterday, date_to=yesterday)
    async for lesson in lessons:
        print(lesson.subject)

    # pobiera imie i nazwisko ucznia
    # name = client.student.full_name
    # print(name)
    # name_doc = open('data/name.txt', 'w', encoding="utf-8")
    # name_doc.write(name)
    # name_doc.close()

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

    # html_template = '<!DOCTYPE html>\
    #                    <html>\
    #                    <head>\
    #                        <meta charset="utf-8">\
    #                    </head>\
    #                    <body>\
    #                        <p>'+all_exams+'  </p>\
    #                    </body>\
    #                    </html>'

    # html = open('website.html', 'w', encoding="utf-8")
    # html.write(html_template)

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
        for i in range(len(exam_list)):
            def replace_empty_lines(text):
                text = text.replace('\n', '<br>')
                return str(text)

            if not (check_exist("notes/"+str(exam_list[i])+'.html')):
                try:
                    response = await g4f.ChatCompletion.create_async(
                        model=g4f.models.gpt_35_turbo,
                        messages=[
                            {"role": "user", "content": "Wygeneruj notatkę dzięki której uczeń przygotuje się na sprawdzian z tematu:" + exam_list[i] + "."}],
                        provider=provider
                    )
                    print(response)
                    with open("notes/"+str(exam_list[i])+'.html', 'w', encoding="utf-8") as plik:

                        plik.write(
                            '<!DOCTYPE html><html><head><meta charset="utf-8"><link rel = "stylesheet" href="notes.css"></head><body>'+replace_empty_lines(str(response))+'</body></html>')

                except Exception as e:
                    print(f"{provider.__name__}:", e)
            else:
                print("Notatka już istnieje!")
        with open('website2.html', 'w', encoding="utf-8") as website:
            website.write('''<!DOCTYPE html> <html> <head> <meta charset="utf-8" /> <link href="styl.css" type="text/css" rel="stylesheet" /> </head> <body> <h1 class="przedmiot">Podstawy przedsiębiorczości</h1>'''+generate_topic_paragraph(exam_list)+''' <br /> <div id="left_arrow"><img src="arrow.png" alt="arrow" /></div> <main>'''+generate_objects(exam_list)+''' </main> <div id="right_arrow"><img src="arrow.png" alt="arrow" /></div> <div id="circles_div"></div> <script> var ilosc_plikow = 6; var NumberOfCircles = ilosc_plikow; var circles_div = document.getElementById("circles_div"); var currentCard = 0; r_arrow = document.getElementById("right_arrow"); l_arrow = document.getElementById("left_arrow"); r_arrow.addEventListener("click", r_arrow_click, false); l_arrow.addEventListener("click", l_arrow_click, false); function r_arrow_click() { console.log("Nacisnąłeś prawą strzałkę"); if (currentCard + 1 < ilosc_plikow) { var div = document.getElementById("circles_div"); var kolka = div.getElementsByTagName("div"); kolka[currentCard].style.background = "white"; kolka[currentCard + 1].style.background = "black"; document.getElementById(ids[currentCard]).style.display = "none"; document.getElementById(ids[currentCard + 1]).style.display = "block"; for (var i = 0; i < ilosc_plikow + 1; i++) { if ((previous_paragraph = document.getElementById(p_ids[i]))) { previous_paragraph.style.display = "none"; } } current_paragraph = document.getElementById(p_ids[currentCard + 1]); current_paragraph.style.display = "block"; currentCard++; } } function l_arrow_click() { console.log("Nacisnąłeś lewą strzałkę"); if (currentCard > 0) { var div = document.getElementById("circles_div"); var kolka = div.getElementsByTagName("div"); kolka[currentCard].style.background = "white"; kolka[currentCard - 1].style.background = "black"; document.getElementById(ids[currentCard]).style.display = "none"; document.getElementById(ids[currentCard - 1]).style.display = "block"; for (var i = 0; i < ilosc_plikow + 1; i++) { if ((previous_paragraph = document.getElementById(p_ids[i]))) { previous_paragraph.style.display = "none"; } } current_paragraph = document.getElementById(p_ids[currentCard - 1]); current_paragraph.style.display = "block"; currentCard--; } } for (let i = 0; i < NumberOfCircles; i++) { const circle = document.createElement("div"); circle.setAttribute("id", "circle" + i.toString() + ""); circles_div.appendChild(circle); circle.addEventListener("click", CircleFunction, false); circle.name = i; } ids = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]; p_ids = [ "pierwszy", "drugi", "trzeci", "czwarty", "piaty", "szosty", "siodmy", "osmy", ]; function display_first() { element = document.getElementById(ids[0]); element.style.display = "block"; first_circle = document.getElementById("circle0"); first_circle.style.background = "black"; } display_first(); function CircleFunction() { current_paragraph = document.getElementById(p_ids[this.name]); current_paragraph.style.display = "block"; console.log( "Wywolales funkcję: CircleFunction poprzez naciśnięcie kółka z ID: " + this.name ); currentCard = this.name; element = document.getElementById(ids[this.name]); element.style.display = "block"; var div = document.getElementById("circles_div"); var kolka = div.getElementsByTagName("div"); for (var i = 0; i < kolka.length; i++) { kolka[i].style.background = "white"; } this.style.background = "black"; for (var i = 0; i < ilosc_plikow + 1; i++) { if (i != this.name) { previous = document.getElementById(ids[i]); other_paragraphs = document.getElementById(p_ids[i]); other_paragraphs.style.display = "none"; previous.style.display = "none"; } } } </script> </body> </html> ''')
    async def run_all():
        calls = [
            run_provider(provider) for provider in _providers
        ]
        await asyncio.gather(*calls)

    asyncio.run(run_all())
    print('___________________________________koniec__________________________________________________')

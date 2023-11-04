from vulcan import *
import asyncio
import vulcan
import datetime
import os
import timedelta
import g4f
import os.path
import re
import time
from winotify import Notification, audio
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


def generate_topic_paragraph(list):
    p_ids = [
        "pierwszy",
        "drugi",
        "trzeci",
        "czwarty",
        "piaty",
        "szosty",
        "siodmy",
        "osmy",
    ]
    paragraphs = ""
    for i in range(len(list)):
        topic = list[i]
        paragraph = '''<p style="display:none;" id="''' + \
            p_ids[i]+'''">'''+str(topic)+'''</p>'''
        paragraphs += paragraph
    return str(paragraphs)


def generate_exam_subject(list):
    sub_ids = ["first", "second", "third", "fourth",
               "fifth", "sixth", "seventh", "eighth"]
    subjects = ""
    for i in range(len(list)):
        subject = list[i]
        subject_text = '''<h1 style="margin-top:90px;color:white;display:none;" id="''' + \
            sub_ids[i]+'''">'''+str(subject)+'''</h1>'''
        subjects += subject_text
    return str(subjects)


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

    lucky_number = await client.data.get_lucky_number(present)
    if (lucky_number.number != 0):
        print("Dzisiejszy szczęśliwy numerek to: " +
              str(lucky_number.number)+"\n")
        number = lucky_number.number

    else:
        number = "Brak"
        print("Dzisiaj nie ma szczęśliwego numerka \n")

    lessons_topics_list = []

    # attendance = await client.data.get_attendance();
    # async for attend in attendance:
    #    print(attend.topic)
    # lessons = await client.data.get_lessons(date_from=yesterday, date_to=yesterday)
    # async for lesson in lessons:
    #    print(lesson.subject)

    name = client.student.full_name
    print(name)
    # name_doc = open('data/name.txt', 'w', encoding="utf-8")
    # name_doc.write(name)
    # name_doc.close()

    exam = await client.data.get_exams()
    # pusta lista na tematy sprawdzianów
    global exam_list
    exam_list = []
    global exam_subjects
    exam_subjects = []
    global exam_deadlines
    exam_deadlines = []
    async for ex_info in exam:
        # kod odpowiedzialny za dodawanie tylko tych sprawdzianow, ktorych jeszcze nie bylo
        str_exam_deadline = str(ex_info.deadline)

        exam_deadline = datetime.datetime.strptime(
            str_exam_deadline, '%Y-%m-%d %H:%M:%S')

        if (present <= exam_deadline):
            exam_deadlines.append(exam_deadline)
            exam_topic = str(ex_info.topic)
            exam_topic = remove_special(re.sub(r'http\S+', '', exam_topic))
            exam_list.append(str(str.replace(exam_topic, '\n', '')))
            exam_subject = str(ex_info.subject.name)
            exam_subjects.append(exam_subject)
    print(return_all(exam_list))
    all_exams = return_all(exam_list)

    exam_doc = open('data/exams.txt', "w", encoding="utf-8")
    exam_doc.write(all_exams)
    exam_doc.close()
    with open("hub.html", "w", encoding="utf-8") as hub:
        hub.write('''<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset="utf-8" />\n    <meta http-equiv="X-UA-Compatible" content="IE=edge" />\n    <title>Hub</title>\n    <meta name="description" content="" />\n <meta charset="UTF-8">\n    <meta name="author" content="Remigiusz Łukasik, Bartosz Łukuasik, Jacek Dombrowski, Jakub Namyślak, Łukasz Piechaczek">\n    <meta name="owner" content="Remigiusz Łukasik, Bartosz Łukuasik, Jacek Dombrowski, Jakub Namyślak, Łukasz Piechaczek">\n    <meta name="rating" content="General">\n    <meta name='HandheldFriendly' content='True'>\n    <meta name='copyright' content='Remigiusz Łukasik, Bartosz Łukuasik, Jacek Dombrowski, Jakub Namyślak, Łukasz Piechaczek'>\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <link rel="stylesheet" href="hub_style.css" />\n  </head>\n  <body>\n    <div class="szczesliwy_nr">Szczęśliwy numerek: <b> '''+str(number)+'''</b></div>\n    <div class="main">\n      <div class="user_welcome">\n        <h1>Cześć,</h1>\n        <p>'''+str(name)+'''</p>\n      </div>\n      <br />\n      <div class="exams_info">Masz zapowiedziane '''+str(len(exam_list)) +
                  ''' sprawdzianów!</div>\n    </div>\n    <div class="kafelki">\n      <div class="kafelek">\n        <center>\n          <img\n            id="notification"\n            src="data/svg/notification_logo.svg"\n            alt="Powiadomienia"\n            onclick="changeImage()"\n          />\n        </center>\n      </div>\n      <a href="website2.html"><div class="kafelek">Notatki</div></a>\n      <a href="archiwum.html"><div class="kafelek">Archiwum</div></a>\n    </div>\n    <script>\n      var ison = 1;\n      function changeImage() {\n        var x = document.getElementById("notification").getAttribute("src");\n        console.log(x);\n        if (\n          document.getElementById("notification").getAttribute("src") ==\n          "data/svg/notification_logo.svg"\n        ) {\n          document\n            .getElementById("notification")\n            .setAttribute("src", "data/svg/alert-bell.svg");\n          var ison = 0;\n          console.log(ison);\n        } else if (\n          document.getElementById("notification").getAttribute("src") ==\n          "data/svg/alert-bell.svg"\n        ) {\n          document\n            .getElementById("notification")\n            .setAttribute("src", "data/svg/notification_logo.svg");\n          var ison = 1;\n          console.log(ison);\n        }\n        $filename = "notification_settings.txt";\n        $content = ison;\n        file_put_contents($filename, $content);\n      }\n    </script>\n  </body>\n</html>\n''')
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
                            {"role": "user", "content": "Wygeneruj szczegółową notatkę dzięki której uczeń w pełni przygotuje się na sprawdzian z tematu:" + exam_list[i] + "z przedmiotu szkolnego: " + exam_subjects[i]+". Zawrzyj wszystkie informacje, które mogą być przydatne."}],
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
            website.write('''<!DOCTYPE html> <html> <head> <title>Tytuł strony</title> <meta charset="utf-8" /> <link href="styl.css" type="text/css" rel="stylesheet" /> </head> <body> <div style="position: absolute"><a href="hub.html" title="Naciśnij aby wrócić do panelu głównego.">   <img  src="data/svg/home-alt-svgrepo-com.svg" style="width: 100px; float: left; margin-left: 100px" />   </a>  </div> '''+generate_exam_subject(exam_subjects)+generate_topic_paragraph(exam_list)+''' <br /> <div id="left_arrow"><img src="arrow.png" alt="arrow" /></div> <main>''' + generate_objects(exam_list)+''' </main> <div id="right_arrow"><img src="arrow.png" alt="arrow" /></div> <div id="circles_div"></div> <script> var ilosc_plikow ='''+str(len(exam_list)) +
                          '''; var NumberOfCircles = ilosc_plikow; var circles_div = document.getElementById("circles_div"); var currentCard = 0; r_arrow = document.getElementById("right_arrow"); l_arrow = document.getElementById("left_arrow"); r_arrow.addEventListener("click", r_arrow_click, false); l_arrow.addEventListener("click", l_arrow_click, false); function r_arrow_click() { console.log("Nacisnąłeś prawą strzałkę"); if (currentCard + 1 < ilosc_plikow) { var div = document.getElementById("circles_div"); var kolka = div.getElementsByTagName("div"); document.getElementById(sub_ids[currentCard]).style.display = "none"; document.getElementById(sub_ids[currentCard + 1]).style.display = "block"; kolka[currentCard].style.background = "white"; kolka[currentCard + 1].style.background = "black"; document.getElementById(ids[currentCard]).style.display = "none"; document.getElementById(ids[currentCard + 1]).style.display = "block"; for (var i = 0; i < ilosc_plikow + 1; i++) { if ((previous_paragraph = document.getElementById(p_ids[i]))) { previous_paragraph.style.display = "none"; } } var current_paragraph = document.getElementById( p_ids[currentCard + 1] ); current_paragraph.style.display = "block"; currentCard++; } } function l_arrow_click() { console.log("Nacisnąłeś lewą strzałkę"); if (currentCard > 0) { var div = document.getElementById("circles_div"); var kolka = div.getElementsByTagName("div"); document.getElementById(sub_ids[currentCard]).style.display = "none"; document.getElementById(sub_ids[currentCard - 1]).style.display = "block"; kolka[currentCard].style.background = "white"; kolka[currentCard - 1].style.background = "black"; document.getElementById(ids[currentCard]).style.display = "none"; document.getElementById(ids[currentCard - 1]).style.display = "block"; for (var i = 0; i < ilosc_plikow + 1; i++) { if ((previous_paragraph = document.getElementById(p_ids[i]))) { previous_paragraph.style.display = "none"; } } current_paragraph = document.getElementById(p_ids[currentCard - 1]); current_paragraph.style.display = "block"; currentCard--; } } for (let i = 0; i < NumberOfCircles; i++) { const circle = document.createElement("div"); circle.setAttribute("id", "circle" + i.toString() + ""); circles_div.appendChild(circle); circle.addEventListener("click", CircleFunction, false); circle.name = i; } ids = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]; p_ids = [ "pierwszy", "drugi", "trzeci", "czwarty", "piaty", "szosty", "siodmy", "osmy", ]; sub_ids = [ "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", ]; function display_first() { element = document.getElementById(ids[0]); element.style.display = "block"; first_circle = document.getElementById("circle0"); first_circle.style.background = "black"; document.getElementById(p_ids[0]).style.display = "block"; document.getElementById(sub_ids[0]).style.display = "block"; } display_first(); function CircleFunction() { current_paragraph = document.getElementById(p_ids[this.name]); current_paragraph.style.display = "block"; console.log( "Wywolales funkcję: CircleFunction poprzez naciśnięcie kółka z ID: " + this.name ); currentCard = this.name; element = document.getElementById(ids[this.name]); element.style.display = "block"; var sub_name = document.getElementById(sub_ids[this.name]); sub_name.style.display = "block"; var div = document.getElementById("circles_div"); var kolka = div.getElementsByTagName("div"); for (var i = 0; i < kolka.length; i++) { kolka[i].style.background = "white"; } this.style.background = "black"; for (var i = 0; i < ilosc_plikow + 1; i++) { if (i != this.name) { previous = document.getElementById(ids[i]); other_paragraphs = document.getElementById(p_ids[i]); var sub_name = document.getElementById(sub_ids[i]); sub_name.style.display = "none"; other_paragraphs.style.display = "none"; previous.style.display = "none"; } } } </script> </body> </html> ''')

    async def run_all():
        calls = [
            run_provider(provider) for provider in _providers
        ]
        await asyncio.gather(*calls)

    asyncio.run(run_all())
    os.system(f'start hub.html')
notifications = True


def arhive_number_of_notes():
    folder_path = 'notes'
    files_list = os.listdir(folder_path)
    global number_of_files
    number_of_files = 0
    for file in files_list:
        if file.endswith('.html') and os.path.isfile(os.path.join(folder_path, file)):
            number_of_files += 1

    return int(number_of_files)


def arhive_generate():
    objects = ""
    for i in range(arhive_number_of_notes()):
        global note_name
        note_name = os.listdir("notes")
        print(note_name[i])
        object = '''<div class="kafelek">'''+str(note_name[i])+''' </div>'''
        objects += object
    print(number_of_files)
    return objects


def arhive_notes_generate():
    notes = ""

    for i in range(number_of_files):
        path = exam_list[i]+'''.html'''

        path = note_name[i]+'''.htmk'''
        note = '''<object data="notes/''' + \
            str(path)+'''"style="width:100%;height=100%;display:none"id=''' + \
            chr(65+1)+'''></object>'''
        notes += note

    return notes


def show_notifications():
    if notifications:
        for i in range(len(exam_deadlines)):
            dates_difference = exam_deadlines[i] - datetime.datetime.now()
            toast = Notification(app_id="Nazwa aplikacji",
                                 title="Zbliża się sprawdzian!",
                                 msg="Za niedlugo masz sprawdzian z " +
                                 exam_subjects[i] + " z tematu: " +
                                 exam_list[i] +
                                     ". Wejdź na NAZWA APLIKACJI i sprawdź swoje notatki!",
                                 duration="short"
                                 )
            toast.set_audio(audio.SMS, loop=False)
            if (dates_difference <= timedelta.Timedelta(days=2)):
                time.sleep(10)
                print(str(exam_subjects[i])+' '+str(exam_list[i]))
                print(dates_difference)
                toast.show()
                time.sleep(1800)


arhive_number_of_notes()
arhive_generate()
show_notifications()
time.sleep(1000)
show_notifications()
print('___________________________________koniec__________________________________________________')

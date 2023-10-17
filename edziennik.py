from vulcan import *
import asyncio
import vulcan
from datetime import datetime
import os
#wczytywanie danych o koncie ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\Users\lukas\Desktop\VULCAN API\account.json") as f:
    account = Account.load(f.read())
#wczytywanie klucza ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\Users\lukas\Desktop\VULCAN API\keystore.json") as f:
    keystore = Keystore.load(f.read())

    
async def main():
    os.system('cls')
    client = Vulcan(keystore, account)
    await client.select_student()
    
    #ustala obecną date
    present = datetime.now()
    
    exam = await client.data.get_exams()
        
    async for ex_info in exam:
        #kod odpowiedzialny za dodawanie tylko tych sprawdzianow, ktorych jeszcze nie bylo
        str_date_deadline = str(ex_info.deadline)
        dtt_date_deadline = datetime.strptime(str_date_deadline, '%Y-%m-%d %H:%M:%S')
        
        if(present<=dtt_date_deadline):
            exam_topic = str(ex_info.topic)
            print(exam_topic)
            
        
        

    

    #exam = [ex_info async for ex_info in exam]
    #print(exam[0])
    #for ex_info in exam:
    #    print(ex_info.topic)

    
    await client.close()
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


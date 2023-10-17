from vulcan import *
import asyncio

import vulcan

#wczytywanie danych o koncie ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\Users\lukas\Desktop\VULCAN API\account.json") as f:
    account = Account.load(f.read())
#wczytywanie klucza ze wczesniej zapisanego pliku json. W cudzyslowach wpisz swoja sciezke do pliku
with open(r"C:\Users\lukas\Desktop\VULCAN API\keystore.json") as f:
    keystore = Keystore.load(f.read())

async def main():
    client = Vulcan(keystore, account)
    await client.select_student()
    
    n = 10
    topics_list = [None] * n

    exam = await client.data.get_exams()
    i = 0
    async for ex_info in exam:
        exam_topic = str(ex_info.topic)
        topics_list[i]=exam_topic
        print(exam_topic)
        if(i==n-1):
            exit(1)
        else:
            i+1


        

    #exam = [ex_info async for ex_info in exam]
    #print(exam[0])
    #for ex_info in exam:
    #    print(ex_info.topic)

    
    await client.close()
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


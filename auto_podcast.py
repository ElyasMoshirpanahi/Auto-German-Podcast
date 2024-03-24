# -*- coding: utf-8 -*-
"""Auto_Podcast.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w-obwRCPFdYhDgXCnI6Yy0lw_8KzkYeK
"""
# from private_data import BOT_TOKEN , CHANNEL_ID

#@title imports
from datetime import datetime
from os import O_APPEND
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
import subprocess
from hurry.filesize import size, si
from glob import glob as g
import librosa
import os
from pydub import AudioSegment
from time import  sleep
from datetime import datetime
import pytz
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID= os.environ.get('CHANNEL_ID')
#@title Podcast Functions

def link_DL(url,Name="Audio_file"):
  """
  Download a link and saves to a given name
  """
  local_filename = url.split('/')[-1]
  # NOTE the stream=True parameter below
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192): 
      # If you have chunk encoded response uncomment if
      # and set chunk_size parameter to None.
      #if chunk: 
        f.write(chunk)
  return local_filename

def del_all_mp3():
  for i in g("/content/*.mp3"):
    os.remove(i) 

# def file_size(url):
#   """
#   Checks the file size of a url
#   """

#   # pass URL as first argument
#   response = requests.head(url, allow_redirects=True)
#   size = response.headers.get('content-length', -1)
#   # size in megabytes (f-string, Python 3 only)
#   fin=f"{'FILE SIZE':<40}: {int(size) / float(1 << 20):.2f} MB"
#   return fin

def grab_link(link):
  """
  Returns download link for a givin podcast
  """
  url = link
  podcast_domains=["detektor.fm","spektrum.de"]
  #Detektor.de
  if podcast_domains[0] in str(url):
    
    payload={}
    headers = {
    'authority': 'detektor.fm',
  'cache-control': 'max-age=0',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'none',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,de;q=0.6,fa;q=0.5',
  'cookie': '_ga=GA1.2.1295397546.1631638849; __gads=ID=15abbf747a00b98f:T=1631638852:S=ALNI_MZvfLMIxcE1QMV6Yu7T4LQNRzg9DA; cf_clearance=uziaBCag3MgWfdRzYGLgq1sfGBjI49eBlMhl4589J28-1632036416-0-250; __cmpcccx21335=aBPRZu7kgAgABA_gACAAQABwAHAAaAA8ACIAFAAQQAjwBMAE0AL0AYwBkADMAHEAP4AhwBFgCQAEwAJ4AUIApQBaAC8gGGAYkAxwDIAHeAPYAgoBC4CJgIoAR4AkgBM4CagJsAUYApcBVQFWAK2AWEAuwBhwDYAHAAPqAhgBE4CRgFAAKOAUgApMBcYDIAGtANzgbqBuwDiQHJAOZAdiBMsC0QAYgOhAhiUJ; __cmpconsentx21335=CPRZu7jPRZu7jAfU3BENB6CsAP_AAH_AAAigIBtf_X_fb3fj-_5_f_t0eY1f9_b_O-wyiheVp-oFyNeQ9L4Gm2M6tEygpigCoR4gqnZBIANsHElMSUER4ABFAAHsAggEpABIICNEiBMZQEIYCBsCAoQQQACZgUkdOBWIm0reYvbvXGFgpIgSRggCoAAgAIABAgMABAAIABAAAAIAgYIBtf_X_fb3fj-_5_f_t0eY1f9_b_O-wyiheVp-oFyNeQ9L4Gm2M6tEygpigCoR4gqnZBIANsHElMSUER4ABFAAHsAggEpABIICNEiBMZQEIYCBsCAoQQQACZgUkdOBWIm0reYvbvXGFgpIgSRggCoAAgAIABAgMABAAIABAAAAIAgYBQKAEAFEBjISAEAFEBjIaAEAFEBjIiAEAFEBjIqAEAFEBjIyAEAFEBjI6AEAFEBjJCAEAFEBjJKAEAFEBjJSAEAFEBjI; _pbjs_userid_consent_data=7543522476517459; pbjs-unifiedid=%7B%22TDID%22%3A%22c07fc458-d7ae-448c-9d1f-ab42a41703ee%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-11-18T06%3A23%3A14%22%7D; __cf_bm=WEBV4dsMcVnY6UV0fJpsY.2o48zA2FxvvrOHtCKH6cQ-1641112643-0-AajXAgdW5QAFzTTdUgPh9xXiNKlxWHKuBV+U7v3+in/NBB4qVp9f5tsy3gYL6UiXQ1mdls46bGI3yfgnPXopBb+i7BQ2Aogv49f7k+8qaL7z1D+OmiKdEDywZ+t7lY41aQ==; dfm=5414b5dba437e98fca169b4f0bdf7f53; _gid=GA1.2.2136843713.1641112645; dfmmc=2; _gat=1; cto_bundle=_kB21F9oN3VoY2klMkZPY2NLMEMlMkJMZWdKTDkxSlNmdkluVk9penNON2ZjZEppejRqeDdOMUZ5TmNrb2dOR1l5cmdDb0U1aHhOem1FdmZHbmNQbm1DUjlQSVljZHMlMkZ5am9ZcU5oR0hEdiUyQjRnM3pXRkdrSHMzSXVDdWF5Q0owT0VFSmUyamx4aXYwOWtOZDYlMkZWamkxajltV0ZwYjZ3JTNEJTNE; cto_bundle=AE6TFF9oN3VoY2klMkZPY2NLMEMlMkJMZWdKTDkxRW1HNUlMTk1jYU10S2FkRjNiamlLSDFsTCUyRnlnMVpBZEF6TWE4NmpZYzA1N2ttN0hhdFRMSkpHWkhGdG56NkUlMkJoT0dPTVh0NjNoQkdYVEdLdWUzV2pYanRMSU0wMHJYZTdwcTJ0bDBSMThGVGVPa1VCMTFIek9QM3c1ZE5iJTJCV3JBJTNEJTNE; cto_bidid=7A31lV9RR0Y2Vjk5WXdzaHQlMkZZUERWVzV6eUtpTW9iaEp4OSUyRmNySVdXS1A2VDdjUUxhQnV3JTJCVDNycktvY1RCYVg5UFRIdExGV1Rsb2dzdW9JM0ZtUWl1am0yNnJ3N01PR1VQMHhrMnAzc2tLdGFmayUzRA' 
  }

    try:
      response = requests.request("GET", url, headers=headers,data=payload)
      if response.status_code == 200:
        soup = BeautifulSoup(response.text)
        fin=[]
        for link in soup.find_all('a'):
          if "mp3" in str(link):
            fin.append(re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(link)))
        podcast_dl_link=fin[0][0]
        return podcast_dl_link
      else:
        return "Couldn't Find The link Sorry!"
    except:
      pass

  #Spektrum.de
  elif podcast_domains[1] in str(url):
    #Case 1 spekrum.de embeded
    try:
      r = requests.get(url)
      soup = BeautifulSoup(r.content, "html.parser")
      scripts = soup.find_all("script")
      fin=[]
      for s in scripts:
        if ".mp3" in str(s):
          fin.append(re.findall('(?<=/)[\w\-\_]+\.mp3', str(s)))
      this="https://cdn.podigee.com/media/"+fin[0][0]
      return this
    except:
      #print("Error for ",url)
      #Trying the second Case
      pass
  #Case 2  
    finally:
      r = requests.get(url)
      soup = BeautifulSoup(r.content,'html.parser')
      second_url=''
      frame=soup.find_all("iframe")
      for f in frame:
        if "embed" in f['src']:
          second_url=f['src']
          break
       
      if second_url != '':
        try:
          r=requests.get(second_url)
          soup = BeautifulSoup(r.content,'html.parser')
          final_link=[]
          for a in soup.find_all("a",href=True):
            if ".mp3" in str(a):
              final_link.append(a["href"])
          
          #print(final_link[0])
          return final_link[0]
        except:#Couldn't parse the Url at all!
           return ''
          #print("Error for ",second_url)

#@title Time and choosing functions

#Todo 0 :DONE
def report_tz(dt=datetime.now())->None:
    print(dt.hour,":",dt.minute)

def right_time()->set:
    """
    Indicates if it is the right time to send the podcasts
    output : boolean , remaining hours for new podcast
    """
    #1: Creating the time and zone
    time = datetime.now()

    #2:Localizeing the timezone
    new_tz = pytz.timezone("Asia/Tehran")

    #3:Converting the time zone
    new_tz_time = time.astimezone(new_tz)
    return (new_tz_time.hour ==  8 , (24 - new_tz_time.hour + 8))

#Todo 1 :DONE
def random_theme()->str:
    themen = ['astronomie','biologie','chemie','erde-umwelt','technik','medizin','physik','psychologie-hirnforschung']
    random_theme = themen[random.randint(0,len(themen)-1)]
    return random_theme

#Todo 2 & 3:DONE
def open_file(file='links.txt')->list:
    
    '''
    opens a txt file and returns all the lines inside
    Also a file is created when this file does not exist
    '''
    
    try:
        with open(file,'r',encoding='utf-8') as f:
            return [line.strip() for line in  f.readlines()]
    except Exception as e:
        print("No such file found , Creating links.txt")
        with open(file,'w',encoding='utf-8') as f:
            f.write('')
            f.close()
    finally:
        with open(file,'r',encoding='utf-8') as f:
            return [line.strip() for line in  f.readlines()]

def add_to_file(content,file='links.txt'):
    with open(file,'a') as f:
        f.write(f"{content}\n")
    print(f"Added {content} to file")

def fetch_and_compare(skip:int = 0):
    #1_Compose the request
    rand= random_theme()
    url = f"https://www.spektrum.de/podcast/{rand}/?skip={skip}"
    print(url)

    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')


    #Open all used links
    lines = open_file() 
    
    
    #Fetch all the links
    if skip == 0 :
        all_articles = [(article.text.split(":")[1],list(article.children)[1].findAll("img")[0]['src'],f"https://www.spektrum.de{list(article.children)[1]['href']}") for article in soup.findAll("article")[1:6]] + [(article.text.split(":")[1],list(article.children)[1].findAll("img")[0]['src'],f"https://www.spektrum.de{list(article.children)[1]['href']}") for article in soup.findAll("article")[-10:]]
    else:
        #No suggested or new Article!
        all_articles = [(article.text.split(":")[1],list(article.children)[1].findAll("img")[0]['src'],f"https://www.spektrum.de{list(article.children)[1]['href']}") for article in soup.findAll("article")[-10:]]
        
    number = 1
    
    #Check if a podcast is already sent
    for element in all_articles:
        link = element[2]
        if link not in lines:
            add_to_file(link)
            return [el.strip() for el in element]
    else:
        print("No new podcast was found skiping to older pages ")
        number = number * 10 
        fetch_and_compare(skip=number)

#@title Telgram functions

#Telegram functions 
def sendMessage(text='Task Finished'):
  token = BOT_TOKEN
  data = {'chat_id': CHANNEL_ID, 'text': text,'parse_mode': 'HTML'}
  url = f'https://api.telegram.org/bot{token}/sendMessage'
  response = requests.get(url, params=data)
  return response.json()

def sendAudio(doc,text=f"""
✅ Link Der Kannale : @BeataVideos
✅ Link Der Gruppe : <u><b><i><a href='https://t.me/+y7-l2vGlTFQ2Njg0'>Link</a></i></b></u>
""", chat_id=CHANNEL_ID):
    files = {'audio': open(doc, 'rb')}
    data={'caption':text,'parse_mode': 'HTML'}
    token = BOT_TOKEN
    URL = f"https://api.telegram.org/bot{token}/"
    response= requests.post(URL + f"sendAudio?chat_id={chat_id}", files=files,data=data)
    return response.json()
def sendImage(doc,name,link, chat_id=CHANNEL_ID):
    intro_suggestion = ["Heute geht es in unserem Podcast um:","Der heutige Podcast dreht sich um das Thema:","Heute hören wir über das Thema:","Heute ,hören wir uns das Thema an:","Heute , betrachten wir das Thema:"]
    hello_suggestion = ["Guten Tag","Guten Morgen","Morgen","Hallo","Hallo, wig geht es Ihnen "]
    kontankten = ["Freunde","Leute","Mitgliedern"]
    random_emoji = ["🙋🏻‍♂️","👋🏻","✌🏻","🖐🏻","✋🏻","🤜🏻🤛🏻"]

    hello = hello_suggestion[random.randint(0,len(hello_suggestion)-1)]
    intro = intro_suggestion[random.randint(0,len(intro_suggestion)-1)]
    emoji=random_emoji[random.randint(0,len(random_emoji)-1)]
    kontakt = kontankten[random.randint(0,len(kontankten)-1)]
    
    caption = f"""
{hello} liebe {kontakt}! {emoji}

<b>{intro}</b>
<i>{name}</i>

<i>weiter lesen sie <a href='{link}'>hier</a></i>


✅ Link Der Kannale : @BeataVideos
✅ Link Der Gruppe : <u><b><i><a href='https://t.me/+y7-l2vGlTFQ2Njg0'>Link</a></i></b></u>

💙Viel Spaß beim Hören💙
    """


    data={'photo':doc,'caption':caption,'parse_mode': 'HTML'}
    token = BOT_TOKEN
    URL = "https://api.telegram.org/bot{}/".format(token)
    response= requests.post(URL + "sendPhoto?chat_id={}".format(chat_id), data=data)
    return response.json()



def check_podcast_exists(title,collection):
    result =True if collection.find_one({"title": title}) else False  # <-- Call find_one on the collection object
    return result
#     return bool(result.acknowledged)

def store_podcast_title(title,collection):
    result = collection.insert_one({"title": title})  # <-- Call insert_one on the collection object
    print(f"New podcast inserted with _id: {result.inserted_id}")




#@title Main Function
def main():

    start = datetime.now()
    print("="*20,start,"="*20,"\n",)

    name,img,link = fetch_and_compare()

    #DB check
    MONGODB_URI = os.environ.get('MONGODB_URI')
    client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    db  = client['podcast']
    collection = db.titles
    podcast_exists = check_podcast_exists(name,collection)

    if podcast_exists == True:
        print("Podcast already exists in the database,skipping")
        main()
    else:
        print("Podcast is brand new , storing the podcast")
        store_podcast_title(name,collection)


    print(f"New podcast {name} will be downloaded")

    download_link = grab_link(link)

    if download_link:
        file_name = download_link.split("/")[-1]

        print(f"Download link retrived :\n {download_link} \n Downloading now...")

        while True:
            try:
                link_DL(download_link)
                break
            except Exception as e:
                print("Error :",e.args)
                print("Fetching a new podcast...")
                main()
        

        print("Download completed")
        path=f"/content/{file_name}"
        
        try:

          duration_secs=librosa.get_duration(filename=path)
        except FileNotFoundError:
          print("bad link or file cannot be downloaded with the provided link,recalling the function")
          main()

        if int(duration_secs/60) < 40:
            file_size= int(size(os.path.getsize(path),system=si).split("M")[0])

            #Case 1 : size < 20 mb no split:
            if file_size < 20:
                print("Sending banner to the group")
                sendImage(img,name,link)
                print("Sending podcast to the group")
                sendAudio(doc=path)
                end = datetime.now() -  start 
                print("="*20,f"Process done in {end} Seconds","="*20,"\n")
                exit()
                #Case 2 : file will be splitted into multiple parts 
            else:
                print("file size is too big , spliting...")
                division_parts=int(str(file_size)[:1])

                CSPerDiv=int(duration_secs/division_parts)

                StartOfSeg=0

                EndOfSeg  = CSPerDiv

                print(f"splitting {file_name} into {division_parts} parts with size of {file_size} parts with durtion of {duration_secs} Seconds ")
                print("Sending banner to the group")
                sendImage(img,name,link)
                print("Sending podcast to the group")
                for div in range(division_parts):
                    files_path = '/content/'
                    file_name = file_name.split(".mp3")[0]
                    startTime = StartOfSeg
                    endTime = EndOfSeg

                    print(f"Segement  Start: {startTime} end :{endTime}")
                    # Opening file and extracting segment
                    song = AudioSegment.from_mp3( files_path+file_name +".mp3")

                    startTime= startTime*1000
                    endTime  = endTime*1000
                    extract = song[startTime:endTime]

                    # Saving
                    File=f"{files_path}{file_name}_Teil {div+1}_.mp3"
                    extract.export( f"{files_path}{file_name}_Teil {div+1}_.mp3", format="mp3")
                    # break

                    StartOfSeg+=CSPerDiv
                    EndOfSeg +=CSPerDiv

                    print(f"End of Loop =>  Start: {StartOfSeg} end :{EndOfSeg}")

                    Name_Only=f"{file_name}_Teil {div+1}_.mp3"

                    text=f"""
                    <u><b><i><a href='{link}'>{Name_Only}</a></i></b></u>
                    ✅ Link Der Kannale : @BeataVideos
                    ✅ Link Der Gruppe : <u><b><i><a href='https://t.me/+y7-l2vGlTFQ2Njg0'>Link</a></i></b></u>
                    """
                    print(f"Sending {Name_Only} now...")
                    sendAudio(File,text)
                    print(f"Sent {Name_Only} , sleeping for 20 Secs for the next part!")
                    sleep(300)

                end = datetime.now() -  start 
                print("="*20,f"Process done in {end} Seconds","="*20,"\n")
                exit()
        else:
            print("Podcast is too long passing...")
            main()

    else:
        print("Podcast link not found skiping to the next podcast")
        main()


del_all_mp3()
main()

  # else:
  #   pass


#Uncomment in servers without cronjob!
#@title Main loop
# def main_loop():
#   while True:
#     del_all_mp3()
#     #0_Check the hour / wait if neccessory or /create a cron job¶
#     time_ok , remaining = right_time()
#     if time_ok:
#       main()
#     else:
#       sleep(remaining * 3600)

# main_loop()
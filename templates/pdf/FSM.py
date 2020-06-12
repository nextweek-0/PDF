from bs4 import BeautifulSoup
import requests
import re
import codecs
import textrank

def getHTMLText(url):

    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return
def light(words_list,filename):
    with open("./pdf/{}.html".format(filename), "r", encoding="utf-8") as f:
        demo = f.read()
    demo = demo.replace('<head>\n','<head>\n<style>mark{ background-color:#00ff90; font-weight:bold;}</style>\n',1)
    for word in words_list:
        demo = demo.replace('{}'.format(word), '<mark>{}</mark>'.format(word))

    with open('./pdf/{}.html'.format(filename), 'w', encoding='UTF-8') as f:
        f.write(demo)




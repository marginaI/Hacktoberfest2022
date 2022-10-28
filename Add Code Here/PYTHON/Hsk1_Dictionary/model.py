import json
import requests
from bs4 import BeautifulSoup as bs
import time


with open("config.json") as f:
    cfg = json.load(f)

def extract_data(url=cfg['url']):
    return requests.get(url).text

def transform_data():
    soup = bs(extract_data(),"html.parser")
    return soup

def new_chn_char(soup=transform_data()):
    new_char = soup.find_all(cfg['html_tag'],{cfg['attribute']:cfg['value'][0]})
    return [sino.get_text() for sino in new_char ]

def old_chn_char(soup=transform_data()):
    old_char = soup.find_all(cfg['html_tag'],{cfg['attribute']:cfg['value'][1]})
    return [sino.get_text() for sino in old_char]

def pinyin(soup=transform_data()):
    pinyins = [soup.find_all(cfg['html_tag'],{cfg['attribute']:cfg['value'][2]})]
    pinyins = [p for p in pinyins[0]]
    return  [p.get_text() for p in pinyins]

def french_definition(soup=transform_data()):
    fr_def = [soup.find_all(cfg['html_tag'],{cfg['attribute']:cfg['value'][3]})]
    fr_def = [w for w in fr_def[0]]
    return [words.get_text() for words in fr_def]

def old_chn_dictionary():
    old = old_chn_char()
    pin = pinyin()
    frdef = french_definition()
    return dict(zip(old,zip(pin,frdef)))

def new_chn_dictionary():
    new = new_chn_char()
    pin = pinyin()
    frdef = french_definition()
    return dict(zip(new,zip(pin,frdef)))

if __name__ == "__main__":

    start = time.time()
    
    d1 = old_chn_dictionary()
    d2= new_chn_dictionary()
    
    with open("old-chinese-dictionary.json","w") as f:
        json.dump(d1,f)
    
    with open("new-chinese-dictionary.json","w") as f:
        json.dump(d2,f)
    
    end = time.time()
    
    print(f"EXECUTION TIME : {end-start}")

import requests
from bs4 import BeautifulSoup
import string
import json
import sys

json.pours = json.dumps

languages_list = ["Eski TÃ¼rkÃ§e", "MoÄ\x9folca", "FransÄ±zca", "Ä°ngilizce", "Almanca", 
                  "Ä°talyanca", "ArapÃ§a", "RusÃ§a", "Ã‡ince", "Japonca", "Korece", "Latince", "FarsÃ§a", "Yunanca", "TÃ¼rkÃ§e", "Eski FarsÃ§a"] #the purpose of this is to make sure that when the Beautiful Soup
                                                                                                                                          #return language names, the program can convert them to actual words in the future

past_tense_endings = ["ti", "di", "tu", "du", "dı", "tı", "dü", "tü"]

languages_dict = {    "Eski TÃ¼rkÃ§e": "Eski Türkçe", #converting the gibberish to actual Turkish words
    "MoÄ\x9folca": "Moğolca",
    "FransÄ±zca": "Fransızca",
    "Ä°ngilizce": "İngilizce",    # 'İ' (capital I with dot)
    "Almanca": "Almanca",       # No special chars, but good to include for completeness
    "Ä°talyanca": "İtalyanca",    # 'İ'
    "Ä°spanyolca": "İspanyolca",  # 'İ'
    "ArapÃ§a": "Arapça",        # 'ç'
    "RusÃ§a": "Rusça",         # 'ç'
    "Ã‡ince": "Çince",         # 'Ç' (capital C with cedilla)
    "Japonca": "Japonca",
    "Korece": "Korece",
    "Latince": "Latince",
    "FarsÃ§a": "Farsça",        # 'ç'
    "Yunanca": "Yunanca",
    "TÃ¼rkÃ§e": "Türkçe",
    "Eski FarsÃ§a" : "Eski Farsça" }

def fetch_etymology(word):
    word = word.lower()
    url = f"https://www.etimolojiturkce.com/kelime/{word}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except requests.RequestException as e: #Not finding the url error
        with open("arabicPercentageErrors.txt", 'a', encoding='utf-8') as file:
            file.write(f"HTTP error: 404 Client Error: Not Found for url: https://www.etimolojiturkce.com/kelime/{word} \n")
        return None
    except Exception as e:
        with open("arabicPercentageErrors.txt", 'a', encoding='utf-8') as file:
            file.write(f"Exception occured : {e}\n")
        return None

    soup = BeautifulSoup(resp.text, 'html.parser')

    bold_tags = soup.find_all('b')

    bold_array = [b.get_text(strip=True) for b in bold_tags]

    lang_name = None


    for bold in bold_array:
        if bold in languages_list:
            lang_name = bold        
            break
    if lang_name is None:
        lang_name = "Eski TÃ¼rkÃ§e"
    
    return lang_name 

    #yokas return lang_name if lang_name else None

def fps_past_ending(word):
    for i in range(len(past_tense_endings)): #I am using this function to check ,after the word returns not found, if it because of a past tense issue, then pop the ending out
        if word.endswith(past_tense_endings[i]+"m"):
            return True
    return False
        
def sps_past_ending(word):
    for i in range(len(past_tense_endings)):
        if word.endswith(past_tense_endings[i]+"n"): #second person singular
            return True
    return False
        
def tps_past_ending(word):    
    for i in range(len(past_tense_endings)): #third person singular
        if word.endswith(past_tense_endings[i]):
            return True
    return False

def fpp_past_ending(word):
    for i in range(len(past_tense_endings)):
        if word.endswith(past_tense_endings[i]+"k"):
            return True
    return False
        
def spp_past_ending(word):
    local_past_tense_list = past_tense_endings.copy()

    for i in range(len(past_tense_endings)): #first making a special new endings list
        if past_tense_endings[i].endswith("ü"):
            local_past_tense_list[i]+="nüz"
        elif past_tense_endings[i].endswith("u"):
            local_past_tense_list[i]+="nuz"
        elif past_tense_endings[i].endswith("i"):
            local_past_tense_list[i]+="niz"
        else :
            local_past_tense_list[i]+="nız"#completely changed each variable in the mother list

    for i in range(len(local_past_tense_list)):
        if word.endswith(local_past_tense_list[i]):
            return True
    return False

def tpp_past_ending(word):
    local_past_tense_list = past_tense_endings.copy()

    for i in range(len(past_tense_endings)): #same as what I did in the funciton above
        if past_tense_endings[i].endswith(("ü","i")):
            local_past_tense_list[i]+="ler"
        else:
            local_past_tense_list[i]+="lar"

    for i in range(len(local_past_tense_list)):
        if word.endswith(local_past_tense_list[i]):
            return True
    return False

def check_past_ending(word):

    new_word = None

    if spp_past_ending(word) or tpp_past_ending(word):
        new_word = word[:-5]
    elif fps_past_ending(word) or sps_past_ending(word) or fpp_past_ending(word):
        new_word = word[:-3]
    elif tps_past_ending(word):
        new_word = word[:-2]
    else :
        new_word = word

    return new_word




if __name__ == "__main__":
    arabicWordCount = 0

    sentence = input("Enter the Turkish sentence you want!\n-> ").strip()

    sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    words = [word.lower() for word in sentence.split()]

    total_words = len(words)

    for word in words:

        language = fetch_etymology(word)

        if language is None:
            word = check_past_ending(word)
            language = fetch_etymology(word)

        if language == "ArapÃ§a":
            arabicWordCount+=1

        if language and language in languages_dict:

            tc_language = languages_dict[language]

            print(f"The etymology is {tc_language}")
        
        else:
            print(f"{word} is not found")

    with open("arabicPercentage.txt", 'a') as file:
        file.write(f"Arapca kelime sayisi: {arabicWordCount}, toplam kelime sayisi: {total_words}, oran: {arabicWordCount/total_words}\n")




import requests
from bs4 import BeautifulSoup
import string
import json
import sys

from past_tense_check import check_past_ending

json.pours = json.dumps

languages_list = ["Eski TÃ¼rkÃ§e", "MoÄ\x9folca", "FransÄ±zca", "Ä°ngilizce", "Almanca", 
                  "Ä°talyanca", "ArapÃ§a", "RusÃ§a", "Ã‡ince", "Japonca", "Korece", "Latince", "FarsÃ§a", "Yunanca", "TÃ¼rkÃ§e", "Eski FarsÃ§a"] #the purpose of this is to make sure that when the Beautiful Soup
                                                                                                                                          #return language names, the program can convert them to actual words in the future

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




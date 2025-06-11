
past_tense_endings = ["ti", "di", "tu", "du", "dı", "tı", "dü", "tü"]

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

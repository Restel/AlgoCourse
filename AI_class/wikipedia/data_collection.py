__author__ = "Lina Brilliantova, RIT"
"""
This script prepare the training, validation and test sets for decision tree algorithm, using wikipedia API
"""
import wikipedia #API
import re # regular expressions
import csv

def random_page():
    random = wikipedia.random(1)
    try:
        result = wikipedia.page(random)
    except wikipedia.exceptions.DisambiguationError:
        result = random_page()
    return result

def splitter(n, s):
    list = []
    pieces = s.split()
    for i in range(0, len(pieces), n):
        chunk = " ".join(pieces[i:i+n])
        list.append(chunk)
    return list

languages = ["it", "nl"]
def collect_data(language, reps):
    wikipedia.set_lang(language)
    i = 0
    while True:
        page = random_page()
        text = page.content
        # Clean text
        text = re.sub(r'==.*?==+', '', text)
        text = text.replace('\n', '')
        splitted = splitter(20, text)
        file = open("wikipedia_data.csv", mode="a+", encoding='utf-8')
        wiki_writer = csv.writer(file)
        for obs in splitted:
            if len(obs.split()) <= 19: # text chunk is too short
                continue
            elif i >= reps:
                return
            #wiki_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wiki_writer.writerow([obs, language])
            i+=1
            print(i)
        file.close()






# wikipedia.set_lang("it")
# wikipedia.set_lang("Nederlands")
# wikipedia.set_lang('en')
# print(wikipedia.summary("Rochester, New York"))
# wikipedia.set_lang("it")
# print(wikipedia.summary("Rochester, New York"))
# wikipedia.set_lang("nl")
# sum = wikipedia.summary("Rochester, New York")
# sum = sum.replace("\n", " ")
# sum.rstrip()
#
# for key in wikipedia.languages():
#     if key[0] in ['n', 'N']:
#         print(key, wikipedia.languages()[key])



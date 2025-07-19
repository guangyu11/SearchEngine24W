from collections import namedtuple
import os
from bs4 import BeautifulSoup
import json
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys
import nltk

posting = namedtuple('posting', ['name', 'id', 'score'])
english_stopwords = set(stopwords.words('english'))

def Indexing(rootFolder):

    index = {}
    titles = {}
    num = 0
    file_num = 1
    threshold = 2000
    id = 1

    for subdir, dirs, files in os.walk(rootFolder):
        print(subdir)
        for file in files:
            file_path = os.path.join(subdir,file)
            success = parseJson(index, file_path, titles, id)
            if success:
                id += 1
                num += 1
                if num > threshold:
                    file_name = f"index_part_{file_num}.json"
                    saveIndexToFile(index, file_name)
                    index.clear()
                    threshold += 2000
                    file_num += 1
                    print(f"Index saved to {file_name}")

    if index:
        file_name = f"index_part_{file_num}.json"
        saveIndexToFile(index, file_name)

    if titles:
        file_name = f"titles.json"
        saveIndexToFile(titles, file_name)

    return None

def parseJson(index, filename, titles, id):
    with open(filename, 'r', encoding='utf-8') as Jfile:
        Jcontent = json.load(Jfile)

    try:
        HTML = Jcontent["content"]
        soup = BeautifulSoup(HTML, 'html.parser')
        text = soup.get_text()
        Name = Jcontent["url"]
    except:
        return False

    try:
        titles[id] = soup.title.string
    except:
        pass

    try:
        if Name:
            tokens = tokenize(text)
            for key, value in tokens.items():
                if key in index:
                    index[key].append(posting(Name, id, value))
                else:
                    index[key] = []
                    index[key].append(posting(Name, id, value))
            return True
        else:
            return False
    except:
        return False



def tokenize(text):
    line_tokens = re.findall(r'[a-zA-Z]+', text.lower(), re.ASCII)
    filtered = [word for word in line_tokens if word not in english_stopwords]
    porter_stemmer = PorterStemmer()
    filtered2 = [porter_stemmer.stem(word) for word in filtered]
    Frequencies = {}
    try:
        for token in filtered2:
            if len(token) >= 2:
                if token not in Frequencies:
                    Frequencies[token] = 1
                else:
                    Frequencies[token] += 1
    except Exception as e:
        return {}
    return Frequencies

def saveIndexToFile(index, file_name):
    with open(file_name, 'w') as f:
        json.dump(index, f)

if __name__ == '__main__':
    Indexing(sys.argv[1])
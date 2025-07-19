import os
import json
import Assignment3_M1
import math
from collections import namedtuple

def query():
    print("Search engine initializing...")
    index, important = merge()
    print("Initialization complete")
    print("You can enter #quit to quit the search engine")

    while(True):
        QUERY = input("Enter a query: ")
        if QUERY == "#quit":
            break

        Qtokens = Assignment3_M1.tokenize(QUERY)
        terms = [word for word in Qtokens.keys() if word in index]

        idf = IDF(index, terms)

        result = compute(index, terms, important, idf)

        i = 1
        for key, value in result.items():
            if i< 11 :
                print(f'{i}st: {key}, {value}')
            i += 1

def compute(index, terms, important, idf):
    result = {}
    for term in terms:
        for posting in index[term]:
            if posting[0] not in result:
                result[posting[0]] = [1, 0, 0]
                result[posting[0]][2] += idf[term] * 1 + math.log10(posting[2])
            else:
                result[posting[0]][2] += idf[term] * 1 + math.log10(posting[2])
                result[posting[0]][0] += 1

            try:
                if str(posting[1]) in important:
                    if important[str(posting[1])]:
                        if term in important[str(posting[1])].lower():
                            result[posting[0]][1] += 1
            except:
                pass

    sorted_result = dict(sorted(result.items(), key = lambda item: (item[1][0], item[1][1], item[1][2]), reverse=True))

    return sorted_result

def IDF(index, terms):
    score = {}
    N = 55393
    for term in terms:
        df = len(index[term])
        score[term] = math.log10(N/df)
    return score

def merge():
    merged = {}
    titles = {}
    dirc= os.getcwd()
    for filename in os.listdir(dirc):
        if filename.endswith('.json') and filename != "titles.json":
            with open(filename, 'r') as json_file:
                tmp = json.load(json_file)
                for key, value in tmp.items():
                    if key in merged:
                        merged[key].extend(value)
                    else:
                        merged[key] = value

    try:
        with open("titles.json", 'r') as json_file:
            titles = json.load(json_file)
    except:
        pass

    return merged, titles

if __name__ == '__main__':
    query()
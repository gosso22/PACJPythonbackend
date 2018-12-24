import json
import pickle
import sys

if __name__ == "__main__":

    file_name = sys.argv[1]
    if file_name.endswith('.json'):

        with open(file_name, "r") as inf:
            jsonData = json.load(inf)

        s = [(k, jsonData[k]) for k in sorted(jsonData, key=jsonData.get, reverse=True)]
        for k, v in s:
            print(k , v, r"------------------------------------->")

    elif file_name.endswith('.pkl'):

        with open(file_name, "rb") as inf:
            acj = pickle.load(inf)

        for i in reversed(range(len(acj.results()[0]))):
            print(acj.results()[0][i][0],int(round(acj.results()[0][i][1])))

        print(round(acj.reliability()[0]*100, 2))

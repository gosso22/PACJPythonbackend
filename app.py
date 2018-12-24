#!/usr/bin/env python
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import pickle
from ACJ import ACJ
import json
import os

app = Flask(__name__)
api = Api(app)

#parser = reqparse.RequestParser()
#parser.add_argument('jsonResultData', type=dict)

class Pair(Resource):
    def get(self, course_name):
        with open(course_name+".pkl", "rb") as input_file:
            acj = pickle.load(input_file)

        pair = acj.nextPair()
        with open(course_name+".pkl", 'wb') as output_file:
            pickle.dump(acj, output_file)
        del(acj)
        print(type(pair))

        return pair

class Result(Resource):

    def post(self):
        received_data = request.get_json()
        result_data = json.loads(received_data)
        print("This was received data",result_data)
        for key, value in result_data.items():
            if(key == "pair"):
                pair = result_data[key]
            if(key == "result"):
                resultSent = result_data[key]
            if(key == "reviewer"):
                reviewerName = result_data[key]
            if(key == "time"):
                timeTaken = result_data[key]
            if(key == "courseName"):
                courseName = result_data[key]

        with open(courseName+".pkl", 'rb') as input_file:
            acj = pickle.load(input_file)

        acj.comp(pair, result=resultSent, reviewer=reviewerName , time=timeTaken)
        with open(courseName+".pkl", 'wb') as output_file:
            pickle.dump(acj, output_file)
        acj.JSONLog()
        del(acj)
        results = ("Response received", json.dumps(result_data))
        
        return True, 201

class ACJObject(Resource):
    def post(self):
        received_info = request.get_json()
        data_for_creating_acj = json.loads(received_info)
        print(data_for_creating_acj)

        for key in data_for_creating_acj:
            if(key == "data"):
                submissions = data_for_creating_acj[key]
            if(key == "maxRounds"):
                maxRounds = data_for_creating_acj[key]
            if(key == "noOfChoices"):
                noOfChoices = data_for_creating_acj[key]
           # if(key == "logPath"):
            #    logPath = data_for_creating_acj[key]
            if(key == "optionNames"):
                optionNames = data_for_creating_acj[key]
            if(key == "courseName"):
                courseName = data_for_creating_acj[key]
                logPath = courseName

        acj = ACJ(submissions, maxRounds, noOfChoices, logPath, optionNames)

        if(os.path.isfile(courseName+".pkl")):
            result = False

        else:
            with open(courseName+".pkl", 'wb') as output_file:
                pickle.dump(acj, output_file)
                os.makedirs(courseName)
                result = True
                
        del(acj)

        return result, 201

class CurrentACJResult(Resource):
    def get(self, course_name):
        try:
            with open(course_name+".pkl", 'rb') as input_file:
                acj = pickle.load(input_file)
                results = acj.results()[0]
            del(acj)
            resultsDict = {}
            for item in results:
                resultsDict[item[0]] = item[1]
            jsonResults = json.dumps(resultsDict)
            
            return jsonResults
        except FileNotFoundError:
            return "NotCreated"

class Reviewers(Resource):
    def get(self, course_name):
        try:     
            with open(course_name+".pkl", 'rb') as input_file:
                acj = pickle.load(input_file)
            choice = acj.optionNames[0]
            del(acj)
            with open(os.path.join(course_name, "ACJ_"+choice+".json")) as input_file:
                json_result = json.load(input_file)
            reviewers = json.dumps(json_result["Reviewers"])
            return reviewers
        except FileNotFoundError:
            return "NotCreated"

class Decisions(Resource):
    def get(self):
        received_data = request.args.get('data')
        data = json.loads(received_data)
        course_name = data["courseName"]
        reviewer = data["reviewer"]

        with open(course_name+".pkl", 'rb') as input_file:
            acj = pickle.load(input_file)

        choice = acj.optionNames[0]
        del(acj)

        with open(os.path.join(course_name, "ACJ_"+choice+".json")) as input_file:
            json_result = json.load(input_file)

        reviewer_decisions = [decision for decision in json_result["Decisions"]
                if(decision["reviewer"]==reviewer)]

        for decision in reviewer_decisions:
            if(decision["Result"] == "True"):
                decision["Result"] = decision["Pair"][0]
            else:
                decision["Result"] = decision["Pair"][1]

        decisions_json = json.dumps(reviewer_decisions)

        return decisions_json

class Kassim(Resource):
    def get(self):

        return "you have reached us!"



api.add_resource(Pair, '/pair/<course_name>')
api.add_resource(Result, '/result')
api.add_resource(ACJObject, '/newacj')
api.add_resource(CurrentACJResult, '/acjresult/<course_name>')
api.add_resource(Reviewers, '/reviewers/<course_name>')
api.add_resource(Decisions, '/decisions')
api.add_resource(Kassim, '/kassim')

if __name__ == '__main__':
    app.run(debug=True)

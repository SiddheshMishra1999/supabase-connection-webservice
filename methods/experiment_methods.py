import json
from supabase_connection import supabase
from flask import Flask, request, render_template


# Retrieve a specific user's experiments
def getExpSpecificUser(experiment_creator):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    experimentsfromId = supabase.table("experiment").select('*').eq("experiment_creator", experiment_creator).execute()
    experimentsStr = experimentsfromId.json()
    experimentsObject = json.loads(experimentsStr)
    allData= experimentsObject["data"]
    if(allData):
       
        exp_list = []
        for experiments in allData:
            experiment_status = supabase.table("experiment_status").select("status_name").eq("pstatus_id", experiments["pstatus_id"]).execute().json()
            status = json.loads(experiment_status)["data"][0]["status_name"]
            user_experiments = {
                "experiment_id": experiments["experiment_id"],
                "experiment_name": experiments["experiment_name"],
                "experiment_status": status,
                "experiment_eligibility": experiments["eligibility"],
                "num_of_participants": experiments["num_of_participants"],
                "start_date": experiments["start_date"],
                "end_date": experiments["end_date"],
                "description": experiments["description"],
            }
            exp_list.append(user_experiments)
        return{"User_experiments": exp_list}, 201, headers
    else:
        return{"Error": "User Does not exist"},400, headers


# Add a new experiment to the experiment table
def insertNewExperiment():
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    if request.is_json:
        supabase.table("experiment").insert(
            {
                "experiment_creator" : request.json["experiment_creator"],
                "experiment_name" : request.json["experiment_name"],
                "pstatus_id" : request.json["pstatus_id"],
                "start_date" : request.json["start_date"],
                "num_of_participants": request.json["num_of_participants"],
                "end_date" : request.json["end_date"],
                "eligibility" : request.json["eligibility"],
                "description" : request.json["description"]
            }
        ).execute()

        return {"Success": 'the experiment has been added'}, 201, headers
    else:
        return{'error': 'Request must be json'}, 400, headers

# Get all Experiments from Supabase
def allExperiments():
    experiments = supabase.table("experiment").select('*').execute()
    experimentsStr = experiments.json()
    experimentsObject = json.loads(experimentsStr)
    allData= experimentsObject["data"]
    experiment_list = []
    for experiment in allData:
        experiment_status = supabase.table("experiment_status").select("status_name").eq("pstatus_id", experiment["pstatus_id"]).execute().json()
        status = json.loads(experiment_status)["data"][0]["status_name"]
        experiment_data = {
            "experiment_id": experiment["experiment_id"],
            "experiment_creator": experiment["experiment_creator"],
            "experiment_name": experiment["experiment_name"],
            "experiment_status": status,
            "experiment_eligibility": experiment["eligibility"],
            "num_of_participants": experiment["num_of_participants"],
            "start_date": experiment["start_date"],
            "end_date": experiment["end_date"],
            "description": experiment["description"],
        }
        experiment_list.append(experiment_data)
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    return {"Experiments": experiment_list}, 201, headers


# Delete an eexperiment from id
def deleteExperimentById(experiment_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    experimentsfromId = supabase.table("experiment").select('*').eq("experiment_id", experiment_id).execute()
    experimentsStr = experimentsfromId.json()
    experimentsObject = json.loads(experimentsStr)
    allData= experimentsObject["data"]
    if(allData):
        supabase.table("experiment").delete().eq("experiment_id", experiment_id).execute()
        return{"Success": "Experiment has been Deleted"}, 201, headers
    else:
        return{"Error": "Experiment Does not exist"},400, headers

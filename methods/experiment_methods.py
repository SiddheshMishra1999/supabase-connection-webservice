import json
from supabase_connection import supabase
from flask import Flask, request, render_template
import methods.exisitance_check as check

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
           
            user_experiments = {
                "experiment_creator": experiments["experiment_creator"],
                "experiment_name": experiments["experiment_name"],
                "experiment_id": experiments["experiment_id"],
                "experiment_status": experiments["pstatus_id"],
                "num_of_participants": experiments["num_of_participants"],


            }
            exp_list.append(user_experiments)
        return{"User_experiments": exp_list}, 201, headers
    else:
        return{"Error": "User Does not exist"},400, headers


# Add a new experiment to the experiment table
def insertNewExperiment(experiment_creator, experiment_name, pstatus_id, start_date, num_of_participants, end_date, eligibility, description):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    if(end_date == "null"):
        supabase.table("experiment").insert(
        {
            "experiment_creator" : str(experiment_creator),
            "experiment_name" : str(experiment_name),
            "pstatus_id" : pstatus_id,
            "start_date" : str(start_date),
            "num_of_participants": num_of_participants,
            "eligibility" : str(eligibility),
            "description" : str(description)
        }
        ).execute()
        return {"Success": 'the experiment has been added'}, 201, headers
    else:
    # if request.is_json:
        supabase.table("experiment").insert(
            {
                "experiment_creator" : str(experiment_creator),
                "experiment_name" : str(experiment_name),
                "pstatus_id" : pstatus_id,
                "start_date" : str(start_date),
                "num_of_participants": num_of_participants,
                "end_date" : str(end_date),
                "eligibility" : str(eligibility),
                "description" : str(description)
            }
        ).execute()

        return {"Success": 'the experiment has been added'}, 201, headers
    # else:
    #     return{'error': 'Request must be json'}, 400, headers

# update an experiment to the experiment table
def updateExperiment(experiment_id, experiment_name, pstatus_id, start_date, num_of_participants, end_date, eligibility, description):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    allData = check.experimentCheck(experiment_id)
    if(allData):
        if(end_date == "null"):
            supabase.table("experiment").update(
            {
                "experiment_name" : str(experiment_name),
                "pstatus_id" : pstatus_id,
                "start_date" : str(start_date),
                "num_of_participants": num_of_participants,
                "eligibility" : str(eligibility),
                "description" : str(description)
            }
            ).eq("experiment_id", experiment_id).execute()
            return {"Success": 'the experiment has been added'}, 201, headers
        else:
        # if request.is_json:
            supabase.table("experiment").update(
                {
                    "experiment_name" : str(experiment_name),
                    "pstatus_id" : pstatus_id,
                    "start_date" : str(start_date),
                    "num_of_participants": num_of_participants,
                    "end_date" : str(end_date),
                    "eligibility" : str(eligibility),
                    "description" : str(description)
                }
            ).eq("experiment_id", experiment_id).execute()

            return {"Success": 'the experiment has been added'}, 201, headers
    else:
        return{"Error": "Experiment Does not exist"},400, headers

# Get a specific experiment 
def getExperimentById(experiment_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    allData = check.experimentCheck(experiment_id)
    if(allData):
        experiment_status = supabase.table("experiment_status").select("status_name").eq("pstatus_id", allData[0]["pstatus_id"]).execute().json()
        status = json.loads(experiment_status)["data"][0]["status_name"]
        experiment_data = {
            "experiment_id": allData[0]["experiment_id"],
            "experiment_creator": allData[0]["experiment_creator"],
            "experiment_name": allData[0]["experiment_name"],
            "experiment_status": status,
            "experiment_eligibility": allData[0]["eligibility"],
            "num_of_participants": allData[0]["num_of_participants"],
            "start_date": allData[0]["start_date"],
            "end_date": allData[0]["end_date"],
            "description": allData[0]["description"],
        }
        return{"Experiment": experiment_data}, 201, headers
    else:
        return{"Error": "Experiment Does not exist"},400, headers


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
    allData = check.experimentCheck(experiment_id)
    if(allData):
        supabase.table("experiment").delete().eq("experiment_id", experiment_id).execute()
        return{"Success": "Experiment has been Deleted"}, 201, headers
    else:
        return{"Error": "Experiment Does not exist"},400, headers

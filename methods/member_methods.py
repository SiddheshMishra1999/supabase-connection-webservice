import json
from supabase_connection import supabase
from flask import Flask, request, render_template
from datetime import datetime, timedelta

# current time
timeNow = datetime.now()

# Get members in an experiment
def membersInExperiment(experiment_id):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    experimentsfromId = supabase.table("experiment").select('*').eq("experiment_id", experiment_id).execute()
    experimentsStr = experimentsfromId.json()
    experimentsObject = json.loads(experimentsStr)
    allData= experimentsObject["data"]
    if(allData):
        members = supabase.table("members").select('*').eq("experiment_id", experiment_id).execute()
        membersStr = members.json()
        membersObj = json.loads(membersStr)
        membersData = membersObj["data"]
        member_list = []
        for member in membersData:
            memberNamefromId = supabase.table("users").select("last_name", "first_name").eq("auth_id", member["user_id"]).execute().json()
            memberFirstName = json.loads(memberNamefromId)["data"][0]["first_name"]
            memberLastName = json.loads(memberNamefromId)["data"][0]["last_name"]
            memberName = f"{memberFirstName} {memberLastName}"
            member_data ={
                "user_id": member["user_id"],
                "member_name" : memberName,
                "join_date": member["join_date"]
            }
            member_list.append(member_data)
        return {"Memebers": member_data}, 201, headers
    else:
        return{"Error": "Experiment Does not exist"},400, headers

# Insert a member in an experiment using their auth_id
def insertMemberInExperiment():
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    if request.is_json:
        experiment_id = request.json["experiment_id"]
        # experimentsfromId = supabase.table("experiment").select('*').eq("experiment_id", experiment_id).execute()
        # experimentsStr = experimentsfromId.json()
        # experimentsObject = json.loads(experimentsStr)
        # allData= experimentsObject["data"]
        # if(not allData):
        #     return{"Error": "Experiment Does not exist"},400, headers
        auth_id = request.json["user_id"]
        # userfromId = supabase.table("users").select("*").eq("auth_id", auth_id).execute()
        # userfromIdStr = userfromId.json()
        # userfromIdObj = json.loads(userfromIdStr)
        # userData = userfromIdObj["data"]
        # print(userData)
        # if(not userData):
        #     return{"Error": "User Does not exist"},400, headers
        supabase.table("members").insert({
            "user_id": auth_id,
            "experiment_id": experiment_id,
            "join_date": str(timeNow)
            
        }).execute()
        return {"Success": 'Member has been added'}, 201, headers
    else:
        return{'error': 'Request must be json'}, 400, headers



    # experimentsfromId = supabase.table("experiment").select('*').eq("experiment_id", experiment_id).execute()
    # experimentsStr = experimentsfromId.json()
    # experimentsObject = json.loads(experimentsStr)
    # allData= experimentsObject["data"]
    # if(allData):
    #     userfromId = supabase.table("users").select("*").eq("auth_id", auth_id).execute()
    #     userfromIdStr = userfromId.json()
    #     userfromIdObj = json.loads(userfromIdStr)
    #     userData = userfromIdObj["data"]
    #     if(userData):
            
    #     else:
    #         return{"Error": "User Does not exist"},400, headers
    # else:
    #     return{"Error": "Experiment Does not exist"},400, headers





        


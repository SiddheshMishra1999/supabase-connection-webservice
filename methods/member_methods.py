import json
from supabase_connection import supabase
from flask import Flask, request, render_template
from datetime import datetime, timedelta
import methods.exisitance_check as check


# current time
timeNow = datetime.now()


def memberCount(experiment_id):
    members = supabase.table("members").select("user_id").eq("experiment_id", experiment_id).execute()
    membersStr = members.json()
    membersObj = json.loads(membersStr)
    membersData = membersObj["data"]
    counter = 0 
    for member in membersData:
        counter += 1
    return counter

# Get count of all members from experiment ID, how many times the experiment id shows up in the memebers table 
# Return count and experiment id
# return list of expriment created by 
def membersCountInExperiment(experiment_id):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    allData = check.experimentCheck(experiment_id)
    if(allData):
        counter = memberCount(experiment_id)
        member_data = {
            "Number_of_participants": counter,
            "Max_number_of_participant": allData[0]["num_of_participants"],
            "experiment_id": experiment_id
        }
        return {"Members": member_data}, 201, headers
    else:
        return{"Error": "Experiment Does not exist"},400, headers


# Get members in an experiment
def membersInExperiment(experiment_id):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    allData = check.experimentCheck(experiment_id)
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
        return {"Memebers": member_list}, 201, headers
    else:
        return{"Error": "Experiment Does not exist"},400, headers

# Get experiments from auth_id
def experimentForMember(auth_id):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    userData = check.userCheck(auth_id)
    if(userData):
        experimentsforMembyID = supabase.table("members").select('*').eq("user_id", auth_id).execute()
        experimentsStr = experimentsforMembyID.json()
        experimentsObj = json.loads(experimentsStr)
        experimentsData = experimentsObj["data"]
        experiment_list = []
        for member in experimentsData:
            experimentNamefromId = supabase.table("experiment").select("experiment_name").eq("experiment_id", member["experiment_id"]).execute().json()
            experimentName = json.loads(experimentNamefromId)["data"][0]
 
            experiment_data ={
                "epxeriment_id": member["experiment_id"],
                "experiment_name" : experimentName,
                "join_date": member["join_date"]
            }
            experiment_list.append(experiment_data)
        return {"Experiments": experiment_list}, 201, headers
    else:
        return{"Error": "User Does not exist"},400, headers


# Insert a member in an experiment using their auth_id
def insertMemberInExperiment():
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    if request.is_json:
        experiment_id = request.json["experiment_id"]
        auth_id = request.json["user_id"]

        allData = check.experimentCheck(experiment_id)
        if(not allData):
            return{"Error": "Experiment Does not exist"},400, headers
        userData = check.userCheck(auth_id)
        if(not userData):
            return{"Error": "User Does not exist"},400, headers
        # check max user 
        maxParticipant = int(allData[0]["num_of_participants"])
        counter = int(memberCount(experiment_id))
        if(counter >= maxParticipant):
            return{"Error": "Maximum number of participant already in the experiment"},400, headers
       
        members = supabase.table("members").select('*').eq("experiment_id", experiment_id).execute()
        membersStr = members.json()
        membersObj = json.loads(membersStr)
        membersData = membersObj["data"]
        for member in membersData:
            if member["user_id"] == auth_id:
                return{"Error": "User already in this experiment"},400, headers
        supabase.table("members").insert({
            "user_id": auth_id,
            "experiment_id": experiment_id,
            "join_date": str(timeNow)
            
        }).execute()
        return {"Success": 'Member has been added'}, 201, headers       
    else:
        return{'error': 'Request must be json'}, 400, headers
    
# Delete a member from exp
def deleteMemberFromExp(auth_id,experiment_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    allData = check.experimentCheck(experiment_id)
    if(not allData):
        return{"Error": "Experiment does not exist"},400, headers
    userData = check.userCheck(auth_id)
    if(not userData):
        return{"Error": "User does not exist"},400, headers
    member = supabase.table("members").select('*').eq("experiment_id", experiment_id).eq("user_id", auth_id).execute()
    membersStr = member.json()
    membersObj = json.loads(membersStr)
    membersData = membersObj["data"]
    if(membersData):
        supabase.table("members").delete().eq("experiment_id", experiment_id).eq("user_id", auth_id).execute()
        usagefromId = supabase.table("usage").select('*').eq("user_id", auth_id).eq("experiment_id", experiment_id).is_("end_date", "null").execute()
        usageStr = usagefromId.json()
        usageObj = json.loads(usageStr)
        usageData = usageObj["data"]
        if(usageData):
            current_date = str(timeNow)
            date_now = current_date.split(" ")[0]
            supabase.table("usage").update({
                "end_date": date_now
            }).eq("usage_id", usageData[0]["usage_id"]).execute()
            supabase.table("inventory").update({
                "istatus_id": 1
            }).eq("inventory_id", usageData[0]["inventory_id"]).execute()
        return{"Success": "Member has been removed from experiment"}, 201, headers
    else:
        return{"Error": "Member is not in Experiment"},400, headers
    





        


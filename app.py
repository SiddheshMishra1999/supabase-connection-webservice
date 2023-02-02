import os
import json
from supabase import create_client, Client
from flask_restful import Resource, Api
from flask import Flask, request, render_template




# pylint: disable=C0103
app = Flask(__name__)

# Connecting database
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL,  SUPABASE_ANON_KEY)


@app.route("/")
def home():
    return "Webservice Connecting to Supabase"

@app.get('/getAllUsers')
# For GET request to http://127.0.0.1:5000/getAllUsers
def getUsers():
    userApi = supabase.table("users").select('*').execute()
    userStr = userApi.json()
    userObject = json.loads(userStr)
    allData= userObject["data"]
    user_list = []
    for user in allData:
        user_data = {
            'user_id': user["user_id"], 
            "first_name": user["first_name"],
            "last_name":user["last_name"],
            'email': user['email'], 
            'gender':user['gender'], 
            'role': user['role_id'],
            "date_of_birth": user["date_of_birth"],
            "avatar_url": user["avatar_url"], 
            "password": user["password"],
            "auth_id": user["auth_id"]
        }
        user_list.append(user_data)
    return {"Users": user_list}, 200

@app.post("/newExperiment")
# For POST request to http://127.0.0.1:5000/newExperiment
def postExperiment():
    if request.is_json:
        print(request.json["experiment_creator"])
        print(request.json["experiment_name"])
        print(request.json["pstatus_id"])
        print(request.json["start_date"])
        print(request.json["end_date"])
        print(request.json["description"])


        experiment = supabase.table("experiment").insert(
            {
                "experiment_creator" : request.json["experiment_creator"],
                "experiment_name" : request.json["experiment_name"],
                "pstatus_id" : request.json["pstatus_id"],
                "start_date" : request.json["start_date"],
                "end_date" : request.json["end_date"],
                "description" : request.json["description"]
            }
        ).execute()
        return {"Success": 'the experiment has been added'}, 201
    else:
        return{'error': 'Request must be json'}, 400
# /experiment/create or other entry points
@app.get("/experimentsforSpecificUser/<experiment_creator>")
# For GET request to http://127.0.0.1:5000/experimentsforSpecificUser/?
def getExpSpecificUser(experiment_creator):
    experimentsfromId = supabase.table("experiment").select('*').eq("experiment_creator", experiment_creator).execute()
    experimentsStr = experimentsfromId.json()
    experimentsObject = json.loads(experimentsStr)
    allData= experimentsObject["data"]
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
    return{"UserS_experiments": exp_list}, 200


@app.get('/getUserById/<auth_id>')
def getUserById(auth_id):
    userfromId = supabase.table("users").select("*").eq("auth_id", auth_id).execute()
    userfromIdStr = userfromId.json()
    userfromIdObj = json.loads(userfromIdStr)
    userData = userfromIdObj["data"]
    for user in userData:
        genderId = supabase.table("gender").select("gender").eq("gender_id", user["gender"]).execute().json()
        gender = json.loads(genderId)["data"][0]["gender"]
        roleId = supabase.table("roles").select("role_name").eq("role_id", user["role_id"]).execute().json()
        role = json.loads(roleId)["data"][0]["role_name"]
        user_data = {
                'user_id': user["user_id"], 
                "first_name": user["first_name"],
                "last_name":user["last_name"],
                'email': user['email'], 
                'gender':gender, 
                'role': role,
                "date_of_birth": user["date_of_birth"],
                "avatar_url": user["avatar_url"], 
                "password": user["password"],
                "auth_id": user["auth_id"]
            }
        return {"User": user_data}, 200



    # def delete(self, id):
    #     print("delete")


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

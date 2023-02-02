import json
from supabase_connection import supabase
from flask import Flask, request, render_template


# Get mothod to retreive all users in the Supabase database
def allUsers():
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
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
    return {"Users": user_list}, 201, headers


# Retrieve a user's info based on their auth id
def getUserById(auth_id):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    userfromId = supabase.table("users").select("*").eq("auth_id", auth_id).execute()
    userfromIdStr = userfromId.json()
    userfromIdObj = json.loads(userfromIdStr)
    userData = userfromIdObj["data"]
    if(userData):

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
            return {"User": user_data}, 201, headers
    else:
        return{"Error": "User Does not exist"},400, headers

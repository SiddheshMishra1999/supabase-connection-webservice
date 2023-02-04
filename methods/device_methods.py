import json
from supabase_connection import supabase
from flask import Flask, request, render_template

# Retrieve all devices from Supabase
def allDevices():
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    deviceApi = supabase.table("device").select('*').execute()
    deviceStr = deviceApi.json()
    deviceObject = json.loads(deviceStr)
    allDevices = deviceObject["data"]
    device_list = []
    for device in allDevices:
        device_data = {
            'device_id': device["device_id"],
            'device_name': device["device_name"],
            'description': device["description"]  
        }
        device_list.append(device_data)
    return {"Device" :device_list } ,201, headers


# Insert a new device to Supabase
def insertNewDevice():
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    if request.is_json:
        supabase.table("device").insert(
            {
            'device_name': request.json["device_name"],
            'description': request.json["description"]  
            }
        ).execute()
        return {"Success": 'Device has been added'}, 201, headers
    else:
        return{'error': 'Request must be json'}, 400, headers





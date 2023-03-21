import json
from supabase_connection import supabase
from flask import Flask, request, render_template
import methods.exisitance_check as check


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

# get a specific device details with all its sensors
def getSpecificDevice(device_id):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    deviceData = check.deviceCheck(device_id)
    if(deviceData):
        sensorApi = supabase.table("sensor").select('sensor_name').eq("device_id", device_id).execute()
        sensoreStr = sensorApi.json()
        sensorObject = json.loads(sensoreStr)
        allSensors = sensorObject["data"]
        sensor_list = []
        for sensor in allSensors:
            print(sensor)
            sensor_list.append(sensor["sensor_name"])
        device_details = {
            'device_id': device_id,
            'device_name': deviceData[0]["device_name"],
            'description': deviceData[0]["description"],
            'sensors': sensor_list
        }

        return {"Device": device_details}, 201, headers
    else:
        return{"Error": "Device Does not exist"},400, headers
    




# get a specific device details with all its sensors
def getSpecificDeviceIdFromName(device_name):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    devicefromId = supabase.table("device").select('device_id').eq("device_name", device_name).execute()
    deviceStr = devicefromId.json()
    deviceObj = json.loads(deviceStr)
    deviceData = deviceObj["data"]
    if(deviceData):
        device_id = deviceData[0]["device_id"]
        return {"Device_id": device_id}, 201, headers
    else:
        return{"Error": "Device Does not exist"},400, headers
    




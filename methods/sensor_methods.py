import json
from supabase_connection import supabase
from flask import Flask, request, render_template


# Add a new sensor to the sensor table
def insertNewSensor():
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    if request.is_json:
        supabase.table("sensor").insert(
            {
                "device_id": request.json["device_id"],
                "type_id": request.json["type_id"],
                "sensor_name": request.json["sensor_name"],
                "measurement_unit": request.json["measurement_unit"],
                "sampling_rate": request.json["sampling_rate"],
                "num_channels": request.json["num_channels"],
                "description": request.json["description"],
            }
        ).execute()
        return {"Success": 'Sensor has been added'}, 201, headers
    else:
        return{'error': 'Request must be json'}, 400, headers


# Get sensors for a specific device
def sensorsForDevice(device_id):
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    deviceAPI = supabase.table("device").select("device_name").eq("device_id", device_id).execute()
    deviceStr = deviceAPI.json()
    deviceObj = json.loads(deviceStr)
    deviceData = deviceObj["data"]
    if(deviceData):
        sensor_list = []
        sensorsApi = supabase.table("sensor").select("*").eq("device_id", device_id).execute()
        sensorsStr = sensorsApi.json()
        sensorsObj = json.loads(sensorsStr)
        sensorsData = sensorsObj["data"]
        for sensor in sensorsData:
            device_id = supabase.table("device").select("device_name").eq("device_id", device_id).execute().json()
            device_name = json.loads(device_id)["data"][0]["device_name"]
            sensors_data = {
                "sensor_id": sensor["sensor_id"],
                "device_name": device_name,
                "type_id": sensor["type_id"],
                "sensor_name": sensor["sensor_name"],
                "measurement_unit": sensor["measurement_unit"],
                "sampling_rate": sensor["sampling_rate"],
                "num_channels": sensor["num_channels"],
                "description": sensor["description"],
            }
            sensor_list.append(sensors_data)
        return{"Sensors": sensor_list}, 201, headers
    else:
        return{"Error": "Device does not exist"},400, headers
        


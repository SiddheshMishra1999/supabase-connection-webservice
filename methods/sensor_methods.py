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

    
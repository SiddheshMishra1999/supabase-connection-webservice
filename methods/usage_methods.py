import json
from supabase_connection import supabase
from flask import Flask, request, render_template
import methods.exisitance_check as check
import methods.inventory_methods as inventory
from datetime import datetime, timedelta


# current time
timeNow = datetime.now()

def getAllUsage():
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    usage = supabase.table("usage").select('*').execute()
    usageStr = usage.json()
    usageObject = json.loads(usageStr)
    allUsage= usageObject["data"]
    usage_list = []
    for usage in allUsage:
        usage_data = {
            "usage_id": usage["usage_id"],
            "user_id": usage["user_id"],
            "experiment_id": usage["experiment_id"],
            "inventory_id": usage["inventory_id"],
            "start_date": usage["start_date"],
            "end_date": usage["end_date"],
        }
        usage_list.append(usage_data)
        
    return {"Usage": usage_list }, 201, headers
    

# Add a new usage to the usage table
def insertNewUsage(experiment_id, user_id, inventory_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    inventoryData = check.inventoryCheck(inventory_id)
    if(not inventoryData):
        return{'Error': 'Device does not exist'}, 400, headers
    allData = check.experimentCheck(experiment_id)
    if(not allData):
        return{"Error": "Experiment does not exist"},400, headers
    userData = check.userCheck(user_id)
    if(not userData):
        return{"Error": "User does not exist"},400, headers
    member = supabase.table("members").select('*').eq("experiment_id", experiment_id).eq("user_id", user_id).execute()
    membersStr = member.json()
    membersObj = json.loads(membersStr)
    membersData = membersObj["data"]
    if(membersData):
        supabase.table("usage").insert({
            "experiment_id": experiment_id,
            "user_id": user_id,
            "inventory_id": inventory_id,
            "start_date": str(timeNow),
        }).execute()
        supabase.table("inventory").update({
                "istatus_id": 2
            }).eq("inventory_id", inventory_id).execute()
        return {"Success": 'Usage has been added'}, 201, headers
    else:
        return{"Error": "Member is not in Experiment"},400, headers

# Update the end date of a usage item
def updateUsageId(usage_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    usageData = check.usageCheck(usage_id)
    if( not usageData):
        return{"Error": "Usade id does not exist"},400, headers
    if request.is_json:
        end_date = request.json["end_date"]
        current_date = str(timeNow)
        date_now = current_date.split(" ")[0]
        # Checking to make sure end date is greater than current date
        if(end_date >= date_now):
            supabase.table("usage").update({
                "end_date": request.json["end_date"]
            }).eq("usage_id", usage_id).execute()
            supabase.table("inventory").update({
                "istatus_id": 1
            }).eq("inventory_id", usageData[0]["inventory_id"]).execute()
            
            return {"Success": "End date has been updated" }, 201, headers
        else:
            return{'Error': 'End date cannot be smaller than current date'}, 400, headers   
    else:
        return{'error': 'Request must be json'}, 400, headers

# Get device name based on user id and experiment id
def getSpecificUseageIdFromUsrExp(user_id, experiment_id, inventory_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    userData = check.userCheck(user_id)
    allData = check.experimentCheck(experiment_id)
    if(not allData):
        return{"Error": "Experiment does not exist"},400, headers
    userData = check.userCheck(user_id)
    if(not userData):
        return{"Error": "User does not exist"},400, headers
    inventoryData = check.inventoryCheck(inventory_id)
    if(not inventoryData):
        return{"Error": "Inventory id does not exist"},400, headers
    if(userData and allData):
        usageIdQuery = supabase.table("usage").select("usage_id").eq("user_id", user_id).eq("experiment_id", experiment_id).eq("inventory_id", inventory_id).is_("end_date", "null").execute()
        usageIdStr = usageIdQuery.json()
        usageIdObj = json.loads(usageIdStr)
        usageIdData = usageIdObj["data"]
        usage_id =  usageIdData[0]["usage_id"]
        usageData = check.usageCheck(usage_id)
        if(usageData):
            # inventory_id = usageData[0]["inventory_id"]
            # deviceid = supabase.table("inventory").select("device_id").eq("inventory_id", inventory_id).execute()
            # deviceidStr = deviceid.json()
            # deviceidObj = json.loads(deviceidStr)
            # deviceId = deviceidObj["data"][0]["device_id"]
            # deviceName = supabase.table("device").select("device_name").eq("device_id", deviceId).execute()
            # deviceNameStr = deviceName.json()
            # deviceNameObj = json.loads(deviceNameStr)
            # devicename = deviceNameObj["data"][0]["device_name"]
            
            return {"usage_id": usage_id }, 201, headers
        else:
            return{"Error": "Usage does not exist"},400, headers
    else:
        return{"Error": "User and/or Experiment does not exist"},400, headers


# Get invnetory id, device name based on user id and experiment id
def getSpecificinventoryIdFromUsrExp(user_id, experiment_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    userData = check.userCheck(user_id)
    allData = check.experimentCheck(experiment_id)
    if(not allData):
        return{"Error": "Experiment does not exist"},400, headers
    userData = check.userCheck(user_id)
    if(not userData):
        return{"Error": "User does not exist"},400, headers

    if(userData and allData):
        usageIdQuery = supabase.table("usage").select("usage_id").eq("user_id", user_id).eq("experiment_id", experiment_id).is_("end_date", "null").execute()
        usageIdStr = usageIdQuery.json()
        usageIdObj = json.loads(usageIdStr)
        usageIdData = usageIdObj["data"]
        usage_id =  usageIdData[0]["usage_id"]
        usageData = check.usageCheck(usage_id)
        if(usageData):
            inventory_id = usageData[0]["inventory_id"]
            deviceid = supabase.table("inventory").select("device_id").eq("inventory_id", inventory_id).execute()
            deviceidStr = deviceid.json()
            deviceidObj = json.loads(deviceidStr)
            deviceId = deviceidObj["data"][0]["device_id"]
            deviceName = supabase.table("device").select("device_name").eq("device_id", deviceId).execute()
            deviceNameStr = deviceName.json()
            deviceNameObj = json.loads(deviceNameStr)
            devicename = deviceNameObj["data"][0]["device_name"]
            data = {
                "inventory_id" : inventory_id,
                "device_id": deviceId,
                "device_name" : devicename
            }
            
            return {"info": data }, 201, headers
        else:
            return{"Error": "Usage does not exist"},400, headers
    else:
        return{"Error": "User and/or Experiment does not exist"},400, headers


# Get Usage detail from usage ID
def getUseageInfo(usage_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    usageData = check.usageCheck(usage_id)
    if(usageData):

        return {"Usage": usageData[0]}, 201, headers
    else:
        return{"Error": "Usage id does not exist"},400, headers

# Getting usage id based on the device name and serial number
def getUseageIdfromName(device_name, serialNum):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    deviceAPI = supabase.table("device").select("device_id").eq("device_name", device_name).execute()
    deviceStr = deviceAPI.json()
    deviceObj = json.loads(deviceStr)
    deviceData = deviceObj["data"]
    device_id = deviceData[0]["device_id"]
    if(deviceData):
        inventoryfromId = supabase.table("inventory").select('inventory_id').eq("device_id", device_id).eq("serial_num", serialNum).execute()
        inventoryStr = inventoryfromId.json()
        inventoryObj = json.loads(inventoryStr)
        inventoryData = inventoryObj["data"]
        inventory_id = inventoryData[0]["inventory_id"]

        # getting all inventory ids for that device that are in use
        # for each of those inventory ids, get all the usage id with a null usage id
        usageApi = supabase.table("usage").select('usage_id').eq("inventory_id", inventory_id).is_("end_date", "null").execute()
        usageStr = usageApi.json()
        usageObject = json.loads(usageStr)
        usageId = usageObject["data"]
        
        return {"Usage": usageId}, 201, headers
    else:
        return{"Error": "Device name invalid"},400, headers




# Get device name based on user id and experiment id
def getSpecificUseageIdFromUsrExponly(user_id, experiment_id):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    userData = check.userCheck(user_id)
    allData = check.experimentCheck(experiment_id)
    if(not allData):
        return{"Error": "Experiment does not exist"},400, headers
    userData = check.userCheck(user_id)
    if(not userData):
        return{"Error": "User does not exist"},400, headers

    if(userData and allData):
        usageIdQuery = supabase.table("usage").select("usage_id").eq("user_id", user_id).eq("experiment_id", experiment_id).is_("end_date", "null").execute()
        usageIdStr = usageIdQuery.json()
        usageIdObj = json.loads(usageIdStr)
        usageIdData = usageIdObj["data"]
        print(usageIdData)
        usage_id =  usageIdData[0]["usage_id"]
        usageData = check.usageCheck(usage_id)
        if(usageData):
            inventory_id = usageData[0]["inventory_id"]
            deviceid = supabase.table("inventory").select("device_id").eq("inventory_id", inventory_id).execute()
            deviceidStr = deviceid.json()
            deviceidObj = json.loads(deviceidStr)
            deviceId = deviceidObj["data"][0]["device_id"]
            deviceName = supabase.table("device").select("device_name").eq("device_id", deviceId).execute()
            deviceNameStr = deviceName.json()
            deviceNameObj = json.loads(deviceNameStr)
            devicename = deviceNameObj["data"][0]["device_name"]
            data = {
                "usage_id": usage_id,
                "device_name": devicename
            }
            return {"usage": data }, 201, headers
        else:
            return{"Error": "Usage does not exist"},400, headers
    else:
        return{"Error": "User and/or Experiment does not exist"},400, headers
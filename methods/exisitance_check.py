import json
from supabase_connection import supabase
from flask import Flask, request, render_template


# Check if user Exists
def userCheck(auth_id):
    userfromId = supabase.table("users").select("*").eq("auth_id", auth_id).execute()
    userfromIdStr = userfromId.json()
    userfromIdObj = json.loads(userfromIdStr)
    userData = userfromIdObj["data"]
    if(userData):
        return userData
    else:
        False

# Check if experiment Exists
def experimentCheck(experiment_id):
    experimentsfromId = supabase.table("experiment").select('*').eq("experiment_id", experiment_id).execute()
    experimentsStr = experimentsfromId.json()
    experimentsObject = json.loads(experimentsStr)
    allData= experimentsObject["data"]

    if(allData):
        return allData
    else:
        return False
    
# Check if Device Exists
def deviceCheck(device_id):
    devicefromId = supabase.table("device").select('*').eq("device_id", device_id).execute()
    deviceStr = devicefromId.json()
    deviceObj = json.loads(deviceStr)
    deviceData = deviceObj["data"]
    if(deviceData):
        return deviceData
    else:
        return False

# Check if Inventory Exists
def inventoryCheck(inventory_id):
    inventoryfromId = supabase.table("inventory").select('*').eq("inventory_id", inventory_id).execute()
    inventoryStr = inventoryfromId.json()
    inventoryObj = json.loads(inventoryStr)
    inventoryData = inventoryObj["data"]
    if(inventoryData):
        return inventoryData
    else:
        return False

# Check if Usage Exists
def usageCheck(usage_id):
    usagefromId = supabase.table("usage").select('*').eq("usage_id", usage_id).execute()
    usageStr = usagefromId.json()
    usageObj = json.loads(usageStr)
    usageData = usageObj["data"]
    if(usageData):
        return usageData
    else:
        return False

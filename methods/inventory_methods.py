import json
from supabase_connection import supabase
from flask import Flask, request, render_template
import methods.exisitance_check as check
from datetime import datetime, timedelta


# current time
timeNow = datetime.now()

# This table is used to see how many devices we have in store and how many are in use
def allItemsInInventory():
    headers = {
    'Access-Control-Allow-Origin': '*'
    }
    inventoryApi = supabase.table("inventory").select('*').execute()
    inventoryStr = inventoryApi.json()
    inventoryObject = json.loads(inventoryStr)
    allItems = inventoryObject["data"]
    inventorylist = []
    for item in allItems:
        deviceAPI = supabase.table("device").select("device_name").eq("device_id", item["device_id"]).execute().json()
        deviceObj = json.loads(deviceAPI)
        deviceName = deviceObj["data"][0]["device_name"]

        istatusAPI = supabase.table("inventory_status").select("status_name").eq("istatus_id", item["istatus_id"]).execute().json()
        istatusObj = json.loads(istatusAPI)
        statusName = istatusObj["data"][0]["status_name"]

        dconditionAPI = supabase.table("device_condition").select("condition_of_device").eq("condition_id", item["condition_id"]).execute().json()
        dconditionObj = json.loads(dconditionAPI)
        condition = dconditionObj["data"][0]["condition_of_device"]

        inventory_data = {
            "inventory_id": item["inventory_id"],
            "device_id": item["device_id"],
            "device_name": deviceName,
            "device_status": statusName,
            "device_condition" : condition, 
            "date_added": item["date_added"]
        }
        inventorylist.append(inventory_data)
    return {"Inventory" : inventorylist } ,201, headers

# Insert a new inventory item
def addInventoryItem():
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    if request.is_json:
        deviceData = check.deviceCheck(request.json["device_id"])
        if(not deviceData):
            return{'Error': 'Device does not exist'}, 400, headers
        
        supabase.table("inventory").insert({
             "device_id": request.json["device_id"],
             "istatus_id": request.json["istatus_id"],
             "condition_id": request.json["condition_id"],
             "serialNum": request.json["serialNum"],
             "date_added": str(timeNow)

        }).execute()
        return {"Success": 'Inventory item has been added'}, 201, headers
    else:
        return{'error': 'Request must be json'}, 400, headers

# get inventory ids from device id which are in use
def inventoryIdFromDeviceId(device_id):
    deviceData = check.deviceCheck(device_id)
    if(deviceData):
        inventoryApi = supabase.table("inventory").select('inventory_id').eq("device_id", device_id).eq("istatus_id", 2).execute()
        inventoryStr = inventoryApi.json()
        inventoryObject = json.loads(inventoryStr)
        allItems = inventoryObject["data"]
        inventorylist = []
        for item in allItems:
            inventorylist.append(item["inventory_id"])
        return inventorylist
    else:
        return {"Error": "Device Does not exist"}


# Get all available devices from inventory
def getAvailableDevices():
        
    headers = {
        'Access-Control-Allow-Origin': '*'
        }
    inventoryApi = supabase.table("inventory").select('*').eq("istatus_id", 1).execute()
    inventoryStr = inventoryApi.json()
    inventoryObject = json.loads(inventoryStr)
    allItems = inventoryObject["data"]
    inventorylist = []
    for item in allItems:
        deviceAPI = supabase.table("device").select("device_name").eq("device_id", item["device_id"]).execute().json()
        deviceObj = json.loads(deviceAPI)
        deviceName = deviceObj["data"][0]["device_name"]

        istatusAPI = supabase.table("inventory_status").select("status_name").eq("istatus_id", item["istatus_id"]).execute().json()
        istatusObj = json.loads(istatusAPI)
        statusName = istatusObj["data"][0]["status_name"]

        dconditionAPI = supabase.table("device_condition").select("condition_of_device").eq("condition_id", item["condition_id"]).execute().json()
        dconditionObj = json.loads(dconditionAPI)
        condition = dconditionObj["data"][0]["condition_of_device"]

        inventory_data = {
            "inventory_id": item["inventory_id"],
            "device_id": item["device_id"],
            "device_name": deviceName,
            "device_status": statusName,
            "device_condition" : condition, 
            "date_added": item["date_added"]
        }
        inventorylist.append(inventory_data)
    return {"Inventory" : inventorylist } ,201, headers
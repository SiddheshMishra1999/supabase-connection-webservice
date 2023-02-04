import json
from supabase_connection import supabase
from flask import Flask, request, render_template

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
            "device_id": item["device_id"],
            "device_name": deviceName,
            "device_status": statusName,
            "device_condition" : condition, 
            "date_added": item["date_added"]
        }
        inventorylist.append(inventory_data)
    return {"Inventory" : inventorylist } ,201, headers

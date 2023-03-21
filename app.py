import os
import json
from supabase import create_client, Client
from flask_restful import Resource, Api
from flask import Flask, request, render_template
import methods.experiment_methods  as exp
import methods.user_methods as users
import methods.member_methods as member
import methods.device_methods as device
import methods.sensor_methods as sensor
import methods.inventory_methods as inventory
import methods.usage_methods as usage



from supabase_connection import supabase


# pylint: disable=C0103
app = Flask(__name__)




@app.route("/")
def home():
    return "Webservice Connecting to Supabase"

# --------------------- User Table methods -----------------------------#

# Route to get all users
@app.get('/users/get/all')
# For GET request to http://127.0.0.1:5000/getAllUsers
def getAllUsers():
    return users.allUsers()

# Route to get User info by auth id
@app.get('/users/get/<auth_id>')
def getSpecificUserInfo(auth_id):
    return users.getUserById(auth_id)


# --------------------- Experiment Table methods -----------------------------#

# Route to Insert new Experiment
@app.post("/experiment/insert/<experiment_creator>/<experiment_name>/<pstatus_id>/<start_date>/<num_of_participants>/<end_date>/<eligibility>/<description>")
def insertExperiment(experiment_creator, experiment_name, pstatus_id, start_date, num_of_participants, end_date, eligibility, description):
    return exp.insertNewExperiment(experiment_creator, experiment_name, pstatus_id, start_date, num_of_participants, end_date, eligibility, description)

# Route to update an Experiment
@app.post("/experiment/update/<experiment_id>/<experiment_name>/<pstatus_id>/<start_date>/<num_of_participants>/<end_date>/<eligibility>/<description>")
def updateOldExperiment(experiment_id, experiment_name, pstatus_id, start_date, num_of_participants, end_date, eligibility, description):
    return exp.updateExperiment(experiment_id, experiment_name, pstatus_id, start_date, num_of_participants, end_date, eligibility, description)


# Route to get Experiment from creator
@app.get("/experiment/get/creator/<experiment_creator>")
def getSpecificUserExperiment(experiment_creator):
    return exp.getExpSpecificUser(experiment_creator)

# Route to get all experiments
@app.get("/experiment/get/all")
def getAllExperiments():
    return exp.allExperiments()

# Route to delete specific experiment 
@app.post("/experiment/delete/<experiment_id>")
def deleteExperiment(experiment_id):
    return exp.deleteExperimentById(experiment_id)

# Route to get a specific Experiment
@app.get("/experiment/get/<experiment_id>")
def getSpecificExperiment(experiment_id):
    return exp.getExperimentById(experiment_id)


# --------------------- Members Table methods -----------------------------#

# Route to get all members in an experiment
@app.get("/members/get/mem/<experiment_id>")
def getMembersForExperiment(experiment_id):
    return member.membersInExperiment(experiment_id)

# Route to get all experiment id in members table 
@app.get("/members/get/expid")
def getExperimentIdInMembers():
    return member.expInMembersTable()

# Route to get all experiments for a member
@app.get("/members/get/exp/<auth_id>")
def getExperimentsForMember(auth_id):
    return member.experimentForMember(auth_id)

# Route to get member count in an experiment 
@app.get("/members/get/count/<experiment_id>")
def getMemberCountForExperiment(experiment_id):
    return member.membersCountInExperiment(experiment_id)

# Route to Insert new Member
@app.post("/members/insert/<experiment_id>/<auth_id>")
def insertMember(experiment_id, auth_id):
    return member.insertMemberInExperiment(experiment_id, auth_id)

# Route to delete a member from experiment 
@app.post("/members/delete/<auth_id>/<experiment_id>")
def deleteMember(experiment_id, auth_id):
    return member.deleteMemberFromExp(auth_id,experiment_id)

# --------------------- Device Table methods -----------------------------#

# Route to get all devices
@app.get("/device/get/all")
def getAllDevices():
    return device.allDevices()

# Route to Insert new Device
@app.post("/device/insert")
def insertDevice():
    return device.insertNewDevice()

# Route to get a specific device details with all its sensors
@app.get("/device/get/<device_id>")
def getSpecificDeviceInfo(device_id):
    return device.getSpecificDevice(device_id)

# Route to get a specific device id from the decice name
@app.get("/device/get/id/<device_name>")
def getSpecificDeviceInfofromName(device_name):
    return device.getSpecificDeviceIdFromName(device_name)

# --------------------- Sensor Table methods -----------------------------#
# Route to Insert new sensor
@app.post("/sensor/insert")
def insertSensor():
    return sensor.insertNewSensor()

# Route to get the sensors in a specific device
@app.get("/sensor/get/device/<device_id>")
def getSensorsForDevice(device_id):
    return sensor.sensorsForDevice(device_id)


# --------------------- Inventory Table methods -----------------------------#

# Route to get all Inventory items
@app.get("/inventory/get/all")
def getAllItemsInInventory():
    return inventory.allItemsInInventory()

# Route to Insert new inventory item
@app.post("/inventory/insert")
def insertInventory():
    return inventory.addInventoryItem()


# Route to get all available Inventory items
@app.get("/inventory/get/available")
def getAllAvailableItemsInInventory():
    return inventory.getAvailableDevices()

# --------------------- Usage Table methods -----------------------------# 
# Route to get specific usage id
@app.get("/usage/get/<auth_id>/<experiment_id>/<inventory_id>")
def getUsageIdFromUsrExp(auth_id, experiment_id, inventory_id):
    return usage.getSpecificUseageIdFromUsrExp(auth_id, experiment_id, inventory_id)

# Route to get specific usage id
@app.get("/usage/get/inventory/<auth_id>/<experiment_id>")
def getinventoryFromUsrExp(auth_id, experiment_id):
    return usage.getSpecificinventoryIdFromUsrExp(auth_id, experiment_id)

# Route to get usage from usage id
@app.get("/usage/get/<usage_id>")
def getUsageFromUsageId(usage_id):
    return usage.getUseageInfo(usage_id)

# Route to get usage from device name
@app.get("/usage/get/device/<device_name>/<serialNum>")
def getUsageIdFromDeviceName(device_name,serialNum):
    return usage.getUseageIdfromName(device_name,serialNum)

# Route to get all usage
@app.get("/usage/get/all")
def getAllUsages():
    return usage.getAllUsage()

# Route to Insert new usage
@app.post("/usage/insert/<experiment_id>/<user_id>/<inventory_id>")
def insertUsage(experiment_id, user_id, inventory_id):
    return usage.insertNewUsage(experiment_id, user_id, inventory_id)

# Route to update the usage end date
@app.put("/usage/update/<usage_id>")
def putUsageEndDate(usage_id):
    return usage.updateUsageId(usage_id)


# Route to get the usage id and device name from authid and exp id 
@app.get("/usage/get/usageid/<user_id>/<experiment_id>")
def getusagefromauthidexpid(user_id, experiment_id):
    return usage.getSpecificUseageIdFromUsrExponly(user_id, experiment_id)


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

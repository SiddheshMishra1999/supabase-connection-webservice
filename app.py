import os
import json
from supabase import create_client, Client
from flask_restful import Resource, Api
from flask import Flask, request, render_template
import methods.experiment_methods  as exp
import methods.user_methods as users
import methods.member_methods as member
from dotenv import load_dotenv

from supabase_connection import supabase


# pylint: disable=C0103
app = Flask(__name__)

load_dotenv()



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
@app.post("/experiment/insert")
def insertExperiment():
    return exp.insertNewExperiment()

# Route to get Experiment from creator
@app.get("/experiment/get/<experiment_creator>")
def getSpecificUserExperiment(experiment_creator):
    return exp.getExpSpecificUser(experiment_creator)

# Route to get all experiments
@app.get("/experiment/get/all")
def getAllExperiments():
    return exp.allExperiments()

# Route to get Experiment from creator
@app.delete("/experiment/delete/<experiment_id>")
def deleteExperiment(experiment_id):
    return exp.deleteExperimentById(experiment_id)

# --------------------- Members Table methods -----------------------------#

# Route to get all members in an experiment
@app.get("/members/get/<experiment_id>")
def getMembersForExperiment(experiment_id):
    return member.membersInExperiment(experiment_id)

# Route to Insert new Member
@app.post("/members/insert")
def insertMember():
    return member.insertMemberInExperiment()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

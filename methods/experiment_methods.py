import json
from supabase_connection import supabase


def getExpSpecificUser(experiment_creator):
    experimentsfromId = supabase.table("experiment").select('*').eq("experiment_creator", experiment_creator).execute()
    experimentsStr = experimentsfromId.json()
    experimentsObject = json.loads(experimentsStr)
    allData= experimentsObject["data"]
    exp_list = []
    for experiments in allData:
        experiment_status = supabase.table("experiment_status").select("status_name").eq("pstatus_id", experiments["pstatus_id"]).execute().json()
        status = json.loads(experiment_status)["data"][0]["status_name"]
        user_experiments = {
            "experiment_id": experiments["experiment_id"],
            "experiment_name": experiments["experiment_name"],
            "experiment_status": status,
            "experiment_eligibility": experiments["eligibility"],
            "num_of_participants": experiments["num_of_participants"],
            "start_date": experiments["start_date"],
            "end_date": experiments["end_date"],
            "description": experiments["description"],
        }
        exp_list.append(user_experiments)
    return{"UserS_experiments": exp_list}, 200
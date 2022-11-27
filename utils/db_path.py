import json

def get_db_path():
    with open("config.json", "r") as f:
        data = json.loads(f.read())
        if data["DB"]["CURRENT_FILE_NAME"] == "":
            return data["DB"]["DEFAULT_FILE_NAME"]
        return data["DB"]["CURRENT_FILE_NAME"]


def set_db_path(db_path):
    print(f"set db file : {db_path}")
    with open("config.json", "r") as f:
        org_data = json.loads(f.read())

    org_data["DB"]["CURRENT_FILE_NAME"] = db_path
        
    with open("config.json", "w") as f:
        json.dump(org_data, f, indent="\t")
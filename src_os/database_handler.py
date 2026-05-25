import json
import threading
import os

db_lock = threading.Lock()
DB_FILE = 'central_db.json'

def initialize_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)

def update_dashboard_data(subgroup, data):
    with db_lock:
        try:
            with open(DB_FILE, 'r') as f:
                db = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            db = {}
        
        db[subgroup] = data
        
        with open(DB_FILE, 'w') as f:
            json.dump(db, f, indent=4)

def get_dashboard_data():
    with db_lock:
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
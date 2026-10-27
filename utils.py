import hashlib

def hash_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    
    return hashed

def check_password(user_entry, db_entry):
    hashed_user_entry = hash_password(user_entry)
    
    return db_entry == hashed_user_entry

def format_date(date_ms):
    from datetime import datetime
    
    date = datetime.fromtimestamp(date_ms / 1000.0)
    
    return date.strftime("%d.%m.%Y")
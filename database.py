from pymongo import MongoClient
from datetime import datetime
import pytz
import jdatetime

client = MongoClient("mongodb://localhost:27017/")  ## Local 
db = client["bale_beauty_clinic"]
users_col = db["users"]

tehran_tz = pytz.timezone("Asia/Tehran")

def save_user_interaction(data):
    now_tehran = datetime.now(tehran_tz)
    data["تاریخ"] = jdatetime.datetime.fromgregorian(datetime=now_tehran).strftime("%Y/%m/%d")
    data["زمان"] = now_tehran.strftime("%H:%M:%S")
    data["timestamp"] = now_tehran
    return users_col.insert_one(data)

def get_bot_stats():
    """دریافت آمار کلی ربات"""
    total_users = users_col.count_documents({})
    
    # آمار امروز
    today = jdatetime.date.today().strftime("%Y/%m/%d")
    today_count = users_col.count_documents({"تاریخ": today})
    
    # آمار این هفته
    from datetime import timedelta
    week_ago = datetime.now(tehran_tz) - timedelta(days=7)
    week_count = users_col.count_documents({"timestamp": {"$gte": week_ago}})
    
    return {
        "total_users": total_users,
        "today_count": today_count,
        "week_count": week_count
    }

def get_all_users_data():
    return list(users_col.find({}, {"_id": 0}))

def get_users_data_by_days(days):
    from datetime import timedelta
    cutoff = datetime.now(tehran_tz) - timedelta(days=days)
    return list(users_col.find({"timestamp": {"$gte": cutoff}}, {"_id": 0}))

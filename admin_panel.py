# admin_panel.py
from datetime import datetime, timedelta
import pytz
from config import TIMEZONE, MAX_ADMIN_ATTEMPTS, ADMIN_BLOCK_MINUTES, ADMIN_SESSION_MINUTES

tehran = pytz.timezone(TIMEZONE)
admin_fails = {}
admin_active_sessions = {}

def admin_login_attempt(user_id, success):
    if success:
        admin_fails.pop(user_id, None)
        return (0, 0)
    now = datetime.now(tehran)
    if user_id not in admin_fails:
        admin_fails[user_id] = {"count": 1, "first_fail": now}
        return (1, MAX_ADMIN_ATTEMPTS - 1)
    else:
        admin_fails[user_id]["count"] += 1
        if admin_fails[user_id]["count"] >= MAX_ADMIN_ATTEMPTS:
            admin_fails[user_id]["blocked_until"] = now + timedelta(minutes=ADMIN_BLOCK_MINUTES)
        return (admin_fails[user_id]["count"], MAX_ADMIN_ATTEMPTS - admin_fails[user_id]["count"])

def is_admin_blocked(user_id):
    if user_id not in admin_fails:
        return False
    block_time = admin_fails[user_id].get("blocked_until")
    if block_time and datetime.now(tehran) < block_time:
        return True
    return False

def start_admin_session(user_id):
    admin_active_sessions[user_id] = datetime.now(tehran)

def is_admin_session_active(user_id):
    if user_id not in admin_active_sessions:
        return False
    if datetime.now(tehran) - admin_active_sessions[user_id] > timedelta(minutes=ADMIN_SESSION_MINUTES):
        return False
    return True

def end_admin_session(user_id):
    admin_active_sessions.pop(user_id, None)

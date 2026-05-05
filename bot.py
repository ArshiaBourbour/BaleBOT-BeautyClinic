# bot.py
import requests
import time
import json
import csv
import io
import sys
import os

# تنظیم کدینگ خروجی کنسول برای ویندوز
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# ایمپورت تنظیمات و ماژول‌های خودمون
from config import TOKEN, BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from database import save_user_interaction, get_all_users_data, get_users_data_by_days, get_bot_stats
from keyboards import *
from admin_panel import *

# متغیرهای سراسری برای ذخیره وضعیت کاربران
user_temp_data = {}      # ذخیره موقت اطلاعات کاربر (نام، شماره، وزن، ...)
user_states = {}         # ذخیره وضعیت کاربر (waiting_fullname, waiting_phone, ...)

# ======================== ادامه کد (توابع send_message, get_updates, ...) ========================

# تنظیم کدینگ خروجی کنسول برای ویندوز
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from config import TOKEN, BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from database import save_user_interaction, get_all_users_data, get_users_data_by_days
from keyboards import *
from admin_panel import *

# متغیرهای ذخیره وضعیت کاربران
user_temp_data = {}
user_states = {}

# ======================== توابع کمکی API بله ========================
def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    response = requests.post(url, json=payload)
    return response.json()

def edit_message_text(chat_id, message_id, text, reply_markup=None):
    url = f"{BASE_URL}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    response = requests.post(url, json=payload)
    return response.json()

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    payload = {"timeout": 30}
    if offset:
        payload["offset"] = offset
    response = requests.post(url, json=payload)
    return response.json().get("result", [])

# ========================  CSV ا========================
def send_csv(chat_id, data_list, filename_prefix):
    if not data_list:
        send_message(chat_id, "⚠️ اطلاعاتی برای این بازه وجود ندارد.")
        return
    
    try:
        my_fields_order = [
            'نام و نام خانوادگی',      
            'شماره تماس',        
            'خدمات انتخاب شده',       
            'نوع مشتری(مخصوص لیزر)', 
            'وزن',       
            'قد',      
            'سن',         
            'جنسیت',      
            'تاریخ',         
            'زمان'           
        ]
        
        # فیلدهایی که اصلاً نمیخوای توی CSV باشن
        unwanted_fields = ['_id', 'timestamp']
        # ==============================================
        
        # فقط فیلدهای مورد نظر رو نگه دار
        fieldnames = [f for f in my_fields_order if f not in unwanted_fields]
        
        # ساخت فایل CSV
        filepath = os.path.join(os.getcwd(), f"{filename_prefix}.csv")
        
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in data_list:
                # فقط فیلدهای مورد نظر رو از دیتابیس بگیر
                filtered_record = {}
                for field in fieldnames:
                    value = record.get(field, "")
                    # اگه مقدار None بود به خالی تبدیل کن
                    if value is None:
                        value = ""
                    filtered_record[field] = value
                writer.writerow(filtered_record)
        
        # ارسال فایل
        url = f"{BASE_URL}/sendDocument"
        
        with open(filepath, 'rb') as f:
            files = {'document': (f"{filename_prefix}.csv", f, 'text/csv')}
            data = {'chat_id': chat_id, 'caption': f'📊 گزارش {filename_prefix}'}
            response = requests.post(url, data=data, files=files)
            result = response.json()
        
        # پاک کردن فایل موقت
        os.remove(filepath)
        
        if result.get('ok'):
            send_message(chat_id, f"✅ فایل {filename_prefix} با موفقیت ارسال شد.")
        else:
            error_msg = result.get('description', 'خطای ناشناخته')
            print(f"API Error: {result}")
            send_message(chat_id, f"❌ خطا در ارسال فایل: {error_msg}")
        
    except Exception as e:
        print(f"Error: {e}")
        send_message(chat_id, f"❌ خطا: {str(e)}")

# ======================== توابع دریافت اطلاعات از کاربر ========================
def ask_fullname(chat_id, user_id, service_info):
    user_temp_data[user_id] = service_info
    user_states[user_id] = "waiting_fullname"
    send_message(chat_id, "👤 لطفاً نام و نام خانوادگی خود را وارد کنید:")

def ask_phone(chat_id, user_id):
    user_states[user_id] = "waiting_phone"
    send_message(chat_id, "📞 لطفاً شماره تلفن خود را وارد کنید (مثال: ۰۹۱۲۳۴۵۶۷۸۹):")

def process_fullname(chat_id, user_id, fullname):
    user_temp_data[user_id]["fullname"] = fullname
    ask_phone(chat_id, user_id)

def process_phone(chat_id, user_id, phone):
    phone = phone.strip().replace(" ", "")
    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    phone = phone.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
    
    if len(phone) == 11 and phone.startswith("09"):
        user_temp_data[user_id]["phone"] = phone
        save_user_interaction(user_temp_data[user_id])
        send_message(chat_id, "✅ اطلاعات شما با موفقیت ثبت شد\nدر اسرع وقت کارشناسان ما با شما تماس خواهند گرفت", reply_markup=back_to_main_button())
        user_temp_data.pop(user_id, None)
        user_states.pop(user_id, None)
    else:
        send_message(chat_id, "⚠️ شماره باید ۱۱ رقمی و با ۰۹ شروع شود. دوباره وارد کنید:")
        user_states[user_id] = "waiting_phone"

# ======================== توابع دریافت رژیم ========================
def ask_weight(chat_id, user_id, service_info):
    user_temp_data[user_id] = service_info
    user_states[user_id] = "waiting_weight"
    send_message(chat_id, "⚖️ وزن خود را به کیلوگرم وارد کنید:")

def ask_height(chat_id, user_id):
    user_states[user_id] = "waiting_height"
    send_message(chat_id, "📏 قد خود را به سانتی‌متر وارد کنید:")

def ask_age(chat_id, user_id):
    user_states[user_id] = "waiting_age"
    send_message(chat_id, "🎂 سن خود را وارد کنید:")

def ask_gender(chat_id, user_id):
    user_states[user_id] = "waiting_gender"
    send_message(chat_id, "👤 جنسیت خود را وارد کنید (مرد/زن):")

def process_weight(chat_id, user_id, weight):
    user_temp_data[user_id]["weight"] = weight
    ask_height(chat_id, user_id)

def process_height(chat_id, user_id, height):
    user_temp_data[user_id]["height"] = height
    ask_age(chat_id, user_id)

def process_age(chat_id, user_id, age):
    user_temp_data[user_id]["age"] = age
    ask_gender(chat_id, user_id)

def process_gender(chat_id, user_id, gender):
    user_temp_data[user_id]["gender"] = gender
    ask_phone(chat_id, user_id)

# ======================== هندلر دکمه‌ها ========================
def handle_callback(chat_id, message_id, callback_data, user_id):
    # برگشت به منوها
    if callback_data == "back_main":
        edit_message_text(chat_id, message_id, "به کلینیک زیبایی لادن خوش آمدید🌹\nلطفا خدمات موردنظر خود را انتخاب کنید", reply_markup=main_menu())
        return
    
    if callback_data == "back_laser":
        edit_message_text(chat_id, message_id, "✨ خدمات لیزر را انتخاب کنید:", reply_markup=laser_menu())
        return
    
    if callback_data == "back_weight_loss":
        edit_message_text(chat_id, message_id, "🏋️ خدمات لاغری را انتخاب کنید:", reply_markup=weight_loss_menu())
        return
    
    # منوی اصلی
    if callback_data == "laser":
        edit_message_text(chat_id, message_id, "✨ خدمات لیزر را انتخاب کنید:", reply_markup=laser_menu())
        return
    
    if callback_data == "injections":
        edit_message_text(chat_id, message_id, "💉 خدمات تزریقات را انتخاب کنید:", reply_markup=injections_menu())
        return
    
    if callback_data == "weight_loss":
        edit_message_text(chat_id, message_id, "🏋️ خدمات لاغری را انتخاب کنید:", reply_markup=weight_loss_menu())
        return
    
    # لیزر موی زائد
    if callback_data == "laser_hair":
        edit_message_text(chat_id, message_id, "🪒 وضعیت خود را انتخاب کنید:", reply_markup=laser_hair_menu())
        return
    
    if callback_data in ["new_customer", "old_customer"]:
        service_name = "لیزر موی زائد"
        customer_type = "مراجعه اول" if callback_data == "new_customer" else "مشتری کلینیک"
        ask_fullname(chat_id, user_id, {"service": service_name, "customer_type": customer_type})
        return
    
    # جوانساز
    if callback_data == "rejuvenation":
        edit_message_text(chat_id, message_id, "✨ خدمات جوانسازی را انتخاب کنید:", reply_markup=rejuvenation_menu())
        return
    
    if callback_data in ["fotona", "hifu", "mesogel", "miracle_package"]:
        service_names = {"fotona": "فوتونا", "hifu": "هایفو", "mesogel": "مزوژل", "miracle_package": "پکیج معجزه جوانسازی"}
        ask_fullname(chat_id, user_id, {"service": f"جوانساز - {service_names[callback_data]}"})
        return
    
    # جای جوش و اسکار
    if callback_data == "scar":
        edit_message_text(chat_id, message_id, "🩹 درمان جای جوش و زخم را انتخاب کنید:", reply_markup=scar_menu())
        return
    
    if callback_data in ["scar_acne", "scar_wound"]:
        service_names = {"scar_acne": "درمان جای جوش", "scar_wound": "درمان جای زخم"}
        ask_fullname(chat_id, user_id, {"service": service_names[callback_data]})
        return
    
    # لاغری
    if callback_data == "consult_weight":
        ask_fullname(chat_id, user_id, {"service": "مشاوره لاغری"})
        return
    
    if callback_data == "get_diet":
        ask_weight(chat_id, user_id, {"service": "دریافت رژیم"})
        return
    
    if callback_data == "weight_device":
        edit_message_text(chat_id, message_id, "🖥️ خدمات مورد نظر خودتون رو انتخاب کنید:", reply_markup=weight_device_menu())
        return
    
    if callback_data in ["shockwave", "lpg", "fotona_device", "rf"]:
        service_names = {"shockwave": "شاک ویو", "lpg": "ال پی جی (LPG)", "fotona_device": "فوتونا", "rf": "آر اف (RF)"}
        ask_fullname(chat_id, user_id, {"service": f"دستگاه لاغری - {service_names[callback_data]}"})
        return
    
    if callback_data == "weight_packages":
        edit_message_text(chat_id, message_id, "📦 پکیج های لاغری را انتخاب کنید:", reply_markup=weight_packages_menu())
        return
    
    if callback_data in ["package_5kg", "package_10kg", "package_20kg"]:
        service_names = {"package_5kg": "۵ کیلو در یک ماه", "package_10kg": "۱۰ کیلو در ۴۰ روز", "package_20kg": "۲۰ کیلو در ۷۰ روز"}
        ask_fullname(chat_id, user_id, {"service": f"پکیج لاغری - {service_names[callback_data]}"})
        return
    
    # تزریقات
    if callback_data in ["lip_filler", "jaw_line", "botox", "body_filler"]:
        service_names = {"lip_filler": "ژل لب", "jaw_line": "زاویه فک", "botox": "بوتاکس", "body_filler": "تزریق ژل بدن"}
        ask_fullname(chat_id, user_id, {"service": f"تزریقات - {service_names[callback_data]}"})
        return
    
    # پنل ادمین
    if callback_data == "admin_all_csv":
        if not is_admin_session_active(user_id):
            send_message(chat_id, "⏰ نشست شما منقضی شده. لطفاً مجدداً /admin را وارد کنید.")
            return
        data_list = get_all_users_data()
        send_csv(chat_id, data_list, "همه_اطلاعات")
        return
    
    if callback_data == "admin_range":
        if not is_admin_session_active(user_id):
            send_message(chat_id, "⏰ نشست شما منقضی شده. لطفاً مجدداً /admin را وارد کنید.")
            return
        edit_message_text(chat_id, message_id, "📆 بازه مورد نظر را انتخاب کنید:", reply_markup=admin_range_menu())
        return
    
    if callback_data in ["admin_today", "admin_last2days", "admin_last7days"]:
        if not is_admin_session_active(user_id):
            send_message(chat_id, "⏰ نشست شما منقضی شده. لطفاً مجدداً /admin را وارد کنید.")
            return
        days = {"admin_today": 1, "admin_last2days": 2, "admin_last7days": 7}
        data_list = get_users_data_by_days(days[callback_data])
        names = {"admin_today": "بازه_امروز", "admin_last2days": "بازه_۲_روز", "admin_last7days": "بازه_۷_روز"}
        send_csv(chat_id, data_list, names[callback_data])
        return
    
    if callback_data == "admin_back":
        edit_message_text(chat_id, message_id, "📋 پنل ادمین:", reply_markup=admin_menu())
        return
    
    if callback_data == "admin_logout":
        end_admin_session(user_id)
        edit_message_text(chat_id, message_id, "🚪 از پنل ادمین خارج شدید.")
        return

# ======================== هندلر پیام‌های متنی ========================
def handle_message(chat_id, user_id, text):
    state = user_states.get(user_id)
    
    if state == "waiting_fullname":
        process_fullname(chat_id, user_id, text)
    
    elif state == "waiting_phone":
        process_phone(chat_id, user_id, text)
    
    elif state == "waiting_weight":
        process_weight(chat_id, user_id, text)
    
    elif state == "waiting_height":
        process_height(chat_id, user_id, text)
    
    elif state == "waiting_age":
        process_age(chat_id, user_id, text)
    
    elif state == "waiting_gender":
        process_gender(chat_id, user_id, text)
    
    else:
        send_message(chat_id, "به کلینیک زیبایی لادن خوش آمدید🌹\nلطفا خدمات موردنظر خود را انتخاب کنید", reply_markup=main_menu())

# ======================== پنل ادمین ========================
# ======================== پنل ادمین (نسخه کاملاً اصلاح شده) ========================
def handle_admin_login(chat_id, user_id, text, step):
    if step == "username":
        if text == ADMIN_USERNAME:
            user_states[user_id] = "admin_waiting_password"
            send_message(chat_id, "🔑 رمز عبور را وارد کنید:")
        else:
            fail = admin_login_attempt(user_id, False)
            send_message(chat_id, f"❌ نام کاربری اشتباه. تلاش {fail[0]} از {MAX_ADMIN_ATTEMPTS}")
            if fail[0] >= MAX_ADMIN_ATTEMPTS:
                send_message(chat_id, f"🔒 به دلیل {MAX_ADMIN_ATTEMPTS} بار تلاش ناموفق، ۱۰ دقیقه مسدود شدید.")
            user_states.pop(user_id, None)
    
    elif step == "password":
        if text == ADMIN_PASSWORD:
            admin_login_attempt(user_id, True)
            start_admin_session(user_id)
            
            # دریافت آمار از دیتابیس
            from database import get_bot_stats
            stats = get_bot_stats()
            
            # متن خوش‌آمدگویی با آمار
            welcome_text = f"""✅ وارد پنل ادمین شدید.
⏱️ شما ۱۰ دقیقه فرصت دارید.

📊 **آمار کلی ربات:**
👥 کل مراجعین: {stats['total_users']}
📅 امروز: {stats['today_count']} نفر
📆 هفته گذشته: {stats['week_count']} نفر"""
            
            send_message(chat_id, welcome_text, reply_markup=admin_menu())
            user_states.pop(user_id, None)
        else:
            fail = admin_login_attempt(user_id, False)
            send_message(chat_id, f"❌ رمز عبور اشتباه. تلاش {fail[0]} از {MAX_ADMIN_ATTEMPTS}")
            if fail[0] >= MAX_ADMIN_ATTEMPTS:
                send_message(chat_id, f"🔒 به دلیل {MAX_ADMIN_ATTEMPTS} بار تلاش ناموفق، ۱۰ دقیقه مسدود شدید.")
            user_states.pop(user_id, None)
# ======================== حلقه اصلی دریافت آپدیت ========================
def main():
    last_update_id = 0
    print("Bale Robot is running...")
    
    while True:
        try:
            updates = get_updates(last_update_id + 1)
            
            for update in updates:
                last_update_id = update["update_id"]
                
                # دریافت پیام
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    user_id = msg["from"]["id"]
                    
                    # بررسی دستور /admin
                    if "text" in msg and msg["text"] == "/admin":
                        if is_admin_blocked(user_id):
                            send_message(chat_id, "❌ شما به مدت ۱۰ دقیقه از ورود به پنل محروم هستید.")
                        else:
                            user_states[user_id] = "admin_waiting_username"
                            send_message(chat_id, "👤 نام کاربری را وارد کنید:")
                        continue
                    
                    # بررسی وضعیت ادمین لاگین
                    if user_states.get(user_id) == "admin_waiting_username":
                        handle_admin_login(chat_id, user_id, msg["text"], "username")
                        continue
                    
                    if user_states.get(user_id) == "admin_waiting_password":
                        handle_admin_login(chat_id, user_id, msg["text"], "password")
                        continue
                    
                    # پیام متنی معمولی
                    if "text" in msg:
                        handle_message(chat_id, user_id, msg["text"])
                    else:
                        send_message(chat_id, "لطفاً متن ارسال کنید.")
                
                # دریافت callback (دکمه شیشه‌ای)
                elif "callback_query" in update:
                    callback = update["callback_query"]
                    chat_id = callback["message"]["chat"]["id"]
                    message_id = callback["message"]["message_id"]
                    callback_data = callback["data"]
                    user_id = callback["from"]["id"]
                    
                    handle_callback(chat_id, message_id, callback_data, user_id)
                    
                    # پاسخ به بله که دکمه بارگذاری حذف شود
                    answer_url = f"{BASE_URL}/answerCallbackQuery"
                    requests.post(answer_url, json={"callback_query_id": callback["id"]})
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
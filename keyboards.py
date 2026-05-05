# keyboards.py
def make_inline_keyboard(buttons):
    """ساخت کیبورد شیشه‌ای با دکمه‌های一行ی"""
    keyboard = {
        "inline_keyboard": [[{"text": btn[0], "callback_data": btn[1]}] for btn in buttons]
    }
    return keyboard

def main_menu():
    return make_inline_keyboard([
        ["✨ لیزر", "laser"],
        ["💉 تزریقات", "injections"],
        ["🏋️ لاغری", "weight_loss"]
    ])

def laser_menu():
    return make_inline_keyboard([
        ["🪒 لیزر موی زائد", "laser_hair"],
        ["✨ جوانساز", "rejuvenation"],
        ["🩹 جای جوش و اسکار", "scar"],
        ["🔙 برگشت", "back_main"]
    ])

def laser_hair_menu():
    return make_inline_keyboard([
        ["🆕 مراجعه اول هستم", "new_customer"],
        ["🏥 مشتری کلینیک هستم", "old_customer"],
        ["🔙 برگشت", "back_laser"]
    ])

def rejuvenation_menu():
    return make_inline_keyboard([
        ["✨ فوتونا", "fotona"],
        ["⚡ هایفو", "hifu"],
        ["💉 مزوژل", "mesogel"],
        ["📦 پکیج معجزه جوانسازی", "miracle_package"],
        ["🔙 برگشت", "back_laser"]
    ])

def scar_menu():
    return make_inline_keyboard([
        ["🩹 درمان جای جوش", "scar_acne"],
        ["🩺 درمان جای زخم", "scar_wound"],
        ["🔙 برگشت", "back_laser"]
    ])

def weight_loss_menu():
    return make_inline_keyboard([
        ["📞 مشاوره لاغری", "consult_weight"],
        ["📋 دریافت رژیم", "get_diet"],
        ["🖥️ دستگاه", "weight_device"],
        ["📦 پکیج های لاغری", "weight_packages"],
        ["🔙 برگشت", "back_main"]
    ])

def weight_device_menu():
    return make_inline_keyboard([
        ["⚡ شاک ویو", "shockwave"],
        ["🔄 ال پی جی (LPG)", "lpg"],
        ["✨ فوتونا", "fotona_device"],
        ["📡 آر اف (RF)", "rf"],
        ["🔙 برگشت", "back_weight_loss"]
    ])

def weight_packages_menu():
    return make_inline_keyboard([
        ["📦 ۵ کیلو در یک ماه", "package_5kg"],
        ["📦 ۱۰ کیلو در ۴۰ روز", "package_10kg"],
        ["📦 ۲۰ کیلو در ۷۰ روز", "package_20kg"],
        ["🔙 برگشت", "back_weight_loss"]
    ])

def injections_menu():
    return make_inline_keyboard([
        ["💋 ژل لب", "lip_filler"],
        ["🦴 زاویه فک", "jaw_line"],
        ["💉 بوتاکس", "botox"],
        ["🧴 تزریق ژل بدن", "body_filler"],
        ["🔙 برگشت", "back_main"]
    ])

def back_to_main_button():
    return make_inline_keyboard([["🔙 برگشت به اول", "back_main"]])

def admin_menu():
    return make_inline_keyboard([
        ["📥 دریافت CSV کل اطلاعات", "admin_all_csv"],
        ["📆 دریافت گزارش بازه‌ای", "admin_range"],
        ["🚪 خروج از پنل", "admin_logout"]
    ])

def admin_range_menu():
    return make_inline_keyboard([
        ["📅 بازه امروز", "admin_today"],
        ["📅 بازه ۲ روز گذشته", "admin_last2days"],
        ["📅 بازه ۷ روز گذشته", "admin_last7days"],
        ["🔙 برگشت", "admin_back"]
    ])
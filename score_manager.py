# این فایل مسئولیت مدیریت امتیازها، مخصوصا بالاترین امتیاز (High Score) رو به عهده داره.

import os

# آدرس پوشه و فایلی که امتیاز رو توش ذخیره می‌کنیم
DATA_DIR = "data"
SCORE_FILE = os.path.join(DATA_DIR, "highscore.txt")

def ensure_data_dir():
    """این تابع چک می‌کنه اگه پوشه 'data' وجود نداشت، اونو بسازه"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_high_score():
    """بالاترین امتیاز ذخیره شده رو از فایل می‌خونه"""
    ensure_data_dir() # اول مطمئن شو پوشه هست
    if os.path.exists(SCORE_FILE): # اگه فایل امتیاز وجود داشت
        try:
            with open(SCORE_FILE, "r") as f:
                # محتویات فایل رو بخون، فاصله‌های اضافی رو حذف کن و به عدد تبدیلش کن
                return int(f.read().strip())
        except (ValueError, IOError):
            # اگه به هر دلیلی فایل خراب بود یا محتواش عدد نبود، صفر برگردون
            return 0
    return 0 # اگه فایل اصلا وجود نداشت، صفر برگردون

def save_high_score(score):
    """امتیاز جدید رو ذخیره می‌کنه، البته فقط اگه از امتیاز قبلی بیشتر باشه"""
    ensure_data_dir() # اول مطمئن شو پوشه هست
    current_high = load_high_score() # بالاترین امتیاز فعلی رو بخون
    if score > current_high: # اگه امتیاز جدید بیشتر بود
        with open(SCORE_FILE, "w") as f:
            f.write(str(score)) # امتیاز جدید رو توی فایل بنویس
        return True # خبر بده که رکورد شکسته شد
    return False # اگه رکورد جدیدی ثبت نشد، فالس برگردون

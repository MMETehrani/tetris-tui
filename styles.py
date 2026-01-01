# این فایل ظاهر برنامه رو با استفاده از CSS مخصوص کتابخونه Textual تعریف می‌کنه

CSS = """
/* تنظیمات کلی صفحه */
Screen {
    background: #151515; /* رنگ پس‌زمینه کل برنامه */
    color: #ffffff;      /* رنگ متن پیش‌فرض */
}

/* --- منوی اصلی --- */
MenuScreen {
    align: center middle; /* همه چیز رو وسط صفحه قرار بده */
    background: #111;     /* پس‌زمینه تیره‌تر برای منو */
}
.menu-title { 
    color: #ffa500;       /* رنگ عنوان (نارنجی) */
    text-style: bold;    /* درشت کردن متن */
    margin-bottom: 2;    /* فاصله ۲ خطی از پایین */
    border-bottom: double #ffa500; /* خط دوتایی نارنجی زیر عنوان */
}
Button { 
    width: 30;           /* عرض دکمه‌ها */
    margin: 1;           /* فاصله از اطراف */
    background: #333;    /* پس‌زمینه خاکستری تیره */
    border: tall #555;   /* حاشیه بلند خاکستری روشن‌تر */
    color: white;        /* رنگ متن دکمه */
}
/* استایل وقتی با کیبورد روی دکمه می‌رویم (focus) */
Button:focus { 
    background: #ffa500; /* پس‌زمینه نارنجی می‌شه */
    color: black;        /* متن سیاه می‌شه */
    border: tall white;  /* حاشیه سفید */
    text-style: bold;    /* متن درشت می‌شه */
}
/* استایل وقتی ماوس روی دکمه می‌ره (hover) */
Button:hover {
    background: #e69500; /* یه کم نارنجی رو تیره‌تر کن */
}

/* --- صفحه بازی --- */
GameScreen {
    layout: horizontal; /* چیدمان افقی (زمین بازی کنار، سایدبار سمت دیگه) */
}

/* کانتینر اصلی زمین بازی */
#game-area-container {
    width: 60%;          /* ۶۰ درصد عرض صفحه رو بگیره */
    height: 100%;        /* تمام ارتفاع رو بگیره */
    align: center middle;/* زمین بازی رو وسط خودش قرار بده */
    background: #000;    /* پس‌زمینه کاملا سیاه */
    border: heavy #ffa500; /* حاشیه ضخیم نارنجی دورش */
}

/* سایدبار (نوار کناری) */
#sidebar { 
    width: 40%;          /* ۴۰ درصد عرض صفحه رو بگیره */
    height: 100%;        
    background: #1a1a1a; /* یه خاکستری تیره برای پس‌زمینه */
    border-left: solid #ffa500; /* یه خط نارنجی سمت چپش برای جدا کردن */
    padding: 1;          /* فاصله از داخل */
}

/* پنل‌های اطلاعاتی داخل سایدبار (امتیاز، مهره بعدی و...) */
.info-panel { 
    background: #252525;     /* پس‌زمینه خاکستری */
    border: round #ffa500;   /* حاشیه گرد نارنجی */
    margin-bottom: 2;        /* فاصله از پنل پایینی */
    padding: 1;              
    height: auto;            /* ارتفاع خودکار */
    align: center middle;    /* محتویات وسط چین */
}
.panel-title { 
    text-align: center;      /* عنوان وسط‌چین باشه */
    color: #ffffff;          
    text-style: bold;        
    border-bottom: solid #444; /* یه خط جداکننده زیر عنوان */
    width: 100%;
}
.score-value { 
    text-align: center;
    text-style: bold;
    color: #ffa500;         /* مقدار امتیاز رو نارنجی کن */
    padding-top: 1;          /* یه کم از بالا فاصله بده */
}

/* جعبه‌ای که مهره بعدی رو نشون می‌ده */
#next-item-box { 
    height: 6;               /* ارتفاع ثابت ۶ خط */
    width: 100%;
    align: center middle;    /* مهره رو وسط خودش نشون بده */
    color: #ffa500;         /* رنگ پیش‌فرض برای مواقعی که متنی باشه */
}

/* پنجره‌های مودال (مثل پیام Pause یا Game Over) */
.modal-box { 
    padding: 2;
    border: heavy #ffa500;
    background: #222;
    width: 50;
    height: auto;
    text-align: center;
}
"""

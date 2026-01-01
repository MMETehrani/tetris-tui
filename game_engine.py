# این فایل قلب تپنده بازیه. تمام منطق اصلی تتریس اینجا اتفاق میفته.

import random
from textual.widgets import Static
from textual.message import Message
from textual.reactive import reactive
from consts import BOARD_WIDTH, BOARD_HEIGHT, SHAPES, THEME_COLORS, TICK_DELAY
from score_manager import save_high_score

# این کلاس زمین بازی ماست. از یه ویجت استاتیک خود تکستال ارث می‌بره
class TetrisBoard(Static):
    # امتیاز بازیکن که به صورت reactive تعریف شده
    # این یعنی هر وقت تغییر کنه، تکستال خودش UI رو آپدیت می‌کنه
    score = reactive(0)

    # --- تعریف پیام‌ها (Events) ---
    # این کلاس‌ها برای ارتباط بین این ویجت (زمین بازی) و ویجت اصلی برنامه (main.py) استفاده میشن

    # وقتی امتیاز تغییر می‌کنه، این پیام فرستاده می‌شه
    class ScoreChanged(Message):
        def __init__(self, score: int):
            self.score = score
            super().__init__()

    # وقتی مهره بعدی مشخص می‌شه، این پیام با ظاهر جدیدش فرستاده می‌شه
    class NextPieceChanged(Message):
        def __init__(self, render_string: str):
            self.render_string = render_string
            super().__init__()
    
    # وقتی بازی تموم می‌شه این پیام رو می‌فرستیم
    class GameOver(Message):
        pass
    # ---------------------

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # وقتی کلاس ساخته می‌شه، متغیرهای بازی رو مقداردهی اولیه می‌کنیم
        self.init_game_state()

    def init_game_state(self):
        #مقداردهی اولیه متغیرهای بازی (برای شروع و ریستارت
        # یه زمین خالی می‌سازیم (لیستی از لیست‌ها)
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None # مهره فعلی که داره میاد پایین
        self.next_piece_shape = None # شکل مهره بعدی
        self.next_piece_color = None # رنگ مهره بعدی
        self.piece_x = 0 # موقعیت افقی مهره
        self.piece_y = 0 # موقعیت عمودی مهره
        self.piece_color = "" # رنگ مهره فعلی
        self.score = 0
        self.game_over = False
        
        # یه مهره برای دست بعد آماده می‌کنیم
        self._generate_next_piece()

    def _generate_next_piece(self):
        #یه مهره به صورت تصادفی از لیست مهره‌ها انتخاب می‌کنه
        idx = random.randint(0, len(SHAPES) - 1)
        self.next_piece_shape = SHAPES[idx]
        self.next_piece_color = THEME_COLORS[idx]

    def on_mount(self):
        #این متد وقتی که ویجت به صفحه اضافه می‌شه، خود به خود توسط تکستال اجرا می‌شه
        self.start_game()

    def start_game(self):
        #شروع حلقه بازی
        self.spawn_piece() # اولین مهره رو بنداز
        # اگر تایمر قبلی وجود داره حذفش کن تا تداخل نشه
        # این برای ریستارت کردن بازی مهمه
        if hasattr(self, 'timer') and self.timer:
            self.timer.stop()
        # یه تایمر درست می‌کنیم که هر چند ثانیه یک بار (بر اساس TICK_DELAY) متد game_tick رو صدا بزنه
        self.timer = self.set_interval(TICK_DELAY, self.game_tick)
        self.update_board() # صفحه رو آپدیت کن
        self.post_message(self.ScoreChanged(0)) # امتیاز رو در UI صفر کن

    def reset_game(self):
        #ریست کردن کامل بازی بدون بستن برنامه
        self.init_game_state()
        self.start_game()

    def spawn_piece(self):
        #یه مهره جدید رو از بالای صفحه وارد بازی می‌کنه
        self.current_piece = self.next_piece_shape
        self.piece_color = self.next_piece_color
        self._generate_next_piece() # سریع یه مهره دیگه برای دور بعد آماده می‌کنیم
        
        # به UI خبر می‌دیم که مهره بعدی چیه تا نمایشش بده
        self.post_message(self.NextPieceChanged(self._render_next_piece_string()))

        # مهره جدید رو وسط بالای صفحه قرار می‌دیم
        self.piece_x = BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0

        # اگه مهره جدید به محض ظاهر شدن با جایی برخورد کنه، یعنی باختی
        if self.check_collision(self.current_piece, self.piece_x, self.piece_y):
            self.game_over = True
            self.timer.pause() # تایمر رو نگه دار
            save_high_score(self.score) # رکورد جدید رو ذخیره کن
            self.post_message(self.GameOver()) # به همه اعلام کن که بازی تموم شد

    def _render_next_piece_string(self):
        #شکل مهره بعدی رو به یه رشته متنی برای نمایش در UI تبدیل می‌کنه
        lines = []
        for row in self.next_piece_shape:
            line = ""
            for cell in row:
                if cell: # اگه این بخش از مهره پر بود
                    # با استفاده از Rich markup یه مربع رنگی درست می‌کنیم
                    line += f"[on {self.next_piece_color}]  [/]"
                else: # اگه خالی بود
                    line += "  " # دو تا فاصله بذار
            lines.append(line)
        return "\n".join(lines)

    def check_collision(self, shape, off_x, off_y):
        #چک می‌کنه که آیا مهره در موقعیت جدید با دیواره‌ها یا مهره‌های دیگه برخورد می‌کنه یا نه
        for cy, row in enumerate(shape):
            for cx, val in enumerate(row):
                if val: # برای هر سلول پر از مهره
                    try:
                        # چک کردن برخورد با دیواره‌های چپ، راست و پایین
                        if off_x + cx < 0 or off_x + cx >= BOARD_WIDTH or off_y + cy >= BOARD_HEIGHT:
                            return True
                        # چک کردن برخورد با مهره‌های دیگه که قبلا در زمین نشستن
                        if off_y + cy >= 0 and self.board[off_y + cy][off_x + cx]:
                            return True
                    except IndexError: # اگه خارج از محدوده زمین بود
                        return True
        return False # اگه هیچ برخوردی نبود

    def game_tick(self):
        #این متد توسط تایمر به صورت مداوم اجرا می‌شه و مهره رو یه خط میاره پایین
        if not self.game_over:
            # اگه حرکت به پایین ممکن نبود (یعنی به زمین یا مهره دیگه رسیده)
            if not self.move(0, 1):
                self.lock_piece() # مهره رو در جاش قفل کن

    def move(self, dx, dy):
        #حرکت دادن مهره به چپ/راست (dx) یا پایین (dy
        if self.game_over: return False
        # اگه بعد از حرکت برخوردی پیش نمیاد
        if not self.check_collision(self.current_piece, self.piece_x + dx, self.piece_y + dy):
            # موقعیت مهره رو آپدیت کن
            self.piece_x += dx
            self.piece_y += dy
            self.update_board() # نمایشگر رو هم آپدیت کن
            return True # حرکت با موفقیت انجام شد
        return False # حرکت ممکن نبود

    def rotate(self):
        #چرخوندن مهره
        if self.game_over: return
        # با یه ترفند لیست‌ها، مهره رو ۹۰ درجه می‌چرخونیم
        rotated = [list(row) for row in zip(*self.current_piece[::-1])]
        # اگه بعد از چرخش برخوردی پیش نمیاد
        if not self.check_collision(rotated, self.piece_x, self.piece_y):
            self.current_piece = rotated # شکل جدید رو جایگزین کن
            self.update_board() # صفحه رو آپدیت کن

    def lock_piece(self):
        #وقتی مهره به مقصد می‌رسه، اون رو به بخشی از زمین بازی تبدیل می‌کنه
        for cy, row in enumerate(self.current_piece):
            for cx, val in enumerate(row):
                if val:
                    # رنگ مهره رو در خونه‌های مربوطه در زمین بازی ثبت می‌کنیم
                    self.board[self.piece_y + cy][self.piece_x + cx] = self.piece_color
        
        self.clear_lines() # خطوط پر شده رو پاک کن
        self.spawn_piece() # یه مهره جدید بیار
        self.update_board()

    def clear_lines(self):
        #چک می‌کنه و هر خطی که کامل پر شده باشه رو حذف می‌کنه
        # یه زمین جدید می‌سازیم فقط با خط‌هایی که کامل پر نشدن
        new_board = [row for row in self.board if any(x == 0 for x in row)]
        lines_cleared = BOARD_HEIGHT - len(new_board) # تعداد خطوط پاک شده
        
        # به تعداد خطوط پاک شده، خطوط خالی به بالای زمین اضافه می‌کنیم
        for _ in range(lines_cleared):
            new_board.insert(0, [0] * BOARD_WIDTH)
        
        self.board = new_board
        if lines_cleared > 0:
            # به ازای هر خط پاک شده امتیاز می‌دیم
            self.score += lines_cleared * 100
            # به UI خبر می‌دیم که امتیاز عوض شده
            self.post_message(self.ScoreChanged(self.score))

    def update_board(self):
        #صفحه بازی رو با توجه به وضعیت فعلی، دوباره رندر میکنه 
        lines = []
        # یه کپی از زمین بازی می‌سازیم تا بتونیم مهره فعلی رو روش بکشیم بدون اینکه زمین اصلی خراب بشه
        display_board = [row[:] for row in self.board]
        
        # اگه مهره‌ای در حال سقوطه و بازی تموم نشده
        if self.current_piece and not self.game_over:
            # مهره در حال حرکت رو روی کپی زمین نقاشی می‌کنیم
            for cy, row in enumerate(self.current_piece):
                for cx, val in enumerate(row):
                    if val and 0 <= self.piece_y + cy < BOARD_HEIGHT:
                        display_board[self.piece_y + cy][self.piece_x + cx] = self.piece_color

        # حالا زمین رو خط به خط به رشته متنی برای نمایش تبدیل می‌کنیم
        for row in display_board:
            line_str = ""
            for cell in row:
                if cell == 0: # اگه خونه خالی بود
                    line_str += "[#333333 on black] .[/]" # یه نقطه کم‌رنگ بذار
                else: # اگه پر بود
                    # یه مربع با رنگی که قبلا ذخیره شده بکش
                    line_str += f"[on {cell}]  [/]"
            lines.append(line_str)
        
        # یه خط مرزی هم زیر زمین بازی می‌کشیم
        bottom_border = "[#ffa500]━━" * BOARD_WIDTH + "[/]"
        # در نهایت ویجت رو با این متن جدید آپدیت می‌کنیم
        self.update("\n".join(lines) + "\n" + bottom_border)

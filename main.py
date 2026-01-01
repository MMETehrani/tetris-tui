# main.py
# این فایل نقطه شروع اصلی برنامه است.
# کلاس اصلی اپلیکیشن (TetrisApp) و مدیریت صفحات مختلف (منو، بازی، ...) اینجا انجام می‌شه.

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, Label
from textual.screen import Screen, ModalScreen
from textual.binding import Binding

from styles import CSS  # وارد کردن استایل‌ها از فایل styles.py
from game_engine import TetrisBoard  # وارد کردن موتور بازی
from score_manager import load_high_score  # وارد کردن تابع خوندن بهترین رکورد

# --- تعریف صفحه‌های مودال (پاپ‌آپ) ---

# صفحه‌ای که وقتی بازی رو متوقف (Pause) می‌کنیم، ظاهر می‌شه
class PauseScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        # یه کانتینر با استایل مودال که در CSS تعریف شده
        with Container(classes="modal-box"):
            yield Label("[bold #ffa500]PAUSED[/]")
            yield Button("Resume", id="resume_btn", variant="primary")
            yield Button("Quit to Menu", id="quit_btn", variant="error")

    # وقتی یه دکمه فشرده می‌شه
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "resume_btn":
            self.dismiss()  # صفحه مودال رو می‌بنده و به بازی برمی‌گرده
        elif event.button.id == "quit_btn":
            self.app.pop_screen()  # برمی‌گرده به صفحه قبلی (منوی اصلی)
            self.dismiss()

# صفحه‌ای که وقتی می‌بازی ظاهر می‌شه
class GameOverScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container(classes="modal-box"):
            yield Label("[bold white on red] GAME OVER [/]")
            yield Label("\nPress [b]R[/b] to Restart", classes="dim-text")
            yield Button("Restart", id="restart_btn", variant="warning")
            yield Button("Menu", id="menu_btn")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "restart_btn":
            self.dismiss()
            self.app.action_restart_game()  # اکشن شروع مجدد بازی رو صدا می‌زنه
        elif event.button.id == "menu_btn":
            self.dismiss()
            self.app.pop_screen()  # برمی‌گرده به منوی اصلی

# --- تعریف صفحه اصلی بازی ---
class GameScreen(Screen):
    # تعریف کلیدهای کنترلی بازی
    BINDINGS = [
        Binding("left", "move_left", "Left"),
        Binding("right", "move_right", "Right"),
        Binding("up", "rotate", "Rotate"),
        Binding("down", "move_down", "Fast Drop"),
        Binding("r", "restart_game", "Restart"),
        Binding("p", "pause_game", "Pause"),
        Binding("escape", "back_to_menu", "Menu"),
    ]

    # متغیری برای نگهداری بهترین رکورد در این دست از بازی
    best_score = 0

    def compose(self) -> ComposeResult:
        # بهترین رکورد رو از فایل می‌خونیم و در متغیر کلاس ذخیره می‌کنیم
        self.best_score = load_high_score()
        
        yield Header()  # هدر بالای صفحه
        with Horizontal():  # چیدمان افقی
            # کانتینر سمت چپ برای زمین بازی
            with Container(id="game-area-container"):
                yield TetrisBoard(id="tetris")  # ویجت زمین بازی رو اینجا قرار می‌دیم
            
            # سایدبار سمت راست برای نمایش اطلاعات
            with Vertical(id="sidebar"):
                # پنل نمایش مهره بعدی
                with Container(classes="info-panel"):
                    yield Label("NEXT PIECE", classes="panel-title")
                    yield Static("", id="next-item-box")
                
                # پنل نمایش امتیاز فعلی
                with Container(classes="info-panel"):
                    yield Label("CURRENT SCORE", classes="panel-title")
                    yield Label("0", classes="score-value", id="score_lbl")

                # پنل نمایش بهترین رکورد
                with Container(classes="info-panel"):
                    yield Label("BEST RECORD", classes="panel-title")
                    yield Label(str(self.best_score), classes="score-value", id="high_score_lbl")
        yield Footer()  # فوتر پایین صفحه که کلیدها رو نشون می‌ده

    # --- مدیریت پیام‌های دریافتی از موتور بازی ---

    # این متد وقتی اجرا می‌شه که از TetrisBoard پیام ScoreChanged بیاد
    def on_tetris_board_score_changed(self, message: TetrisBoard.ScoreChanged):
        # امتیاز فعلی رو در UI آپدیت می‌کنیم
        self.query_one("#score_lbl", Label).update(str(message.score))
        
        # اگه امتیاز فعلی از بهترین رکورد بیشتر شد، اون رو هم آپدیت کن
        if message.score > self.best_score:
             self.best_score = message.score
             self.query_one("#high_score_lbl", Label).update(str(self.best_score))

    # وقتی از TetrisBoard پیام NextPieceChanged میاد
    def on_tetris_board_next_piece_changed(self, message: TetrisBoard.NextPieceChanged):
        # جعبه نمایش مهره بعدی رو با شکل جدید آپدیت می‌کنیم
        self.query_one("#next-item-box", Static).update(message.render_string)

    # وقتی از TetrisBoard پیام GameOver میاد
    def on_tetris_board_game_over(self, message: TetrisBoard.GameOver):
        # صفحه "باختی" رو نشون بده
        self.app.push_screen(GameOverScreen())

    # --- اکشن‌های تعریف شده در BINDINGS ---
    # این اکشن‌ها به کلیدها متصل هستن

    def action_move_left(self): self.query_one("#tetris").move(-1, 0)
    def action_move_right(self): self.query_one("#tetris").move(1, 0)
    def action_move_down(self): self.query_one("#tetris").move(0, 1)
    def action_rotate(self): self.query_one("#tetris").rotate()
    def action_pause_game(self): self.app.push_screen(PauseScreen())
    def action_back_to_menu(self): self.app.pop_screen()
    
    def action_restart_game(self):
        """بازی رو از اول شروع می‌کنه"""
        # رکورد رو دوباره از فایل بخون تا اگه تو بازی قبلی رکورد زده شده، آپدیت بشه
        self.best_score = load_high_score()
        self.query_one("#high_score_lbl", Label).update(str(self.best_score))
        # موتور بازی رو ریست کن
        self.query_one("#tetris").reset_game()

# --- صفحه منوی اصلی ---
class MenuScreen(Screen):
    BINDINGS = [
        Binding("up", "focus_previous", "Previous"),
        Binding("down", "focus_next", "Next"),
        Binding("enter", "select", "Select"),
    ]

    def compose(self) -> ComposeResult:
        yield Label("TETRIS PRO", classes="menu-title")
        yield Button("Start Game", id="start")
        yield Button("Quit", id="quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.app.push_screen(GameScreen())  # برو به صفحه بازی
        elif event.button.id == "quit":
            self.app.exit()  # از برنامه خارج شو

# --- کلاس اصلی اپلیکیشن ---
class TetrisApp(App):
    CSS = CSS  # استایل کلی برنامه
    SCREENS = {"menu": MenuScreen}  # تعریف صفحات برنامه
    BINDINGS = [("ctrl+c", "quit", "Quit")] # با کنترل+سی خارج شو

    def on_mount(self) -> None:
        """وقتی برنامه شروع می‌شه، اولین صفحه رو نشون بده"""
        self.push_screen("menu")
    
    def action_restart_game(self):
        """این اکشن رو اینجا هم تعریف می‌کنیم تا از صفحه GameOver قابل دسترسی باشه"""
        if isinstance(self.screen, GameScreen):
             self.screen.action_restart_game()

# این قسمت تضمین می‌کنه که کد فقط وقتی اجرا شده باشه که این فایل به صورت مستقیم اجرا شده باشه
if __name__ == "__main__":
    app = TetrisApp()
    app.run()  # برنامه رو اجرا کن
import datetime
import inspect
import os
import pprint
import re
import shutil
import time
import unicodedata

from rich import print as print_


class logging:
    CRITICAL = 4
    ERROR = 3
    WARNING = 2
    INFO = 1
    DEBUG = 0

    def __init__(self, **kwargs):
        self.data_format = kwargs.get('data_format', "[%H:%M:%S]")
        self.time_len = len(datetime.datetime.now().strftime(self.data_format))
        self.level = None
        self.last_print_time = ""
        self.console_width = shutil.get_terminal_size().columns

    def set_format_setting(self, **kwargs):
        self.format_settings = kwargs

    def setLevel(self, level):
        self.level = level

    def len_byte(self, text):
        byteCount = (len(text.encode('Shift_JIS')))
        return byteCount

    def now_date(self):
        # 現在時刻を取得、整形
        now = datetime.datetime.now()
        now_format = now.strftime(self.data_format)

        if self.last_print_time == now_format:
            now_format = " "*len(now_format)
        else:
            self.last_print_time = now_format

        return now_format

    def format_text(self, text):
        # テキストを整形
        setting = self.format_settings
        result = pprint.pformat(text, **setting)
        if not "\n" in result:
            return str(text)
        return result

    def add_line_display(self, text, indent):
        text_split = text.split("\n")

        filename = os.path.basename(inspect.stack()[3].filename)
        line = inspect.stack()[3].lineno

        line_text = f"[white dim]{filename}:{line}[/]"

        if len(text_split[0]) > (self.console_width-len(line_text)-5):
            return text
        else:
            line_text_raw = re.sub("\[.*?\]", "", line_text)
            text_split_0_raw = re.sub("\[.*?\]", "", text_split[0])
            space_len = self.console_width - \
                self.len_byte(line_text_raw) - \
                self.len_byte(text_split_0_raw) - \
                indent - 4

            text_split[0] = text_split[0] + \
                (" "*space_len)+line_text

        return "\n".join(text_split)

    def create_message(self, *messages, **kwargs):
        # 引数を展開し 整形
        line_color = kwargs.pop('line_color', "white")

        text = ""
        for message in messages:
            text = text + "\n" + self.format_text(message)
        text = text.strip("\n")

        # 時間とログレベル分の空白
        indent = self.time_len+3

        text = text.replace("\n", "\n"+" "*indent+f" [{line_color}]|[/]  ")
        text = self.add_line_display(text, indent)
        return text

    def critical(self, *messages):
        # ログレベルの確認
        if self.level == None:
            print_("[red]ログレベルが設定されていません![/]")
            return
        if self.level > self.CRITICAL:
            return

        text = self.create_message(*messages, line_color="red")
        now = datetime.datetime.now()
        now_time = now.strftime(self.data_format)

        print_(
            f"[red reverse]{now_time}[/]  [red reverse]C[/] [red]|  {text}[/]")

    def error(self, *messages):
        # ログレベルの確認
        if self.level == None:
            print_("[red]ログレベルが設定されていません![/]")
            return
        if self.level > self.ERROR:
            return

        text = self.create_message(*messages, line_color="red")
        now_time = self.now_date()

        print_(f"[red]{now_time}  E |[/]  {text}")

    def warning(self, *messages):
        # ログレベルの確認
        if self.level == None:
            print_("[red]ログレベルが設定されていません![/]")
            return
        if self.level > self.WARNING:
            return

        text = self.create_message(*messages, line_color="yellow")
        now_time = self.now_date()

        print_(f"[yellow]{now_time}  W |[/]  {text}")

    def info(self, *messages):
        # ログレベルの確認
        if self.level == None:
            print_("[red]ログレベルが設定されていません![/]")
            return
        if self.level > self.INFO:
            return

        text = self.create_message(*messages, line_color="green")
        now_time = self.now_date()

        print_(f"[green]{now_time}  I |[/]  {text}")

    def debug(self, *messages):
        # ログレベルの確認
        if self.level == None:
            print_("[red]ログレベルが設定されていません![/]")
            return
        if self.level > self.DEBUG:
            return

        text = self.create_message(*messages, line_color="blue")
        now_time = self.now_date()

        print_(f"[blue]{now_time}  D |[/]  {text}")

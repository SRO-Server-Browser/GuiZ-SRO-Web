import sys
import ctypes
import tempfile
import os
from ctypes import wintypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Windows API için ctypes tanımlamaları
user32 = ctypes.WinDLL('user32', use_last_error=True)
GetAsyncKeyState = user32.GetAsyncKeyState
GetAsyncKeyState.argtypes = [wintypes.INT]
GetAsyncKeyState.restype = wintypes.SHORT
SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [wintypes.HWND]
SetForegroundWindow.restype = wintypes.BOOL
FindWindowW = user32.FindWindowW
FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindowW.restype = wintypes.HWND

# VK kodu için Z tuşu
VK_Z = 0x5A

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GuiZ")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.NoFocus)  # GUI klavye/mouse focus’u almasın

        # Web engine
        self.browser = QWebEngineView()
        self.browser.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        self.browser.load(QUrl("https://www.vsro.org/"))

        # Layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.browser)
        self.setCentralWidget(central_widget)

        # GUI başlangıçta gizli
        self.visible = False
        self.hide()

        # Log dosyası temp dizininde
        self.log_file = os.path.join(tempfile.gettempdir(), "guiZ_log.txt")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("guiZ.exe başlatıldı!\n")

        # Klavye kontrolü için timer
        self.last_z_state = 0  # Z tuşunun önceki durumunu takip et
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_key)
        self.timer.start(50)  # Her 50ms’de kontrol et

        # sro_client.exe penceresini bul
        # Not: "client" yerine sro_client.exe’nin tam pencere başlığını yaz (örneğin, "Silkroad Online")
        self.game_window = FindWindowW(None, "client")
        if not self.game_window:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write("Oyun penceresi bulunamadı!\n")

    def toggle_visibility(self):
        if self.visible:
            self.hide()
            self.visible = False
        else:
            self.showNormal()
            self.raise_()  # GUI’yi üstte tut
            if self.game_window:
                SetForegroundWindow(self.game_window)  # Focus’u oyuna geri ver
            self.visible = True

    def check_key(self):
        # Z tuşunun durumunu kontrol et
        current_state = GetAsyncKeyState(VK_Z)
        # 0x8000: Tuş şu anda basılı
        # last_z_state ile tekrarlanan basımları önle
        if (current_state & 0x8000) and not (self.last_z_state & 0x8000):
            self.toggle_visibility()
        self.last_z_state = current_state

    def closeEvent(self, event):
        # Çarpı tuşu programı kapatmaz, sadece gizler
        self.toggle_visibility()
        event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec_())

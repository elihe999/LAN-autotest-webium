import win32gui, win32con
import platform
from webium.i18n import swtLang


class Wingui_open_file():
    lang_obj = None
    def __init__(self):
        super().__init__()
        self.lang_obj = swtLang("simpleCN")
        wdname = self.lang_obj.get("uploadpopwintitle")
        if platform.system() == 'Windows':
            pass
        self.hwnd = win32gui.FindWindow(None, wdname)

    def upload_pop_win(self, filepath="", filename=""):
        if self.hwnd != 0:
            win32gui.SetForegroundWindow(self.hwnd)
            ComboBoxEx32 = win32gui.FindWindowEx(self.hwnd, 0, "ComboBoxEx32", None)
            comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)
            edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)
            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, "")
            for i in range(100):
                pass
            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filepath)

            button = win32gui.FindWindowEx(self.hwnd, 0, 'Button', self.lang_obj.get("openbtn"))
            win32gui.SendMessage(self.hwnd,win32con.WM_COMMAND, 1, button)

            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filename)
            win32gui.SendMessage(self.hwnd,win32con.WM_COMMAND, 1, button)
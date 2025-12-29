import os,ctypes,datetime,subprocess,shutil,traceback,winreg,sys
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QTextEdit,QLabel,QGroupBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
class PalworldSaboteurGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sabotage_active=False
        self.share_name="EOSTestShare"
        self.kill_external_test()
        self.setWindowTitle("Palworld Environment Tester")
        self.setMinimumSize(700,450)
        self.apply_window_icon()
        self.central_widget=QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout=QVBoxLayout(self.central_widget)
        self.setup_ui()
    def apply_window_icon(self):
        if hasattr(sys,'_MEIPASS'):
            ico_p=os.path.join(sys._MEIPASS,"pal.ico")
        else:
            ico_p=os.path.join(os.path.abspath("."),"pal.ico")
        if os.path.exists(ico_p):
            self.setWindowIcon(QIcon(ico_p))
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("palworld.tester.v1")
    def setup_ui(self):
        ctrl_group=QGroupBox("Environment Testing")
        ctrl_layout=QVBoxLayout()
        self.btn_toggle=QPushButton("Trigger EOS Error Environment")
        self.btn_toggle.setMinimumHeight(50)
        self.btn_toggle.clicked.connect(self.toggle_sabotage)
        self.btn_toggle.setStyleSheet("background-color: #3d0000; color: white; font-weight: bold;")
        ctrl_layout.addWidget(self.btn_toggle)
        ctrl_group.setLayout(ctrl_layout)
        self.main_layout.addWidget(ctrl_group)
        self.log_view=QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("background-color: #1e1e1e; color: #ff9999; font-family: Consolas; font-size: 10pt;")
        self.main_layout.addWidget(QLabel("Test Log:"))
        self.main_layout.addWidget(self.log_view)
    def log(self,m):
        t=datetime.datetime.now().strftime("%H:%M:%S")
        self.log_view.append(f"[{t}] {m}")
    def auto_terminate_game(self):
        try:
            cmd='powershell "Get-Process Palworld-Win64-Shipping -ErrorAction SilentlyContinue"'
            r=subprocess.run(cmd,shell=True,capture_output=True,text=True,creationflags=0x08000000)
            if "Palworld-Win64-Shipping" in r.stdout:
                subprocess.run("taskkill /F /IM Palworld-Win64-Shipping.exe /T",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
                self.log("Detected running game. Automatically terminated Palworld.")
        except:pass
    def set_docs_path(self,path):
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",0,winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key,"Personal",0,winreg.REG_EXPAND_SZ,path)
        winreg.CloseKey(key)
        ctypes.windll.shell32.SHGetSetSettings(None,0,0)
        ctypes.windll.shell32.SHChangeNotify(0x08000000,0,None,None)
    def kill_external_test(self):
        try:
            curr_pid=os.getpid()
            subprocess.run(f'taskkill /F /FI "PID ne {curr_pid}" /IM PalworldEOSTest.exe',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
        except:pass
    def toggle_sabotage(self):
        self.auto_terminate_game()
        if not self.sabotage_active:
            self.activate_sabotage()
        else:
            self.deactivate_sabotage()
    def activate_sabotage(self):
        try:
            local_fake=os.path.join(os.environ["USERPROFILE"],"Desktop","FakeNetworkShare")
            os.makedirs(local_fake,exist_ok=True)
            subprocess.run(f'net share {self.share_name}="{local_fake}" /grant:everyone,full',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
            unc_path=f"\\\\{os.environ['COMPUTERNAME']}\\{self.share_name}"
            self.set_docs_path(unc_path)
            pal_path=os.path.join(unc_path,"Palworld")
            os.makedirs(pal_path,exist_ok=True)
            self.sabotage_active=True
            self.btn_toggle.setText("Restore Environment to Normal")
            self.btn_toggle.setStyleSheet("background-color: #003d00; color: white; font-weight: bold;")
            self.log(f"SABOTAGE: Documents redirected to {unc_path}")
            self.log("Status: Fake network environment active.")
        except Exception as e:self.log(f"Error activating test: {e}")
    def deactivate_sabotage(self):
        try:
            self.set_docs_path("%USERPROFILE%\\Documents")
            subprocess.run(f"net share {self.share_name} /delete",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
            local_fake=os.path.join(os.environ["USERPROFILE"],"Desktop","FakeNetworkShare")
            if os.path.exists(local_fake):shutil.rmtree(local_fake,ignore_errors=True)
            self.sabotage_active=False
            self.btn_toggle.setText("Trigger EOS Error Environment")
            self.btn_toggle.setStyleSheet("background-color: #3d0000; color: white; font-weight: bold;")
            self.log("SUCCESS: Local path restored and network share deleted.")
        except Exception as e:self.log(f"Error restoring environment: {e}")
    def closeEvent(self,event):
        if self.sabotage_active:
            self.auto_terminate_game()
            self.deactivate_sabotage()
        self.kill_external_test()
        event.accept()
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=PalworldSaboteurGUI()
    window.show()
    sys.exit(app.exec())
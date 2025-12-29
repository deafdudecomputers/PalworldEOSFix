import os,ctypes,datetime,subprocess,shutil,traceback,winreg,sys
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QTextEdit,QLabel,QGroupBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
class PalworldFixerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kill_external_fixer()
        self.setWindowTitle("Palworld Fixer")
        self.setMinimumSize(700,450)
        self.log_path=os.path.join(os.getcwd(),"documents_eos_audit.log")
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
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("palworld.fixer.v1")
    def setup_ui(self):
        ctrl_group=QGroupBox("Available Fixes")
        ctrl_layout=QHBoxLayout()
        self.btn_sync=QPushButton("Sync System Time")
        self.btn_sync.clicked.connect(self.sync_time)
        self.btn_mods=QPushButton("Remove Mods")
        self.btn_mods.clicked.connect(self.cleanup_mods)
        self.btn_shell=QPushButton("Fix Documents Path")
        self.btn_shell.clicked.connect(self.fix_shell_manual)
        ctrl_layout.addWidget(self.btn_sync)
        ctrl_layout.addWidget(self.btn_mods)
        ctrl_layout.addWidget(self.btn_shell)
        ctrl_group.setLayout(ctrl_layout)
        self.main_layout.addWidget(ctrl_group)
        self.log_view=QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas; font-size: 10pt;")
        self.main_layout.addWidget(QLabel("Activity Log:"))
        self.main_layout.addWidget(self.log_view)
    def log(self,m):
        t=datetime.datetime.now().strftime("%H:%M:%S")
        s=f"[{t}] {m}"
        self.log_view.append(s)
        with open(self.log_path,"a",encoding="utf-8",errors="ignore") as f:f.write(s+"\n")
    def auto_terminate_game(self):
        try:
            cmd='powershell "Get-Process Palworld-Win64-Shipping -ErrorAction SilentlyContinue"'
            r=subprocess.run(cmd,shell=True,capture_output=True,text=True,creationflags=0x08000000)
            if "Palworld-Win64-Shipping" in r.stdout:
                subprocess.run("taskkill /F /IM Palworld-Win64-Shipping.exe /T",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
                self.log("Detected running game. Automatically terminated Palworld.")
        except:pass
    def kill_external_fixer(self):
        try:
            curr_pid=os.getpid()
            subprocess.run(f'taskkill /F /FI "PID ne {curr_pid}" /IM PalworldEOSFix.exe',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
        except:pass
    def sync_time(self):
        self.auto_terminate_game()
        try:
            subprocess.run("w32tm /resync /force",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
            self.log("System time synchronized successfully.")
        except:self.log("Failed to sync time. Please run as Administrator.")
    def fix_shell_manual(self):
        self.auto_terminate_game()
        try:
            std=os.path.join(os.environ["USERPROFILE"],"Documents")
            if not os.path.exists(std):os.makedirs(std,exist_ok=True)
            key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",0,winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key,"Personal",0,winreg.REG_EXPAND_SZ,"%USERPROFILE%\\Documents")
            winreg.CloseKey(key)
            ctypes.windll.shell32.SHGetSetSettings(None,0,0)
            ctypes.windll.shell32.SHChangeNotify(0x08000000,0,None,None)
            self.log("Documents path has been restored to default.")
        except:self.log("Could not update the Documents path registry key.")
    def cleanup_mods(self):
        self.auto_terminate_game()
        try:
            hkey=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 1623730")
            path,_=winreg.QueryValueEx(hkey,"InstallLocation")
            winreg.CloseKey(hkey)
            self.log(f"Accessing game directory: {path}")
            root_mods=os.path.join(path,"Mods")
            if os.path.exists(root_mods):shutil.rmtree(root_mods,ignore_errors=True)
            bin_p=os.path.join(path,"Pal","Binaries","Win64")
            u4ss,dwm=os.path.join(bin_p,"ue4ss"),os.path.join(bin_p,"dwmapi.dll")
            if os.path.exists(u4ss):shutil.rmtree(u4ss,ignore_errors=True)
            if os.path.exists(dwm):os.remove(dwm)
            paks_p=os.path.join(path,"Pal","Content","Paks")
            if os.path.exists(paks_p):
                for item in os.listdir(paks_p):
                    if item.lower()!="pal-windows.pak":
                        fp=os.path.join(paks_p,item)
                        if os.path.isfile(fp):os.remove(fp)
                        elif os.path.isdir(fp):shutil.rmtree(fp,ignore_errors=True)
            app_p=os.path.join(os.environ["LOCALAPPDATA"],"Pal","Saved")
            if os.path.exists(app_p):
                shutil.rmtree(os.path.join(app_p,"Config"),ignore_errors=True)
                shutil.rmtree(os.path.join(app_p,"Logs"),ignore_errors=True)
            self.log("Successfully removed mods and cleared configuration cache.")
        except:self.log("Could not find the game installation. Is it installed via Steam?")
    def closeEvent(self,event):
        self.kill_external_fixer()
        event.accept()
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=PalworldFixerGUI()
    window.show()
    sys.exit(app.exec())
def audit_and_fix_documents_for_eos():
    import os,ctypes,datetime,subprocess,shutil,traceback,time,winreg
    ctypes.windll.kernel32.SetConsoleTitleW("Palworld Fixer")
    log_path=os.path.join(os.getcwd(),"documents_eos_audit.log")
    def log(m):
        t=datetime.datetime.now().strftime("%H:%M:%S")
        s=f"[{t}] {m}"
        print(s)
        with open(log_path,"a",encoding="utf-8",errors="ignore") as f:f.write(s+"\n")
    def set_docs_shell_path(path):
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",0,winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key,"Personal",0,winreg.REG_EXPAND_SZ,path)
        winreg.CloseKey(key)
        ctypes.windll.shell32.SHGetSetSettings(None,0,0)
        ctypes.windll.shell32.SHChangeNotify(0x08000000,0,None,None)
    def sync_system_time():
        try:
            subprocess.run("w32tm /resync /force",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            log("System time synchronized via w32tm.")
        except:log("Failed to sync system time.")
    def cleanup_palworld_mods():
        try:
            hkey=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 1623730")
            path,_=winreg.QueryValueEx(hkey,"InstallLocation")
            winreg.CloseKey(hkey)
            log(f"Game Path: {path}")
            root_mods=os.path.join(path,"Mods")
            if os.path.exists(root_mods):
                shutil.rmtree(root_mods,ignore_errors=True)
                log("Deleted root Mods folder.")
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
            log("Internal mods and Paks cleaned.")
            app_p=os.path.join(os.environ["LOCALAPPDATA"],"Pal","Saved")
            if os.path.exists(app_p):
                shutil.rmtree(os.path.join(app_p,"Config"),ignore_errors=True)
                shutil.rmtree(os.path.join(app_p,"Logs"),ignore_errors=True)
                log("Cleaned EOS/Pal AppData Logs & Config.")
        except:log("Registry check failed: Game not found or access denied.")
    try:
        curr_pid=os.getpid()
        subprocess.run(f'taskkill /F /FI "PID ne {curr_pid}" /IM PalworldEOSFix.exe',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except:pass
    cleanup_palworld_mods()
    while True:
        try:
            std=os.path.join(os.environ["USERPROFILE"],"Documents")
            if not os.path.exists(std):os.makedirs(std,exist_ok=True)
            set_docs_shell_path("%USERPROFILE%\\Documents")
            sync_system_time()
            buf=ctypes.create_unicode_buffer(260)
            ctypes.windll.shell32.SHGetFolderPathW(None,5,None,0,buf)
            log(f"SHELL & TIME SECURED: {buf.value}")
            print(">>> Path & Time secured. Mods cleaned. You can now try joining or hosting.")
        except Exception:
            log(traceback.format_exc())
        time.sleep(60)
if __name__=="__main__":
    audit_and_fix_documents_for_eos()
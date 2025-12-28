def trigger_eos_error_environment():
    import os,ctypes,subprocess,winreg,time,shutil
    ctypes.windll.kernel32.SetConsoleTitleW("Palworld Saboteur")
    def set_docs_path(path):
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",0,winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key,"Personal",0,winreg.REG_EXPAND_SZ,path)
        winreg.CloseKey(key)
        ctypes.windll.shell32.SHGetSetSettings(None,0,0)
        ctypes.windll.shell32.SHChangeNotify(0x08000000,0,None,None)
    try:
        curr_pid=os.getpid()
        subprocess.run(f'taskkill /F /FI "PID ne {curr_pid}" /IM eos_trigger.exe',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except:pass
    try:
        local_fake=os.path.join(os.environ["USERPROFILE"],"Desktop","FakeNetworkShare")
        os.makedirs(local_fake,exist_ok=True)
        share_name="EOSTestShare"
        subprocess.run(f'net share {share_name}="{local_fake}" /grant:everyone,full',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        unc_path=f"\\\\{os.environ['COMPUTERNAME']}\\{share_name}"
        print(f"SABOTAGE: Setting Documents to {unc_path}")
        set_docs_path(unc_path)
        pal_path=os.path.join(unc_path,"Palworld")
        os.makedirs(pal_path,exist_ok=True)
        print("Status: Environment sabotaged. EOS should now fail.")
        input(">>> Press ENTER to restore local Documents and clean up...")
        set_docs_path("%USERPROFILE%\\Documents")
        subprocess.run(f"net share {share_name} /delete",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if os.path.exists(local_fake):shutil.rmtree(local_fake,ignore_errors=True)
        print("SUCCESS: Local path restored and share deleted.")
    except Exception as e:
        print(f"Error: {e}")
if __name__=="__main__":
    trigger_eos_error_environment()
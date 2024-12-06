from advance_adb.adb import Adb
from advance_adb.files import files
from advance_adb.app import app
import os
class utils:
    def __init__(self, device_id=None):
        self.adb = Adb(device_id)
        self.file = files(device_id)
        self.app = app(device_id)
        
    def manual_debloat(self):
        '''Manually debloats the device'''
        print("Fetching list of packages installed in your device...")
        packages = self.app.get_installed_packages_names()
        launchable_packages = []
        for p in packages:
            if self.app.if_launchable(p):
                launchable_packages.append(p)
        print("List of packages installed in your device :")
        for i in range(len(launchable_packages)):
            print(f'{i + 1}. {launchable_packages[i]}')
        apps = input("Enter apps which you want to remove (like 3 or 1,3,5) : ")
        l = apps.split(",")
        for i in l:
            if i.isdigit():
                print(f"Uninstalling {launchable_packages[int(i) - 1]}...")
                result = self.adb.shell(f'pm uninstall --user 0 {launchable_packages[int(i) - 1]}')
                if "Success" in result:
                    print(f"Successfully uninstalled {launchable_packages[int(i) - 1]}.")
                else:
                    print(f"Failed to uninstall {launchable_packages[int(i) - 1]}. Error: {result}")
            else:
                print("Wrong input")
                break
        print("Debloat successful.")
    def backup(self):
        '''Backs up all the picture, videos, documents and audio file into separated directories'''
        self.backup_pictures()
        self.backup_videos()
        self.backup_documents()
        self.backup_audio()
        print("Backup successful.")
    def backup_pictures(self):
        '''Backs up all the pictures from across the device into specified path'''
        self.adb.shell('cd /sdcard && find -type f \\( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \\) > jpeg_files.txt')
        self.file.pull('/sdcard/jpeg_files.txt', 'jpeg_files.txt')
        self.adb.shell('rm /sdcard/jpeg_files.txt')
        with open('jpeg_files.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                line = line.strip('./')
                line = './sdcard/' + line
                self.file.pull(line, line.split('/')[-1])
        os.system('mkdir -p Pictures')
        os.system('mv *.jpg Pictures')
        os.system('mv *.jpeg Pictures')
        os.system('mv *.png Pictures')
        print("Pictures backed up successfully.")
    def backup_videos(self):
        self.adb.shell('cd /sdcard && find -type f \\( -name "*.mp4" -o -name "*.mkv" -o -name "*.mpeg" \\) > video_files.txt')
        self.file.pull('/sdcard/video_files.txt', 'video_files.txt')
        self.adb.shell('rm /sdcard/video_files.txt')
        with open('video_files.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                line = line.strip('./')
                line = './sdcard/' + line
                self.file.pull(line, line.split('/')[-1])
        os.system('mkdir -p Videos')
        os.system('mv *.mp4 Videos')
        os.system('mv *.mkv Videos')
        os.system('mv *.mpeg Videos')
        print("Videos backed up successfully.")
    def backup_documents(self):
        self.adb.shell('cd /sdcard && find -type f \\( -name "*.pdf" -o -name "*.docx" \\) > doc_files.txt')
        self.file.pull('/sdcard/doc_files.txt', 'doc_files.txt')
        self.adb.shell('rm /sdcard/doc_files.txt')
        with open('doc_files.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                line = line.strip('./')
                line = './sdcard/' + line
                self.file.pull(line, line.split('/')[-1])
        os.system('mkdir -p Documents')
        os.system('mv *.pdf Documents')
        os.system('mv *.docx Documents')
        print("Documents backed up successfully.")
    def backup_audio(self):
        self.adb.shell('cd /sdcard && find -type f \\( -name "*.mp3" -o -name "*.wav" \\) > audio_files.txt')
        self.file.pull('/sdcard/audio_files.txt', 'audio_files.txt')
        self.adb.shell('rm /sdcard/audio_files.txt')
        with open('audio_files.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                line = line.strip('./')
                line = './sdcard/' + line
                self.file.pull(line, line.split('/')[-1])
        os.system('mkdir -p Audio')
        os.system('mv *.wav Audio')
        os.system('mv *.mp3 Audio')
        print("Audio backed up successfully.")
    def backup_apps(self):
        '''Backs up all the apps (with or without data) into specified path'''
        self.adb.shell_raw('backup -all -apk -shared -f backup.ab')
        print("Backup successful.")
    def restore(self):
        '''Copies file from system to device'''
        self.file.push('/Pictures/*', '/sdcard/Pictures/')
        self.file.push('/Videos/*', '/sdcard/Videos/')
        self.file.push('/Documents/*', '/sdcard/Documents/')
        self.file.push('/Audio/*', '/sdcard/Audio/')
        print("Files restored successfully.")
    def restore_apps(self):
        '''Restores apps (with or without data) to device'''
        self.adb.shell_raw(f'restore backup.ab')
        print("Restore successful.")
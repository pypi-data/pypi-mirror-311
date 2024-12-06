from advance_adb.adb import Adb
from advance_adb.files import files
class Misc:
    def __init__(self, device_id=None):
        self.adb = Adb(device_id)
        self.file = files(device_id)
    def get_battery_level(self):
        return self.adb.shell('dumpsys battery | grep level')
    
    def get_battery_status(self):
        return self.adb.shell('dumpsys battery | grep status')
    
    def screenshot(self, file_path='/sdcard/screenshot.png'):
        return self.adb.shell(f'screencap {file_path}')
    
    def screenrecord(self, file_path='/sdcard/screenrecord.mp4', time_limit=180):
        return self.adb.shell(f'screenrecord --time-limit {time_limit} {file_path}')
    
    def pull_screenshot(self, file_path):
        return self.file.pull('/sdcard/screenshot.png', file_path)
    
    def pull_screenrecord(self, file_path):
        return self.file.pull('/sdcard/screenrecord.mp4', file_path)
    
    def get_screen_size(self):
        return self.adb.shell('wm size')
    
    def get_screen_density(self):
        return self.adb.shell('wm density')
    
    def get_screen_orientation(self):
        return self.adb.shell('dumpsys input | grep SurfaceOrientation')
    
    def open_url(self, url):
        return self.adb.shell(f'am start -a android.intent.action.VIEW -d {url}')
    
from advance_adb.adb import Adb

class app:
    def __init__(self, device_id=None):
        self.adb = Adb(device_id)
    def install(self, apk_path):
        return self.adb.shell_raw(f'install -r {apk_path}')
    
    def uninstall(self, package_name):
        return self.adb.shell_raw(f'uninstall {package_name}')
    
    def clear_data(self, package_name):
        return self.adb.shell(f'pm clear {package_name}')
    
    def launch_app(self, package_name):
        return self.adb.shell(f'monkey -p {package_name} 1')
    
    def force_stop(self, package_name):
        return self.adb.shell(f'am force-stop {package_name}')
    
    def start_activity(self, activity):
        return self.adb.shell(f'am start -n {activity}')
    
    def stop_activity(self, activity):
        return self.adb.shell(f'am force-stop {activity}')
    
    def get_current_activity(self):
        return self.adb.shell('dumpsys window windows | grep mCurrentFocus')
    
    def get_installed_packages(self):
        return self.adb.shell('pm list packages')
    
    def get_installed_packages_names(self):
        return [package.split(':')[1] for package in self.get_installed_packages().splitlines()]
    
    def disable(self, package_name):
        return self.adb.shell('pm disable --user 0 ' + package_name)
    
    def enable(self, package_name):
        return self.adb.shell('pm enable ' + package_name)
    
    def is_package_installed(self, package_name):
        return package_name in self.get_installed_packages_names()
    
    def grant_permission(self, package_name, permission):
        return self.adb.shell(f'pm grant {package_name} {permission}')
    
    def revoke_permission(self, package_name, permission):
        return self.adb.shell(f'pm revoke {package_name} {permission}')
    
    def get_permissions(self, package_name):
        return self.adb.shell(f'pm dump {package_name} | grep permission')
    
    def if_launchable(self, package_name):
        return True if self.adb.shell(f'pm dump {package_name} | grep -A 1 android.intent.action.MAIN | grep android.intent.category.LAUNCHER') else False
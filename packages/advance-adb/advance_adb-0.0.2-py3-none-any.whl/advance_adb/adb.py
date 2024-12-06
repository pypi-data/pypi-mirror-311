import subprocess as sp
import advance_adb.Exceptions as ex

class Adb():
    def __init__(self, device_id=None):
        self.device_id = device_id
        
    @staticmethod
    def devices():
        return sp.run(['adb', 'devices'], capture_output=True, text=True).stdout.strip()
    
    @staticmethod
    def kill_server():
        return sp.run(['adb', 'kill-server'], capture_output=True, text=True).stdout.strip()

    @staticmethod
    def start_server():
        return sp.run(['adb', 'start-server'], capture_output=True, text=True).stdout.strip()
    
    @staticmethod
    def restart_server():
        Adb.kill_server()
        return Adb.start_server()
    
    def shell_raw(self, cmd):
        cmd2 = ['adb']
        if self.device_id:
            cmd2 += ['-s', self.device_id]
        cmd2 += cmd.split()
        try:
            result =  sp.run(cmd2, capture_output=True, text=True).stdout.strip()
        except ex.AdbError as e:
            raise ex.AdbError(e)
        return result
    
    def shell(self, cmd_2):
        cmd = ['adb']
        if self.device_id:
            cmd += ['-s', self.device_id]
        cmd += ['shell', cmd_2]
        try:
            result =  sp.run(cmd, capture_output=True, text=True).stdout.strip()
        except ex.AdbError as e:
            raise ex.AdbError(e)
        return result
    
    def getprop(self, key):
        return self.shell(f'getprop {key}').strip()
    
    def setprop(self, key, value):
        return self.shell(f'setprop {key} {value}').strip()
    
    def get_device_id(self):
        return self.getprop('ro.serialno')
    
    def get_android_version(self):
        return self.getprop('ro.build.version.release')
    
    def get_sdk_version(self):
        return self.getprop('ro.build.version.sdk')
    
    def get_model(self):
        return self.getprop('ro.product.model')
    
    def get_manufacturer(self):
        return self.getprop('ro.product.manufacturer')
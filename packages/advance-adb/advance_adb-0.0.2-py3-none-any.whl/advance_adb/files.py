from advance_adb.adb import Adb

class files:
    def __init__(self, device_id=None):
        self.adb = Adb(device_id)
        
    def push(self, file_path, device_path):
        return self.adb.shell_raw(f'push {file_path} {device_path}')
    
    def pull(self, device_path, file_path):
        return self.adb.shell_raw(f'pull {device_path} {file_path}')
    
    def list_files(self, path):
        return self.adb.shell(f'ls {path}')
    
    def delete_file(self, file_path):
        return self.adb.shell(f'rm {file_path}')
    
    def delete_dir(self, dir_path):
        return self.adb.shell(f'rm -r {dir_path}')
    
    def make_dir(self, dir_path):
        return self.adb.shell(f'mkdir {dir_path}')
    
    def rename(self, old_path, new_path):
        return self.adb.shell(f'mv {old_path} {new_path}')
    
    def copy(self, src_path, dest_path):
        return self.adb.shell(f'cp {src_path} {dest_path}')
    
    def re_list_files(self, path):
        return self.adb.shell(f'ls -R {path}')
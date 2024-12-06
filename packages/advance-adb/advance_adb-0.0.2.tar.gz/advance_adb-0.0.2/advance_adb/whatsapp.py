from advance_adb.adb import Adb
from advance_adb.files import files
from advance_adb.app import app
from advance_adb.misc import Misc
from time import sleep
import csv

class whatsapp:
    def __init__(self, device_id=None):
        self.adb = Adb(device_id)
        self.files = files()
        self.app = app()
        self.misc = Misc()
        
    def __csv_to_dict(self, file_path):
        '''Converts the csv file to dictionary'''
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            num_msg_dict = dict(reader)
        return num_msg_dict
    def send_msg(self, mob_no, msg):
        '''Sends the specified whatsapp message to specified/multiple mobile number'''
        if type(mob_no) == str:
            mob_no = [mob_no]
        for mob in mob_no:
            self.adb.shell(f'am start -a android.intent.action.VIEW -d "whatsapp://send?phone={mob}&text={msg}"')
            sleep(5)
            self.adb.shell('input keyevent 66')
        self.app.force_stop('com.whatsapp')
    def send_bulk_msg(self, num_msg_dict):
        '''Sends the specified whatsapp message to specified multiple mobile numbers
        \nnum_msg_dict: dictionary or csv file containing mobile number and message'''
        if type(num_msg_dict) != dict:
            num_msg_dict = self.__csv_to_dict(num_msg_dict)
        for mob, msg in num_msg_dict.items():
            self.send_msg(mob, msg)
        sleep(2)
        self.app.force_stop('com.whatsapp')
from advance_adb.adb import Adb
from advance_adb.files import files

class Analytics:
    def __init__(self, device_id=None):
        self.adb = Adb(device_id)
        self.file = files(device_id)
        
    @staticmethod
    def __parse_data_to_dic(data):
        id = 1
        final_dic = {}
        data = data.split('\n')
        data = [d[7:] for d in data]
        for d in data:
            pairs = d.split(', ')
            d = {}
            for p in pairs:
                p = p.split('=')
                if len(p)>1:
                    d.update({p[0]:p[1]})
            final_dic.update({id:d})
            id += 1
        return final_dic
    
    def retrieve_call_log(self):
        return Analytics.__parse_data_to_dic(self.adb.shell('content query --uri content://call_log/calls'))
    
    def analyse_call_log(self):
        '''Analyse the call log and return a dictionary with the following keys:
        - 5 most frequent caller
        - 5 most longest call duration'''
        call_log = self.retrieve_call_log()
        call_duration = {}
        call_count = {}
        for k,v in call_log.items():
            if call_duration.get(v.get('number')):
                call_duration[v.get('number')] += int(v.get('duration'))
            else:
                call_duration[v.get('number')] = int(v.get('duration'))
            if call_count.get(v.get('number')):
                call_count[v.get('number')] += 1
            else:
                call_count[v.get('number')] = 1
        call_duration = sorted(call_duration.items(), key=lambda x: x[1], reverse=True)
        call_count = sorted(call_count.items(), key=lambda x: x[1], reverse=True)
        return {
            'longest_caller' : call_duration[:5],
            'frequent_caller' : call_count[:5]
        }
    def retrieve_sms_log(self):
        return Analytics.__parse_data_to_dic(self.adb.shell('content query --uri content://sms'))
    
    def retrieve_screen_time(self):
        return self.adb.shell('dumpsys usagestats')
    
    def analyse_screen_time(self):
        '''Analyse the screen time and return a dictionary with the following keys
        - most used app
        - most used app duration
        - maximum app duration'''
        screen_time = self.retrieve_screen_time()
        screen_time = screen_time.split('\n')
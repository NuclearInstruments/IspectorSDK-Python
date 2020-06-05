import requests
import json
from enum import Enum
class ispector_sdk:

    class RunMode(Enum):
        FREE =0
        TIME_MS=1
        COUNTS=2

    class BaselineLength(Enum):
        BASELINE_1024 =1024
        BASELINE_512 =512
        BASELINE_256 =256
        BASELINE_128 = 128
        BASELINE_64 = 64
        BASELINE_32 = 32
        BASELINE_16 = 16

    class HVCompensation(Enum):
        DISABLE_COMPENSATION = "digital"
        ENABLE_COMPENSATION = "temperature"

    API_ENDPOINT = ""

    def __bool_to_str(self, bValue):
        return  (str(bValue)).lower()

    def __float_to_str(self, fValue):
        return   str(fValue).replace(",",".")

    def __int_to_str(self, iValue):
        return   str(iValue)
    def __init__(self, ip):
        self.API_ENDPOINT = "http://" + ip

    def set_hv_basic(self, hv_on, hv_voltage):
        JSON_COMMAND = '{"command": "SET_CHANNEL_CONFIG", "channel_config": [{"id": 0, "HV_STATUS": ' + \
                       self.__bool_to_str(hv_on)  + ', "HV_VOLTAGE": ' + \
                       self.__float_to_str(hv_voltage) + '}], "store_flash": false}'
        r = requests.post(url=(self.API_ENDPOINT + "/set_config.cgi"), data=JSON_COMMAND)

    def set_hv_compensation(self, mode, temp_coeff):
        JSON_COMMAND = '{"command": "SET_CHANNEL_CONFIG", "channel_config": [{"id": 0, "HV_MODE": ' + \
                       mode.value + ', "TCoeff": ' + \
                       self.__float_to_str(temp_coeff) + '}], "store_flash": false}'
        r = requests.post(url=(self.API_ENDPOINT + "/set_config.cgi"), data=JSON_COMMAND)

    def set_hv_cfg(self, ramp, maxI, maxV, on_starup):
        JSON_COMMAND = '{"command" : "SET_CHANNEL_CONFIG","channel_config" :[{"id" : 0,' + \
                       '"MaxV" : '+ self.__float_to_str(maxV) +',' + \
                       '"MaxI" : '+ self.__float_to_str(maxI)+',' + \
                       '"MaxT" : 0,' + \
                       '"RAMP" : '+ self.__float_to_str(ramp) +',' + \
                       '"HV_PWRON" : '+ self.__bool_to_str(on_starup)  +'}],"store_flash" : false}'
        r = requests.post(url=(self.API_ENDPOINT + "/set_config.cgi"), data=JSON_COMMAND)


    def configureMCA(self, trigger_threshold,
                     trigger_inibit, pre_int_time,
                     int_time, int_gain, pileup_inib,
                     pileup_penality, baseline_inib,
                     baseline_len, target_run,
                     target_value):


        JSON_COMMAND = '{"command" : "SET_CHANNEL_CONFIG","mca_config" :[{"id" : 0,' \
                       '"trigger_thrs" : '+ self.__int_to_str(trigger_threshold) +',' \
                       '"trigger_inib" : '+ self.__int_to_str(trigger_inibit) +',' \
                       '"int_pre" : '+ self.__int_to_str(pre_int_time) +',' \
                       '"int_val" : '+ self.__int_to_str(int_time) +',' \
                       '"int_gain" : '+ self.__int_to_str(int_gain) +',' \
                       '"pileup_inib" : '+ self.__int_to_str(pileup_inib) +',' \
                       '"pileup_pen" : '+ self.__int_to_str(pileup_penality) +',' \
                       '"baseline_inib" : '+ self.__int_to_str(baseline_inib) +',' \
                       '"baseline_len" : '+ self.__int_to_str(baseline_len.value) +',' \
                       '"taget_run" : '+ self.__int_to_str(target_run.value) +',' \
                       '"taget_value" : '+ self.__int_to_str(target_value)+',' \
                       '"reset_on_apply" : true}],"store_flash" : false}}'
        r = requests.post(url=(self.API_ENDPOINT + "/set_config.cgi"), data=JSON_COMMAND)

    def getChannelStatus(self):
        r = requests.get(url=(self.API_ENDPOINT + "/status.cgi"))
        return json.loads(r.text)["current_status"]["channels"][0]

    def getSystemStatus(self):
        r = requests.get(url=(self.API_ENDPOINT + "/status.cgi"))
        return json.loads(r.text)["current_status"]["system_status"]

    def getWave(self):
        r = requests.get(url=(self.API_ENDPOINT + "/wavedump.cgi"))
        return json.loads(r.text)["data"]

    def getSpectrum(self):
        r = requests.get(url=(self.API_ENDPOINT + "/spectrum.cgi"))
        return json.loads(r.text)["data"]

    def resetSpectrum(self):
        r = requests.get(url=(self.API_ENDPOINT + "/resetspectrum.cgi"))
        return

    def runSpectrum(self):
        r = requests.get(url=(self.API_ENDPOINT + "/mca_run.cgi"))
        return

    def stopSpectrum(self):
        r = requests.get(url=(self.API_ENDPOINT + "/mca_stop.cgi"))
        return
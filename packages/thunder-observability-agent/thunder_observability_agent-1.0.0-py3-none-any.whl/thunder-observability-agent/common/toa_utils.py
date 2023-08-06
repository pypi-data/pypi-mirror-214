#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT

"""
Configure utility methods for toa framework.
To use, simply 'import Utils' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

from common.toa_logging import Logging
import json 
import datetime
from common.toa_constant import Constant
import requests
import asyncio
from requests.exceptions import ConnectTimeout, ReadTimeout

class Utils:
    
    def __init__(self): 
        pass 
    
    _logger = Logging().get_logger("Utils")
    _active_metric_provider=None
    _active_log_provider=None
    _main=None
    _config=None
    _thunders=None
    _aws_credentials=None
    _aws_config=None
    _azure_credentials=None
    _vmware_credentials=None
    _metrics=None
    _non_l4v_metrics=None
    _datetime      = datetime.datetime.now(datetime.timezone.utc)
    _datetime_epoc = int(datetime.datetime.timestamp(_datetime) * 1000)
    _datetime_str  =_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    _datetime_id   =_datetime.strftime("%Y%m%d%H%M%S")
    _datetime_gmt_str =  _datetime.strftime('%a, %d %b %Y %H:%M:%S GMT')
    _http_ssl_verify=None
    
    @staticmethod
    def load_properties():
        Utils._main = Utils.load_configuration(Constant._MAIN_CONF_PATH, Utils._main, Constant._ERROR_MAIN_NOT_FOUND, Constant._KEYVALUE) 
    
    @staticmethod
    def load_config():
        Utils._config = Utils.load_configuration(Utils._main.get(Constant._CONFIG_PATH), Utils._config, Constant._ERROR_CONFIG_NOT_FOUND, Constant._JSON) 
    
    @staticmethod
    def load_collect_provider():
        Utils._thunders = Utils.load_configuration(Utils._main.get(Constant._THUNDER_CREDENTIALS_PATH), Utils._thunders, Constant._ERROR_THUNDER_CREDENTIALS_NOT_FOUND, Constant._JSON)
        
    @staticmethod
    def load_publish_provider():
        Utils.validate_provider()
        Utils.load_active_log_provider()
        Utils.load_active_metric_provider()
        if(not Utils.is_valid(Utils._active_log_provider) and not Utils.is_valid(Utils._active_metric_provider)):
            Utils._logger.warn(Constant._ERROR_NO_VALID_PROVIDER_CONFIG_FOUND)
            
        if(Utils.is_valid(Utils._main)):
            if(not Utils.is_valid(Utils._main.get(Constant._LOG_DELAY_MIN)) or not Utils.is_integer(Utils._main.get(Constant._LOG_DELAY_MIN)) or int(Utils._main.get(Constant._LOG_DELAY_MIN)) < 0):
                Utils._logger.warn((Constant._ERROR_NO_VALID_LOG_DELAY_IN_MIN_FOUND).format(Utils._main.get(Constant._LOG_DELAY_MIN)))
                Utils._main[Constant._LOG_DELAY_MIN] =  0
            
            if(not Utils.is_valid(Utils._main.get(Constant._CRON_DELAY_MIN)) or not Utils.is_integer(Utils._main.get(Constant._CRON_DELAY_MIN)) or int(Utils._main.get(Constant._CRON_DELAY_MIN)) < 0):
                Utils._logger.warn((Constant._ERROR_NO_VALID_CRON_DELAY_IN_MIN_FOUND).format(Utils._main.get(Constant._CRON_DELAY_MIN)))
                Utils._main[Constant._CRON_DELAY_MIN] = 1
                
        if(Utils.is_valid(Utils._active_log_provider) or Utils.is_valid(Utils._active_metric_provider)):
            # Azure validation.
            if(Utils._active_log_provider==Constant._AZURE_LOG or Utils._active_metric_provider==Constant._AZURE_METRIC):
                if(not Utils.is_valid(Utils._azure_credentials)):
                    Utils._azure_credentials =  Utils.load_configuration(Utils._main.get(Constant._AZURE_CREDENTIALS_PATH), Utils._azure_credentials, Constant._ERROR_AZURE_CREDENTIALS_NOT_FOUND, Constant._KEYVALUE) 
                
                if(Utils._active_metric_provider==Constant._AZURE_METRIC):
                    if(not Utils.is_valid(Utils._azure_credentials) or (Utils.is_valid(Utils._azure_credentials) 
                        and (not Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_CLIENT_ID))
                        or not Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_SECRET_ID))
                        or not Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_TENANT_ID))
                        or not Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_LOCATION))))): 
                        Utils._logger.error(Constant._ERROR_AZURE_CREDENTIALS_METRIC_NOT_FOUND)
                        Utils._active_metric_provider=None
                    
                    if(Utils.is_valid(Utils._config)
                        and not Utils.is_valid(Utils._config.get(Constant._AZURE_METRIC_RESOURCE_ID))):  
                        Utils._logger.error(Constant._ERROR_AZURE_CONFIG_METRIC_NOT_FOUND)
                        Utils._active_metric_provider=None
                
                if(Utils._active_log_provider==Constant._AZURE_LOG):
                    if(not Utils.is_valid(Utils._azure_credentials) or (Utils.is_valid(Utils._azure_credentials)
                        and not Utils.is_valid(Utils._azure_credentials.get(Constant._AZURE_WORKSPACE_PRIMARY_KEY)))): 
                        Utils._logger.error(Constant._ERROR_AZURE_CREDENTIALS_LOG_NOT_FOUND) 
                        Utils._active_log_provider = None
                                
                    if(Utils.is_valid(Utils._config)
                        and not Utils.is_valid(Utils._config.get(Constant._AZURE_LOG_WORKSPACE_ID))):  
                        Utils._logger.error(Constant._ERROR_AZURE_CONFIG_LOG_NOT_FOUND)
                        Utils._active_log_provider = None
                
            if((Utils._active_log_provider==Constant._AWS_LOG or Utils._active_metric_provider==Constant._AWS_METRIC)):
                if(not Utils.is_valid(Utils._aws_credentials)): 
                    Utils._aws_credentials =  Utils.load_configuration(Utils._main.get(Constant._AWS_CREDENTIALS_PATH), Utils._aws_credentials, Constant._ERROR_AWS_CREDENTIALS_NOT_FOUND, Constant._KEYVALUE) 
                if(not Utils.is_valid(Utils._aws_config)): 
                    Utils._aws_config =  Utils.load_configuration(Utils._main.get(Constant._AWS_CONFIG_PATH), Utils._aws_config, Constant._ERROR_AWS_CONFIG_NOT_FOUND, Constant._KEYVALUE) 
                
                if(not Utils.is_valid(Utils._aws_credentials) or (Utils.is_valid(Utils._aws_credentials)
                    and (not Utils.is_valid(Utils._aws_credentials.get(Constant._AWS_ACCESS_KEY_ID)) 
                    or not Utils.is_valid(Utils._aws_credentials.get(Constant._AWS_SECRET_ACCESS_KEY))))): 
                        Utils._logger.error(Constant._ERROR_AWS_CRED_NOT_FOUND)
                        Utils._active_log_provider=None
                        Utils._active_metric_provider=None
                        
                if(not Utils.is_valid(Utils._aws_config) or (Utils.is_valid(Utils._aws_config)
                    and not Utils.is_valid(Utils._aws_config.get(Constant._AWS_REGION)))):  
                        Utils._logger.error(Constant._ERROR_AWS_CONFIG_METRIC_NOT_FOUND)
                        Utils._active_log_provider=None
                        Utils._active_metric_provider=None
                        
                if(Utils.is_valid(Utils._config) and Utils._active_log_provider==Constant._AWS_LOG 
                        and (not Utils.is_valid(Utils._config.get(Constant._AWS_LOG_GROUP_NAME)))): 
                        Utils._logger.error(Constant._ERROR_AWS_CONFIG_LOG_NOT_FOUND) 
                        Utils._active_log_provider = None
                            
            if(Utils._active_metric_provider==Constant._VMWARE_METRIC or Utils._active_log_provider==Constant._VMWARE_LOG):
                if(not Utils.is_valid(Utils._vmware_credentials)): 
                    Utils._vmware_credentials = Utils.load_configuration(Utils._main.get(Constant._VMWARE_CREDENTIALS_PATH), Utils._vmware_credentials, Constant._ERROR_VMWARE_CREDENTIALS_NOT_FOUND, Constant._KEYVALUE) 
                
                if(not Utils.is_valid(Utils._vmware_credentials) or 
                        (Utils.is_valid(Utils._vmware_credentials) and Utils._active_metric_provider==Constant._VMWARE_METRIC 
                        and (not Utils.is_valid(Utils._vmware_credentials.get(Constant._VMWARE_VROPS_USERNAME)) 
                        or not Utils.is_valid(Utils._vmware_credentials.get(Constant._VMWARE_VROPS_PASSWORD))))):
                        Utils._logger.error(Constant._ERROR_VMWARE_CRED_METRIC_NOT_FOUND)
                        Utils._active_metric_provider = None
                        
                if(Utils.is_valid(Utils._config)
                    and Utils._active_log_provider==Constant._VMWARE_LOG
                    and (not Utils.is_valid(Utils._config.get(Constant._VMWARE_VRLI_HOST)))):
                    Utils._logger.error(Constant._ERROR_VMWARE_CONFIG_LOG_NOT_FOUND)
                    Utils._active_log_provider = None
                    
                if(Utils.is_valid(Utils._config)
                    and Utils._active_metric_provider==Constant._VMWARE_METRIC
                    and (not Utils.is_valid(Utils._config.get(Constant._VMWARE_VROPS_HOST)))):
                    Utils._logger.error(Constant._ERROR_VMWARE_CONFIG_METRIC_NOT_FOUND)
                    Utils._active_metric_provider = None
               
             
    
    @staticmethod
    def validate_provider():
        if(Utils.is_valid(Utils._config)):
            if ((not Utils.is_valid(Utils._config.get(Constant._AZURE_PROVIDER)) or  Utils._config.get(Constant._AZURE_PROVIDER)!=1)
                and ((Utils.is_valid(Utils._config.get(Constant._AZURE_METRIC)) and Utils._config.get(Constant._AZURE_METRIC) == 1)
                or ((Utils.is_valid(Utils._config.get(Constant._AZURE_LOG)) and Utils._config.get(Constant._AZURE_LOG) == 1)))):
                Utils._logger.warn(Constant._ERROR_NO_VALID_PROVIDER_FOUND.format(str(Utils._config.get(Constant._AZURE_METRIC)),str(Utils._config.get(Constant._AZURE_LOG)), Constant._AZURE_PROVIDER))
            
            elif ((not Utils.is_valid(Utils._config.get(Constant._AWS_PROVIDER)) or  Utils._config.get(Constant._AWS_PROVIDER)!=1)
                and ((Utils.is_valid(Utils._config.get(Constant._AWS_METRIC)) and Utils._config.get(Constant._AWS_METRIC) == 1)
                or ((Utils.is_valid(Utils._config.get(Constant._AWS_LOG)) and Utils._config.get(Constant._AWS_LOG) == 1)))):
                Utils._logger.warn(Constant._ERROR_NO_VALID_PROVIDER_FOUND.format(str(Utils._config.get(Constant._AWS_METRIC)),str(Utils._config.get(Constant._AWS_LOG)), Constant._AWS_PROVIDER))
            
            elif ((not Utils.is_valid(Utils._config.get(Constant._VMWARE_PROVIDER)) or  Utils._config.get(Constant._VMWARE_PROVIDER)!=1)
                and ((Utils.is_valid(Utils._config.get(Constant._VMWARE_METRIC)) and Utils._config.get(Constant._VMWARE_METRIC) == 1)
                or ((Utils.is_valid(Utils._config.get(Constant._VMWARE_LOG)) and Utils._config.get(Constant._VMWARE_LOG) == 1)))):
                Utils._logger.warn(Constant._ERROR_NO_VALID_PROVIDER_FOUND.format(str(Utils._config.get(Constant._VMWARE_METRIC)),str(Utils._config.get(Constant._VMWARE_LOG)), Constant._VMWARE_PROVIDER))
            
    @staticmethod
    def load_active_log_provider():
        if(not Utils.is_valid(Utils._config)):
            return None
        if (Utils._config.get(Constant._AZURE_PROVIDER) 
            and Utils._config.get(Constant._AZURE_LOG)
            and Utils._config.get(Constant._AZURE_PROVIDER) == 1
            and Utils._config.get(Constant._AZURE_LOG)==1):
            Utils._logger.info(Constant._INFO_ACTIVE_PROVIDER_LOG.format(Constant._AZURE.upper()))
            Utils._active_log_provider = Constant._AZURE_LOG
        elif (Utils._config.get(Constant._VMWARE_PROVIDER) 
            and Utils._config.get(Constant._VMWARE_LOG)
            and Utils._config.get(Constant._VMWARE_PROVIDER) == 1
            and Utils._config.get(Constant._VMWARE_LOG)==1):
            Utils._logger.info(Constant._INFO_ACTIVE_PROVIDER_LOG.format(Constant._VMWARE.upper()))
            Utils._active_log_provider =  Constant._VMWARE_LOG
        elif (Utils._config.get(Constant._AWS_PROVIDER) 
            and Utils._config.get(Constant._AWS_LOG)
            and Utils._config.get(Constant._AWS_PROVIDER) == 1
            and Utils._config.get(Constant._AWS_LOG)==1):
            Utils._logger.info(Constant._INFO_ACTIVE_PROVIDER_LOG.format(Constant._AWS.upper()))
            Utils._active_log_provider =  Constant._AWS_LOG
        if(Utils.is_valid(Utils._active_log_provider)):
            Utils._logger.info(Constant._INFO_ACTIVE_LOG_PROVIDER_FOUND.format(Utils._active_log_provider.upper())) 
        count = 0    
        
        if(Utils._config.get(Constant._AZURE_LOG)==1):
            count = count + 1
        if(Utils._config.get(Constant._VMWARE_LOG)==1):
            count = count + 1    
        if(Utils._config.get(Constant._AWS_LOG)==1):
            count = count + 1
            
        if(count > 1):
            Utils._logger.warn(Constant._WARN_MULTIPLE_LOG_FOUND) 
                   
    @staticmethod
    def load_active_metric_provider():
        if(not Utils.is_valid(Utils._config)):
            return None
        if (Utils._config.get(Constant._AZURE_PROVIDER) 
            and Utils._config.get(Constant._AZURE_METRIC) 
            and Utils._config.get(Constant._AZURE_PROVIDER) == 1
            and Utils._config.get(Constant._AZURE_METRIC)==1):
            Utils._logger.info(Constant._INFO_ACTIVE_PROVIDER_METRIC.format(Constant._AZURE.upper()))
            Utils._active_metric_provider=Constant._AZURE_METRIC
            Utils._metrics = []
            Utils._non_l4v_metrics = []
            if(Utils._config.get(Constant._AZURE_CPU)==1):
                Utils._metrics.append(Constant._AZURE_CPU)
                
            if(Utils._config.get(Constant._AZURE_MEMORY)==1):
                Utils._non_l4v_metrics.append(Constant._AZURE_MEMORY)
                
            if(Utils._config.get(Constant._AZURE_DISK)==1):
                Utils._non_l4v_metrics.append(Constant._AZURE_DISK)
                
            if(Utils._config.get(Constant._AZURE_THROUGHPUT)==1):
                Utils._metrics.append(Constant._AZURE_THROUGHPUT)
                
            if(Utils._config.get(Constant._AZURE_INTERFACES)==1):
                Utils._metrics.append(Constant._AZURE_INTERFACES)
                
            if(Utils._config.get(Constant._AZURE_CPS)==1):
                Utils._metrics.append(Constant._AZURE_CPS)
                
            if(Utils._config.get(Constant._AZURE_TPS)==1):
                Utils._metrics.append(Constant._AZURE_TPS)
                
            if(Utils._config.get(Constant._AZURE_SERVER_DOWN_COUNT)==1):
                Utils._metrics.append(Constant._AZURE_SERVER_DOWN_COUNT) 
                
            if(Utils._config.get(Constant._AZURE_SERVER_DOWN_PERCENTAGE)==1):
                Utils._metrics.append(Constant._AZURE_SERVER_DOWN_PERCENTAGE)
                
            if(Utils._config.get(Constant._AZURE_SSL_CERT)==1):
                Utils._metrics.append(Constant._AZURE_SSL_CERT) 
               
            if(Utils._config.get(Constant._AZURE_SERVER_ERROR)==1):
                Utils._metrics.append(Constant._AZURE_SERVER_ERROR)
                
            if(Utils._config.get(Constant._AZURE_SESSION)==1):
                Utils._metrics.append(Constant._AZURE_SESSION)
                
            if(Utils._config.get(Constant._AZURE_PACKET_RATE)==1):
                Utils._metrics.append(Constant._AZURE_PACKET_RATE)
                
            if(Utils._config.get(Constant._AZURE_PACKET_DROP)==1):
                Utils._metrics.append(Constant._AZURE_PACKET_DROP)
            
        elif (Utils._config.get(Constant._VMWARE_PROVIDER) 
            and Utils._config.get(Constant._VMWARE_METRIC)
            and Utils._config.get(Constant._VMWARE_PROVIDER) == 1
            and Utils._config.get(Constant._VMWARE_METRIC)==1):
            Utils._active_metric_provider=Constant._VMWARE_METRIC;
            Utils._logger.info(Constant._INFO_ACTIVE_PROVIDER_METRIC.format(Constant._VMWARE.upper()))
            Utils._metrics = []
            Utils._non_l4v_metrics = []
            if(Utils._config.get(Constant._VMWARE_CPU)==1):
                Utils._metrics.append(Constant._VMWARE_CPU)
                
            if(Utils._config.get(Constant._VMWARE_MEMORY)==1):
                Utils._non_l4v_metrics.append(Constant._VMWARE_MEMORY)
                
            if(Utils._config.get(Constant._VMWARE_DISK)==1):
                Utils._non_l4v_metrics.append(Constant._VMWARE_DISK)
                
            if(Utils._config.get(Constant._VMWARE_THROUGHPUT)==1):
                Utils._metrics.append(Constant._VMWARE_THROUGHPUT)
                
            if(Utils._config.get(Constant._VMWARE_INTERFACES)==1):
                Utils._metrics.append(Constant._VMWARE_INTERFACES)
                
            if(Utils._config.get(Constant._VMWARE_CPS)==1):
                Utils._metrics.append(Constant._VMWARE_CPS)
                
            if(Utils._config.get(Constant._VMWARE_TPS)==1):
                Utils._metrics.append(Constant._VMWARE_TPS)
                
            if(Utils._config.get(Constant._VMWARE_SERVER_DOWN_COUNT)==1):
                Utils._metrics.append(Constant._VMWARE_SERVER_DOWN_COUNT) 
                
            if(Utils._config.get(Constant._VMWARE_SERVER_DOWN_PERCENTAGE)==1):
                Utils._metrics.append(Constant._VMWARE_SERVER_DOWN_PERCENTAGE)
                
            if(Utils._config.get(Constant._VMWARE_SSL_CERT)==1):
                Utils._metrics.append(Constant._VMWARE_SSL_CERT) 
               
            if(Utils._config.get(Constant._VMWARE_SERVER_ERROR)==1):
                Utils._metrics.append(Constant._VMWARE_SERVER_ERROR)
                
            if(Utils._config.get(Constant._VMWARE_SESSION)==1):
                Utils._metrics.append(Constant._VMWARE_SESSION)
                
            if(Utils._config.get(Constant._VMWARE_PACKET_RATE)==1):
                Utils._metrics.append(Constant._VMWARE_PACKET_RATE)
                
            if(Utils._config.get(Constant._VMWARE_PACKET_DROP)==1):
                Utils._metrics.append(Constant._VMWARE_PACKET_DROP)
                
        elif (Utils._config.get(Constant._AWS_PROVIDER) 
            and Utils._config.get(Constant._AWS_METRIC)
            and Utils._config.get(Constant._AWS_PROVIDER) == 1
            and Utils._config.get(Constant._AWS_METRIC)==1):
            Utils._active_metric_provider=Constant._AWS_METRIC;
            Utils._logger.info(Constant._INFO_ACTIVE_PROVIDER_METRIC.format(Constant._AWS.upper()))
            Utils._metrics = []
            Utils._non_l4v_metrics = []
            if(Utils._config.get(Constant._AWS_CPU)==1):
                Utils._metrics.append(Constant._AWS_CPU)
                
            if(Utils._config.get(Constant._AWS_MEMORY)==1):
                Utils._non_l4v_metrics.append(Constant._AWS_MEMORY)
                
            if(Utils._config.get(Constant._AWS_DISK)==1):
                Utils._non_l4v_metrics.append(Constant._AWS_DISK)
                
            if(Utils._config.get(Constant._AWS_THROUGHPUT)==1): 
                Utils._metrics.append(Constant._AWS_THROUGHPUT)
                
            if(Utils._config.get(Constant._AWS_INTERFACES)==1):
                Utils._metrics.append(Constant._AWS_INTERFACES)
                
            if(Utils._config.get(Constant._AWS_CPS)==1):
                Utils._metrics.append(Constant._AWS_CPS)
                
            if(Utils._config.get(Constant._AWS_TPS)==1):
                Utils._metrics.append(Constant._AWS_TPS)
                
            if(Utils._config.get(Constant._AWS_SERVER_DOWN_COUNT)==1):
                Utils._metrics.append(Constant._AWS_SERVER_DOWN_COUNT) 
                
            if(Utils._config.get(Constant._AWS_SERVER_DOWN_PERCENTAGE)==1):
                Utils._metrics.append(Constant._AWS_SERVER_DOWN_PERCENTAGE)
                
            if(Utils._config.get(Constant._AWS_SSL_CERT)==1):
                Utils._metrics.append(Constant._AWS_SSL_CERT) 
               
            if(Utils._config.get(Constant._AWS_SERVER_ERROR)==1):
                Utils._metrics.append(Constant._AWS_SERVER_ERROR)
                
            if(Utils._config.get(Constant._AWS_SESSION)==1):
                Utils._metrics.append(Constant._AWS_SESSION)
                
            if(Utils._config.get(Constant._AWS_PACKET_RATE)==1):
                Utils._metrics.append(Constant._AWS_PACKET_RATE)
                
            if(Utils._config.get(Constant._AWS_PACKET_DROP)==1):
                Utils._metrics.append(Constant._AWS_PACKET_DROP)
        
        if(Utils.is_valid(Utils._active_metric_provider)):
            Utils._logger.info(Constant._INFO_ACTIVE_METRIC_PROVIDER_FOUND.format(Utils._active_metric_provider.upper())) 
        count = 0    
        
        if(Utils._config.get(Constant._AZURE_METRIC)==1):
            count = count + 1
        if(Utils._config.get(Constant._VMWARE_METRIC)==1):
            count = count + 1    
        if(Utils._config.get(Constant._AWS_METRIC)==1):
            count = count + 1
            
        if(count > 1):
            Utils._logger.warn(Constant._WARN_MULTIPLE_METRIC_FOUND)  
            
    @staticmethod
    def validate():
        status=True
        if(Utils._thunders is None or Utils._thunders.get(Constant._THUNDERS) is None or Utils._thunders.get(Constant._THUNDERS)[0] is None or Utils._config is None or Utils._main is None):
            return False

        if(not Utils.is_valid(Utils._active_log_provider) and not Utils.is_valid(Utils._active_metric_provider)):
            return False
        
        if(Utils.is_valid(Utils._active_metric_provider) and  ((not Utils.is_valid(Utils._metrics) and not Utils.is_valid(Utils._non_l4v_metrics)) or (len(Utils._metrics) + len(Utils._non_l4v_metrics)) <=0)):
            Utils._logger.warn(Constant._ERROR_NO_VALID_METRIC_FOUND)
            
        if(Utils.is_valid(Utils._active_log_provider) or Utils.is_valid(Utils._active_metric_provider)): 
            status = True
            Utils.http_ssl_verify()
        else:
            status=False
        
        return status
        
    @staticmethod
    def date_time_utc():
        return datetime.datetime.now(datetime.timezone.utc)
     
    @staticmethod
    def is_valid(*arguments):
        valid=True
        for arg in arguments:
            if(arg is None or arg =="XXXX" or arg=="" or arg==" " or arg=="none" or arg=="None"):
                return False
        return valid;
    
    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    @staticmethod
    def map_to_value(content, file):
        
        if(content):
            if(not Utils.is_valid(file)):
                file = {}
                for line in content.split("\n"):
                    if not line:
                        continue
                    if "=" in line:
                        key, val = line.split("=",1)
                        file[key.strip()] = val.strip()
        return file
    
    @staticmethod
    def load_configuration(path, variable, error, mode):
        if(not Utils.is_valid(variable) and Utils.is_valid(path)):
            variable = None
            try:
                # JSON file
                con = open (path.strip(' \t\n\r'), "r", encoding=Constant._ENCODING)
                
                if(mode==Constant._KEYVALUE):
                    # Reading from key/value file
                    variable = Utils.map_to_value(con.read(), variable)
                elif(mode==Constant._JSON):
                    # Reading from json file
                    variable = json.loads(con.read())
                con.close()
            except Exception as exp:
                Utils._logger.error((Constant._ERROR_FILE_NOT_FOUND.format(path)) + error)
                Utils._logger.debug(exp)
            return variable
     
    @staticmethod
    def load_temp_storage(file):
        try:
            with open(Constant._TEMP_CONF_PATH + file, "r", encoding="utf-8") as con:
                variable = json.loads(con.read())
            con.close()
        except Exception:
            variable = {}
        return variable
    
    
    @staticmethod
    def write(variable, file):
        try:
            asyncio.run(Utils.async_write(variable, file))
        except Exception:
            Utils.sync_write(variable, file)
        
    @staticmethod
    async def async_write(variable, file):
        data = Utils.load_temp_storage(file)
        for key in variable.keys():
            data[key]=variable[key]
        with open(Constant._TEMP_CONF_PATH + file, "w+", encoding="utf-8") as con:
                    json.dump(data, con, default=str)
        con.close()
        
    @staticmethod
    def sync_write(variable, file):
        data = Utils.load_temp_storage(file)
        for key in variable.keys():
            data[key]=variable[key]
        with open(Constant._TEMP_CONF_PATH + file, "w+", encoding="utf-8") as con:
                    json.dump(data, con, default=str)
        con.close()
        
        
               
    @staticmethod
    def get_headers(token):
        _headers = {
            Constant._AUTHORIZATION: token,
            Constant._CONTENT_TYPE: Constant._APPLICATION_JSON,
            Constant._ACCEPT: Constant._APPLICATION_JSON 
        }
        return _headers
    
    @staticmethod
    def rest_api(url, headers, body, method, error, ip):
        try:
            response = requests.request(method, url,
                                        headers=headers, data=body, verify=Utils._http_ssl_verify,
                                        timeout=(int(Utils._main.get(Constant._API_TIMEOUT))))
            if response.status_code != 200 and response.status_code != 201 and response.status_code != 202 and response.status_code != 203 and response.status_code != 204:
                Utils._logger.error((Constant._ERROR_REQUEST_FAILED+error).format(url,response.json() if Utils.is_valid(response.text) else "{}" ,ip))
                return None
            return response
        except (ConnectionError, ConnectTimeout, ReadTimeout) as con:
            Utils._logger.error((Constant._ERROR_SERVER_NOT_REACHABLE).format(url,con))
            return None
        except (OSError) as os:
            Utils._logger.error((Constant._ERROR_SSL_NOT_REACHABLE+error).format(url,os,ip))
            return None
        except Exception as exp:
            Utils._logger.error((Constant._ERROR_REQUEST_FAILED+error).format(url,exp,ip))
            return None 
            
    @staticmethod
    def priority(log):
        if(" Info " in log):
            return "Info"
        elif(" Warning " in log):
            return "Warning"
        elif(" Error " in log):
            return "Error"
        elif(" Notice " in log):
            return "Notice"
        elif(" Debug " in log):
            return "Debug"
        else:
            return "Info"
                
    @staticmethod
    def http_ssl_verify():
        Utils._http_ssl_verify = Utils._main.get(Constant._SSL_VERIFY, "True")
        if(Utils._http_ssl_verify=="False"):
            Utils._http_ssl_verify = False
        elif(Utils.is_valid(Utils._http_ssl_verify)=="True"):
            Utils._http_ssl_verify = True
        else:
            Utils._http_ssl_verify = Utils._main.get(Constant._SSL_VERIFY)
            
        
        
        
        
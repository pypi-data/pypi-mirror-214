#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT

"""
Configure constants values.
To use, simply 'import Constant' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

import os
import sys
import warnings

class Constant:

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))  
    warnings.filterwarnings('ignore')
    
    _DEFAULT_TOA_PACKAGE_PATH = "/usr/toaenv/thunder-observability-agent"
    _TOA_CONFIG_PATH = os.environ.get("TOA_CONFIG_PATH", _DEFAULT_TOA_PACKAGE_PATH)
    _LOGGING_CONF_PATH = _TOA_CONFIG_PATH + "/logging.conf"
    _MAIN_CONF_PATH = _TOA_CONFIG_PATH + "/main.properties"
    _TEMP_CONF_PATH = _TOA_CONFIG_PATH + "/"
    _CONFIG_PATH = "config_path"
    _AWS_CREDENTIALS_PATH = "aws_credentials_path"
    _AWS_CONFIG_PATH = "aws_config_path"
    
    _AZURE_CREDENTIALS_PATH = "azure_credentials_path"
    _VMWARE_CREDENTIALS_PATH = "vmware_credentials_path"
    _THUNDER_CREDENTIALS_PATH = "thunder_credentials_path"
    _LOG_DELAY_MIN="log_collection_delay_min"
    _CRON_DELAY_MIN="cron_job_frequency_min"
    _THREADPOOL_MAX_WORKERS="max_threads"
    _API_TIMEOUT="http_connection_timeout_sec"
    _SSL_VERIFY="http_ssl_verify"
    _USERNAME="username"
    _PASSWORD="password"
    _IP="ip"
    _PRIVATE_IP="private_ip"
    _RESOURCE_ID="resource_id"
    _CREDENTIALS="credentials"
    _AUTHORIZATION="Authorization"
    _DATA="data"
    _CLOUD="cloud"
    
    _VMWARE_VROPS_HOST="vmware_vrops_host"
    _VMWARE_VRLI_HOST="vmware_vrli_host"
    _VMWARE_VROPS_USERNAME="vmware_vrops_username"
    _VMWARE_VROPS_PASSWORD="vmware_vrops_password"
    
    _AWS_ACCESS_KEY_ID="aws_access_key_id"
    _AWS_SECRET_ACCESS_KEY="aws_secret_access_key"
    _AWS_REGION="region"
    _AWS_METRIC_NAMESPACE="aws_metric_namespace"
    _AWS_LOG_GROUP_NAME="aws_log_group_name"
    _AWS_OUTPUT="output"
    
    _THUNDER="THUNDER"
    _THUNDERS="thunders"
    _SYSLOG="Syslog"
    _TOA="TOA"
    _NAMESPACE="namespace"
    
    _PARTITION_NAME="partition-name"
    #_ACTIVE_PARTITIONS="active_partitions"
    _PARTITION="active_partitions"
    _SHARED="shared"
    _PARTITION_LIMIT=20
    _DELIMETER=","
    _NON_L3V="non-l3v"
    _L3V="l3v"
    
    
    _AZURE_CLIENT_ID="azure_client_id"
    _AZURE_SECRET_ID="azure_secret_id"
    _AZURE_TENANT_ID="azure_tenant_id"
    _AZURE_LOG_WORKSPACE_ID="azure_log_workspace_id"
    _AZURE_WORKSPACE_PRIMARY_KEY="azure_workspace_primary_key"
    _AZURE_LOCATION="azure_location"
    _AZURE_METRIC_RESOURCE_ID="azure_metric_resource_id"
    
    
    _ENCODING = "utf-8"
    _KEYVALUE="keyvalue"
    _JSON="json"
    _AWS_THUNDER_AUTOSCALABLE="aws_thunder_auto_scalable"
    _AZURE_THUNDER_AUTOSCALABLE="azure_thunder_auto_scalable"
    _VMWARE_THUNDER_AUTOSCALABLE="vmware_thunder_auto_scalable"
    
    
    _ERROR_FILE_NOT_FOUND       = "Error           : File not found or corrupt. Please check file and path: [{}]. "
    _ERROR_REQ_PARAM_NOT_FOUND  = "Error           : Required params not found. " 
    _DEFAULT_PATH               = "Default file path is /usr/toaenv/thunder-observability-agent or check TOA_CONFIG_PATH environment variable."
    _ERROR_SERVER_NOT_REACHABLE = "Error           : Server connection timeout. [URI: {}, Trace: {}]. Please ping ip or check network settings."
    _ERROR_SSL_NOT_REACHABLE    = "Error           : TLS secure connection error. Please check network settings or param [http_ssl_verify] options in documentation. [URI: {}, Trace: {}]. "
    _ERROR_REQUEST_FAILED       = "Error           : Request failed. [URI: {}, Trace: {}]. "
    _ERROR_TASK_ABORT           = " Task abort for thunder: {}."
    

    _ERROR_MAIN_NOT_FOUND               ="Main properties not found. " + _DEFAULT_PATH
    _ERROR_CONFIG_NOT_FOUND             ="Application config not found. Please check [config_path] in main.properties. "
    _ERROR_AZURE_CREDENTIALS_NOT_FOUND  ="Azure credentials not found. Please check [azure_credentials_path] in main.properties. "
    _ERROR_THUNDER_CREDENTIALS_NOT_FOUND="Thunder credentials not found. Please check [thunder_credentials_path] in main.properties. "
    _ERROR_AWS_CREDENTIALS_NOT_FOUND    ="AWS credentials not found. Please check [aws_credentials_path] in main.properties. "
    _ERROR_AWS_CONFIG_NOT_FOUND         ="AWS config not found. Please check [aws_config_path] in main.properties. "
    _ERROR_VMWARE_CREDENTIALS_NOT_FOUND ="VMWare credentials not found. Please check [vmware_credentials_path] in main.properties. "
    _ERROR_AWS_CRED_NOT_FOUND           =_ERROR_REQ_PARAM_NOT_FOUND + "Please check [aws_access_key_id, aws_secret_access_key] in aws credentials. Metric/log publish task abort."
    

    _ERROR_AZURE_CRED_AUTO_METRIC_NOT_FOUND  = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [azure_client_id, azure_secret_id, azure_tenant_id] in azure credentials. Collect thunders from autoscale task abort."
    _ERROR_AZURE_CREDENTIALS_METRIC_NOT_FOUND= _ERROR_REQ_PARAM_NOT_FOUND + "Please check [azure_client_id, azure_secret_id, azure_tenant_id, azure_location] in azure credentials. Metric publish task abort."
    _ERROR_AZURE_CREDENTIALS_LOG_NOT_FOUND   = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [azure_workspace_primary_key] in azure credentials. Log publish task abort."
    _ERROR_AZURE_CONFIG_METRIC_NOT_FOUND     = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [azure_metric_resource_id] in config.json. Metric publish task abort."
    _ERROR_AZURE_CONFIG_LOG_NOT_FOUND        = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [azure_log_workspace_id] in config.json. Log publish task abort."
    _ERROR_AWS_CONFIG_METRIC_NOT_FOUND       = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [region] in aws config. Metric/Log publish task abort."
    _ERROR_AWS_CONFIG_LOG_NOT_FOUND          = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [aws_log_group_name] in config.json. Log publish task abort."
    _ERROR_VMWARE_CONFIG_METRIC_NOT_FOUND    = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [vmware_vrops_host] in config.json. Metric publish task abort."
    _ERROR_VMWARE_CONFIG_LOG_NOT_FOUND    = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [vmware_vrli_host] in config.json. Log publish task abort."
    
    _ERROR_VMWARE_CRED_METRIC_NOT_FOUND      = _ERROR_REQ_PARAM_NOT_FOUND + "Please check [vmware_vrops_username, vmware_vrops_password] in vmware credentials. Metric publish task abort."
    
    
    _ERROR_NO_VALID_LOG_DELAY_IN_MIN_FOUND   = "WARNING       : Invalid value found for "+_LOG_DELAY_MIN  +": [{}]. Only positive integer value is allowed for example [0 or 1 or 2 or nth.]. Considering default value [0] for processing, please check and update in main.properties"
    _ERROR_NO_VALID_CRON_DELAY_IN_MIN_FOUND  = "WARNING       : Invalid value found for "+_CRON_DELAY_MIN +": [{}]. Only positive integer value is allowed for example [0 or 1 or 2 or nth.]. Considering default value [1] for processing, please check and update in main.properties"
    
    
    _ERROR_AWS_LOGSTREAM            = "Error           : Request failed [Trace: {}]. Unable to publish logstream into aws cloudwatch."            + _ERROR_TASK_ABORT
    _ERROR_AWS_CLOUDWATCH_LOGS      = "Error           : Request failed [LogGroupName: {}, Trace: {}]. Unable to publish log into aws cloudwatch."                  + _ERROR_TASK_ABORT
    _ERROR_AWS_CLOUDWATCH_METRICS   = "Error           : Request failed [Namespace: {}, Trace: {}]. Unable to publish metric: [{}] into aws cloudwatch."         + _ERROR_TASK_ABORT
    _ERROR_AWS_AUTOSCALE_GROUP_LOGS = "Error           : Request failed [resource_id: {}, Trace: {}]. Unable to fetch thunder instances from aws autoscale group."
   
    _ERROR_VMWARE_AUTH_RESPONSE = "Unable to fetch token. Please check [vmware_vrops_host, vmware_vrops_username, vmware_vrops_password] in config.json/vmware credentials." + _ERROR_TASK_ABORT
    _ERROR_AZURE_AUTH_RESPONSE=   "Unable to fetch token. Please check [azure_client_id, azure_secret_id, azure_tenant_id] in azure credentials." + _ERROR_TASK_ABORT
    _ERROR_THUNDER_AUTH_RESPONSE= "Unable to fetch token. Please check [username, password] in thunder credentials."  + _ERROR_TASK_ABORT
    
    _ERROR_THUNDER_MANG_IP_NOT_FOUND    = "Unable to fetch 'datetime' from thunder."                                + _ERROR_TASK_ABORT
    _ERROR_THUNDER_CLOCK_NOT_FOUND      = "Unable to fetch 'datetime' from thunder."                                + _ERROR_TASK_ABORT
    _ERROR_THUNDER_LOGOFF_RESPONSE      = "Unable to call 'logout' from thunder."                                  + _ERROR_TASK_ABORT
    
    _ERROR_METRIC_CPS_NOT_FOUND         = "Unable to fetch 'Total New Connection (Per Sec)' metric from thunder."   + _ERROR_TASK_ABORT
    _ERROR_METRIC_CPU_NOT_FOUND         = "Unable to fetch 'CPU Usage Percentage (Data)' metric from thunder."      + _ERROR_TASK_ABORT
    _ERROR_METRIC_MEMORY_NOT_FOUND      = "Unable to fetch 'Memory Usage Percentage' metric from thunder."          + _ERROR_TASK_ABORT
    _ERROR_METRIC_DISK_NOT_FOUND        = "Unable to fetch 'Disk Usage Percentage' metric from thunder. "           + _ERROR_TASK_ABORT
    _ERROR_METRIC_THROUGHPUT_NOT_FOUND  = "Unable to fetch 'Throughput Rate (Global/BPS)' metric from thunder."     + _ERROR_TASK_ABORT
    _ERROR_METRIC_INTERFACES_NOT_FOUND  = "Unable to fetch 'Interface Down Count (Data)' metric from thunder."      + _ERROR_TASK_ABORT
    _ERROR_METRIC_TPS_NOT_FOUND         = "Unable to fetch 'Transactions Rate (Sec)' metric from thunder."          + _ERROR_TASK_ABORT
    _ERROR_METRIC_SERVER_DOWN_NOT_FOUND = "Unable to fetch 'Server Down Count' metric from thunder."                + _ERROR_TASK_ABORT
    _ERROR_METRIC_SERVER_PER_NOT_FOUND  = "Unable to fetch 'Server Down Percentage' metric from thunder."           + _ERROR_TASK_ABORT
    _ERROR_METRIC_SSL_NOT_FOUND         = "Unable to fetch 'SSL Errors Count' metric from thunder."                 + _ERROR_TASK_ABORT
    _ERROR_METRIC_SERVER_ERROR_NOT_FOUND= "UnaRble to fetch 'Server Errors Count' metric from thunder."              + _ERROR_TASK_ABORT
    _ERROR_METRIC_SESSION_NOT_FOUND     = "Unable to fetch 'Total Session Count' metric from thunder."              + _ERROR_TASK_ABORT
    _ERROR_METRIC_PACKET_RATE_NOT_FOUND = "Unable to fetch 'Packet Rate (Sec)' metric from thunder."                + _ERROR_TASK_ABORT
    _ERROR_METRIC_PACKET_DROP_NOT_FOUND = "Unable to fetch 'Packet Drop Rate (Sec)' metric from thunder."           + _ERROR_TASK_ABORT
    
    _ERROR_PARTITION_NOT_FOUND = "Unable to fetch partition details from thunder."           + _ERROR_TASK_ABORT 
    _ERROR_PARTITION = "Unable to activate partition into thunder."           + _ERROR_TASK_ABORT 
    
    
    
    _ERROR_VMWARE_VROPS_METRIC              = "Unable to publish metric into vmware vrops."                   + _ERROR_TASK_ABORT
    _ERROR_VMWARE_VRLI_LOGS                 = "Unable to publish logs into vmware vrli."                            + _ERROR_TASK_ABORT
    _ERROR_AZURE_LOGS                       = "Unable to publish logs into azure log workspace."                    + _ERROR_TASK_ABORT
    _ERROR_AZURE_METRICS                    = "Unable to publish metric into azure insight/vm."               + _ERROR_TASK_ABORT
    _ERROR_AZURE_AUTOSCALE_THUNDERS         = "Unable to fetch thunder instances from azure autoscale [resource_id: {}]."
    
    _ERROR_NO_VALID_PROVIDER_FOUND          ="WARNING       : No provider is enabled for [metric: {}, log: {}]. To enable [provider: {} set to [1]] in config.json."
    _ERROR_NO_VALID_PROVIDER_CONFIG_FOUND   ="WARNING       : No log or metric is enabled. To enable [metric, log set to [1]] in config.json."
    _ERROR_NO_VALID_METRIC_FOUND            ="WARNING       : No metric enabled. To enable [cpu, memory, ...etc seto to [1]] in config.json."
    
    _ERROR_INVALID_THUNDER_AUTO             ="WARNING       : No thunder found for autoscale provider: {}, please check [autoscale[0/1], provider[aws/azure], username, password and resource_id] in thunder credentials. Thunder collection in autoscale mode task abort."
    _ERROR_INVALID_THUNDER_PARAMETERS       ="WARNING       : No thunder found, please check [ip, username, password and resource_id] in thunder credentials. Thunder collection task abort."
    
    _WARN_MULTIPLE_LOG_FOUND                ="WARNING       : Multiple log enabled,  please check [aws_log, azure_log, vmware_log] only one can be allowed."
    _WARN_MULTIPLE_METRIC_FOUND             ="WARNING       : Multiple metric enabled,  please check [aws_metric, azure_metric, vmware_metric] only one can be allowed."
    
    
    _WARN_ACTIVE_PARTITION_NOT_FOUND        ="WARNING       : No active partitions found for thunder [{}], setting to default 'SHARED'. Multiple L3V partition can be configured as comma separated for example if we have partition 'P1' and 'P2' then we can define as ['partition' : ' Shared,P1,P2'] upto "+str(_PARTITION_LIMIT)+" partitions."
    _WARN_PARTITION_NOT_FOUND               ="WARNING       : Provided partition [{}] not found in thunder."+_ERROR_TASK_ABORT
    _WARN_STANDBY_PARTITION                 ="WARNING       : Provided partition [{}] is in standby mode."+_ERROR_TASK_ABORT
    
   
    _AZURE_PROVIDER="azure_provider"
    _AZURE_METRIC="azure_metric"
    _AZURE_LOG="azure_log"
    
    _AUTOSCALE="autoscale"
    _PROVIDER="provider"
    _AZURE="azure"
    _AWS="aws"
    _VMWARE="vmware"
    
    _VMWARE_PROVIDER="vmware_provider"
    _VMWARE_METRIC="vmware_metric"
    _VMWARE_LOG="vmware_log"
    
    
    _AWS_PROVIDER="aws_provider"
    _AWS_METRIC="aws_metric"
    _AWS_LOG="aws_log"
    
    _AZURE_CPU="azure_cpu"
    _AZURE_MEMORY="azure_memory"
    _AZURE_DISK="azure_disk"
    _AZURE_THROUGHPUT="azure_throughput"
    _AZURE_INTERFACES="azure_interfaces"
    _AZURE_CPS="azure_cps"
    _AZURE_TPS="azure_tps"
    _AZURE_SERVER_DOWN_COUNT="azure_server_down_count"
    _AZURE_SERVER_DOWN_PERCENTAGE="azure_server_down_percentage"
    _AZURE_SSL_CERT="azure_ssl_cert"
    _AZURE_SERVER_ERROR="azure_server_error"
    _AZURE_SESSION="azure_sessions"
    _AZURE_PACKET_RATE="azure_packet_rate"
    _AZURE_PACKET_DROP="azure_packet_drop"
    
    _AWS_CPU="aws_cpu"
    _AWS_MEMORY="aws_memory"
    _AWS_DISK="aws_disk"
    _AWS_THROUGHPUT="aws_throughput"
    _AWS_INTERFACES="aws_interfaces"
    _AWS_CPS="aws_cps"
    _AWS_TPS="aws_tps"
    _AWS_SERVER_DOWN_COUNT="aws_server_down_count"
    _AWS_SERVER_DOWN_PERCENTAGE="aws_server_down_percentage"
    _AWS_SSL_CERT="aws_ssl_cert"
    _AWS_SERVER_ERROR="aws_server_error"
    _AWS_SESSION="aws_sessions"
    _AWS_PACKET_RATE="aws_packet_rate"
    _AWS_PACKET_DROP="aws_packet_drop"
    
    _AWS_BOTO3_SERVICE_LOGS="logs"
    _AWS_BOTO3_SERVICE_CLOUDWATCH="cloudwatch"
    _AWS_BOTO3_SERVICE_AUTOSCALING="autoscaling"
    _AWS_BOTO3_SERVICE_EC2="ec2"
    
    _VMWARE_CPU="vmware_cpu"
    _VMWARE_MEMORY="vmware_memory"
    _VMWARE_DISK="vmware_disk"
    _VMWARE_THROUGHPUT="vmware_throughput"
    _VMWARE_INTERFACES="vmware_interfaces"
    _VMWARE_CPS="vmware_cps"
    _VMWARE_TPS="vmware_tps"
    _VMWARE_SERVER_DOWN_COUNT="vmware_server_down_count"
    _VMWARE_SERVER_DOWN_PERCENTAGE="vmware_server_down_percentage"
    _VMWARE_SSL_CERT="vmware_ssl_cert"
    _VMWARE_SERVER_ERROR="vmware_server_error"
    _VMWARE_SESSION="vmware_sessions"
    _VMWARE_PACKET_RATE="vmware_packet_rate"
    _VMWARE_PACKET_DROP="vmware_packet_drop"
    
    _TEMP_LAST_PACKET_SENT_TIME = "last_packet_sent_time"
    _TEMP_LAST_PACKET_COUNT = "last_packet_count"
    
    _TEMP_LAST_PACKET_DROPPED_SENT_TIME = "last_packet_dropped_sent_time"
    _TEMP_LAST_PACKET_DROPPED_COUNT = "last_packet_dropped_count"
    
    
    
    _THUNDER_BASE_URL="https://{}/axapi/v3"
    _VMWARE_BASE_URL="https://{}/suite-api/api"
    _VMWARE_VRLI_URL="https://{}/api/v2/events/ingest/{}"
    #TODO
      
    _AZURE_METRICS_URL = "https://{}.monitoring.azure.com{}/metrics"
    _AZURE_OAUTH2_URL = "https://login.microsoftonline.com/{}/oauth2/token"
    _AZURE_LOGS_URL = "https://{}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
    _AZURE_VIRTUALMACHINES_URL="https://management.azure.com{}/virtualMachines?api-version=2022-11-01"
    _AZURE_BASE_URL="https://management.azure.com/{}?api-version=2022-03-01"
    _AZURE_MONITORING_RESOURCE="https://monitoring.azure.com/"
    _AZURE_MANAGEMENT_RESOURCE="https://management.azure.com/"
  
    
    _CONTENT_TYPE="Content-Type"
    _ACCEPT="Accept"
    _APPLICATION_JSON="application/json"
    _APPLICATION_URLENCODED="application/x-www-form-urlencoded"
    
    _POST="POST"
    _GET="GET"
    _SUCCESS="success"

    _INFO_JOB_ID                         = "Job No           : {}."
    _INFO_JOB_START                      = "Job Start Time   : {}."
    _INFO_JOB_TIME                       = "Job Execution    : {} seconds."
    _INFO_JOB_END                        = "Job End Time     : {}"
    _INFO_ACTIVE_THUNDERS_COUNT          = "No of Thunders   : {} {}."
    _INFO_ACTIVE_PARTITIONS_COUNT        = "No of Partitions : {} [Count: {}] [{}]."
    _INFO_ACTIVE_PROVIDER_LOG            = "Log Provider     : {}."
    _INFO_ACTIVE_PROVIDER_METRIC         = "Metric Provider  : {}."
    _INFO_ACTIVE_LOG_PROVIDER_FOUND      = "Log              : {}."
    _INFO_ACTIVE_METRIC_PROVIDER_FOUND   = "Metric           : {}."
    _SUCCESS_METRIC                      = "Published Metric : {} {} [Count: {}] [{}]."
    _SUCCESS_LOG                         = "Published Log    : {} {} [Count: {}]."
    _SKIP_LOG                            = "Published Log    : {} {} [No Data Found]."
    _SKIP_METRIC                         = "Published Metric : {} {} [No Data Found]."
    _DOCS                                = "Documentation    : www.a10networks.com or https://github.com/a10networks/thunder-observability-agent."
    
    
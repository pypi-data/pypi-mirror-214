#!/usr/bin/python
# Copyright 2023, A10 Networks Inc. All Rights Reserved.
# THUNDER OBSERVABILITY AGENT END USER SOFTWARE LICENSE AGREEMENT
"""
Processing engine to process metrics information from thunder to configured provider.
To use, simply 'import Metric' and use it!
"""
__author__ = 'Dinesh Kumar Lohia (DLohia@a10networks.com)'

from common.toa_constant import Constant
from common.toa_utils import Utils
from collections import ChainMap
import concurrent.futures
from common.toa_logging import Logging
from handler.thunder_handler import ThunderHandler
from handler.aws_handler import AWSHandler
from handler.vmware_handler import VMWareHandler
from handler.azure_handler import AzureHandler
from concurrent.futures import ThreadPoolExecutor

class MetricProcessor:
    
    _logger = Logging().get_logger("MetricProcessor")
    _metric=None
    _type=None
      
    def __init__(self, metric, partition):
        self._metric=metric
        self._type=partition
    
    def process(self, thunder):
        if(Utils.is_valid(Utils._active_metric_provider) and Utils.is_valid(self._metric) and len(self._metric) >0):
            _thunder = dict(thunder._thunder)
            if Utils._active_metric_provider==Constant._AWS_METRIC:
                self.process_aws_metric(_thunder, thunder)
            elif Utils._active_metric_provider==Constant._AZURE_METRIC:
                self.process_azure_metric(_thunder, thunder)
            elif Utils._active_metric_provider==Constant._VMWARE_METRIC:
                self.process_vmware_metric(_thunder, thunder)
    
    def process_aws_metric(self, _thunder, thunder):
        _metrics = self.collect_metric(_thunder, thunder, None)
        if(Utils.is_valid(_metrics)):
            AWSHandler(_thunder, Constant._AWS_BOTO3_SERVICE_CLOUDWATCH).publish_metric(_metrics)
       
    def process_vmware_metric(self, _thunder, thunder): 
        _metrics = self.collect_metric(_thunder, thunder, None)
        if(Utils.is_valid(_metrics)):
            handler = VMWareHandler(_thunder, None)
            handler.token()
            handler.publish_metric(_metrics)
       
    def process_azure_metric(self, _thunder, thunder): 
        handler = AzureHandler(_thunder, None)
        handler.token(Constant._AZURE_MONITORING_RESOURCE)
        handler.log(self.collect_metric(_thunder, thunder, handler.publish_metric))
        
    def collect_metric(self, _thunder,  thunder, callback):
        metric_data = []
        thunders = [ThunderHandler(metric=metric, date=None, thunder=_thunder, token=thunder._token, callback=callback) for metric in self._metric]
        with ThreadPoolExecutor(max_workers=int(Utils._main.get(Constant._THREADPOOL_MAX_WORKERS))) as collect:
            futures = [collect.submit(thunder.collect_metric) for thunder in thunders]
            for future in concurrent.futures.as_completed(futures):
                if future.result() is not None:
                    metric_data.append(future.result())
            return dict(ChainMap(*metric_data))
     
    
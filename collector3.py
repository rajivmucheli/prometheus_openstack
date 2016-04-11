#!/usr/bin/env python

import time
from novaclient import client as nova_client
from prometheus_client import Metric, CollectorRegistry, generate_latest, Gauge, start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY


class CustomCollector(object):
    """
    hypervisor metrics
        current_workload
        running_vms
         state = 1
         status = 1

         memory_mb
         memory_mb_used
         free_ram_mb

         vcpus
         vcpus_used

         local_gb
         local_gb_used
         free_disk_gb
    """
    def collect(self):
        username = 'admin'
        password = '90224bdeb6394f65'
        tenant = 'admin'
        auth_url = 'http://192.168.123.140:5000/v2.0'

        nova = nova_client.Client("2", username, password, tenant, auth_url)
        print nova

        g = GaugeMetricFamily('current_workload', 'Current hypervisor workload', value=None, labels=['host'])

        hyp_metrics = nova.hypervisors.list()
        for i in hyp_metrics:
            # print i.local_gb_used
            g.add_metric([i.hypervisor_hostname], i.current_workload)
            g.add_metric([i.hypervisor_hostname], i.running_vms)
        yield g


REGISTRY.register(CustomCollector())
start_http_server(8000)
while True:
    generate_latest(REGISTRY)
    time.sleep(30)
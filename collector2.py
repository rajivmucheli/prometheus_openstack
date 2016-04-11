#!/usr/bin/env python

import time
from novaclient import client as nova_client
from prometheus_client import Metric, CollectorRegistry, generate_latest, Gauge, start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY


class CustomCollector(object):
    def collect(self):
        username = 'admin'
        password = '90224bdeb6394f65'
        tenant = 'admin'
        auth_url = 'http://192.168.123.140:5000/v2.0'

        nova = nova_client.Client("2", username, password, tenant, auth_url)
        print nova


        yield GaugeMetricFamily('my_gauge', 'Help text', value=7)
        c = CounterMetricFamily('my_counter_total', 'Help text', labels=['foo'])

        hyp_metrics = nova.hypervisors.list()
        for i in hyp_metrics:
            # print i.local_gb_used
            c.add_metric(['workload'], i.current_workload)
            c.add_metric(['running_vms'], i.running_vms)
        yield c


REGISTRY.register(CustomCollector())
start_http_server(8000)
while True:
  generate_latest(REGISTRY)
  time.sleep(10)

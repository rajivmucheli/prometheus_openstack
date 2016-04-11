#!/usr/bin/env python


""" example
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())

"""
import time
from novaclient import client as nova_client
from prometheus_client import Gauge, start_http_server


g = Gauge('my_inprogress_requsests', 'Description of gauge')


class OpenStackCollector(object):

    def __init__(self, **kwargs):
        """
        OpenStack metrics collector
        :rtype: object
        """
        self.username = kwargs.pop('username', 'admin')
        self.password = kwargs.pop('password', 'admin')
        self.tenant = kwargs.pop('tenant', 'admin')
        self.auth_url = kwargs.pop('auth_url', 'http://127.0.0.1:5000/v2.0')
        self.nova = nova_client.Client("2", self.username, self.password, self.tenant, self.auth_url)

    def set_gauge(self, g_name, g_value):
        _gauge = Gauge(g_name, 'name is %s' % g_name)
        setattr(self, g_name, _gauge)
        _gauge.set(g_value)

    def get_hypervisor_stats(self):
        """
        Collect hypervisor statistics
        """
        hyp_metrics = self.nova.hypervisors.list()
        for i in hyp_metrics:
            # print i.local_gb_used
            self.set_gauge("workload", i.current_workload)
            self.set_gauge("running_vms", i.running_vms)

            """
            hypervisor_hostname


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

        time.sleep(15)


if __name__ == '__main__':
    start_http_server(8000)
    while True:
        metrics = OpenStackCollector(username='admin',
                                     password='90224bdeb6394f65',
                                     tenant='admin',
                                     auth_url='http://192.168.123.140:5000/v2.0')
        metrics.get_hypervisor_stats()


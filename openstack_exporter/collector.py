#!/usr/bin/env python

from novaclient import client as nova_client
from prometheus_client.core import GaugeMetricFamily


class NovaCollector(object):
    """ Collects Nova metrics """

    def __init__(self, config):
        self.config = config

    def collect(self):
        username = self.config['openstack']['username']
        password = '90224bdeb6394f65'
        tenant = 'admin'
        auth_url = 'http://192.168.123.140:5000/v2.0'
        nova = nova_client.Client("2", username, password, tenant, auth_url)

        METRIC_PREFIX = 'openstack_nova'
        LABELS = ['hypervisor']

        metrics = ['current_workload', 'running_vms', 'vcpus', 'vcpus_used', 'memory_mb', 'memory_mb_used',
                   'free_ram_mb', 'local_gb', 'local_gb_used', 'free_disk_gb']
        gauges = {}

        for metric in metrics:
            gauges[metric] = GaugeMetricFamily('%s_%s' % (METRIC_PREFIX, metric),
                                               '%s' % metric,
                                               value=None,
                                               labels=LABELS)

        hypervisors = nova.hypervisors.list()

        for h in hypervisors:
            for metric in metrics:
                gauges[metric].add_metric([h.hypervisor_hostname], getattr(h, metric))

        for metric in metrics:
            yield gauges[metric]



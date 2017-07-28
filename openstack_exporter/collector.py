#!/usr/bin/env python
""" OpenStack metrics exporter for prometheus.io"""

from novaclient import client as nova_client
from keystoneclient.v3 import client as keystone_client
from prometheus_client.core import GaugeMetricFamily


class NovaCollector(object):
    """ Collects Nova metrics """

    def __init__(self, config):
        self.config = config

    def collect(self):
        username = self.config['openstack']['username']
        password = self.config['openstack']['password']
        tenant = self.config['openstack']['tenant']
        auth_url = self.config['openstack']['auth_url']

        nova = nova_client.Client("3", username, password, tenant, auth_url)

        keystone = keystone_client.Client(
                   username = username,
                   password = password,
                   tenant_name = tenant,
                   auth_url = auth_url)


        METRIC_PREFIX = 'openstack_nova'

        TENANT_METRICS = ['maxTotalInstances', 'totalInstancesUsed',
                          'maxTotalRAMSize', 'totalRAMUsed',
                          'maxTotalCores', 'totalCoresUsed',
                          'maxTotalFloatingIps', 'totalFloatingIpsUsed',
                          'maxSecurityGroups', 'totalSecurityGroupsUsed',
                          'maxServerGroups', 'totalServerGroupsUsed']

        HYPERVISOR_METRICS = ['current_workload', 'running_vms', 'vcpus', 'vcpus_used',
                              'memory_mb', 'memory_mb_used', 'free_ram_mb', 'local_gb',
                              'local_gb_used', 'free_disk_gb']
        gauges = {}

        for metric in HYPERVISOR_METRICS:
            gauges[metric] = GaugeMetricFamily('%s_%s' % (METRIC_PREFIX, metric),
                                               '%s' % metric,
                                               value=None,
                                               labels=['hypervisor'])

        for metric in TENANT_METRICS:
            gauges[metric] = GaugeMetricFamily('%s_%s' % (METRIC_PREFIX, metric),
                                               '%s' % metric,
                                               value=None,
                                               labels=['tenant'])

        hypervisors = nova.hypervisors.list()
        tenants = keystone.tenants.list()

        for tenant in tenants:
            limits = nova.limits.get(tenant.name)._info['absolute']
            for metric in TENANT_METRICS:
                gauges[metric].add_metric([tenant.name], limits[metric])

        for hypervisor in hypervisors:
            for metric in HYPERVISOR_METRICS:
                gauges[metric].add_metric([hypervisor.hypervisor_hostname],
                                          getattr(hypervisor, metric))


        for metric in (TENANT_METRICS + HYPERVISOR_METRICS):
            yield gauges[metric]


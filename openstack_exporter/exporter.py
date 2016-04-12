#!/usr/bin/env python

import time
import yaml
from collector import NovaCollector
from prometheus_client.core import REGISTRY
from prometheus_client import generate_latest, start_http_server

with open('openstack_exporter.yaml', 'r') as f:
    config = yaml.load(f)


REGISTRY.register(NovaCollector(config))
start_http_server(8000)
while True:
    generate_latest(REGISTRY)
    time.sleep(30)
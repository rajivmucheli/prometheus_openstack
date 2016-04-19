#!/usr/bin/env python
""" HTTP server for metrics """

import time
from collector import NovaCollector
from prometheus_client.core import REGISTRY
from prometheus_client import generate_latest, start_http_server


def start_exporter(config, port, interval):
    """ run the exporter every <interval> seconds """
    REGISTRY.register(NovaCollector(config))
    start_http_server(port)
    while True:
        generate_latest(REGISTRY)
        time.sleep(30)

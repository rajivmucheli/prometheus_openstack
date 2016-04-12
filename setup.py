import os
from setuptools import setup

setup(
    name = "openstack_exporter",
    version = "0.0.1",
    author = "George Vauter",
    author_email = "george.vauter@inin.com  ",
    description = ("OpenStack exporter for the Prometheus monitoring system."),
    long_description = ("See https://github.com/... for documentation."),
    license = "Apache Software License 2.0",
    keywords = "prometheus exporter monitoring openstack metrics",
    url = "https://github.com/gvauter/prometheus_openstack",
    scripts = ["scripts/openstack_exporter"],
    packages=['openstack_exporter'],
    test_suite="tests",
    install_requires=["prometheus_client>=0.0.11", "pyyaml", "python-novaclient"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: Apache Software License",
    ],
)

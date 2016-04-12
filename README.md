# prometheus_openstack
Prometheus exporter for OpenStack

See https://prometheus.io 

## Install
pip install git+github.com/gvauter/prometheus_openstack

## Usage

`openstack_exporter --config <file> --port <port> --interval <seconds>`


#### Sample config file
```yaml
openstack:
    username: <usename>
    password: <password>
    tenant: <tenant name>
    auth_url: <http://<ip>:5000/v2.0
```

## Metrics

Currently only collecting hypervisor metrics from the Nova API 



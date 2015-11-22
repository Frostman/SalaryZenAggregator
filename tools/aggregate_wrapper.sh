#!/usr/bin/env bash

flock -n /var/run/salaryzen/aggregator.lock timeout -k 2m 3m /opt/SalaryZenAggregator/tools/aggregate.sh -o /etc/public_files/salaryzen/data.json 2>&1 | tee -a  /var/log/salaryzen/aggregate.log

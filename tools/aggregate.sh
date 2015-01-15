#!/usr/bin/env bash

cd /opt/SalaryZenAggregator
git reset --hard HEAD
git pull origin
virtualenv venv
. venv/bin/activate
pip install -U .
salaryzen-aggregate "$@"
deactivate

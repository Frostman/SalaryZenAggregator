# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from datetime import datetime
import time

from stevedore import extension

from salaryzenaggr.formatters import json_formatter


_fetchers = extension.ExtensionManager(namespace='salaryzenaggr.fetchers', invoke_on_load=True)


def _get_fetchers(banks, currencies):
    for ext in _fetchers.extensions:
        fetcher = ext.obj
        if (any([bank in fetcher.get_supported_banks() for bank in banks]) and
                any([curr in fetcher.get_supported_currencies() for curr in currencies])):
            yield fetcher


def aggregate_rates(banks, currencies, from_date, result_file, debug):
    res = {}

    for fetcher in _get_fetchers(banks, currencies):
        fetcher.fetch_data(res, currencies, from_date)

    formatter = json_formatter.JsonPrettyFormatter if debug else json_formatter.JsonFormatter
    res['aggregated_at'] = int(time.time())
    output = formatter().format_data(res)

    if debug:
        print output

    print "New data aggregated at %s UTC" % datetime.utcnow()

    if result_file:
        result_file.write(output)
        result_file.close()
        print "Data successfully written to %s" % result_file
    else:
        print output

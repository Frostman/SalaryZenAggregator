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

from salaryzenaggr.constants import *  # noqa
from salaryzenaggr.utils.abstracts import *  # noqa


def write_data_set(result, bank, currency, data_type, exchange_type, value, date=None):
    value = _cleanup_val(value)
    date = _cleanup_val(date)

    key = '%s_%s_%s_%s' % (bank, currency, data_type, exchange_type)
    if data_type == DATA_TYPE_CURRENT:
        result[key] = value
    elif data_type == DATA_TYPE_HISTORIC:
        if key not in result:
            result[key] = dict()
        result[key][date] = value


def _cleanup_val(val):
    if val is None:
        return None

    # only format datetime to string
    if isinstance(val, datetime):
        return val.strftime('%d.%m.%Y')

    val = val.replace(',', '.')

    # convert val to float if possible
    try:
        val = float(val)
    except ValueError:
        pass

    # ensure that we have <= 4 digits precision
    if isinstance(val, float):
        val = float('{:.4f}'.format(val))

    return val


@abstractclass()
class Fetcher(object):
    @required
    def fetch_data(self, data, datasets=None):
        raise NotImplemented()

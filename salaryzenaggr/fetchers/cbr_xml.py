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
from datetime import timedelta
import functools

from salaryzenaggr.constants import *  # noqa
from salaryzenaggr import fetchers
from salaryzenaggr.fetchers import rest_api

_cbr_currencies = {
    CURRENCY_USD: "R01235",
    CURRENCY_EURO: "R01239"
}


def _parse_date(value):
    return datetime.strptime(value, '%d.%m.%Y')


def _format_date(value):
    return value.strftime('%d.%m.%Y')


def _tomorrow():
    return _format_date(datetime.utcnow() + timedelta(days=1))


def _xml_get_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


class CbrXmlFetcher(rest_api.XmlRestApiFetcher):
    def fetch_data(self, data, datasets=None):
        for dataset in datasets:
            if dataset[0] != BANK_CBR:
                continue
            if dataset[1] not in _cbr_currencies:
                continue
            if dataset[2] != DATA_TYPE_HISTORIC:
                continue
            if len(dataset) < 4:
                continue
            from_date = dataset[3]
            to_date = dataset[4] if len(dataset) == 5 else _tomorrow()
            currency = dataset[1]

            write_data = functools.partial(fetchers.write_data_set,
                                           result=data,
                                           bank=BANK_CBR,
                                           currency=currency,
                                           data_type=DATA_TYPE_HISTORIC,
                                           exchange_type=EXCHANGE_RATE)

            cbr_url = 'http://www.cbr.ru/scripts/XML_dynamic.asp'
            response = self._fetch_url(cbr_url, params=dict(
                date_req1=from_date,
                date_req2=to_date,
                VAL_NM_RQ=_cbr_currencies[currency]
            ))

            for record in response.getElementsByTagName("Record"):
                date = _parse_date(record.getAttribute("Date"))
                value = _xml_get_text(record.getElementsByTagName("Value")[0].childNodes)
                write_data(value=value, date=date)

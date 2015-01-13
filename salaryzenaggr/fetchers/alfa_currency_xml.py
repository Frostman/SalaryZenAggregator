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


import functools

from salaryzenaggr.constants import *  # noqa
from salaryzenaggr import fetchers
from salaryzenaggr.fetchers import rest_api


def _get_currency_name(currency_id):
    currency_ids = {
        '840': CURRENCY_USD,
        '978': CURRENCY_EURO,
    }
    return currency_ids[currency_id] if currency_id in currency_ids else None


class AlfaBankCurrencyXmlFetcher(rest_api.XmlRestApiFetcher):
    def fetch_data(self, data, datasets=None):
        alfa_bank_url = 'http://alfabank.ru/_/_currency.xml'
        response = self._fetch_url(alfa_bank_url)

        date_type = DATA_TYPE_CURRENT

        for rate_tag in response.getElementsByTagName('rates'):
            rate_type = rate_tag.getAttribute('type')

            items = rate_tag.getElementsByTagName('item')

            if rate_type not in ['non-cash', 'cb']:
                continue

            for item in items:
                currency = _get_currency_name(item.getAttribute('currency-id'))
                if currency:
                    bank = BANK_CBR if rate_type == 'cb' else BANK_ALFA

                    if (bank, currency, date_type) not in datasets:
                        continue

                    write_data = functools.partial(fetchers.write_data_set,
                                                   result=data,
                                                   bank=bank,
                                                   currency=currency,
                                                   data_type=date_type)

                    if item.getAttribute('value'):
                        write_data(exchange_type=EXCHANGE_RATE, value=item.getAttribute('value'))
                    else:
                        write_data(exchange_type=EXCHANGE_SELL, value=item.getAttribute('value-selling'))
                        write_data(exchange_type=EXCHANGE_BUY, value=item.getAttribute('value-buying'))

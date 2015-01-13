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


CURRENCIES = (
    CURRENCY_USD, CURRENCY_EURO
) = (
    'usd', 'euro'
)

DEFAULT_CURRENCY = CURRENCIES[0]


DATA_TYPES = (
    DATA_TYPE_HISTORIC, DATA_TYPE_CURRENT
) = (
    'historic', 'current'
)

DEFAULT_DATA_TYPE = DATA_TYPES[0]


BANKS = (
    BANK_CBR, BANK_ALFA
) = (
    'cbr', 'alfa'
)

DEFAULT_BANK = BANKS[0]


EXCHANGE_TYPES = (
    EXCHANGE_SELL, EXCHANGE_BUY, EXCHANGE_RATE
) = (
    'sell', 'buy', 'rate'
)

DEFAULT_EXCHANGE = EXCHANGE_TYPES[0]

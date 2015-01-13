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


from salaryzenaggr.constants import *  # noqa
from salaryzenaggr.fetchers import alfa_currency_xml
from salaryzenaggr.fetchers import cbr_xml
from salaryzenaggr.formatters import json_formatter


def main():
    print "Aggregate!"

    a = alfa_currency_xml.AlfaBankCurrencyXmlFetcher()
    res = {}
    a.fetch_data(res, datasets=(
        (BANK_CBR, CURRENCY_USD, DATA_TYPE_CURRENT),
        (BANK_CBR, CURRENCY_EURO, DATA_TYPE_CURRENT),
        (BANK_ALFA, CURRENCY_USD, DATA_TYPE_CURRENT),
        (BANK_ALFA, CURRENCY_EURO, DATA_TYPE_CURRENT),
    ))
    b = cbr_xml.CbrXmlFetcher()
    b.fetch_data(res, datasets=(
        (BANK_CBR, CURRENCY_USD, DATA_TYPE_HISTORIC, "30.08.2014"),
        (BANK_CBR, CURRENCY_EURO, DATA_TYPE_HISTORIC, "30.08.2014"),
    ))

    print json_formatter.JsonPrettyFormatter().format_data(res)


if __name__ == "__main__":
    main()

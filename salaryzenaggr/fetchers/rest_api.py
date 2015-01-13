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


from xml.dom import minidom as xml

import requests

from salaryzenaggr import fetchers


def _verify_response(response):
        if not response or response.status_code != 200:
            print("Failed to access %s with status_code %s" % (response.url, response.status_code))
            exit(-1)


class RestApiFetcher(fetchers.Fetcher):

    def _fetch_url(self, url, params=None):
        response = requests.get(url, params=params)
        _verify_response(response)
        return response


class XmlRestApiFetcher(RestApiFetcher):
    def _fetch_url(self, url, params=None):
        response = super(XmlRestApiFetcher, self)._fetch_url(url, params=params)
        return xml.parseString(response.text)


class JsonRestApiFetcher(RestApiFetcher):
    def _fetch_url(self, url, params=None):
        response = super(JsonRestApiFetcher, self)._fetch_url(url, params=params)
        return json_formatter.loads(response.text)

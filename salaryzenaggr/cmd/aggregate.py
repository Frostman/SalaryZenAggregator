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


import argparse
import os

from salaryzenaggr import manager


def parse_args():
    def is_valid_file(parser, arg):
        if not os.access(arg, os.W_OK):
            parser.error("No write permissions for '%s'!" % arg)
        else:
            return open(arg, 'w')  # return an open file handle

    parser = argparse.ArgumentParser(description='Currency rates aggregator.')
    parser.add_argument("-o", "--output", dest="result_file", required=False,
                        help="Output file for aggregated rates", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-b", "--banks", dest="banks", required=False, default=["alfa", "cbr"],
                        help="List of the banks short names (alfa, cbr) to aggregate rates",
                        nargs="+")
    parser.add_argument("-c", "--currencies", dest="currencies", required=False, default=["usd"],
                        help="List of currencies (usd, euro) to aggregate rates",
                        nargs="+")
    parser.add_argument("-f", "--from-date", dest="from_date", required=False, default="30.08.2014",
                        help="Start aggregation of historic data from this date")
    parser.add_argument("-d", "--debug", dest="debug", required=False, default=False,
                        action="store_true",
                        help="Enable debug mode to print json to output too")
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    manager.aggregate_rates(**vars(args))


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# This file is part of tcollector.
# Copyright (C) 2010  The tcollector Authors.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.

import sys
import time
import os

try:
    import json
except ImportError:
    json = None

from common.lib import utils
from common.lib.hadoop_http import HadoopHttp


EXCLUDED_CONTEXTS = ('regionserver', 'regions', )


class HBaseMaster(HadoopHttp):
    """
    Class to get metrics from Apache HBase's master

    Require HBase 0.96.0+
    """

    def __init__(self):
        super(HBaseMaster, self).__init__('hbase', 'master', 'localhost', 60010)

    def emit(self):
        step = os.path.realpath(__file__).split("/")[-1].split("_", 2)[0]
        current_time = int(time.time())
        metrics = self.poll()
        for context, metric_name, value in metrics:
            if any(c in EXCLUDED_CONTEXTS for c in context):
                continue
            self.emit_metric(context, current_time, metric_name, value, step)


def main(args):
    utils.drop_privileges()
    if json is None:
        utils.err("This collector requires the `json' Python module.")
        return 13  # Ask tcollector not to respawn us
    hbase_service = HBaseMaster()
    hbase_service.emit()



if __name__ == "__main__":
    sys.exit(main(sys.argv))


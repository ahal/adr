"""
Compare subtest performance across all suites for two revisions

.. code-block:: bash

    adr perf_tp6_compare -r <revision1> -r <revision2> [-t <subtest>]

<subtest> defaults to "-loadtime"

"""

from __future__ import absolute_import, print_function

import logging

from ..query import run_query

log = logging.getLogger('adr')


RUN_CONTEXTS = [
    'platform',
    'branches',
]


def run(args, config):

    # PULL DATA FOR REVISIONS

    limit = args.limit
    delattr(args, 'limit')

    data = run_query('perf_tp6_compare', config, args)['data']
    result = []
    for record in data:
        if record[2] is None:
            continue
        record[2] = round(record[2] / 60, 2)
        record.append(int(round(record[1] * record[2], 0)))
        result.append(record)

    result = sorted(result, key=lambda k: k[args.sort_key], reverse=True)[:limit]
    result.insert(0, ['Taskname', 'Num Jobs', 'Average Hours', 'Total Hours'])
    return result



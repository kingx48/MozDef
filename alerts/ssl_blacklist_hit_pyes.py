#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2014 Mozilla Corporation
#
# Contributors:
# Michal Purzynski michal@mozilla.com

from lib.alerttask import AlertTask
from query_models import SearchQuery, TermFilter, ExistsFilter


class AlertSSLBlacklistHit(AlertTask):
    def main(self):
        search_query = SearchQuery(minutes=15)

        search_query.add_must([
            TermFilter('_type', 'bro'),
            TermFilter('eventsource', 'nsm'),
            TermFilter('category', 'brointel'),
            TermFilter('details.sources', 'abuse.ch SSLBL'),
            ExistsFilter('details.sourceipaddress')
        ])

        self.filtersManual(search_query)

        # Search events
        self.searchEventsSimple()
        self.walkEvents()

    # Set alert properties
    def onEvent(self, event):
        category = 'correlatedalerts'
        tags = ['nsm,bro,correlated']
        severity = 'NOTICE'
        hostname = event['_source']['hostname']

        # the summary of the alert is the same as the event
        summary = '{0} {1}'.format(hostname, event['_source']['summary'])

        # Create the alert object based on these properties
        return self.createAlertDict(summary, category, tags, [event], severity)


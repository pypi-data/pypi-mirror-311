import os
import shutil
import datetime
from requests.auth import HTTPBasicAuth
import os
import io
import json
import argparse
import time
import ntpath
import requests
from pathlib import Path
import yaml
from lxml import etree
from lxml.etree import fromstring
import uuid
import datetime
from pypers.steps.base.fetch_step_api import FetchStepAPI
from . import Trademarks

import logging
import logging.handlers 

#get here pypers logging 
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#logging.getLogger("urllib3").setLevel(logging.ERROR)

from . import get_auth_token

class TrademarksFull(Trademarks):
    spec = {
        "version": "2.0",
        "descr": [
            "Fetch full update using REST API"
        ],
    }

    def get_intervals(self):
        """ 
        Return the intervals to be downloaded, in our case one interval is 30 days, so
        we enumerate approx. months from the month of the last update. In addition, as it is a full
        update, the starting date corresponds to the oldest available trademark application.
        """
        # get the date of the last update
        if not len(self.done_archives):
            # no done archives in dynamodb table gbd_pypers_done_archive 
            last_update = datetime.datetime.fromisoformat("1947-01-01")
        else:
            # we get the day of the last update from the last "done_archive" file name stored 
            # in dynamodb table gbd_pypers_done_archive 
            # # expecting names like : 2018-01-01.TO.2018-01-31.1.txt
            last_update = sorted(self.done_archives)[-1].split('.')[2]
            if '_' in last_update:
                last_update = last_update.split('_')[0]
            last_update = datetime.datetime.fromisoformat(last_update)

        today = datetime.datetime.today()

        result = []
        current_date = last_update.strftime("%Y-%m-%d")

        addDays = datetime.timedelta(days=30)
        one_date = last_update
        while one_date <= today:
            one_date = one_date + addDays
            next_date = one_date.strftime("%Y-%m-%d")
            result.append( (current_date, next_date) )
            current_date = next_date

        return result

    template_update = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
        "<ApiRequest xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"urn:ige:schema:xsd:datadeliverycore-1.0.0 urn:publicid:-:IGE:XSD+DATADELIVERYCORE+1.0.0:EN " \
        "urn:ige:schema:xsd:datadeliverycommon-1.0.0 urn:publicid:-:IGE:XSD+DATADELIVERYCOMMON+1.0.0:EN urn:ige:schema:xsd:datadeliverytrademark-1.0.0 urn:publicid:-:IGE:XSD+DATADELIVERYTRADEMARK+1.0.0:EN\" " \
        "xmlns=\"urn:ige:schema:xsd:datadeliverycore-1.0.0\" xmlns:tm=\"urn:ige:schema:xsd:datadeliverytrademark-1.0.0\">" \
        "<Action type=\"TrademarkSearch\">" \
        "<tm:TrademarkSearchRequest xmlns=\"urn:ige:schema:xsd:datadeliverycommon-1.0.0\">" \
            "<Representation details=\"Maximal\" image=\"Embed\"/>" \
            "<Query>" \
            "    <tm:ApplicationDate from=\"{{$start_date}}\" includeFrom=\"true\" to=\"{{$end_date}}\" includeTo=\"false\"></tm:ApplicationDate>" \
            "</Query>" \
            "<Sort>" \
            "    <LastUpdateSort>Ascending</LastUpdateSort>" \
            "</Sort>" \
        "</tm:TrademarkSearchRequest>" \
        "</Action>" \
        "</ApiRequest>"




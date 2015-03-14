#! /usr/bin/env python2.7

# Copyright 2013 Jtmorgan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import operator
import re
from datetime import datetime, timedelta
import time
import dateutil.parser
from dateutil.relativedelta import relativedelta

#import MySQLdb

import output_settings


def addDefaults(member_list):
    """
    Adds pre-specified set of default (null) fields to a dictionary.
    """
    params = output_settings.Params()
    print params
    mem_defaults = dict.fromkeys(params.getParams('profile defaults'), "")
    print(mem_defaults)
    for m in member_list:
        for k,v in mem_defaults.iteritems():
            if k not in m.keys():
                m[k] = v
    return member_list

# test me
def setTimeValues(member_list, val="timestamp"):
    """
    Adds a python date object and a pretty formatted date string
    to each dict in a list of dicts.
    Requires that dict contains a 'timestamp' key with a
    a 12-digit date string (like rev_timestamp from MediaWiki database)
    or an ISO 8601 date string (like MediaWiki API timestamp)
    """
    for m in member_list:
        try:
            m['datetime'] = dateutil.parser.parse(m[val])
            m['time'] = datetime.strftime(m['datetime'], '%d %B %Y')
        except:
            pass
#               print "no timestamp available for " + m['title']
    return member_list

def utcnow():
    """Wrapper function for datetime.datetime.utcnow() to facilitate
    testing."""
    return datetime.utcnow()

# test me
def getSubDate(day_interval):
    """
    Returns the date a specified number of days before the current date
    as an API and database-friendly 14-digit timestamp string.
    """
    today = datetime.utcnow()
    sd_datetime = today - relativedelta(days=day_interval)
    sd_datetime = utcnow().replace(tzinfo=dateutil.tz.tzutc())-timedelta(days=day_interval)
    sd_string = sd_datetime.strftime('%Y%m%d%H%M%S')
    subdate = (sd_datetime, sd_string)
    return subdate


# test me
def titleFromPath(path):
    """
    Get the title of the lowest subpage from a long path.
    Example: "IdeaLab/Ideas/My_great_idea" returns "My great idea".
    """
    title = re.search('([^/]+$)', path).group(1).replace("_", " ")
    return title


# test me
# will api:extracts do this?
def formatSummaries(text): #need to be able to pass in a custom dict here, like in scrapeInfobox above
    """
    Cleans markup from strings of profile summary text.
    """
    text = text.strip()
    text = re.sub("(\[\[)(.*?)(\|)","",text)
    text = re.sub("\]","",text)
    text = re.sub("\[","",text)
    text = text + "..."
#       text = (text[:200] + '...') if len(text) > 200 else text
    return text


# test me
def dedupeMemberList(mem_list, sort_val, dict_val):
    """
    Sort and remove duplicates from a list of dicts
    based on a specified key/value pair.
    """
    mem_list.sort(key=operator.itemgetter(sort_val), reverse=True)
    seen_list = [] #why is this here?
    unique_list = []
    for mem in mem_list:
        t = mem[dict_val]
        if t not in seen_list:
            seen_list.append(t)
            unique_list.append(mem)
        else:
            pass
    return unique_list


# test me
def excludeSubpages(mem_list, path_key, depth=1, skip_list=False):
    """
    Takes a list of dictionaries that contains data about a bunch of wiki-pages,
    including the page path. Removes dicts from the list
    if their page depth ("/") is greater than the defined value.
    """
    depth_constrained_list = []
    for mem in mem_list:
        if (skip_list and mem[path_key] in skip_list):
            depth_constrained_list.append(mem)
        else:
            path_comps = [p for p in mem[path_key].split('/') if p] #rmvs empty strings if path starts or ends in '/'
            if len(path_comps) == depth:
                depth_constrained_list.append(mem)
            else:
                pass

    return depth_constrained_list

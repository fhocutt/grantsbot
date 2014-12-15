#!usr/bin/python2.7
#
# Quick test script.
# Uses raw API calls through mwclient to test the Flow web API.
# Uses prop=flowinfo to see if Flow is enabled.
# Posts a new topic on a Flow board through action=flow&submodule=new-topic.
#
# GPL v3.

import json
import time
import mwclient
import flow_mw_settings as mwcreds

def flowenabled(title, site):
    """Given a string with the page title, return True if Flow is enabled"""
    query = site.api(action = 'query',
                     titles = title,
                     prop = 'flowinfo')
    print(query)
    pagedict = query['query']['pages']
    for page in pagedict:
        if page == '-1':
            return None
        else:
            return (u'enabled' in pagedict[page]['flowinfo']['flow'])

# TODO: put this in place with logic (flow enabled or not), make it return
def postflow(page, topic, message, site):
    """testing posting a new Flow topic through the API"""
    token = site.get_token('csrf')
    cooptitle = 'Wikipedia:Co-op/Mentorship match'
    kwargs = {'action': 'flow',
              'page': cooptitle,
              'submodule': 'new-topic',
              'token': token,
              'nttopic': topic,
              'ntcontent': message}
    query2 = site.api(**kwargs)
    return True

def userid(title, site):
    """ Returns the user who made the first edit to a page.

    Given a string with the page title, returns (user, userid)

    # /w/api.php?action=query&prop=revisions&format=json&rvdir=newer&titles=Wikipedia%3ACo-op%2FPerson2
    """
    query = site.api(action = 'query',
                     prop = 'revisions',
                     rvprop = 'user|userid',
                     rvdir = 'newer',
                     titles = title,
                     rvlimit = 1,
                     indexpageids = "")
    pagedict = query['query']['pages']
    for page in pagedict:
        user = pagedict[page]['revisions'][0]['user']
        userid = pagedict[page]['revisions'][0]['userid']
    return (user, userid)

# TODO: put in the call, make it return appropriately
def newmembers(categoryname, site, timelastchecked='2014-11-05T01%3A12%3A00Z'):
    """ Data for the following API call: """
    #   /w/api.php?action=query&list=categorymembers&format=json&cmtitle=Category%3AWants%20to%20edit&cmprop=ids|title|timestamp&cmlimit=max&cmsort=timestamp&cmdir=older&cmend=2014-11-05T01%3A12%3A00Z&indexpageids=
#    categoryname = 'Wants to learn to edit'
    t = '2014-11-05T01:12:00Z'
    timelastchecked = time.strptime(t, '%Y-%m-%dT%H:%M:%SZ') #DEBUG FIXME don't use this
    recentkwargs = {'action': 'query',
                    'list': 'categorymembers',
                    'cmtitle': categoryname,
                    'cmprop': 'ids|title|timestamp',
                    'cmlimit': 'max',
                    'cmsort': 'timestamp',
                    'cmdir': 'older',
                    'cmend': timelastchecked,
                    'indexpageids': ''}
    result = site.api(**recentkwargs)
    catusers = []
    for page in result['query']['categorymembers']:
        userdict = {'profileid': page['pageid'],
                    'profile': page['title'],
                    'cattime': page['timestamp'],
                    'category': categoryname}
        catusers.append(userdict)
    return catusers

#TODO
def getallmembers(category, site):
    kwargs = {'action': 'query',
              'list': 'categorymembers',
              'cmtitle': category,
              'cmprop': 'ids|title'}
    query = site.api(**kwargs)
    catmembers = []
    for page in query['query']['categorymembers']:
        userdict = {'profileid': page['pageid'], 'profile': page['title']}
        catmembers.append(userdict)
    return catmembers

if __name__ == '__main__':
    # Initializing site + logging in
    site = mwclient.Site(('https', 'test.wikipedia.org'),
                         clients_useragent=mwcreds.useragent)
    site.login(mwcreds.username, mwcreds.password)
    print("You are logged in as %s." % mwcreds.username)

    userid('Wikipedia:Co-op/Person2')
    print(flowenabled('Wikipedia:Co-op/Mentorship match'))

#!usr/bin/python2.7
#
# Quick test script.
# Uses raw API calls through mwclient to test the Flow web API.
# Uses prop=flowinfo to see if Flow is enabled.
# Posts a new topic on a Flow board through action=flow&submodule=new-topic.
#
# GPL v3.


import mwclient
import flow_mw_settings as mwcreds

def flowenabled(title):
    """Given a string with the page title, return True if Flow is enabled"""
    query = site.api(action = 'query',
                     titles = title,
                     prop = 'flowinfo')
    pagedict = query['query']['pages']
    for page in pagedict:
        return (u'enabled' in pagedict[page]['flowinfo']['flow'])

# TODO: put this in place with logic (flow enabled or not), make it return
def postflow():
    """testing posting a new Flow topic through the API"""
    token = site.get_token('csrf')
    cooptitle = 'Wikipedia:Co-op/Mentorship match'
    kwargs2 = {'action': 'flow',
               'page': cooptitle,
               'submodule': 'new-topic',
               'ntcontent': 'MatchBot test',
               'token': token,
               'nttopic': 'MatchBot\'s newer topic',
               'ntcontent': 'This is some more new content.'}
    query2 = site.api(**kwargs2)
    print(query2)

def userid(title):
    """ Returns the user who made the first edit to a page.

    Given a string with the page title, returns (user, userid, timestamp)

    # /w/api.php?action=query&prop=revisions&format=json&rvdir=newer&titles=Wikipedia%3ACo-op%2FPerson2
    """

    query = site.api(action = 'query',
                     prop = 'revisions',
                     rvprop = 'user|userid|timestamp',
                     rvdir = 'newer',
                     titles = title,
                     rvlimit = 1,
                     indexpageids = "")

    pages = query['query']['pages']
    pageid = query['query']['pageids'][0]
    user = pages[pageid]['revisions'][0]['user']
    userid = pages[pageid]['revisions'][0]['userid']
    timestamp = pages[pageid]['revisions'][0]['timestamp']
    return (user, userid, timestamp)

# TODO: put in the call, make it return appropriately
def newmembers(categoryname, timelastchecked):
    """ Data for the following API call: """
    #   /w/api.php?action=query&list=categorymembers&format=json&cmtitle=Category%3AWants%20to%20edit&cmprop=ids|title|timestamp&cmlimit=max&cmsort=timestamp&cmdir=older&cmend=2014-11-05T01%3A12%3A00Z&indexpageids=
#    categoryname = 'Wants to learn to edit'
#    timelastchecked = '2014-11-05T01%3A12%3A00Z'
    recentkwargs = {'action': 'query',
                    'list': 'categorymembers',
                    'cmtitle': categoryname,
                    'cmprop': 'ids|title|timestamp',
                    'cmlimit': 'max',
                    'cmsort': 'timestamp',
                    'cmdir': 'older',
                    'cmend': timelastchecked,
                    'indexpageids': ''}


if __name__ == '__main__':
    # Initializing site + logging in
    site = mwclient.Site(('https', 'test.wikipedia.org'),
                         clients_useragent=mwcreds.useragent)
    site.login(mwcreds.username, mwcreds.password)
    print("You are logged in as %s." % mwcreds.username)

    userid('Wikipedia:Co-op/Person2')
    print(flowenabled('Wikipedia:Co-op/Mentorship match'))

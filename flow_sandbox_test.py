#!usr/bin/python2.7
#
# Quick test script.
# Uses raw API calls through mwclient to test the Flow web API.
# Uses prop=flowinfo to see if Flow is enabled.
# Posts a new topic on a Flow board through action=flow&submodule=new-topic.
#
# GPL v3.


import mwclient
import pp
import flow_mw_settings as mwcreds

if __name__ == '__main__':
    # Initializing site + logging in
    site = mwclient.Site(('https', 'en.wikipedia.org'),
                         clients_useragent=mwcreds.useragent)
    site.login(mwcreds.username, mwcreds.password)
    print "You are logged in as %s." % mwcreds.username

    # testing prop=flowinfo on a known Flow-enabled page
    kwargs = {'action': 'query',
              'titles': 'Wikipedia:Co-op/Mentorship match',
              'prop': 'flowinfo'}
    query1 = site.api(**kwargs)
    pp.pprint(query1)

    # testing posting a new Flow topic through the API
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
    pp.pprint(query2)

    # testing site.api(*args) to compare to site.api(**kwargs)
    query3 = site.api(action = 'query',
                      titles = 'Wikipedia:Co-op/Mentorship match',
                      prop = 'flowinfo')
    pp.pprint(query3)

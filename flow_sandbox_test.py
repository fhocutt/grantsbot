#!usr/bin/python2.7
#
# Uses raw API calls through mwclient, eventually to get to the Flow web API.
#
# GPL v3.


import mwclient
import pp
import flow_mw_settings as mwcreds

if __name__ == '__main__':
    # Initializing site + logging in
    site = mwclient.Site(('https', 'www.mediawiki.org'),
                         clients_useragent=mwcreds.useragent)
    site.login(mwcreds.username, mwcreds.password)
    print "You are logged in as %s." % mwcreds.username

    kwargs = {'titles': 'API:Client code', 'prop': 'categories'}

    query1 = site.api('query', **kwargs)
    pp.pprint(query1)

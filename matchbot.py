#!usr/lib/python2.7

# matchbot is a script to do things with stuff.
# you point it at a space with subpages and categories
# and it tells you who matches whom

# matchbot currently runs in this test space: 
# https://test.wikipedia.org/wiki/Wikipedia:Co-op

# All mentor and learner profile pages are subpages of Wikipedia:Co-op.

# Category tags: 
#   Co-op (maybe not necessary because implied by subpage status?)
#   Co-op mentor
#   Co-op learner
#   Teaches research
#   Teaches editing
#   Wants to do research
#   Wants to edit


import mwclient

import matchbot_settings

useragent = 'MatchBot, based on mwclient v0.6.5. Run by User:Fhocutt, frances.hocutt@gmail.com'

site = mwclient.Site(('https', 'test.wikipedia.org'), clients_useragent=useragent)
# site.login(matchbot_settings.username, matchbot_settings.password)

for page in site.Categories['Co-op']:
    print page.page_title

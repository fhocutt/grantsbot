#!usr/lib/python2.7

# MatchBot is MediaWiki bot that finds and notifies entities of matches
# based on categories on profile pages. It will be incorporated into the en.wp
# Co-op program and should be able to be extended to match people with projects
# in the IdeaLab.
#
# Released under GPL v3.
# 
# In early development as of Oct 31, 2014.

# MatchBot currently runs in this test space: 
# https://test.wikipedia.org/wiki/Wikipedia:Co-op

# All mentor and learner profile pages are subpages of Wikipedia:Co-op.

# Category tags: 
#   Co-op (maybe not necessary because implied by subpage status?)
#   Co-op mentor
#   Co-op Learner
#   Teaches research
#   Teaches editing
#   Wants to do research
#   Wants to edit

import mwclient

# Config file with login information
import matchbot_settings

useragent = 'MatchBot, based on mwclient v0.6.5. Run by User:Fhocutt, '\
              'frances.hocutt@gmail.com'

# Not currently used
mentor_cats = {'Teaches research', 'Teaches editing'}
learner_cats = {'Wants to do research', 'Wants to edit'}

# Initializing site + logging in
site = mwclient.Site(('https', 'test.wikipedia.org'), 
         clients_useragent=useragent)
site.login(matchbot_settings.username, matchbot_settings.password)

# Go through learners, get corresponding talk page title
# TODO: leave a message on the talk page.

talk_page_titles = []

print "Learners:"
for profile in site.Categories['Co-op learner']:
    print profile.page_title
    talk_page_titles.append(u'%s:%s' % (site.namespaces[5], profile.page_title))

# debugging print statements
print talk_page_titles
print site.pages[talk_page_titles[0]]

# Now edit the learner's wiki page with a list of relevant mentors
for profile in site.Categories['Wants to edit']:
    text = profile.text()
    for mentor in site.Categories['Teaches editing']:
        text = text + '\n\n' + mentor.page_title
    text = text + '\n\nare interested in teaching editing.'
    profile.save(text, summary = 'Testing category matching + page editing')

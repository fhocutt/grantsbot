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

 
# FIXME: works, but there's inconsistency between site.Pages['Category:Blah']
#        and site.Categories['Blah']; could be confusing.
mentor_cats = ['Teaches research', 'Teaches editing']
learner_cats = ['Category:Wants to do research', 'Category:Wants to edit']
category_dict = {k:v for (k,v) in zip(learner_cats, mentor_cats)}

# Initializing site + logging in
site = mwclient.Site(('https', 'test.wikipedia.org'), 
         clients_useragent=useragent)
site.login(matchbot_settings.username, matchbot_settings.password)

# Go through learners, find mentors for each learner category, post
# matching mentors to learner's talk page.

# FIXME: Icky nested loops to refactor!

# Anyone tagged with 'Co-op learner' is a learner
# site.Categories['Foo'] is a List(?) of Pages with 'Category:Foo' (iterable)
for profile in site.Categories['Co-op learner']:
    # Get the corresponding talk page title
    talk_page_title = u'%s:%s' % (site.namespaces[5], profile.page_title)

    # New Page object for the talk page
    talk_page = site.Pages[talk_page_title]
    talk_page_text = u'' # NOTE this will delete existing text

    # get a list of categories on the learner's page
    categories = profile.categories()
    for cat in categories:
        # for the ones we can match on...
        if cat.name in category_dict:
            matchcat = category_dict[cat.name]
            # List the mentors who've marked the corresponding category
            mentors = site.Categories[matchcat]
            for mentor in mentors:
                talk_page_text += u'\n\n%s can mentor you! '\
                                  u'(%s)' % (mentor.page_title, matchcat)

    # once done with all relevant categories, post an invitation
    # NOTE this overwrites any existing text on the talk page
    talk_page.save(talk_page_text, summary = 'Notifying of available mentors')

#    talk_page.save(talk_page_text, summary = 'clearing out tests')


##################
# Another approach: go through each category; possibly less efficient?
# # now edit the learner's wiki page with a list of relevant mentors
# for profile in site.categories['wants to edit']:
#     text = profile.text()
#     for mentor in site.categories['teaches editing']:
#         text = text + '\n\n' + mentor.page_title
#     text = text + '\n\nare interested in teaching editing.'
# #    profile.save(text, summary = 'testing category matching + page editing')

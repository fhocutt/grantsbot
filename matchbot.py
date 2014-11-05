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

# Config file with login information and user-agent string
import matchbot_settings

def get_talk_page(page):
    """Given a Page, return a Page for the talk page from the
    corresponding namespace.

    Assumes that odd values for page.namespace mean that the given Page
    is already a talk page and passes it back.
    """
    if page.namespace % 2 == 0:
        talk_ns = page.namespace + 1
    else:
        return page

    talk_page_title = u'%s:%s' % (page.site.namespaces[talk_ns],
                                  page.page_title)
    return site.Pages[talk_page_title]



# FIXME: works, but there's inconsistency between site.Pages['Category:Blah']
#        and site.Categories['Blah']; could be confusing.
mentor_cats = ['Teaches research', 'Teaches editing']
learner_cats = ['Category:Wants to do research', 'Category:Wants to edit']
category_dict = {k:v for (k,v) in zip(learner_cats, mentor_cats)}

#TODO
def matchcat(categories, category_dict):
    pass

#TODO
def findmentors():
    pass

#TODO
def choosementor(mentors):
    """Given a list of mentors (?) return one mentor to contact."""
    # unclear whether this will be as a name or as a Page item
    pass

#TODO
def buildgreeting(learner, mentor, skill):
    """Puts the string together that can be posted to a talk page or
       Flow board to introduce a potential mentor to a learner.
    """
    return ''

if __name__ == 'main':
    # Initializing site + logging in
    site = mwclient.Site(('https', 'test.wikipedia.org'), 
                         clients_useragent=matchbot_settings.useragent)
    site.login(matchbot_settings.username, matchbot_settings.password)

# Go through learners, find mentors for each learner category, post
# matching mentors to learner's talk page.

# Anyone tagged with 'Co-op learner' is a learner
# site.Categories['Foo'] is a List(?) of Pages with 'Category:Foo' (iterable)
    for profile in site.Categories['Co-op learner']:
        profile_talk = get_talk_page(profile)

    # get a list of categories on the learner's page
        categories = profile.categories()

#possible approach:
#        learner_cats = matchcat(categories, category_dict)
    # feed the categories to a method
    # method returns categories we care about
    # for the relevant categories, fetch mentors
    # choose a mentor
    # build a greeting
    # post the greeting


        for cat in categories:
        # for the ones we can match on...
            if cat.name in category_dict:
                matchcat = category_dict[cat.name]
            # List the mentors who've marked the corresponding category
                mentors = site.Categories[matchcat]
                mentor = choosementor(mentors)
                # FIXME: figure out types for this, this is sketchy
                greeting = buildgreeting(profile.name, mentor, matchcat)
                profile_talk_text += greeting
    # once done with all relevant categories, post an invitation
    # NOTE this overwrites any existing text on the talk page!
        profile_talk.save(profile_talk_text, summary = 
                          'Notifying of available mentors')

#        talk_page.save(talk_page_text, summary = 'clearing out tests')

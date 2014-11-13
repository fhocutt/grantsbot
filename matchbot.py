#!usr/lib/python2.7
#
# MatchBot is MediaWiki bot that finds and notifies entities of matches
# based on categories on profile pages. It will be incorporated into the en.wp
# Co-op program and should be able to be extended to match people with projects
# in the IdeaLab.
#
# Released under GPL v3.
#
# MatchBot currently runs in this test space: 
# https://test.wikipedia.org/wiki/Wikipedia:Co-op
#
# All mentor and learner profile pages are subpages of Wikipedia:Co-op.
#
# Test category tags: 
#   Co-op (maybe not necessary because implied by subpage status?)
#   Co-op mentor
#   Co-op Learner
#   Teaches research
#   Teaches editing
#   Teaches template writing
#   Wants to do research
#   Wants to edit
#   Wants to write templates
#
# For each page tagged "Co-op learner", MatchBot v0.1.0 leaves a message on
# the corresponding talk page with the name of a possible mentor (one for
# each learning interest category on the page).


import mwclient

# Config file with login information and user-agent string
import matchbot_settings
import matcherrors

# TODO: works, but there's inconsistency between site.Pages['Category:Blah']
#        and site.Categories['Blah']; could be confusing. mwclient issue.
mentor_cats = ['Teaches research', 'Teaches editing', 'Teaches template writing']
learner_cats = ['Category:Wants to do research', 'Category:Wants to edit', 'Category:Wants to write templates']
category_dict = {k:v for (k,v) in zip(learner_cats, mentor_cats)}


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

#TODO
def matchcat(categories, category_dict):
    pass

#TODO
def findmentors():
    pass

def getusername(profile_title):
    """Strips the namespace and Co-op page from profile titles (Co-op
    subpages). Returns the username as a string. If neither
    'Wikipedia:' nor 'Co-op/' is present at the beginning of the string
    returns the original string.
    """
    if profile_title[:10] == u'Wikipedia:':
        profile_title = profile_title.strip(u'Wikipedia:')

    if profile_title[:6] == u'Co-op/':
        profile_title = profile_title.strip(u'Co-op/')

    return profile_title


def choosementor(mentors):
    """Given a list of mentor names/profile titles chooses one mentor
    to recommend. Returns the mentor name or profile title as a string.
    """
    return mentors[0]


def buildgreeting(learner, mentor, skill):
    """Puts the string together that can be posted to a talk page or
       Flow board to introduce a potential mentor to a learner.
    """
    greeting = 'Hello, [[User:%(l)s|%(l)s]]! Thank you for your interest in '\
               'the Co-op. [[User:%(m)s|%(m)s]] has listed "%(s)s" in their '\
               'mentorship profile. '\
               'Leave them a message on their talk page and see if you want '\
               'to work together!' % {'l': learner, 'm': mentor, 's': skill}
    return greeting

if __name__ == '__main__':
    # Initializing site + logging in
    site = mwclient.Site(('https', 'test.wikipedia.org'), 
                         clients_useragent=matchbot_settings.useragent)
    site.login(matchbot_settings.username, matchbot_settings.password)


    # site.Categories['Foo'] is a List(?) of Pages with 'Category:Foo'
    for profile in site.Categories['Co-op learner']:
        profile_talk = get_talk_page(profile)
        profile_talk_text = u''                  # to replace text
#       profile_talk_text = profile_talk.text()   # to append text

        # get a list of categories on the learner's page
        categories = profile.categories()

        for cat in categories:
            # for the ones we can match on...
            if cat.name in category_dict:
                matchcat = category_dict[cat.name]

                try:
                    # Make a collection of mentors who marked the matching category
                    mentors = site.Categories[matchcat]
                    mentorprofiles = []

                    for page in mentors:
                        mentorprofiles.append(page.page_title) 

                if mentorprofiles == []:
                        raise matcherrors.MatchError

                    mentor = getusername(choosementor(mentorprofiles))
                    learner = getusername(profile.name)

                    greeting = buildgreeting(learner, mentor, matchcat)

                # if no match is found
                except (matcherrors.MatchError):
                    greeting = u'Oops, we don\'t have a mentor for you! '\
                               u'No mentors have listed "%s".' % matchcat
                    profile_text = (profile.text() +
                                    '[[Category:Orphaned request]]')
#                    profile.save(profile_text)
                profile_talk_text += (u'\n\n' + greeting)
        # once done with all relevant categories, post invitations
#        profile_talk.save(profile_talk_text, summary = 
#                          'Notifying of available mentors')

####
# Debugging and profile talk page clean-up.
#        print profile_talk_text
#        talk_page.save(talk_page_text, summary = 'clearing out tests')

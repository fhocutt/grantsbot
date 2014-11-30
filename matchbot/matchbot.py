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

import datetime
import logging
import logging.handlers
import sqlalchemy
import mwclient

# Config file with login information and user-agent string
import matchbot_settings
import matcherrors
import mbapi
import mblog

# TODO: works, but there's inconsistency between site.Pages['Category:Blah']
#        and site.Categories['Blah']; could be confusing. mwclient issue.
mentor_cats = ['Teaches research', 'Teaches editing', 'Teaches template writing']
learner_cats = ['Category:Wants to do research', 'Category:Wants to edit', 'Category:Wants to write templates']
category_dict = {k:v for (k,v) in zip(learner_cats, mentor_cats)}


# constants for run logs:
run_id = 0 #parameter passed in when the job is run? TODO
edited_pages = False
wrote_db = False
logged_errors = False


#TODO
def matchcat(categories, category_dict):
    pass

#TODO
def findmentors():
    pass

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
    try:
        site = mwclient.Site(('https', 'test.wikipedia.org'),
                              clients_useragent=matchbot_settings.useragent)
        site.login(matchbot_settings.username, matchbot_settings.password)
    except(LoginError):
        mblog.logerror('LoginError: could not log in')
        logged_errors = True
    except:
        mblog.logerror('Login failed')
        logged_errors = True
        #TODO

    '''Rewriting this to work on a minimum number of pages. Looking for
    user pages with new categories first, then will match based on those.'''

    users = []
    # get the new learners for all the categories
    # info to start: profile page id, profile name, time cat added, category
    for category in lcats:
        try:
            # API call with that category
            newusers = mbapi.newmembert(category, timelastchecked)
            for userdict in newusers:
                # add the results of that call to the list of users?
                users.append(userdict)
        except:
            mblog.logerror('Could not fetch newly categorized profiles in %s' % 
                     category)

    # add information: username, userid, talk page id
    for userdict in users:
        #figure out who it is
        if userdict['profile'].startswith('Wikipedia:Co-op/'):
            learner, luid, ltalkid = mbapi.userid(userdict[lpgid])
            userdict['learner'] = learner
            userdict['luid'] = luid
            userdict['ltalkid'] = ltalkid

        else:
            pass

    # find available mentors
    mentors = {}
    nomorementees = mbapi.getmembers() #nomorementees TODO
    for category in mcats:
        try:
            # mentors[category] = mbapi.getmembers(category)
            # remove mentors on that second list from mentors[category] for
            # all categories
        except:
            mblog.logerror('Could not fetch list of mentors for %s') % category

    for learner in learners:
        # make the matches, logging info
        try:
            mentor = match(mentors[category]) # FIXME figure out how categories
                                              # are matched/stored
            mentor, muid, mtalk = mbapi.userid(choosementor(mentorprofiles))
            if mentor = None:
                raise matcherrors.MatchError
        except(matcherrors.MatchError):
            # do no-match flow
            pass

        # build the message
        flowenabled = mbapi.flowenabled(talkpage) #FIXME this isn't talkpage

        greeting = buildgreeting(learner, mentor, matchcat) # also consider flw

        # post the message (talk page or profile's talk page? AHHHH profile's?
        #TODO: eventually if flow isn't enabled post to new flow board?

        # post invitation
        if flowenabled:
            mbapi.postflow(learner_talk.name, greeting)
        elif not flowenabled and learner_talk.text() == '':
            mbapi.newflow(learner_talk.name, greeting)
        else:
            pass #FIXME

    #        profile_talk.save(profile_talk_text, summary = 
    #                          'Notifying of available mentors')
        edited_pages = True
        matchtime = datetime.datetime.now()



        # log the match
        try:
            #TODO: write to DB
            mblog.logmatch(luid=, muid=, category=matchcat, cattime=,
                     matchtime=matchtime, notmatched=,
                     lpageid)
            wrote_db = True
        except:
            mblog.logerror('Could not write to DB')
            logged_errors = True


    # log the run
    mblog.logrun(run_id, edited_pages, wrote_db, logged_errors)


'''
                # if no match is found
                except (matcherrors.MatchError):
                    greeting = u'Oops, we don\'t have a mentor for you! '\
                               u'No mentors have listed "%s".' % matchcat
                    profile_text = (profile.text() +
                                    '[[Category:Orphaned request]]')
#                    profile.save(profile_text)
                profile_talk_text += (u'\n\n' + greeting)


####
# Debugging and profile talk page clean-up.
#        print profile_talk_text
#        talk_page.save(talk_page_text, summary = 'clearing out tests')'''

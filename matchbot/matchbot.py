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

import random
import datetime
import logging
import logging.handlers
import ConfigParser

import sqlalchemy
import mwclient

# Config file with login information and user-agent string
import matchbot_settings
import mberrors
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
def match(catmentors, genmentors):
    if catmentors:
        mentor = random.choice(catmentors)
        return mentor
    elif genmentors:
        mentor = random.choice(genmentors)
        return mentor
    else:
        return None

def buildgreeting(learner, mentor, skill, matchmade):
    """Puts the string together that can be posted to a talk page or
       Flow board to introduce a potential mentor to a learner.
    """
    if matchmade:
        greeting = 'Hello, [[User:%(l)s|%(l)s]]! Thank you for your interest '\
                   'in the Co-op. [[User:%(m)s|%(m)s]] has listed "%(s)s" in '\
                   'their mentorship profile. '\
                   'Leave them a message on their talk page and see if you '\
                   'want to work together!' % {'l': learner, 'm': mentor,
                                               's': skill}
        topic = 'Welcome to the Co-op! Here is your match.'
    else:
        greeting = 'Sorry, we don\'t have a match for you!'
        topic = 'Welcome to the Co-op!'
    return (greeting, topic)

def postinvite(pagetitle, greeting, topic, flowenabled):
    if flowenabled:
        mbapi.postflow(pagetitle, greeting, topic)
        return True
    else:
        profile = site.Pages[pagetitle]
        pagetext = profile.text()
        if pagetext == '':
            mbapi.newflow(learner_talk.name, greeting, topic)
            return True
        else:
            newtext = pagetext + '\n\n' + greeting
            profile.save(newtext, summary = topic)
            return True
    return False

if __name__ == '__main__':
    # log (time)-started-running here TODO
    with open('time.log', 'wb') as timelog:
        timelog.write(str(datetime.datetime.now()))
    # Initializing site + logging in
    try:
        site = mwclient.Site(('https', 'test.wikipedia.org'),
                              clients_useragent=matchbot_settings.useragent)
        site.login(matchbot_settings.username, matchbot_settings.password)
    except(LoginError):
        mblog.logerror('LoginError: could not log in')
        logged_errors = True
    except(Exception):
        mblog.logerror('Login failed')
        logged_errors = True
        #TODO - sys or os.exit()

    learners = []
    # get the new learners for all the categories
    # info to start: profile page id, profile name, time cat added, category
    for category in lcats:
        try:
            # API call with that category
            newlearners = mbapi.newmembers(category, timelastchecked)
            for userdict in newlearners:
                # add the results of that call to the list of users?
                learners.append(userdict)
        except (Exception):
            mblog.logerror('Could not fetch newly categorized profiles in %s' % 
                     category)
            logged_errors = True
    # add information: username, userid, talk page id
    for userdict in learners:
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
    nomore = set(mbapi.getallmembers(NOMENTEES)) #nomorementees FIXME
    for category in mcats: #MCATS: where is it FIXME
        try:
            catmentors = mbapi.getallmembers(category)
            # this may be slowish...
            mentors[category] = [x for x in catmentors if x not in nomore]
        except(Exception):
            mblog.logerror('Could not fetch list of mentors for %s') % category

    for learner in learners:
        # make the matches, logging info
        try:
            notmatched = True
            mentor = match(learner[category]) # FIXME figure out category store
            if mentor = None:
                raise mberrors.MatchError
            mname, muid, mtalk = mbapi.userid(mentor)
            notmatched = False
        except (mberrors.MatchError):
            # add '[[Category:No match found]]' to their page
            profile = site.Pages(learner[profile])
            newprofiletext = profile.text() + NOMATCH #FIXME
            profile.save(newprofiletext, NOMATCHSUMMARY) #FIXME
        except (Exception):
            mblog.logerror('Matching/default match failed')
            logged_errors = True
            break

        # build the message and post it
        flowenabled = mbapi.flowenabled(talkpage) #FIXME this isn't talkpage
        greeting, topic = buildgreeting(learner, mentor, matchcat, notmatched)
        try:
            postinvite(talkpage, greeting, topic, flowenabled) # return? test?
            edited_pages = True
            matchtime = datetime.datetime.now()
        except (Exception):
            mblog.logerror('Could not post match on page')
            logged_errors = True
            break

        # log the match
        try:
            #TODO: write to DB
            mblog.logmatch(luid=, muid=, category=matchcat, cattime=,
                     matchtime=matchtime, notmatched=,
                     lpageid)
            wrote_db = True
        except (Exception):
            mblog.logerror('Could not write to DB')
            logged_errors = True
            break

    # log time-finished-running here?
    mblog.logrun(run_id, edited_pages, wrote_db, logged_errors)

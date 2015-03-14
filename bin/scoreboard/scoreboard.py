#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

import mwclient

import cnf

# contributors to: campaign page spaces?
# Inspire campaign subcategory etc. categorize category page

# since March 1.

# ask Jamie if she has written up docs around Wikimetrics development and stuff
# helping with wikimetrics dev prioritization, can she share any docs that might be helpful?



def main():
    creds = {'protocol': cnf.protocol,
             'site': cnf.site,
             'useragent': cnf.useragent,
             'username': cnf.username,
             'password': cnf.password}
    site = login(creds)

    # get data for scoreboard
    new_participants = get_new_participant_count(site)
    inspire_idea_count = get_inspire_idea_count(site)
    days_left = calculate_days_left()

    # fill in template with data
    text_to_post = format_template(inspire_idea_count, new_participants,
                                   days_left)
    # post updated template
    update_templates(text_to_post, site)


def login(creds):
    """Initialize mwclient Site and log in."""
    site = mwclient.Site((creds['protocol'], creds['site']),
                          clients_useragent=creds['useragent'])
    site.login(creds['username'], creds['password'])
    return site


def get_new_participant_count(site):
    """Get the count of all logged-in contributors to pages in the main
    Inspire namespace and to their associated talk pages, if any.
    """
    main_participants, page_ids = get_main_inspire_info(site)
    talk_participants = get_talk_page_contributors(get_talk_page_ids(page_ids, site), site)
    all_participants = main_participants + talk_participants
    return len(set(all_participants))


def get_main_inspire_info(site):
    """Get a list of logged-in contributors' userids and a list of
    pageids from all pages in Category:IdeaLab/Ideas/Inspire."""
    response = site.api(action='query',
                        prop='contributors',
                        pcexcludegroup='bot|flow-bot',
                        pclimit='max',
                        indexpageids='',
                        generator='categorymembers',
                        gcmtitle='Category:IdeaLab/Ideas/Inspire',
                        gcmlimit='max')
    participants = []
    pages = response['query']['pages']

    for page in pages:
        if pages[page]['ns'] == 200:
            for contributor in pages[page]['contributors']:
                participants.append(contributor['userid'])
        else:
            pass
    page_ids = response['query']['pageids']
    return (participants, page_ids)


def get_talk_page_ids(page_ids, site):
    """Given a list of page ids, get a list of page ids of the
    corresponding talk pages (if they exist)."""
    page_ids_string = '|'.join(page_ids)
    response = site.api(action='query',
                            prop='info',
                            inprop='talkid',
                            pageids=page_ids_string)
    pages = response['query']['pages']
    talk_page_ids = []
    for page in pages:
        if pages[page]['ns'] == 200 and pages[page].get('talkid'):
            talk_page_ids.append(str(pages[page]['talkid']))
    return talk_page_ids


def get_talk_page_contributors(talk_page_ids, site):
    """Given a list of talk page ids, get a list of all the
    contributors' userids. Userids may be listed more than once."""
    talk_page_id_string = '|'.join(talk_page_ids)
    response = site.api(action='query',
                         prop='contributors',
                         pcexcludegroup='bot|flow-bot',
                         pclimit='max',
                         pageids=talk_page_id_string)
    talkparticipants = []
    pages = response['query']['pages']
    for page in pages:
        for contributor in pages[page]['contributors']:
            talkparticipants.append(contributor['userid'])
    return talkparticipants


def get_inspire_idea_count(site):
    """Get the number of pages in Category:IdeaLab/Ideas/Inspire, and
    correct for the three that are templates, not ideas."""
    response = site.api(action='query',
                        prop='categoryinfo',
                        titles='Category:IdeaLab/Ideas/Inspire')
    page_count = parse_idea_count_response(response)

    # don't count probox, etc
    actual_page_count = page_count - 3
    return actual_page_count


def parse_idea_count_response(response):
    for page in response['query']['pages']:
        page_count = response['query']['pages'][page]['categoryinfo']['pages']
        return page_count


def calculate_days_left():
    """Calculate the number of days until March 31, 2015. If the date
    has passed, return 0."""
    ending_date = datetime.date(2015, 03, 31)
    days_left = (ending_date - datetime.date.today()).days
    if days_left >= 0:
        return days_left
    else:
        return 0


def format_template(ideas, participants, days_left):
    """Put the collected data in the template."""
    filled_template = '{{{{IdeaLab/Inspire/Scoreboard\n|ideas= {}\n|'\
                      'participants= {}\n|'\
                      'days_left= {}\n}}}}'.format(ideas, participants,
                                                   days_left)
    return filled_template


def update_templates(text_to_post, site):
    """"""
    scoreboard = site.Pages['Grants:IdeaLab/Inspire/Scoreboard']
    response = scoreboard.save(text_to_post,
                               summary='Automatic scoreboard update',
                               bot='')
    return response


if __name__=='__main__':
    main()

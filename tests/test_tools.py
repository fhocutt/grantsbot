#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import dateutil
from nose.tools import *

import mock

from grantsbot import tools


def setup():
    print('Setup!')


def teardown():
    print('Teardown!')


# test cases for addDefaults
def test_addDefaults():
    member_list = [{'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'timestamp': u'2015-03-13T09:03:19Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368'},
{'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'timestamp': u'2015-03-12T15:35:42Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874'},
{'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'timestamp': u'2015-03-12T13:39:04Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165'}]
    params = tools.output_settings.Params
    params.getParams = mock.MagicMock(return_value ={'username': '', 'title link': '', 'name': '', 'page path': '', 'timestamp': '', 'image': '', 'summary': '', 'talkpage id': '', 'datetime': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': '', 'title': '', 'problem': '', 'page id': '', 'badge': ''})
    new_list = tools.addDefaults(member_list)
    target = [
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    assert new_list == target

def test_addDefaults_empty_member_list():
    assert tools.addDefaults([]) == []

def test_addDefaults_test_for_overwrite():
    params = tools.output_settings.Params
    params.getParams = mock.MagicMock(return_value = {'username': '', 'title link': '', 'name': '', 'page path': '', 'timestamp': '', 'image': '', 'summary': '', 'talkpage id': '', 'datetime': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': '', 'title': '', 'problem': '', 'page id': '', 'badge': ''})
    member_list = [{'username': 'ChickensRCool', 'title link': '', 'name': 'ilikechickens', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''}]
    target = [{'username': 'ChickensRCool', 'title link': '', 'name': 'ilikechickens', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''}]
    new_list = tools.addDefaults(member_list)
    assert new_list == target


# test cases for setTimeValues
def test_setTimeValues():
    member_list = [{'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'timestamp': u'2015-03-13T09:03:19Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368'},
{'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'timestamp': u'2015-03-12T15:35:42Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874'},
{'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'timestamp': u'2015-03-12T13:39:04Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165'}]
    new_list = tools.setTimeValues(member_list)
    print new_list
    target = [{'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'timestamp': u'2015-03-13T09:03:19Z', 'talkpage id': '', 'datetime': datetime.datetime(2015, 3, 13, 9, 3, 19, tzinfo=dateutil.tz.tzutc()), 'time': '13 March 2015', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368'},
              {'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'timestamp': u'2015-03-12T15:35:42Z', 'talkpage id': '', 'datetime': datetime.datetime(2015, 3, 12, 15, 35, 42, tzinfo=dateutil.tz.tzutc()), 'time': '12 March 2015', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874'},
              {'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'timestamp': u'2015-03-12T13:39:04Z', 'talkpage id': '', 'datetime': datetime.datetime(2015, 3, 12, 13, 39, 4, tzinfo=dateutil.tz.tzutc()), 'time': '12 March 2015', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165'}]
    assert new_list == target

def test_setTimeValues_emptylist():
    assert tools.setTimeValues([]) == []

def test_setTimeValues_val_not_in_dicts():
    member_list = [{'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'timestamp': u'2015-03-13T09:03:19Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368'},
{'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'timestamp': u'2015-03-12T15:35:42Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874'},
{'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'timestamp': u'2015-03-12T13:39:04Z', 'talkpage id': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165'}]
    new_list = tools.setTimeValues(member_list, 'chickens')
    assert new_list == member_list


# test cases for getSubDate
def test_getSubDate_14_days():
    tools.utcnow = mock.MagicMock(return_value=datetime.datetime(2015, 3, 14, 1, 59, 26, 353187))
    date = tools.getSubDate(10)
    target = (datetime.datetime(2015, 3, 4, 1, 59, 26, 353187, tzinfo=dateutil.tz.tzutc()), '20150304015926')
    assert date == target

@raises(TypeError)
def test_getSubDate_input_string():
    dates = tools.getSubDate('14')

@raises(TypeError)
def test_getSubDate_input_datetime():
    date = tools.getSubDate(datetime.datetime(2015, 3, 15, 1, 59, 26, 353187))
    assert False

@raises(TypeError)
def test_getSubDate_input_timedelta():
    date = tools.getSubDate(datetime.timedelta())

def test_getSubDate_negative_interval():
    tools.utcnow = mock.MagicMock(return_value=datetime.datetime(2015, 3, 14, 1, 59, 26, 353187))
    dates = tools.getSubDate(-1)
    target = (datetime.datetime(2015, 3, 15, 1, 59, 26, 353187,
        tzinfo=dateutil.tz.tzutc()), '20150315015926')
    assert dates == target


# test cases for titleFromPath
def test_titleFromPath_two_deep():
    title = tools.titleFromPath('IdeaLab/Ideas/My_great_idea')
    assert title == 'My great idea'

def test_titleFromPath_two_deep_unicode():
    title = tools.titleFromPath(u'IdeaLab/Ideas/My_great_idea')
    assert title == u'My great idea'

def test_titleFromPath_two_deep_nonlatintitle():
    title = tools.titleFromPath(u'IdeaLab/Ideas/Rege̿̔̉x-based HTML parsers')
    assert title == u'Rege̿̔̉x-based HTML parsers'

def test_titleFromPath_onlypage():
    title = tools.titleFromPath('My_great_idea')
    assert title == 'My great idea'

def test_titleFromPath_beginning_slash():
    title = tools.titleFromPath(u'/IdeaLab/Ideas/My_great_idea')
    assert title == u'My great idea'

@raises(AttributeError)
def test_titleFromPath_ending_slash():
    title = tools.titleFromPath(u'IdeaLab/Ideas/My_great_idea/')

@raises(AttributeError)
def test_titleFromPath_empty():
    title = tools.titleFromPath('')

def test_titleFromPath_only_underscores():
    title = tools.titleFromPath('______')
    assert title == '      '


# test cases for formatSummaries
def test_formatSummaries():
    text = '''I have over five-year experience with Czech projects focused on enriching Wikimedia Commons with multimedia content related to the Czech Republic: [[Wikimedia Czech Republic/Mediagrant II|Mediagrant I and II]] projects and [[:cs: Wikipedie:WikiProjekt Fotografování/Foto českých obcí|Czech Municipalities]] project (over 26,000 photos). I am also organizing [[:commons: Category:Czech Photo Workshops|Czech Photo Workshops]].

I am founding member of Czech chapter. Since June 2011, I am member of Grant Advisory Committee.'''

    summary = tools.formatSummaries(text)
    target = '''I have over five-year experience with Czech projects focused on enriching Wikimedia Commons with multimedia content related to the Czech Republic: Mediagrant I and II projects and Czech Municipalities project (over 26,000 photos). I am also organizing Czech Photo Workshops.

I am founding member of Czech chapter. Since June 2011, I am member of Grant Advisory Committee....'''
    assert summary == target

def test_formatSummaries_single_square_brackets():
    text = u'I am a summary [that is to say, a summary] that contains []s.'
    summary = tools.formatSummaries(text)
    target = u'I am a summary that is to say, a summary that contains s....'
    assert summary == target

def test_formatSummaries_has_pipe():
    text = u'I am a summary that contains a pipe (|). Ceci c\'est une pipe. |'
    summary = tools.formatSummaries(text)
    target = u'I am a summary that contains a pipe (|). Ceci c\'est une pipe. |...'
    assert summary == target

def test_formatSummaries_unicode():
    text = u'c͒ͪo͛ͫrrupt entities'
    summary = tools.formatSummaries(text)
    target = u'c͒ͪo͛ͫrrupt entities...'
    assert summary == target

@raises(AttributeError)
def test_formatSummaries_input_int():
    summary = tools.formatSummaries(1337)

def test_formatSummaries_empty_string():
    summary = tools.formatSummaries('')
    assert summary == '...'


# test cases for dedupeMemberList
# TODO: more test cases
def test_dedupeMemberList():
    member_list = [
                    {'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
                    {'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
                    {'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
                    {'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
                    {'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
                  ]
   
    deduped_list = [
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    new_list = tools.dedupeMemberList(member_list, 'page id', 'page id')
    assert new_list == deduped_list

def test_dedupeMemberList_nodupes():
    member_list = [
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    new_list = tools.dedupeMemberList(member_list, 'page id', 'page id')
    assert new_list == member_list

@raises(KeyError)
def test_dedupeMemberList_empty_sort_val():
    member_list = [
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    new_list = tools.dedupeMemberList(member_list, '', 'page id')

@raises(KeyError)
def test_dedupeMemberList_empty_dict_val():
    member_list = [
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    new_list = tools.dedupeMemberList(member_list, '', 'page id')

@raises(TypeError)
def test_dedupeMemberList_listofstrs():
    new_list = tools.dedupeMemberList(['chickens', 'more chickens'], 'page id', 'page id')

def test_dedupeMemberList_emptylist():
    new_list = tools.dedupeMemberList([], 'page id', 'page id')
    assert new_list == []

@raises(KeyError)
def test_dedupeMemberList_None_dict_val():
    member_list = [
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    new_list = tools.dedupeMemberList(member_list, 'page id', None)


# test cases for excludeSubpages
# find memberlist format
def test_excludeSubpages():
    dicts = [{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]

    new_list = tools.excludeSubpages(dicts, 'page path')
    print new_list
    assert new_list == []

def test_excludeSubpages_includeall():
    dicts = [{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    new_list = tools.excludeSubpages(dicts, 'page path', depth=2)
    assert new_list == dicts

def test_excludeSubpages_with_skip_list():
    skip_list = [u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen"]
    dicts = [{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/Debates on facts given in Inspire Campaign mass message', 'datetime': '', 'timestamp': u'2015-03-13T09:03:19Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7059368', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'datetime': '', 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055874', 'badge': '', 'problem': ''},
{'username': '', 'title link': '', 'name': '', 'page path': u'Grants:IdeaLab/ Hipatia de Alejandr\xeda Las-10-mujeres-cient\xedficas-m\xe1s-importantes-de-la-historia-1.jpgHipatia de Al', 'datetime': '', 'timestamp': u'2015-03-12T13:39:04Z', 'image': '', 'title': '', 'talkpage id': '', 'summary': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'page id': '7055165', 'badge': '', 'problem': ''},
]
    new_list = tools.excludeSubpages(dicts, 'page path', skip_list=skip_list)
    target = [{'username': '', 'page id': '7055874', 'title link': '', 'name': '', 'page path': u"Grants:IdeaLab/'weibliche Themen', die Zwischenmenschliches betreffen.. nicht l\xf6schen", 'timestamp': u'2015-03-12T15:35:42Z', 'image': '', 'title': '', 'talkpage id': '', 'datetime': '', 'item': '', 'participants': '', 'create date': '', 'time': '', 'action': 3, 'event type': 'participants wanted', 'summary': '', 'badge': '', 'problem': ''}]
    assert new_list == target

def test_excludeSubpages_emptyList():
    new_list = tools.excludeSubpages([], 'page path')
    assert new_list == []

def test_excludeSubpages_emptylist_emptypathkey():
    assert tools.excludeSubpages([], '') == []

@raises(KeyError)
def test_excludeSubpages_empty_path_key():
    new_list = tools.excludeSubpages([{'a': 1}, {'a': 2}], '')
    assert new_list == [{'a': 1}, {'a': 2}]

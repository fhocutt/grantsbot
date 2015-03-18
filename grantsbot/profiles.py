#! /usr/bin/env python2.7

# Copyright 2013 Jtmorgan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import mwclient

import grantsbot_settings
import templates
import re

class Profiles:
    """Operations you might want to perform on and with profiles."""

    def __init__(self, path, id = False, settings = False):
        """
        Instantiate page-level variables for building a set of profiles.
        """
        self.page_path = path

        if id:
            self.page_id = str(id)
        else:
            pass

        if settings:
            self.profile_settings = settings
        else:
            pass

        self.site = mwclient.Site((grantsbot_settings.protocol,
                                   grantsbot_settings.site))
        self.site.login(grantsbot_settings.username,
                        grantsbot_settings.password)


    def getPageSectionData(self, level = False):
        """
        Returns the section titles and numbers for a given page.
        Level arg can be used to return only sections of a given indentation level.
        Sample request: http://meta.wikimedia.org/w/api.php?action=parse&page=Grants:IdeaLab/Introductions&prop=sections&format=jsonfm
        """
        params = {
            'action': 'parse',
            'page': self.page_path,
            'prop': 'sections',
        }
        response = self.site.api(**params)

        if level:
            secs_list = [{'title' : unicode(x['line']), 'index' : x['index']} for x in response['parse']['sections'] if x['toclevel'] == level]
        else:
            secs_list = [{'title' : unicode(x['line']), 'index' : x['index']} for x in response['parse']['sections']]
        return secs_list


    ''' Hard to say what's needed here--took this from categories.py
    def getPageMetaData(self, mempage): #Need to make this a call to profiles.py.
        """
        Gets some additional metadata about each page.
        Currently just the local talkpage id or subjectid and the full url.
        """
        params = {
            'action': 'query',
            'titles': mempage['page path'],
            'prop': 'info',
            'inprop' : 'talkid|subjectid|url'
        }
        response = self.site.api(**params)
        pageid = str(mempage['page id'])
        try:
            mempage['talkpage id'] = str(response['query']['pages'][pageid]['talkid'])
        except KeyError:
            mempage['talkpage id'] = "" #probably not necessary anymore, if I add these default params in to every one anyway.
        return mempage
    '''

    def getPageText(self, section = False):
        """
        Gets the raw text of a page or page section.
        Sample: http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&titles=Grants:Learning_patterns/Repeat_events&rvprop=content&rvsection=0&format=jsonfm
        """
        params = {
            'action': 'query',
            'prop': 'revisions',
            'titles': self.page_path,
            'rvprop' : 'content',
            'rvsection' : '',
        }
        if section:
            params['rvsection'] = section
        response = self.site.api(**params)
        for page in response['query']['pages']:
            text = response['query']['pages'][page]['revisions'][0]['*']

#        text = response['query']['pages'][self.page_id]['revisions'][0]['*']

#        text2 = self.site.Pages[self.page_path].text()
# this seems to make the rest of
#        print(text2)
#        print(text == text2)
        return text

#       Retrieve latest revision metadata.
#       Sample: http://meta.wikimedia.org/w/api.php?action=query&prop=info&titles=Grants:IEG/GIS_and_Cartography_in_Wikimedia&format=jsonfm
#       latest_rev = response['query']['pages'][self.page_id]['lastrevid']

    def getPageEditInfo(self, sort_dir="older", page = False, rvstart = False, rvend = False): #should just be 'getPageRecentRevs'
        """
        Returns a list of values for revision properties you specify. Can use the page id associated with the current profiles object, or another one specified through the page arg.
        Example: http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&pageids=2101758&rvdir=newer&rvstart=20130601000000&rvprop=comment|ids|timestamp|user|userid&rvlimit=50&format=jsonfm
        """
        if page:
            page_id = page
        else:
            page_id = self.page_id

        params = {
                'action': 'query',
                'prop': 'revisions',
                'pageids': page_id,
                'rvprop' : 'comment|ids|timestamp|user|userid',
                'rvlimit' : 'max',
                'rvdir' : sort_dir,
                    }
        if rvstart:
            params['rvstart'] = rvstart
        if rvend:
            params['rvend'] = rvend
        response = self.site.api(**params)
        try:
            revs = response['query']['pages'][page_id]['revisions']
        except:
            revs = []
        return revs

    def getUserRecentEditInfo(self, user_name, edit_namespace = False): #rename
        """
        Get edits by a user in a given namespace within the past month
        (or whatever range recentchanges is set to on your wiki).
        Sample: http://meta.wikimedia.org/w/api.php?action=query&list=recentchanges&rcnamespace=200&rcuser=Jmorgan_(WMF)&rclimit=500&format=jsonfm
        """
        params = {
                'action': 'query',
                'list': 'recentchanges',
                'rcuser': user_name,
                'rcnamespace': edit_namespace,
        }
        response = self.site.api(**params)
        recent_edits = len(response['query']['recentchanges'])
        recent_edits = len(response['query']['recentchanges'])
        return recent_edits

    def getRecentIntros(self, rvend): #should generalize this a bit, like getPageEditInfo
        """
        Gets recent profiles added to a page. Example:
http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&pageids=2101758&rvdir=older&rvend=20131001000000&rvprop=comment|ids|timestamp|user|userid&rvlimit=50&format=jsonfm
        """
        params = {
                'action': 'query',
                'prop': 'revisions',
                'pageids': self.page_id,
                'rvprop' : 'comment|ids|timestamp|user',
                'rvend' : rvend,
                'rvlimit' : 100, #arbitrarily high
                'rvdir' : 'older',
                    }
        intro_list = []
        suffix = "new section"
        response = self.site.api(**params)
        revs = response['query']['pages'][self.page_id]['revisions']
        for r in revs:
            if r['comment'].endswith(suffix):
                intro = {'username' : r['user'], 'timestamp' : r['timestamp'], 'page path' : self.page_path, 'page id' : self.page_id}
                intro_list.append(intro)
        return intro_list

    def scrapeInfobox(self, member, infobox, redict = False, trans_tag = False):
        """
        Method for grabbing the values of parameters from an infobox.
        Regexes for each infobox param are specified in the settings for the profile object.
        You can also pass a custom dict of regex strings to look for, via redict.
        Translate tags ('<translate>') and other tags that push
        the param value to the next line can be specified by passing the tag string
        in the optional trans_tag argument.
        """
        if redict:
            re_types = redict #this is now very inconsistent, because of the away I'm storing these regexes. Fix!
        else:
            re_types = self.profile_settings[self.profile_settings['subtype']]['infobox params']
        second_line = False #used to test for translate tags
        for k,v in re_types.iteritems():    #params are loaded when the profile object is created
            for line in infobox.split('\n'):
                if second_line:
                    try:
                        member[k] = re.sub('(<[^>]+>)+', '', line)
                    except:
                        pass
                        # print "can't capture the second line"
                    second_line = False
                    break #we found the value below the param, let's move on to another param
                else:
                    if re.search(v, line): #can I just search for the key?
                        if (trans_tag and trans_tag in line):
                            second_line = True
                            continue
                        else:
                            try:
                                member[k] = re.search('(?<=\=)(.*?)(?=<|\||$)',line).group(1) #am I ignoring HTML comments?
                            except:
                                pass
#                               print "can't find this param in the infobox"
                    else:
                        continue #should I ignore profiles that don't have, say summaries?
        return member

    def formatProfile(self, val):
        """
        Takes in a dictionary of parameter values and plugs them
        into the specified template by matching keys.
        """
        page_templates = templates.Template()
        tmplt = page_templates.getTemplate(self.profile_settings['type'])
        tmplt = tmplt.format(**val).encode('utf-8')
        return tmplt

    def publishProfile(self, val, path, edit_summ, sb_page = False, edit_sec = False):
        """
        Publishes a profile or set of concatenated profiles to a page on a wiki.
        """
        if sb_page:
            path += str(sb_page)
#       print path
#       print val
#       print edit_summ
#       print edit_sec

        page = self.site.Pages[path]

        if edit_sec:
            page.save(val, section=edit_sec, summary=edit_summ)
        else:
            page.save(val, summary=edit_summ)

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

# from wikitools import category as wtcat
import wikitools
import grantsbot_settings
import templates
import pages

class Profiles:
	"""A page on a wiki."""

	def __init__(self, title, type, namespace = grantsbot_settings.rootpage):
		"""
		Instantiates page-level variables for building a set of profiles.
		"""
		self.title = title
		print self.title
		self.type = type
# 		print self.type
		self.namespace = namespace #used for people, not ideas
# 		print self.namespace
		self.page_path = namespace + title #not using this for featured ideas
# 		print self.page_path
		self.wiki = wikitools.Wiki(grantsbot_settings.apiurl)
		self.wiki.login(grantsbot_settings.username, grantsbot_settings.password)

	def getPageSectionData(self):
		"""
		Returns the section titles and numbers for a given page.
		Sample request: http://meta.wikimedia.org/w/api.php?action=parse&page=Grants:IdeaLab/Introductions&prop=sections&format=jsonfm
		"""
		params = {
			'action': 'parse',
			'page': self.page_path,
			'prop': 'sections',
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		secs_list = [{'username' : x['line'], 'profile_index' : x['index']} for x in response['parse']['sections']]
		return secs_list

	def getPageText(self, section = False):
		"""
		Gets the raw text of a page or page section.
		Sample: http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&titles=Grants:IdeaLab/Introductions&rvprop=content&rvsection=21&format=jsonfm
		"""
		params = {
			'action': 'query',
			'prop': 'revisions',
			'titles': self.page_path,
			'rvprop' : 'content',
			'rvsection' : section,
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		page_id = response['query']['pages'].keys()[0]
		text = response['query']['pages'][page_id]['revisions'][0]['*']
		return text

	def getUserRecentEditInfo(self, user_name, edit_namespace = False): #rename
		"""
		Get edits by a user in a given namespace within the past month, and the time of their most recent edit.
		Sample: http://meta.wikimedia.org/w/api.php?action=query&list=recentchanges&rcnamespace=200&rcuser=Jmorgan_(WMF)&rclimit=500&format=jsonfm
		"""
		params = { #need to update this so that it will accept recent edits, or first edit to the page (page edits by user sorted in reverse date order)
			'action': 'query',
			'list': 'recentchanges',
			'rcuser': user_name,
			'rcnamespace': edit_namespace,
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		recent_edits = len(response['query']['recentchanges'])
		if recent_edits > 0:
			latest_edit = response['query']['recentchanges'][0]['timestamp']
			latest_rev = response['query']['recentchanges'][0]['revid']
			edit_info = (recent_edits, latest_rev, latest_edit)
		else:
			edit_info = (0, 0, "")
		return edit_info

	def getPageInfo(self, val):
		"""
		Retrieve the value of any one of the default page info metadata.
		Sample:
		FIXME
		"""
		params = {
			'action': 'query',
			'titles': self.title,
			'prop': 'info',
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		page_id = response['query']['pages'].keys()[0]
		info = response['query']['pages'][page_id][val]
		return info


	def formatProfile(self, val):
		"""
		takes in a dictionary of parameter values and plugs them into the specified template
		"""
		page_templates = templates.Template()
		tmplt = page_templates.getTemplate(self.type)
		tmplt = tmplt.format(**val).encode('utf-8')
		return tmplt

	def publishProfile(self, val, pth, edt_summ, sb_page = False):
		"""
		Publishes a profile or set of concatenated profiles to a page on a wiki.
		"""
		if sb_page:
			pth += str(sb_page)
		print pth
		print val
		print edt_summ
		output = wikitools.Page(self.wiki, pth)
		output.edit(val, summary=edt_summ, bot=1) #need to specify the section!
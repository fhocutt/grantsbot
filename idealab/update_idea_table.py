#! /usr/bin/python2.7

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

import MySQLdb
from datetime import datetime
import grantsbot_settings
from warnings import filterwarnings

conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=True, charset="utf8")
cursor = conn.cursor()
filterwarnings('ignore', category = MySQLdb.Warning)

##FUNCTIONS##
def add_ideas(cursor):
	"""
	Add newly created ideas.
	"""
	cursor.execute('''
insert ignore into idealab_ideas
		(idea_id, idea_title, idea_creator, idea_created)
		select page_id, page_title, creator, create_date FROM 
(select page_id, page_title, rev_user_text AS creator, STR_TO_DATE(rev_timestamp,'%Y%m%d%H%i%s') AS create_date
FROM metawiki_p.page AS p 
JOIN metawiki_p.categorylinks AS cl 
ON p.page_id = cl.cl_from 
JOIN metawiki_p.revision AS r
ON p.page_id = r.rev_page
WHERE cl.cl_to IN ("IdeaLab/Ideas/IdeaLab", "IdeaLab/Ideas/Inspire")
AND cl.cl_type = "page"
AND p.page_namespace = 200
AND p.page_title LIKE "IdeaLab/%"
AND p.page_title NOT LIKE "%/%/%"
AND r.rev_parent_id = 0) AS tmp ORDER BY create_date ASC
	''')
	conn.commit()

def add_talk_pages(cursor):
	"""
	Adds the talkpage id for each idea, if there is a talkpage.
	"""
	cursor.execute('''
	UPDATE idealab_ideas AS i, metawiki_p.page as p
		SET i.idea_talk_id = p.page_id
		WHERE i.idea_talk_id IS NULL
		AND p.page_namespace = 201
		AND p.page_is_redirect = 0
		AND i.idea_title = p.page_title;
	''')
	conn.commit()

def update_endorsements(cursor):
	"""
	Add in how many endorsements there have been for each idea.
	"""
	cursor.execute('''
	UPDATE idealab_ideas AS ii, (SELECT COUNT(rev_comment) as endorsements, rev_page 
	FROM metawiki_p.revision AS r WHERE r.rev_page IN (SELECT idea_id FROM idealab_ideas) 
	AND (r.rev_comment LIKE ("%Endorse%") OR r.rev_comment LIKE ("%endorse%")) GROUP BY 	rev_page) AS tmp 
	SET ii.idea_endorsements =
	CASE
	WHEN tmp.endorsements = 0 THEN 0
	ELSE tmp.endorsements
	END
	WHERE ii.idea_id = tmp.rev_page
	''')
	conn.commit()

#this version doesn't work yet 	
# 	cursor.execute('''
# 	UPDATE idealab_ideas AS i,
# (SELECT COUNT(distinct rev_user) AS endorsements, idea_id FROM
# (SELECT r.rev_user, i.idea_id FROM metawiki_p.page AS p 
# JOIN metawiki_p.categorylinks AS cl 
# ON p.page_id = cl.cl_from 
# JOIN metawiki_p.revision AS r
# ON p.page_id = r.rev_page
# JOIN idealab_ideas AS i
# ON p.page_id = i.idea_id
# WHERE rev_user != 0 
# AND (r.rev_comment LIKE ("%Endorse%") OR r.rev_comment LIKE ("%endorse%"))
# AND r.rev_user_text NOT LIKE "%(WMF)") AS tmp1
# GROUP BY idea_id) AS tmp2
# SET i.idea_endorsements = tmp2.endorsements
# WHERE i.idea_id = tmp2.idea_id;
# 	''')

def update_recent_editors(cursor):
	"""
	Add in all edits to the idea page within the past two weeks.
	"""
	cursor.execute('''
	UPDATE idealab_ideas AS ii INNER JOIN 
	(
	SELECT COUNT(distinct r.rev_user) AS recent_editors, r.rev_page 
	FROM metawiki_p.revision r INNER JOIN idealab_ideas i ON r.rev_page = i.idea_id 
	WHERE STR_TO_DATE(r.rev_timestamp, '%Y%m%d%H%i%s') > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 14 DAY),'%Y%m%d%H%i%s') 
	GROUP BY r.rev_page
	) AS tmp 
	ON ii.idea_id = tmp.rev_page
	SET ii.idea_recent_editors = 
	CASE
	  WHEN tmp.recent_editors = 0 THEN 0
	  ELSE tmp.recent_editors
	 END
	 ''')
	conn.commit()

# this version doesn't work yet	 
# UPDATE idealab_ideas AS ii, (SELECT COUNT(distinct r.rev_user) AS recent_editors, p.page_title FROM metawiki_p.revision r, metawiki_p.page p WHERE r.rev_page = p.page_id AND p.page_namespace IN (200, 201) AND p.page_title IN (SELECT idea_title FROM idealab_ideas) AND STR_TO_DATE(r.rev_timestamp, '%Y%m%d%H%i%s') > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 14 DAY),'%Y%m%d%H%i%s') GROUP BY page_title) AS tmp SET ii.idea_recent_editors = tmp.recent_editors WHERE ii.idea_title = tmp.page_title;


##MAIN##
add_ideas(cursor)
add_talk_pages(cursor)
update_endorsements(cursor)
update_recent_editors(cursor)
cursor.close()
conn.close()

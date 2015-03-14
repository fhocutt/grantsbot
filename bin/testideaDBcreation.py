import sys
import os
import json
import sqlalchemy as sqa
import datetime


def main(filepath):
#    conn_str = makeconnstr(config)
#    createtable(conn_str)
    createtable('sqlite:////home/fhocutt/WMFContractWork/IdeaLab/grantsbot-matching/ideas.db')
    ideas_list = load_ideas(filepath)
    mangle_datetime(ideas_list)
    insert_matches('sqlite:////home/fhocutt/WMFContractWork/IdeaLab/grantsbot-matching/ideas.db', ideas_list)


def createtable(conn_str):
    engine = sqa.create_engine(conn_str, echo=True)
    metadata = sqa.MetaData()
    matches = sqa.Table('idealab_ideas', metadata,
                        sqa.Column('id', sqa.Integer, primary_key = True),
                        sqa.Column('idea_id', sqa.Integer, unique=True),
                        sqa.Column('idea_title', sqa.String(255)),
                        sqa.Column('idea_talk_id', sqa.Integer),
                        sqa.Column('idea_creator', sqa.String(255)),
                        sqa.Column('idea_created', sqa.DateTime),
                        sqa.Column('idea_endorsements', sqa.Integer),
                        sqa.Column('idea_recent_editors', sqa.Integer))
    metadata.create_all(engine)


def mangle_datetime(ideas_list):
    idea_list_copy = ideas_list[:]
    for idea in ideas_list:
        time_created = idea['idea_created']
        idea['idea_created'] = datetime.datetime.strptime(time_created, '%Y-%m-%d %H:%M:%S')


def load_ideas(filepath):
    with open('/home/fhocutt/WMFContractWork/IdeaLab/grantsbot-matching/newideas.json', 'rb') as ideas:
        ideas_list = json.loads(ideas.read())
    return ideas_list


def insert_matches(conn_str, ideas_list):
    engine = sqa.create_engine(conn_str, echo=True)
    metadata = sqa.MetaData()
    ideas = sqa.Table('idealab_ideas', metadata, autoload=True,
                        autoload_with=engine)
    ins = ideas.insert()
    conn = engine.connect()
    conn.execute(ins, ideas_list)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = './matching/'

    main(filepath)

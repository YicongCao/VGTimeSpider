import os
import csv
import json
import sqlite3

CLEAR_TABLE = '''
drop table if exists games;
'''

CREATE_TABLE = '''
create table games
(
    name varchar(255) default 'noname',
    nickname varchar(255) default 'nonickname',
    score int default -1,
    pop int default -1,
    date varchar(255) default '1970-01-01',
    dna varchar(255) default 'nodna',
    company varchar(255) default 'nocompany',
    tag varchar(255) default 'notag',
    url varchar(255) default 'https://www.vgtime.com',
    img varchar(255) default 'https://static.vgtime.com/image/noimage_vg.png'
);
'''

INSERT_DATA = '''
insert into games (name, nickname, score, pop, date, dna, company, tag, url, img)
values ("{name}", "{nickname}", "{score}", "{pop}", "{date}", "{dna}", "{company}", "{tag}", "{url}", "{img}")
'''

QUERY_BY_NAME = '''
select *
from games where name LIKE "%{name}%" or nickname LIKE "%{name}%"
'''

conn = sqlite3.connect('gamesqlite.db')
cursor = conn.cursor()
cursor.execute(CLEAR_TABLE)
cursor.execute(CREATE_TABLE)

with open('gamedata.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        columns = {}
        columns['name'] = line['name']
        columns['nickname'] = line['nickname']
        columns['score'] = line['score']
        columns['pop'] = line['count']
        columns['platform'] = line['platform']
        columns['date'] = line['date']
        columns['dna'] = line['dna']
        columns['company'] = line['company']
        columns['tag'] = 'null'
        columns['url'] = line['url']
        columns['img'] = line['img']
        cursor.execute(INSERT_DATA.format(**columns))

print('insert {0} lines'.format(cursor.rowcount))
cursor.close()
conn.commit()
cursor = conn.cursor()
keyword = '塞尔达'
query = {'name': keyword}
cursor.execute(QUERY_BY_NAME.format(**query))
result = cursor.fetchall()
print('games matching {0}:\r\n'.format(keyword))
for game in result:
    print(str(game) + '\r\n')
conn.close()

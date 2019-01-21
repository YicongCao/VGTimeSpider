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
    platform varchar(255) default 'noplatform',
    company varchar(255) default 'nocompany',
    tag varchar(255) default 'notag',
    url varchar(255) default 'https://www.vgtime.com',
    img varchar(255) default 'https://static.vgtime.com/image/noimage_vg.png'
);
'''

INSERT_DATA = '''
insert into games (name, nickname, score, pop, date, dna, company, platform, tag, url, img)
values ("{name}", "{nickname}", "{score}", "{pop}", "{date}", "{dna}", "{company}", "{platform}", "{tag}", "{url}", "{img}")
'''

QUERY_BY_NAME = '''
select *
from games where name LIKE "%{name}%" or nickname LIKE "%{name}%" order by pop desc
'''


def NounReplace(sourcestr):
    targetstr = str(sourcestr).strip().replace("Microsoft", "微软")
    targetstr = targetstr.replace(
        "Nintendo", "任天堂").replace("Naughty Dog", "顽皮狗")
    targetstr = targetstr.replace(
        "Rockstar Games", "R星").replace("CAPCOM", "卡普空")
    targetstr = targetstr.replace("Blizzard", "暴雪").replace("Ubisoft", "育碧")
    targetstr = targetstr.replace("SEGA", "世嘉").replace(
        "Sony Interactive Entertainment", "索尼")
    targetstr = targetstr.replace("Sony", "索尼").replace("SONY", "索尼")
    targetstr = targetstr.replace("角色扮演", "角色扮演 RPG").replace("射击", "射击 FPS")
    targetstr = targetstr.replace("动作", "动作 ACT").replace("多人", "MOBA MMO")
    targetstr = targetstr.replace("XBone", "Xbox").replace("Switch", "switch")
    targetstr = targetstr.replace("马里欧", "马里奥").replace("马力欧", "马里奥")
    return targetstr


conn = sqlite3.connect('gamesqlite.db')
cursor = conn.cursor()
cursor.execute(CLEAR_TABLE)
cursor.execute(CREATE_TABLE)
gameset = set()

with open('gamedata.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for line in reader:
        if line['name'] in gameset:
            continue
        columns = {}
        columns['name'] = NounReplace(line['name'])
        columns['nickname'] = line['nickname']
        columns['score'] = line['score']
        columns['pop'] = line['count']
        columns['platform'] = NounReplace(line['platform'])
        columns['date'] = line['date']
        columns['dna'] = NounReplace(line['dna'])
        columns['company'] = NounReplace(line['company'])
        columns['tag'] = 'null'
        columns['url'] = line['url']
        columns['img'] = line['img']
        cursor.execute(INSERT_DATA.format(**columns))
        gameset.add(line['name'])

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

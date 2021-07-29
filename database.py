# This code is adapted from the tutorial hosted below:
# http://www.postgresqltutorial.com/postgresql-python/connect/
from web_scrapping import OlimpicScraper
from datetime import date
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
print('Conectando...')

def createDb():
    create_db = "CREATE DATABASE olimpic;"
    con = psycopg2.connect("user=lucas password='oracao34'")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(create_db)
    finally:
        con.close()
        cur.close()

def createTable():
    create_table =  '''
                 CREATE TABLE medal_{}(
                 rank INTEGER,
                 team VARCHAR (50),
                 gold INTEGER,
                 silver INTEGER,
                 bronze INTEGER,
                 total INTEGER,
                 rank_by_total INTEGER
                 );
                    '''.format(date.today().day)
    con = psycopg2.connect("dbname=olimpic user=lucas password=oracao34")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(create_table)
    finally:
        con.close()
        cur.close()

def insertTable(rank, team, gold, silver, bronze, total, rank_by_total):
    insert_table = '''
                INSERT INTO medal_{}(rank, team, gold, silver, bronze, total, rank_by_total)
                VALUES({},'{}',{},{},{},{},{});
                    '''.format(date.today().day,rank, team, gold, silver, bronze, total, rank_by_total)

    con = psycopg2.connect("dbname=olimpic user=lucas password=oracao34")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(insert_table)
    finally:
        con.close()
        cur.close()

def queryTable():
    query = '''
                SELECT *
                FROM medal_{};
            '''.format(date.today().day)
    con = psycopg2.connect("dbname=olimpic user=lucas password=oracao34")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(query)
        cur.fetchall()
    finally:
        con.close()
        cur.close()

createDb()
createTable()
ws = OlimpicScraper()
ws.init_session()
ws.accept_cookies()
table = ws.scrapp_table()
for row in table:
    if row[1] == "People's Republic of China":
        row[1] = "People''s Republic of China"
    elif row[1] == "Côte d'Ivoire":
        row[1] = "Côte d''Ivoire"
    insertTable(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
print(queryTable())



import sqlite3
import re
import sys


def create_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def parse_txt_to_db(lex_file, conn):
    fh = open(lex_file)
    counter = 0
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE lex ([id] INTEGER PRIMARY KEY,[eng] text, [ger] text)')
    conn.commit()
    for line_num, line in enumerate(fh):
        if not line.startswith(('#', ' ', '\n')):
            eng = re.sub(r"\[.*?\]", "", line.split('\t', 1)[0])
            ger = re.sub(r"  |   |^ | $", "", re.sub(r"\(.*?\)|\[.*?\]|\{.*?\}|verb|adj|noun|adv|\t|\n", "", line.split('\t', 1)[1]))
            if " " != eng or " " != ger or "" != eng or "" != ger:
                cursor.execute('INSERT INTO lex VALUES (' + str(line_num) + ', "' + eng + '", "' + ger + '")')
                conn.commit()
                print(eng, ger)
    fh.close()


def parse_db_to_xdxf(xdxf_file, conn):
    df = open(xdxf_file, 'a')
    cursor = conn.cursor()
    cursor.execute('SELECT eng, GROUP_CONCAT(ger) FROM LEX GROUP BY eng Order by id asc')
    for row in cursor:
        df.write('<ar><k>' + row[0] + '</k><def><deftext>' + row[1] + '</deftext></def></ar>')
    df.write('</lexicon></xdxf>')


if __name__ == '__main__':
    txt = './lex.txt'
    db = './lex_big_3.db'
    xdxf = './lex.xdxf'
    connect = create_db(db)
    # parse_txt_to_db(txt, connect)
    parse_db_to_xdxf(xdxf, connect)

    connect.close()


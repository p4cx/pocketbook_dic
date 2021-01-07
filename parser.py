import sqlite3
import re
import sys


def create_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def parse_txt_to_db(lex_file, conn):
    fh = open(lex_file)
    #fh = ["% weight/weight  <% w/w\tGewichtsprozent  <Gew.-%, %   ",
    # "fen orchid [Liparis loeselii, syn.: Ophrys loeselii]\tSumpf-Glanzorchis Sumpfglanzorchis"]
    counter = 0
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE lex ([id] INTEGER PRIMARY KEY,[eng] text, [ger] text)')
    conn.commit()
    for line_num, line in enumerate(fh):
        if not line.startswith(('#', ' ', '\n')):
            print(">> " + line)
            eng = line.split('\t', 1)[0]
            ger = line.split('\t', 1)[1]
            
            eng = re.sub(r'\(.*\)', '', eng)
            eng = re.sub(r'\[.*\]', '', eng)
            eng = re.sub(r'\{.*\}', '', eng)
            ger = re.sub(r'\(.*\)', '', ger)
            ger = re.sub(r'\[.*\]', '', ger)
            ger = re.sub(r'\{.*\}', '', ger)
            #eng = re.sub(r'[^\w]', ' ', eng)
            #ger = re.sub(r'[^\w]', ' ', ger)
            eng = re.sub(r'\s+', ' ', eng)
            ger = re.sub(r'\s+', ' ', ger)
            
            sub_list = ['<','>','verb','adj','noun','adv', 'past p',
                'pres-p', 'past-p', 'prep', 'conj', 'pron', 'prefix', 'suffix', '\t','\n'] 
            for sub in sub_list: 
                eng = eng.replace(sub, '')
                ger = ger.replace(sub, '')
            eng = eng.strip()
            ger = ger.strip()
            
            if " " != eng or " " != ger or "" != eng or "" != ger:
                cursor.execute('INSERT INTO lex VALUES (' + str(line_num) + ', "' + eng + '", "' + ger + '")')
                conn.commit()
                print(eng, " | ", ger)
    fh.close()


def parse_db_to_xdxf(xdxf_file, conn):
    df = open(xdxf_file, 'a')
    cursor = conn.cursor()
    cursor.execute('SELECT eng, GROUP_CONCAT(ger) FROM LEX GROUP BY eng Order by id asc')
    df.write('<?xml version="1.0" encoding="UTF-8" ?>' + 
    '<!DOCTYPE xdxf SYSTEM \"https://raw.github.com/soshial/xdxf_makedict/master/format' + 
    '_standard/xdxf_strict.dtd\">\n<xdxf lang_from=\"ENG\" lang_to=\"DEU\" format=\"logical\" ' +       'revision=\"033\">\n<meta_info>\n<title>ENG-GER Dictionary</title>\n<full_title>ENG-GER ' +         'Dictionary based on dict.cc</full_title>\n</meta_info>\n<lexicon>')
    for row in cursor:
        df.write('<ar><k>' + row[0] + '</k><def><deftext>' + row[1] + '</deftext></def></ar>\n')
    df.write('</lexicon></xdxf>')


if __name__ == '__main__':
    txt = './lex.txt'
    db = './lex_big_3.db'
    xdxf = './lex.xdxf'
    connect = create_db(db)
    parse_txt_to_db(txt, connect)
    parse_db_to_xdxf(xdxf, connect)

    connect.close()


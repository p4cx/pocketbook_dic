import argparse
import pathlib
import os
import sqlite3
import re
import sys


def uniquify_file(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def remove_text_inside_brackets(text, brackets="()[]{}"):
    """Remove text inside brackets from the input text."""
    stack, result = [], []
    pair = {brackets[i]: brackets[i+1] for i in range(0, len(brackets), 2)}
    
    for char in text:
        if char in pair:
            stack.append(char)
        elif char in pair.values() and stack and pair[stack[-1]] == char:
            stack.pop()
        elif not stack:
            result.append(char)
    
    return ''.join(result)


def parse_txt_to_db(lex_file, conn):
    """Parse the txt file into the database."""
    with open(lex_file, encoding="utf-8") as fh:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lex (
                            id INTEGER PRIMARY KEY,
                            eng TEXT,
                            ger TEXT,
                            level INTEGER,
                            eng_words TEXT,
                            typ TEXT,
                            category TEXT
                        )''')
        conn.commit()

        for line_num, line in enumerate(fh):
            if line.startswith(('#', ' ', '\n')):
                continue
            
            line = re.sub(r'\<|\>', '\'', line)
            entry_arr = line.split('\t')
            entry_arr[3] = entry_arr[3].strip()

            eng_word_string = entry_arr[1]
            if any(x in eng_word_string for x in '()[]{}'):
                eng_word_string = remove_text_inside_brackets(eng_word_string)

            eng_word_chunk_list = [chunk.rstrip(',;.!?:') for chunk in eng_word_string.split(' ')]
            word_pattern = re.compile(r"^[\À-ÿĀ-ſƀ-ȳa-zA-Z0-9-']+$")
            word_list = []

            for chunk in eng_word_chunk_list:
                if word_pattern.match(chunk) and chunk != 'to':
                    for sub in ['sth.', 'sb.', '\'s', 's\'']:
                        chunk = chunk.replace(sub, '')
                    if chunk:
                        word_list.append(chunk)

            sys.stdout.write(f'#[{line_num}]\r')

            cursor.execute('''
                INSERT INTO lex (eng, ger, level, eng_words, typ, category) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                entry_arr[1].strip(),
                entry_arr[0].strip(),
                len(word_list),
                " ".join(word_list).strip(),
                entry_arr[2].strip(),
                " ".join(entry_arr[3:]).strip()
            ))

        conn.commit()


def parse_db_to_xdxf(xdxf_file, conn):
    """Parse the database and write it to an XDxf file."""
    with open(xdxf_file, 'a', encoding="utf-8") as df:
        df.write('<?xml version="1.0" encoding="UTF-8" ?>\n'
                 '<xdxf lang_from="eng" lang_to="de" format="visual">\n'
                 '<full_name>DICT.CC Wörterbuch EN-DE</full_name>\n'
                 '<description>\n'
                 'Generated with https://github.com/p4cx/pocketbook_dic based on data from dict.cc\n'
                 '</description>\n'
                 '<lexicon>\n')

        dest = sqlite3.connect(':memory:')
        conn.backup(dest)
        cursor = dest.cursor()
        cursor.execute('DELETE FROM lex WHERE level >= 2')
        cursor.execute('SELECT DISTINCT(eng_words) FROM LEX WHERE level = 1 ORDER BY eng_words ASC')
        entry_term_list = cursor.fetchall()

        for i, (entry_term,) in enumerate(entry_term_list):
            entry_term_string = entry_term.replace("'", "\'")
            xdxf_collect = f'<ar><k>{entry_term_string}</k><def>\n'

            entry_list = cursor.execute("""
                SELECT eng, GROUP_CONCAT(CONCAT(ger, ' ', category), '; '), typ 
                FROM lex 
                WHERE level = 1 AND eng_words = ? 
                GROUP BY eng 
                ORDER BY CASE typ 
                  WHEN 'noun' THEN 0 
                  WHEN 'verb' THEN 1 
                  WHEN 'adj' THEN 2 
                  WHEN 'adv' THEN 3 
                END,
                LENGTH(eng)
            """, (entry_term_string,))

            for entry in entry_list:
                eng, ger, typ = entry
                eng = eng.replace('] [', '][').replace('  ', ' ')
                ger = ger.replace('] [', '][').replace('  ', ' ').replace(' ;', ';')
                if typ:
                    xdxf_collect += f'<b>{eng}</b> <i>{typ}</i> → {ger}\n'
                else:
                    xdxf_collect += f'<b>{eng}</b> → {ger}\n'

            df.write(f'{xdxf_collect}</def></ar>\n')
            sys.stdout.write(f'#[{i}]\r')

        df.write('</lexicon></xdxf>')


def main():
    """Main function to handle command-line arguments and orchestrate the process."""
    parser = argparse.ArgumentParser(
        prog='DICT.CC TO POCKETBOOK DICT EN-DE CONVERTER',
        description='Convert a vocabulary file from dict.cc into the xdxf format for Pocketbook e-readers.',
        epilog='Written under the influence of caffeine - License MIT'
    )

    parser.add_argument('-i', '--input_vocabulary', help="Path to dict.cc vocabulary file.", type=pathlib.Path)
    parser.add_argument('-d', '--db_file', help="Path to the SQLite database file.", type=pathlib.Path)
    parser.add_argument('-o', '--output_file', help="Path to save the xdxf file.", type=pathlib.Path)

    args = parser.parse_args()
    run_mode = 0

    if args.input_vocabulary and os.path.exists(args.input_vocabulary):
        print(f"Vocabulary file: {args.input_vocabulary}")
        run_mode = 1
    else:
        print("No vocabulary file provided.")
        if args.db_file and os.path.exists(args.db_file):
            run_mode = 2
        else:
            print("Error: Please specify a dict.cc vocabulary file with -i or --input_vocabulary "
                  "or specify an SQLite database file with -d or --db_file.")
            sys.exit(1)

    if args.db_file:
        print(f"Database file: {args.db_file}")
    else:
        print("No database file provided.")
        if args.input_vocabulary:
            args.db_file = uniquify_file(f"{args.input_vocabulary}.db")
            print(f"Database file: {args.db_file} will be created.")

    if args.output_file:
        print(f"xdxf file: {args.output_file}")
    else:
        print("No xdxf file provided.")
        args.output_file = uniquify_file(f"{args.input_vocabulary}.xdxf")
        print(f"xdxf file: {args.output_file} will be created.")

    if run_mode == 1:
        print("Parse the dict.cc vocabulary file.")
        connect = sqlite3.connect(args.db_file)
        parse_txt_to_db(args.input_vocabulary, connect)
        parse_db_to_xdxf(args.output_file, connect)
    elif run_mode == 2:
        print("Ignore the dict.cc vocabulary file if provided, as an existing database file was specified.")
        connect = sqlite3.connect(args.db_file)
        parse_db_to_xdxf(args.output_file, connect)
    else:
        print("Error: Something is wrong :(")
        sys.exit(1)

    connect.close()


if __name__ == '__main__':
    main()

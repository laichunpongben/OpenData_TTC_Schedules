import os
import sqlite3


def init_tables():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    tables = [f[:-4] for f in sorted(os.listdir(folder_path)) if f.endswith('.txt')]

    conn = sqlite3.connect(os.path.join(folder_path, 'ttc_schedules.db'))
    with conn:
        for table in tables:
            with open(os.path.join(folder_path, '{}.txt'.format(table)), 'r') as table_txt:
                lines = table_txt.read().splitlines()

            conn.execute("DROP TABLE IF EXISTS {0}".format(table))
            conn.execute("CREATE TABLE {0} ({1})".format(table, lines[0]))

            header = lines[0].split(',')
            placeholder = '?,' * (len(header) - 1) + '?'
            values = [tuple(line.split(',')) for line in lines[1:]]
            conn.executemany("INSERT INTO {0} VALUES ({1})".format(table, placeholder), values)

if __name__ == '__main__':
    import time

    start = time.time()
    init_tables()
    end = time.time()
    lapsed = end - start
    print('lapsed: {0}'.format(lapsed))

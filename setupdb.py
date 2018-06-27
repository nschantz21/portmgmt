import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect('portmgmt2.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    
    c = conn.cursor()
    
    with open('setupdb.sql', 'r') as f:
        c.executescript(f.read())

    conn.commit()
    conn.close()

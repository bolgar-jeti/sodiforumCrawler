import sqlite3
import sys

con=sqlite3.connect("sodiforum.db")
cur=con.cursor()

if ("select" not in sys.argv[1]):
    cur.execute(sys.argv[1])
else:
    if (len(sys.argv)>1):
        for row in (cur.execute(sys.argv[1]).fetchall()):
                print(row)
con.commit()
con.close()
input("END")
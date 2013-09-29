import sqlite3 as lite
import sys

con = None

try:
  con = lite.connect('moztnbot.db')

  cur = con.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT, url TEXT)")
except lite.Error, e:
  f = open("/var/log/moztnbot.log", "a")
  f.write('[SQLite Error]: %s\n' % e.args[0])
  f.close()
  sys.exit(1)

finally:

  if con:
    con.close()

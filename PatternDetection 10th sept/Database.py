import MySQLdb, csv, sys
conn = MySQLdb.connect (host = "localhost",user = "root", passwd = "",db = "AAMeetings")
cur = conn.cursor()
cur2 = conn.cursor()
cur.execute("SELECT userID FROM testtable")
for i in range(cur.rowcount):	
	row = cur.fetchone()
	print row[0]
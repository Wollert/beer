import MySQLdb

db = MySQLdb.connect(user="beeruser",db="beerdb")
c = db.cursor()
c.execute("""SELECT now()-Time, Flag from Times WHERE ID = 5""")
#print c.fetchall()[0][0]
[time_on, state] =  c.fetchone()
print time_on
print state

#c.execute("""UPDATE Times SET Time=Now(), Flag = 1 WHERE ID = %s""",(self.dbid))
#db.commit()

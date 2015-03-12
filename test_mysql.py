import MySQLdb

db = MySQLdb.connect(user="beeruser", db="beerdb")

c = db.cursor()

id = 1

#c.execute("""SELECT Value from Temperature where ID = %s""", (id,))
c.execute("""SELECT Value from Temperature""")

print c.fetchall()

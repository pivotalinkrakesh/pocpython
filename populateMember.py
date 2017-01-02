import cx_Oracle
import json
import random

def main():
	print 'In Main..'
	#conn=jaydebeapi.connect('org.hsqldb.jdbcDriver',['jdbc:hsqldb:hsql://localhost/', 'SA', ''],'C:/Users/cho922/.m2/repository/org/hsqldb/hsqldb/2.3.3/hsqldb-2.3.3.jar',)
	#cursor = conn.cursor()
	cursor = initOracle()
	randomRecords = sorted([random.randrange(20) for n in range(10)])

	#membersToLoad = readFile("C:\\spring-workspace\\json-data-generator-1\\src\\dist\\conf\\memberIdsData_6879622688657050390.json");
	membersToLoad = readFile("../JsonDatagenerator/json-data-generator-1.2.6-Pivotalink/conf/memberIdsData_6879622688657050390.json");
	
	readMembersData(cursor)
	
	inserMembers(cursor, membersToLoad)
	readMembersData(cursor)
	cursor.close()
	conn.close()
	# read data

def initOracle():
	conn = cx_Oracle.connect('system', 'pass_4Temp', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	cursor = conn.cursor()
	return cursor

def initHSQL():
	#import jaydebeapi
	conn=jaydebeapi.connect('org.hsqldb.jdbcDriver',['jdbc:hsqldb:hsql://localhost/', 'SA', ''],'C:/Users/cho922/.m2/repository/org/hsqldb/hsqldb/2.3.3/hsqldb-2.3.3.jar',)


def inserMembers(cursor, memberIds):
	#cur.bindarraysize=100
	for member in memberIds:
		print member
		#cursor.executemany('insert into json_members (json_doc) values(:1)
		cursor.prepare('insert into json_members (memberid) values(:1)')
		cursor.execute(None, {1,member})
		#cursor.execute('insert into json_members (memberid) values(' +member +')')
		commit

def readMembersData(cursor):

	print "Reading member data"
	cursor.execute('select * from json_members ')
	colnames = [desc[0] for desc in cursor.description]
	print colnames
	count = 0
	for row in cursor.fetchall():
		count += 1
		for (name, value) in zip(colnames, row):
			print name, '\t->', value
			print
	print "Total Records %d", count



def readFile(filename):
	print 'Reading file %s', filename
	rows = open(filename, 'r')
	memberIds = [] 
	for row in rows.readlines():
		#print 'row:' + row)
		_tmp = row.strip('[')
		_tmp = _tmp.strip(']')
		row = _tmp.strip(',\n')
		print row)
		if(row.strip()):
			_data = json.loads(row)
			memberIds.append(_data.get('memberId'))
		#print _data.get('memberId'))

	#print "dict data",props
	#print (memberIds)
	return memberIds


if __name__ == '__main__': # self test
	main()

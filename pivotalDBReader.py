#import perf
defaultpropertiesfile = 'inquirer.properties'

def readFile(filename):
	print 'Reading file %s', filename
	propsfile = open(filename, 'r')
	props = {}
	for line in propsfile.readlines():
		if(line.strip()):
			#print line
			if(line.find('#') <0):
				key,val = line.split('=',1)
				props[key]=val.strip('\n')

	#print "dict data",props
	
	return props

def executeQueries(props):
	connection = initOracle(props);	
	cursor = connection.cursor()

	queries=[]
	params=[]

	for k in sorted(props.keys()):
		match = re.search(r'\.query', k)
		if(match):
			query = props.get(k)
			match  = re.search(r'\?', query)
			if (not match):
				print '### Executing query id:{} sql:{}'.format(k,query)
				start = time.time()
				cursor.execute(query, params)
				rs = cursor.fetchone()
				if(rs):
					print '!@#$ ', len(rs)
					result = rs[0]
				else:
					result = 'null'
				elapsed = (time.time() - start)	
				print 'result {} took {}'.format(result, elapsed)
		

def init():
	file = defaultpropertiesfile		
	if(len(sys.argv) >= 2):
		file = sys.argv[1]	
	#print('using property file ', file)
	props = readFile(file)
	return props
	
def initOracle(props):
	import cx_Oracle
	print props.get('db.oracle.userId')
	print props.get('db.oracle.passwd')
	print props.get('db.oracle.connectString.python')
	#print 'user:%s, pwd:%s, server:%s' %(props.get('db.oracle.userId'), props.get('db.oracle.passwd'), props.get('db.oracle.connectString.python'))
	#conn = cx_Oracle.connect(props.get('db.oracle.userId'), props.get('db.oracle.passwd'), props.get('db.oracle.connectString.python'))
	conn = cx_Oracle.connect('system', 'pass_4Temp', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	return conn


def main():
	properties = init()	
	executeQueries(properties)


if __name__ == '__main__':
	import sys
	import re
	import time
	main()

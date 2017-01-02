#import perf
defaultpropertiesfile = 'inquirer.properties'

def readFile(filename):
	propsfile = open(filename, 'r')
	props = {}
	for line in propsfile.readlines():
		if(line.strip()):
			key,val = line.split('=',1)
			props[key]=val.strip('\n')

	#print "dict data",props
	return props

def executeQueries(props):
	connection = initOracle(props);	
	#cursor = connection.cursor()

	queries=[]
	for k in props.keys():
		match = re.search(r'\.query', k)
		if(match):
			queries.append(props.get(k))

	for query in queries:
		#print (query)
		#print(type(query))
		match  = re.findall(r'\?', query)
		if (not match):
			#print(len(query))
			#print (query.find('\?'))
			#print ('Executing query...', query)
			start = time.time()
			#cursor.execute(query)
			elapsed = (time.time() - start)	
			#print (elapsed, ' seconds')	
			

def init():
	file = defaultpropertiesfile		
	if(len(sys.argv) >= 2):
		file = sys.argv[1]	
	#print('using property file ', file)
	props = readFile(file)
	return props
	
def initOracle(props):
	print('skiiping initOracle')
	#import cx_Oracle
	
	print('user:{} pwd:{} server:{}'.format(props.get('db.oracle.userId'), props.get('db.oracle.passwd'), props.get('db.oracle.connectString.python')))
	#print ('user:{}, pwd:{}, server:{}'.format((props.get('db.oracle.userId'), props.get('db.oracle.passwd'), props.get('db.oracle.connectString.python'))
	#conn = cx_Oracle.connect(props['db.oracle.userId'], props['db.oracle.passwd'], props['db.oracle.connectString.python'])
	#return conn


def main():
	properties = init()	
	executeQueries(properties)


if __name__ == '__main__':
	import sys
	import re
	import time
	main()

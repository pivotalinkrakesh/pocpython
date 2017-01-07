#import perf
defaultpropertiesfile = 'inquirer.properties'

def readFile(filename):
	print 'Reading file {}'.format(filename)
	propsfile = open(filename, 'r')
	props = {}
	for line in propsfile.readlines():
		if(line.strip()):
			#print line
			if(line.find('#') <0):
				match = re.search(r'QUERY', line)
				if(match):
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
		query = props.get(k)
		#print '### Executing query id:{} sql:{}'.format(k,query)
		start = time.time()

		cursor.execute(query, params)
		
		if(k.find('COUNT') >=0):
			rs = cursor.fetchone()
			result = rs[0]
		else:
			count=0
			for row in cursor.fetchall():
				count += 1
			
			result = count
			
		elapsed = time.time() - start
		print 'query {}, {}, {} '.format(k, elapsed, result)
		

def init():
	file = defaultpropertiesfile		
	if(len(sys.argv) >= 2):
		file = sys.argv[1]	
	#print('using property file ', file)
	props = readFile(file)
	return props
	
def initOracle(props):
	conn = cx_Oracle.connect('med_json', 'med_json', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	return conn


def main():
	start = time.time()
	properties = init()	
	executeQueries(properties)
	elapsed = (time.time() - start)	
	print '### Total execution time {} seconds'.format(elapsed)


if __name__ == '__main__':
	import sys
	import re
	import time
	import cx_Oracle
	main()

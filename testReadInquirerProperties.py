#import perf
import sys
import re
import time

defaultpropertiesfile = 'inquirer.properties'

def readFile(filename):
	print ('Reading file %s' % (filename))
	propsfile = open(filename, 'r')
	props = {}
	for line in propsfile.readlines():
		if(line.strip()):
			#print line
			if(line.find('#') <0):
				key,val = line.split('=',1)
				props[key]=val.strip('\n')

	print ("dict data",props)
	
	return props

def main():
	start = time.time()
	properties = init()	
	#executeQueries(properties)
	elapsed = (time.time() - start)	
	print ('### Total execution time %s seconds' % (elapsed))


def init():
	file = defaultpropertiesfile		
	if(len(sys.argv) >= 2):
		file = sys.argv[1]	
	#print('using property file ', file)
	props = readFile(file)
	return props


if __name__ == '__main__':
	#import cx_Oracle
	main()

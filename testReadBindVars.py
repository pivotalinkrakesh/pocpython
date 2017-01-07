import cx_Oracle
import sys
import json
import cx_Oracle
import random
import time

DATA_MISSING='PROF'
defaultpropertiesfile = 'processEpisodeClaims.properties'
readsize=1000
## global properties
props = {}

claimfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']

rxclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']
instclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processEndDate']
professionalclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']

episodefields=[]

episodeSidList=[]
membersList=[]
episodesidrange=5000
	
def getEpisodeJson(claimDict):
	_jsonDict = {}
	for i in range(len(episodefields)):
		if(episodefields[i] == 'episodeSid'):
			_jsonDict[claimfields[i]]=claimDict.get(episodefields[i], getRandomEpisodesid())
		else:
			_jsonDict[claimfields[i]]=claimDict.get(episodefields[i], DATA_MISSING)
	#print ('Json data is %s', (json.dumps(_jsonDict)))
	return json.dumps(_jsonDict)

def getRandomEpisodesid():
	return episodeSidList[random.randrange(episodesidrange)]

def populateEpisodeSids():
	global episodeSidList
	filename='/home/opc/JsonDatagenerator/json-data-generator-1.2.6-Pivotalink/conf/episodeSidData_5856712544197501077.json'
	print 'populateEpisodeSids from file {}'.format(filename)
	propsfile = open(filename, 'r')
	for line in propsfile.readlines():
		if(line.strip()):
			if(line.find(',') >= 0):
				sidjson = json.loads(line[:-3])
			else:
				sidjson = json.loads(line[:-2])
			#print sidjson.get('episodeSid')
			episodeSidList.append(sidjson.get('episodeSid'))
	#print episodeSidList

def populateFromRxClaims():
	global episodefields
	print('populating from PJ_RXClaims..')
	episodefields=rxclaimsfields
	populateEpisodeClaimFromTable('PJ_RXCLAIMS')

def populateFromInstClaims():
	global episodefields
	print('populating from PJ_INSTCLAIMS..')
	episodefields=instclaimsfields
	populateEpisodeClaimFromTable('PJ_INSTCLAIMS')

def populateFromProfessionalClaims():
	global episodefields
	print('populating from PJ_PROFESSIONALCLAIMS..')
	episodefields=professionalclaimsfields
	populateEpisodeClaimFromTable('PJ_PROFESSIONALCLAIMS')

def populateEpisodeClaimFromTable(tableName):
	global membersList

	start = time.time()
	print 'loading from table:{}'.format(tableName)
	connection = initOracle()	
	cursor = connection.cursor()

	query = "select xx.json_document from " + tableName + " xx where xx.json_document.memberId in %s" % str(tuple(membersList)).replace(',)',')')

	print 'Executing select on {} using query {}...'.format(tableName, query)
	cursor.arraysize = readsize
	cursor.execute(query, [])
	count=0
        for result in cursor.fetchall():
                _json = json.loads(result[0])
                print 'Data {}'.format(_json)
         	count = count + 1

        cursor.close()
        connection.close()

	elapsed = (time.time() - start)	
	print 'Inserted {} records from Table:{} and took {} seconds'.format(count, tableName, elapsed)


def processEpisodeClaims():
	populateFromRxClaims()

def readMembersData():
	global membersList
	#membersList= ['brRv24283381fcALAl', 'nLiB80843933FLaLWo']
	membersList= ['brRv24283381fcALAl']
	print 'membersList is {}'.format(membersList)
	
def init():

	readMembersData()

def readProperties(filename):
	print 'Reading properties file {} '.format(filename)
	global props
	propsfile = open(filename, 'r')
	for line in propsfile.readlines():
		if(line.strip()):
			key,val = line.split('=',1)
			props[key]=val.strip('\n')

def initOracle():
	try:
		conn = cx_Oracle.connect('med_json', 'med_json', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	except cx_Oracle.DatabaseError, exception:
		printf ('Failed to connect to %s\n','med_json')
		printException (exception)
		exit (1)

	return conn


def main():
	start = time.time()

	init()
	processEpisodeClaims()

	elapsed = (time.time() - start)	
	print '### Total execution time {} seconds'.format(elapsed)

if __name__== '__main__':
	main()

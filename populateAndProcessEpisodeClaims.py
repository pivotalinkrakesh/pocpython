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

rxclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processEndDate']
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
	print('populating from JSON_RXClaims..')
	episodefields=rxclaimsfields
	populateEpisodeClaimFromTable('JSON_RXCLAIMS')

def populateFromInstClaims():
	global episodefields
	print('populating from JSON_INSTCLAIMS..')
	episodefields=instclaimsfields
	populateEpisodeClaimFromTable('JSON_INSTCLAIMS')

def populateFromProfessionalClaims():
	global episodefields
	print('populating from JSON_PROFESSIONALCLAIMS..')
	episodefields=professionalclaimsfields
	populateEpisodeClaimFromTable('JSON_PROFESSIONALCLAIMS')

def populateEpisodeClaimFromTable(tableName):
	global membersList
	print 'loading from table:{}'.format(tableName)
	connection = initOracle()	
	cursor = connection.cursor()
	params=[]
	
	query = 'select xx.json_doc from ' + tableName + ' xx where xx.json_doc.memberId in :1'
	try:
		cursor.prepare(query)
	except cx_Oracle.DatabaseError, exception:
		printf ('Failed to prepare query %s\n',query)
		printException (exception)
		exit (1)

	print 'Executing select on {} using query {}...'.format(tableName, query)
	start = time.time()
	cursor.arraysize = readsize
	cursor.execute(None, membersList)
	
	# get another connection
	conn2 = initOracle()
	cursor2=conn2.cursor()
	cursor2.prepare("insert into json_episodeclaims (json_doc) values(:1)")
        count = 0
        massiveData=[]

        for result in cursor.fetchall():
                _json = json.loads(result[0])
                del massiveData[:]
                #print 'Data {}'.format(_json)
              	massiveData.append(getEpisodeJson(_json))
		#print 'inserting {} into json_episodeclaims'.format(massiveData)
		cursor2.execute(None, massiveData)
         	count = count + 1
        
        cursor2.close()
        conn2.commit()
        conn2.close()

        cursor.close()
        connection.close()

        print "Total Records Inserted {}".format(count)
	
	elapsed = (time.time() - start)	
	print elapsed, ' seconds'


def processEpisodeClaims():

	#'''Read n members with status='Active' randomly from members table '''
	#''' Delete from json_episodeclaims where memberId in n
	#'''	read rxClaims by member id and insert into episodeClaims '''
	#'''	read proClaims by member id and insert into episodeClaims, validate provider against provider table '''
	#'''	read instClaims by member id and insert into episodeClaims, validate provider against provider table '''
	#'''		

	deleteEpisodeClaims()
	populateFromRxClaims()
	populateFromInstClaims()
	populateFromProfessionalClaims()

def deleteEpisodeClaims():
	connection = initOracle();	
	cursor = connection.cursor()
	print 'Deleting from episodeclaims'

	cursor.prepare('delete from json_episodeclaims rx where rx.json_doc.memberId=:memberid')

	for member in membersList:
		try:
			cursor.execute(None, memberid=member)		
			#result = cursor.fetchone()
			#print 'delete returned {}'.format(result)
		except cx_Oracle.DatabaseError, exception:
			printf ('Failed to execute cursor\n')
			printException (exception)
			exit (1)	

	cursor.close()
	connection.commit()
	connection.close()


def readMembersData():
	global membersList
	# get connection
	conn = initOracle()
	# read members data into a collection.
	cursor = conn.cursor()
	cursor.execute("select members.json_doc.baseKey from json_members members where members.json_doc.status = \'Accepted\'")
	_count=0
	_randList = getRandomList()
	
	randomMember=_randList.pop(0)
	for result in cursor.fetchall():
		_count += 1
		if(_count == randomMember):
			membersList.append(result[0])
			if len(_randList) >0:
				randomMember=_randList.pop(0)
			else:
				break
	print 'membersList is {}'.format(membersList)
	
	
def getRandomList():
	# Get Total Records from Table where status='Active'.
	#cursor.execute('select count(*) from members where json_doc.id=\"Active\"')
	#totalrecs = cursor.fetch()
	# for sake of POC we know we have 1999 members
	totalrecs = 1999

	# Number of records to process
	nummembers = int(props.get('membersToProcess'))
	print "Random member records to process {}".format(nummembers)
	
	# save random number in a list.
	_randList = []
	for i in range(nummembers):
		_randList.append(random.randrange(totalrecs))
		_randList.sort()
	print _randList
	return _randList

def init():
	file = defaultpropertiesfile		
	if(len(sys.argv) >= 2):
		file = sys.argv[1]	

	readProperties(file)

	populateEpisodeSids()
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
	import cx_Oracle
	try:
		conn = cx_Oracle.connect('system', 'pass_4Temp', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	except cx_Oracle.DatabaseError, exception:
		printf ('Failed to connect to %s\n',databaseName)
		printException (exception)
		exit (1)

	return conn


def main():
	init()
	processEpisodeClaims()

if __name__== '__main__':
	main()

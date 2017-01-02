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
	print episodeSidList

def populateEpisodeClaims():
	#populateFromRxClaims()
	#populateFromInstClaims()
	populateFromProfessionalClaims()


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

	print 'loading from table:{}'.format(tableName)
	connection = initOracle()	
	cursor = connection.cursor()
	params=[]
	
	query = 'select json_doc from ' + tableName
	print 'Executing select on {} using query {}...'.format(tableName, query)
	start = time.time()
	cursor.arraysize = readsize
	cursor.execute(query, params)
	
	# get another connection
	conn2 = initOracle()
	cursor2=conn2.cursor()
	cursor2.prepare("insert into json_episodeclaims (json_doc) values(:1)")
        count = 0
        commitCount=0
        massiveData=[]

        for result in cursor.fetchall():
                _json = json.loads(result[0])
                del massiveData[:]
                #print 'Data {}'.format(_json)
              	massiveData.append(getEpisodeJson(_json))
		#if(commitCount >= 100):
			#reset commit count.
			#cursor2.executemany(None,massiveData)
			#conn2.commit()
			#commitCount=0
		#print 'inserting {} into json_episodeclaims'.format(massiveData)
		cursor2.execute(None, massiveData)
		conn2.commit()
         	count = count + 1
                #commitCount += 1
        
        cursor2.close()
        conn2.close()
        cursor.close()
        connection.close()
        print "Total Records Inserted {}".format(count)
	
	elapsed = (time.time() - start)	
	print elapsed, ' seconds'


def processEpisodeClaims(props):

	'''Read n members with status='Active' randomly from members table '''
	''' Delete from json_episodeclaims where memberId in n
	'''	read rxClaims by member id and insert into episodeClaims '''
	'''	read proClaims by member id and insert into episodeClaims, validate provider against provider table '''
	'''	read instClaims by member id and insert into episodeClaims, validate provider against provider table '''
	'''		

	connection = initOracle();	
	cursor = connection.cursor()

	
	cursor.execute('select json_doc from json_members where json_doc._id=\"Active\"')

        #colnames = [desc[0] for desc in cursor.description]
        #print(colnames)
        count = 0
        for row in cursor.fetchall():
                #print(row)
                
                _jsondata = json.loads(row)
                
                count = count + 1
                for (name, value) in zip(colnames, row):
                        print(name, '\t->', value)
                        print


	queries=[]
	for k in props.keys():
		match = re.search(r'\.query', k)
		if(match):
			queries.append(props.get(k))

	params=[]
	for query in queries:
		match  = re.search(r'\?', query)
		if (not match):
			print 'Executing query...', query
			start = time.time()
			cursor.execute(query, params)
			elapsed = (time.time() - start)	
			print elapsed, ' seconds'



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
	i=0
	for result in cursor.fetchall()
		_count += 1
		if(_count == randomMember):
			memberList[i]=result[0]
			i += 1
			if len(_randList) >0:
				randomMember=_randList.pop(0)
			else:
				break
	print 'memberList is {}'.format(membersList)
	
	
def getRandomList():
	# Get Total Records from Table where status='Active'.
	#cursor.execute('select count(*) from members where json_doc.id=\"Active\"')
	#totalrecs = cursor.fetch()
	# for sake of POC we know we have 1999 members
	totalrecs = 1999

	# Number of records to process
	nummembers = props.get('membersToProcess')
	print("Random member records to process", nummembers)
	
	# save random number in a list.
	_randList = []
	for i in range nummembers:
	_randList.append(randrange(totalrecs))
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
	print 'Reading file %s', filename
	propsfile = open(filename, 'r')
	for line in propsfile.readlines():
		if(line.strip()):
			key,val = line.split('=',1)
			props[key]=val.strip('\n')

def initOracle():
	import cx_Oracle
	conn = cx_Oracle.connect('system', 'pass_4Temp', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	return conn


def main():
	init()
	populateEpisodeClaims()

if __name__== '__main__':
	main()

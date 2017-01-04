import json
import cx_Oracle
import random
import time

DATA_MISSING='PROF'
defaultpropertiesfile = 'inquirer.properties'
readsize=1000

claimfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']

rxclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']
instclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processEndDate']
professionalclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']

episodefields=[]

episodeSidList=[]
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

def readEpisodeSidsFile(episodeSidList):
	filename='/home/opc/JsonDatagenerator/json-data-generator-1.2.6-Pivotalink/conf/episodeSidData_5856712544197501077.json'
	print 'Reading file %s', filename
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
	return episodeSidList


def populateEpisodeClaims():
	populateFromRxClaims()
	populateFromInstClaims()
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
	start = time.time()
	
	connection = initOracle()	
	cursor = connection.cursor()
	params=[]
	
	query = 'select json_document from ' + tableName
	#print 'Executing select on {} using query {}...'.format(tableName, query)

	cursor.arraysize = readsize
	cursor.execute(query, params)
	
	# get another connection
	conn2 = initOracle()
	cursor2=conn2.cursor()
	cursor2.prepare("insert into hyb_episodeclaims (json_document, memberid, \"_ID\") values(:json,:memberId,:id)")
        count = 0
        massiveData={}
        # INSERT ONE RECORD
        #rs =cursor.fetchone()
        #_json = json.loads(rs[0])
        #print _json
        #jsondoc=getEpisodeJson(_json)
        #massiveData['json']=jsondoc
        #massiveData['memberId']=_json.get('memberId')
        #massiveData['id']=_json['_id']
	#print 'inserting {} into json_episodeclaims'.format(massiveData)
	#massiveData.append((jsondoc, 'false', _json['_id']))
	#cursor2.execute(None, massiveData)
	
        for result in cursor.fetchall():
                massiveData.clear()
                _json = json.loads(result[0])
                jsondoc=getEpisodeJson(_json)
		massiveData['json']=jsondoc
		massiveData['memberId']=_json.get('memberId')
		massiveData['id']=_json['_id']
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


def init():
	readEpisodeSidsFile(episodeSidList)


def initOracle():
	import cx_Oracle
	conn = cx_Oracle.connect('med_json', 'med_json', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	return conn


def main():
	start = time.time()
	init()
	populateEpisodeClaims()

	elapsed = (time.time() - start)	
	print '### Total execution time {} secnds'.format(elapsed)


if __name__== '__main__':
	main()
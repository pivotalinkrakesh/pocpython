import json
import cx_Oracle
import random
import time

DATA_MISSING='PROF'
defaultpropertiesfile = 'inquirer.properties'
readsize=1000

claimfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']

rxclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processEndDate']
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
        # INSERT ONE RECORD
        #rs =cursor.fetchone()
        #_json = json.loads(rs[0])
	#massiveData.append(getEpisodeJson(_json))
	#print 'inserting {} into json_episodeclaims'.format(massiveData)
	#cursor2.execute(None, massiveData)
	#conn2.commit()

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


def init():
	readEpisodeSidsFile(episodeSidList)


def initOracle():
	import cx_Oracle
	conn = cx_Oracle.connect('system', 'pass_4Temp', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	return conn


def main():
	init()
	populateEpisodeClaims()

if __name__== '__main__':
	main()

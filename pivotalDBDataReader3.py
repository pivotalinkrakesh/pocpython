#import perf
defaultTable = 'json_members'
DATA_MISSING='DATAMISSING'
episodefields=['_id', 'subClientId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processEndDate']
	
def getEpisodeJson(claimDict):
	_jsonDict = {}
	for field in episodefields:
		_jsonDict[field]=claimDict.get(field, DATA_MISSING)
	print(json.dumps(_jsonDict))

def executeQuery(tableName):
	conn = cx_Oracle.connect('system', 'pass_4Temp', '129.144.154.94:1521/pdb1.a428714.oraclecloud.internal')
	cursor = conn.cursor()
	params=[]
	
	query = 'select json_doc from ' + tableName
	print ('Executing select on {} using query {}...'.format(tableName, query))
	start = time.time()
	cursor.execute(query, params)
	
        #colnames = [desc[0] for desc in cursor.description]
        #print(colnames)
	count = 0
	for result in cursor.fetchall():
		_json = json.loads(result[0])
		#print 'Data _id is {} and status is {}'.format(_json.get('_id', 'DATAMISSING'), _json.get('_id', 'DATAMISSING'))
		count = count + 1
                #for (name, value) in zip(colnames, row):
                #        print(name, value)
                        
        #print "Total Records {}".format(count)
	
	elapsed = (time.time() - start)	
	#print elapsed, ' seconds'
		

def init():
	_table = defaultTable		
	if(len(sys.argv) >= 2):
		file = sys.argv[1]	
	return _table
	

def main():
	tableName = init()	
	executeQuery(tableName)
	

if __name__ == '__main__':
	import sys
	import re
	import time
	import json
	#import cx_Oracle
	_testrxClaim = '{\"baseKey\":\"fEhSgHT75Cfe73eT5\",\"filler\":1482547093545,\"_id\":\"fEhSgHT75Cfe73eT5--1482547093545\",\"clientId\":\"HCS\",\"subClientId\":\"NM1\",\"isLatest\":\"false\",\"processDate\":\"2015-06-25T08:17:52.000Z\",\"sourceIdentifier\":\"MIDV\",\"status\":\"Accepted\",\"memberId\":\"null\",\"dispensedDate\":\"2015-08-07T09:54:42.000Z\",\"ndc\":\"00591320201\",\"drugCodeDesc\":\"Hydrocodone-Acetaminophen Tab 5-325 MG\",\"productCodeDescAbbr\":\"HYDROCO/APAP TAB 5-325MG\",\"quantityDispensed\":53,\"daysSupply\":\"NumberLong(5)\",\"refillNumber\":\"0\",\"prescriptionNumber\":\"00000110144492169024\",\"copayAmount\":4.8,\"allowedAmount\":4.8,\"ingredientCost\":4.8,\"claimNumber\":\"WjubpByKajRQsrQvY\",\"prescriberId\":\"0098383UXNNMFW\",\"adjustmentTypeCode\":\"3\",\"orderingProviderDeaId\":\"0098383UXNNMFW\",\"pharmacyID\":\"UNKNOWN\",\"chargedDollarAmount\":7.92,\"deductible\":0,\"dispenseAsWrittenCode\":\"0\",\"dispenseFee\":2,\"groupID\":\"G1008635672\",\"healthPlanName\":\"H613018451\",\"patientFirstName\":\"Steve\",\"patientLastName\":\"Smith\",\"patientRelation\":\"1\",\"brandName\":\"G\",\"drugType\":\"G\",\"providerFirstName\":\"Steve\",\"providerLastName\":\"Loxly\",\"pcpFirstName\":null,\"pcpId\":\"UNKNOWN\",\"pcpLastName\":null,\"routeOfAdministration\":\"OR\",\"adminRouteDesc\":\"Oral\",\"gpi10Code\":\"6599170210\",\"gpi10Description\":\"Hydrocodone-Acetaminophen\",\"drugPackageSize\":100,\"drugPackageDescription\":\"BOTTLE\"}'
	json.loads(_testrxClaim)
	getEpisodeJson(json.loads(_testrxClaim))
	#main()

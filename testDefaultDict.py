import json
import random
import collections

DATA_MISSING='PROF'
rxclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processEndDate']
professionalclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']
instclaimsfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processEndDate']

claimfields=rxclaimsfields

claimfields=['_id', 'subClientId', 'memberId', 'episodeSid', 'claimNumber', 'claimLineNumber', 'claimType', 'processDate']
episodeSidList=[]

def getEpisodeJson(claimDict):
	_jsonDict = {}
	for i in range(len(episodefields)):
		if(episodefields[i] == 'episodeSid'):
			_jsonDict[claimfields[i]]=claimDict.get(episodefields[i], getRandomEpisodesid())
		else:
			_jsonDict[claimfields[i]]=claimDict.get(episodefields[i], DATA_MISSING)
	print ('Json data is %s', (json.dumps(_jsonDict)))
	#return json.dumps(_jsonDict)


def readEpisodeSidsFile(episodeSidList):
	filename='C:\\spring-workspace\\json-data-generator-1\\src\\dist\\conf\\episodeSidData_5856712544197501077.json'
	print ('Reading file %s', (filename))
	propsfile = open(filename, 'r')
	for line in propsfile.readlines():
		if(line.strip()):
			print (line[:-2])
			if(line.find(',') >= 0):
				sidjson = json.loads(line[:-2])
			else:
				sidjson = json.loads(line[:-1])
			#print sidjson.get('episodeSid')
			episodeSidList.append(sidjson.get('episodeSid'))
	#print episodeSidList
	return episodeSidList

def getRandomEpisodesid():
	episodeSidList=[1,2,3,4,5,6,7,8,9,10]
	return episodeSidList[random.randrange(10)]


if __name__== '__main__':
	#readEpisodeSidsFile(episodeSidList)

	rxClaimjson='{\"baseKey\":\"fEhSgHT75Cfe73eT5\",\"filler\":1482547093545,\"_id\":\"fEhSgHT75Cfe73eT5--1482547093545\",\"clientId\":\"HCS\",\"subClientId\":\"NM1\",\"isLatest\":\"false\",\"processDate\":\"2015-06-25T08:17:52.000Z\",\"sourceIdentifier\":\"MIDV\",\"status\":\"Accepted\",\"memberId\":\"null\",\"dispensedDate\":\"2015-08-07T09:54:42.000Z\",\"ndc\":\"00591320201\",\"drugCodeDesc\":\"Hydrocodone-Acetaminophen Tab 5-325 MG\",\"productCodeDescAbbr\":\"HYDROCO/APAP TAB 5-325MG\",\"quantityDispensed\":53,\"daysSupply\":\"NumberLong(5)\",\"refillNumber\":\"0\",\"prescriptionNumber\":\"00000110144492169024\",\"copayAmount\":4.8,\"allowedAmount\":4.8,\"ingredientCost\":4.8,\"claimNumber\":\"WjubpByKajRQsrQvY\",\"prescriberId\":\"0098383UXNNMFW\",\"adjustmentTypeCode\":\"3\",\"orderingProviderDeaId\":\"0098383UXNNMFW\",\"pharmacyID\":\"UNKNOWN\",\"chargedDollarAmount\":7.92,\"deductible\":0,\"dispenseAsWrittenCode\":\"0\",\"dispenseFee\":2,\"groupID\":\"G1008635672\",\"healthPlanName\":\"H613018451\",\"patientFirstName\":\"Steve\",\"patientLastName\":\"Smith\",\"patientRelation\":\"1\",\"brandName\":\"G\",\"drugType\":\"G\",\"providerFirstName\":\"Steve\",\"providerLastName\":\"Loxly\",\"pcpFirstName\":null,\"pcpId\":\"UNKNOWN\",\"pcpLastName\":null,\"routeOfAdministration\":\"OR\",\"adminRouteDesc\":\"Oral\",\"gpi10Code\":\"6599170210\",\"gpi10Description\":\"Hydrocodone-Acetaminophen\",\"drugPackageSize\":100,\"drugPackageDescription\":\"BOTTLE\"}'
	profClaimjson='{\"baseKey\":\"UKv6wkRNHSi2fAbtz\",\"claimLineNumber\":1,\"claimNumber\":\"8IvM80GqvmdoMN13i\",\"isLatest\":\"false\",\"processDate\":1482283624319,\"sourceIdentifier\":\"MIDg\",\"status\":\"Accepted\",\"memberId\":\"rmPp71886425gXCSSE\",\"subscriberId\":null,\"membershipId\":\"rmPp71886425gXCSSE\",\"allowedAmountClaimLevel\":3725.12,\"allowedAmountLineLevel\":76.04,\"claimAdjustmentTypeCode\":\"3\",\"claimReceivedDate\":1482283624362,\"_id\":\"8IvM80GqvmdoMN13i-1-1482283624362\",\"claimServicingProviderId\":\"UNKNOWN\",\"claimStatus\":\"1\",\"servicingProviderId\":\"UNKNOWN\",\"startOfServiceDate\":\"2016-05-14T08:21:32.000Z\",\"endOfServiceDate\":\"2016-11-06T20:22:42.000Z\",\"subClientId\":\"NM1\",\"subscriberDateOfBirth\":396390417000,\"subscriberFirstName\":\"Sarah\",\"subscriberGender\":\"F\",\"subscriberLastName\":\"Smith\",\"subscriberMiddleName\":null,\"typeOfService\":\"20\",\"clientId\":\"NM1\",\"divisionId\":\"G1441708933\",\"dxRelatedGroup\":\"690\",\"healthPlanCode\":\"H613018451\",\"organizationId\":\"E679287285\",\"placeOfService\":\"21\",\"placeOfServiceDesc\":\"Inpatient Hospital\",\"principalDx\":\"59010\",\"principalDxTypeCode\":\"BK\",\"dxCode0\":47256,\"dxCode1\":\"0539\",\"dxCode10\":null,\"dxCode11\":null,\"dxCode2\":\"25000\",\"dxCode3\":\"2768\",\"dxCode4\":null,\"dxCode5\":null,\"dxCode6\":null,\"dxCode7\":null,\"dxCode8\":null,\"dxCode9\":null,\"dxCodeType0\":\"BF\",\"dxCodeType1\":\"BF\",\"dxCodeType10\":null,\"dxCodeType11\":null,\"dxCodeType2\":\"BF\",\"dxCodeType3\":\"BF\",\"dxCodeType4\":null,\"dxCodeType5\":null,\"dxCodeType6\":null,\"dxCodeType7\":null,\"dxCodeType8\":null,\"dxCodeType9\":null,\"procedureOneCodeModifier1\":null,\"procedureOneCodeModifier2\":null,\"procedureOneCodeModifier3\":null,\"procedureOneCodeModifier4\":null,\"procedureTypeCode\":\"HC\",\"anesthesiaProcedureCode1\":null,\"anesthesiaProcedureCode2\":null,\"anesthesiaProcedureType1\":null,\"anesthesiaProcedureType2\":null,\"serviceSetcode\":\"J36001\",\"serviceSetDescription\":\"VENIPUNCTURE/BLOOD SPECIMEN COLLECTION\",\"serviceSetTypeCode\":\"P\",\"serviceSetTypeDescription\":\"Procedure\"}'

	#lookup= entrymap(

	testJson = profClaimjson
	episodefields=professionalclaimsfields
	
	_json = json.loads(testJson)
	## Convert java timestmp to date time
	#datetime.datetime.fromtimestamp(int("1483216985433"[:10])).strftime('%Y-%m-%d %H:%M:%S')
	
	print(_json.get('processEndDate'), _json.get('processDate'))

	print(_json.get('test', getRandomEpisodesid()))

	#dd = collections.defaultdict(getRandomEpisodesid())
	#dd = _json
	getEpisodeJson(_json)


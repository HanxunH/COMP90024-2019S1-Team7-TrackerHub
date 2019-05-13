import json
from files import lst 

resultDict = {}
outputfile = open("offence_results.json","w")
for name in lst:
	file = open(name,"rb")

	dictionary = json.loads(file.read())
	features = dictionary["features"]

	for district in features:
		lganame = district["properties"]["lga_name11"]
		if lganame not in resultDict.keys():
			
			resultDict[lganame] = {}
			resultDict[lganame]["weapons related"] = 0
			resultDict[lganame]["assaults"] = 0
			resultDict[lganame]["sexual offences"] = 0 
			resultDict[lganame]["robbery"] = 0 
			resultDict[lganame]["harassment and threatening"] = 0 
			resultDict[lganame]["total"] = 0 


		if district["properties"]["d10_weapons__and__explosives_offences"]!=None :
			resultDict[lganame]["weapons related"] += district["properties"]["d10_weapons__and__explosives_offences"]
		if district["properties"]["a20_assault__and__related_offences"] !=None:
			resultDict[lganame]["assaults"] += district["properties"]["a20_assault__and__related_offences"]
		if district["properties"]["a30_sexual_offences"] != None:
			resultDict[lganame]["sexual offences"] += district["properties"]["a30_sexual_offences"]
		if district["properties"]["a70_stalking_harassment__and__threatening_behaviour"] != None:
			resultDict[lganame]["harassment and threatening"] += district["properties"]["a70_stalking_harassment__and__threatening_behaviour"]
		if  district["properties"]["a50_robbery"] != None :
			resultDict[lganame]["robbery"] += district["properties"]["a50_robbery"]
		resultDict[lganame]["total"] += district["properties"]["grand_total_offence_count"]




json.dump(resultDict, outputfile, indent=2)
outputfile.close()
file.close()



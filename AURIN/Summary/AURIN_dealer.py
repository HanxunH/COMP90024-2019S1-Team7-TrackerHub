import json

outputfile = open("total_results.json","w")
econ_file = open("econ_results.json","r")
offence_file= open("offence_results.json","r") 

econ_dict = json.loads(econ_file.read())
offence_dict = json.loads(offence_file.read())

resultDict = {}

for key in econ_dict.keys():

	resultDict[key] = {}
	resultDict[key]["econ"] = {}
	resultDict[key]["offence"] = {}
	resultDict[key]["econ"]["unemployment_num"] = econ_dict[key]["unemployment_num"]
	resultDict[key]["econ"]["total_people_hospital"] = econ_dict[key]["total_people_hospital"]
	resultDict[key]["econ"]["total_male_hospital"] = econ_dict[key]["total_male_hospital"]
	resultDict[key]["econ"]["total_female_hospital"] = econ_dict[key]["total_female_hospital"]

	if key in offence_dict.keys():

		resultDict[key]["offence"]["weapons related"] = offence_dict[key]["weapons related"]
		resultDict[key]["offence"]["assaults"] = offence_dict[key]["assaults"]
		resultDict[key]["offence"]["sexual offences"] = offence_dict[key]["sexual offences"]
		resultDict[key]["offence"]["robbery"] = offence_dict[key]["robbery"]
		resultDict[key]["offence"]["harassment and threatening"] = offence_dict[key]["harassment and threatening"]
		resultDict[key]["offence"]["total"] = offence_dict[key]["total"]



json.dump(resultDict, outputfile, indent=2)

outputfile.close()
econ_file.close()
offence_file.close()



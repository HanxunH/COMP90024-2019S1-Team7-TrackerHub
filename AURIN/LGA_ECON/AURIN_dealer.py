import json
from econ_files import lst 

resultDict = {}
outputfile = open("econ_results.json","w")
for name in lst:
	file = open(name,"rb")

	dictionary = json.loads(file.read())
	features = dictionary["features"]

	for district in features:
		if "lga_name17" in district["properties"].keys():
			lganame = district["properties"]["lga_name17"]
		else:
			lganame = district["properties"]["lga_name16"]

		if lganame not in resultDict.keys():
			
			resultDict[lganame] = {}
			resultDict[lganame]["unemployment_num"] = 0
			resultDict[lganame]["total_people_hospital"] = 0
			resultDict[lganame]["total_male_hospital"] = 0 
			resultDict[lganame]["total_female_hospital"] = 0 



		if "lbr_frc_statistics_unemp_num" in district["properties"] and district["properties"]["lbr_frc_statistics_unemp_num"]!=None :
			resultDict[lganame]["unemployment_num"] += district["properties"]["lbr_frc_statistics_unemp_num"]
		if "tot_admis_all_hosps_2016_17_num" in district["properties"] and district["properties"]["tot_admis_all_hosps_2016_17_num"]!=None :
			resultDict[lganame]["total_people_hospital"] += district["properties"]["tot_admis_all_hosps_2016_17_num"]
		if "m_tot_admis_all_hosps_2016_17_num" in district["properties"] and district["properties"]["m_tot_admis_all_hosps_2016_17_num"]!=None :
			resultDict[lganame]["total_male_hospital"] += district["properties"]["m_tot_admis_all_hosps_2016_17_num"]
		if "f_tot_admis_all_hosps_2016_17_num" in district["properties"] and district["properties"]["f_tot_admis_all_hosps_2016_17_num"]!=None :
			resultDict[lganame]["total_female_hospital"] += district["properties"]["f_tot_admis_all_hosps_2016_17_num"]


json.dump(resultDict, outputfile, indent=2)
outputfile.close()
file.close()



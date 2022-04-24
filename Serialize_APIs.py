import os
import pickle
from MALDOZER_CONSTANTS import CLASSIFICATIONS, CLASS_LIST,Extracted_Features_Dir,api_to_method_id_pickle,file_contents_to_list

def Unique_APIs():
	Unique_APIs = set()
	for i in range(CLASSIFICATIONS):
		
		home_dir = Extracted_Features_Dir+'/'+CLASS_LIST[i]
		files=os.listdir(home_dir)

		print("started for ", home_dir)
		for j in range(len(files)):
			path = home_dir+'/'+files[j]
			temp_API_set = set(file_contents_to_list(path))

			if(len(Unique_APIs) == 0):
				Unique_APIs = temp_API_set
			else:
				Unique_APIs.update(temp_API_set)
		unique_API_set_size = len(Unique_APIs)
		print("Completed Unique API set merge for ", home_dir)
		print("Size of unique API set after merge with",CLASS_LIST[i],"class of APKs = ",unique_API_set_size)

	print("Unique APIs extracted for all classes of APKs. Size of set is ",unique_API_set_size)
	print("Proceeding to serialize the API call methods")
	return Unique_APIs


def serialize_APIs():
	unique_API_set = Unique_APIs()
	API_Serial_Dict = dict()
	serialization_count = 1

	for eachAPI in unique_API_set:
		API_Serial_Dict[str(eachAPI).replace("\n","")] = serialization_count
		serialization_count+=1
	
	pickle_file = open(api_to_method_id_pickle, 'wb')
	pickle.dump(API_Serial_Dict,pickle_file)
	
	if((serialization_count-1 == len(unique_API_set)) and (serialization_count-1 == len(API_Serial_Dict))):
		print("API call methods serialized without any loss or errors")
	else:
		print("Error in API call methods serialization")

	del(API_Serial_Dict)
	del(unique_API_set)

	pickle_file.close
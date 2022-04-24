from API_Features_Utils import extract_APIs
from API_Method_to_ID_Utils import mapping
from Word2vec_Utils import normalize_words
from Serialize_APIs import serialize_APIs
from DL_MODEL import deep_learning
from MALDOZER_CONSTANTS import CLASS_LIST,CLASSIFICATIONS, Mapping_Method_to_ID_path, Extracted_Features_Dir
from MALDOZER_CONSTANTS import Training_Data_Dir,Word2Vec_Files_Dir,Testing_Data_Dir,create_required_directories



def main():

    #creating Required directories
    create_required_directories(Extracted_Features_Dir)
    create_required_directories(Mapping_Method_to_ID_path)
    create_required_directories(Word2Vec_Files_Dir)
    for i in range(CLASSIFICATIONS):
        create_required_directories(Extracted_Features_Dir + '/' + CLASS_LIST[i])
        create_required_directories(Training_Data_Dir + '/' + CLASS_LIST[i])
        create_required_directories(Testing_Data_Dir + '/' + CLASS_LIST[i])
    

    #analyze all APK files, extract the features and API and save it in a .features file
    extract_APIs()

    #serializing API methods with unique Identification numbers
    serialize_APIs()

    #mapping API Methods to specific IDs using a pickle file
    mapping()

    #using word2vec to normalize
    normalize_words()

    #Running the Model
    deep_learning()


if __name__ == "__main__":
    main()
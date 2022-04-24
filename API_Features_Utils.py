import argparse
import os
from androguard.misc import AnalyzeAPK
from MALDOZER_CONSTANTS import APK_Files_Dir,Extracted_Features_Dir,CLASS_LIST,VERBOSE_LOGGING

#Function to list dub directories and sub directory files
def get_sub_directories(path,file_type):
    list_of_subdirs_and_files = os.listdir(path)
    Files_and_SubDirs = []
    for file in list_of_subdirs_and_files:
        AbsPath_of_file = os.path.abspath(os.path.join(path,file))
        if os.path.splitext(file)[1]==file_type:
            Files_and_SubDirs.append(AbsPath_of_file)
    return Files_and_SubDirs


#Function to extract features from APK files
def get_features(Directories):
    Files_and_SubDirs = []
    for SubDirectories in Directories.keys():
        Files_and_SubDirs.extend(get_sub_directories(SubDirectories,""))
        Files_and_SubDirs.extend(get_sub_directories(SubDirectories,".apk"))

    for APK in Files_and_SubDirs:
        path = os.path.join(Directories[os.path.split(APK)[0]],os.path.split(APK)[1])

        if os.path.exists(path+'.feature'):
            if VERBOSE_LOGGING:
                print("API already extracted for :", path)
            pass
        else:
            try:
                if VERBOSE_LOGGING:
                    print("Extracting API calls and features for:", path)
                _,_,dx = AnalyzeAPK(APK)
                features_path = path+'.feature'
                file = open(features_path,'w')
                for class_name in dx.get_classes():
                    for method in dx.classes[class_name.name].get_methods():
                        for _,API_Call,_ in method.get_xref_to():
                            file.write("{}:{}\n".format(API_Call.class_name,API_Call.name))
                file.close()
            except:
                if VERBOSE_LOGGING:
                    print("Failure getting features for : ", path)
                continue
    

# Function to set API and APK paths for all Classes (Benign, Adware, Banking, Riskware, SMS)
def set_path_args(): 
    paths = argparse.ArgumentParser("maldozer")

    paths.add_argument("--benigndir", default=APK_Files_Dir+'/'+CLASS_LIST[0])
    paths.add_argument("--adwaredir", default = APK_Files_Dir+'/'+CLASS_LIST[1]) 
    paths.add_argument("--bankingdir", default=APK_Files_Dir+'/'+CLASS_LIST[2])
    paths.add_argument("--riskwaredir", default=APK_Files_Dir+'/'+CLASS_LIST[3])
    paths.add_argument("--smsdir", default=APK_Files_Dir+'/'+CLASS_LIST[4])

    paths.add_argument("--benignfeaturedir",default=Extracted_Features_Dir+'/'+CLASS_LIST[0])
    paths.add_argument("--adwarefeaturedir",default=Extracted_Features_Dir+'/'+CLASS_LIST[1])
    paths.add_argument("--bankingfeaturedir",default=Extracted_Features_Dir+'/'+CLASS_LIST[2])
    paths.add_argument("--riskwarefeaturedir",default=Extracted_Features_Dir+'/'+CLASS_LIST[3])
    paths.add_argument("--smsfeaturedir",default=Extracted_Features_Dir+'/'+CLASS_LIST[4])

    return paths.parse_args()


#Function to map API directories to their APK directories
def map_APK_API_directories():
    paths = set_path_args()
    BenignDir = os.path.abspath(paths.benigndir)
    AdwareDir = os.path.abspath(paths.adwaredir)
    BankingDir = os.path.abspath(paths.bankingdir)
    RiskwareDir = os.path.abspath(paths.riskwaredir)
    SMSDir = os.path.abspath(paths.smsdir)

    benignfeaturedir = os.path.abspath(paths.benignfeaturedir)
    adwarefeaturedir = os.path.abspath(paths.adwarefeaturedir) 
    bankingfeaturedir = os.path.abspath(paths.bankingfeaturedir) 
    riskwarefeaturedir = os.path.abspath(paths.riskwarefeaturedir) 
    smsfeaturedir = os.path.abspath(paths.smsfeaturedir)

    Directories = dict()  
    Directories[AdwareDir] = adwarefeaturedir
    Directories[BenignDir] = benignfeaturedir
    Directories[BankingDir] = bankingfeaturedir
    Directories[RiskwareDir] = riskwarefeaturedir
    Directories[SMSDir] = smsfeaturedir
    #print(Directories)
    return Directories


def extract_APIs():
    get_features(map_APK_API_directories())
    print("APIs and Features extraction completed")
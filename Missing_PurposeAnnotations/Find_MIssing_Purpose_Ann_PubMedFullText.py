import os
from os import listdir
from os.path import isfile, join

# we are interested only on annotations set of:  (software_usage and purpose annotations)

Usage_ = ['Application_Usage', 'ProgrammingEnvironment_Usage', 'PlugIn_Usage', 'OperatingSystem_Usage']

Purpose_ = ['Purpose_Analysis', 'Purpose_Modelling', 'Purpose_Stimulation', 'Purpose_DataCollection',
            'Purpose_DataPreProcss', 'Purpose_Simulation', 'Purpose_Visualization', 'Purpose_Programming']

dict_missingAnnforUsage2 = {}
# file path
path = '/home/beck/Desktop/Automatic-classifcation-of-purpose-of-software-in-Scientific-articles/somecode/SoMeSci/Pubmed_fulltext/'

# iterating over all files in the dir
for file_name2 in os.listdir(path):

    # if the file is .ann
    if file_name2.endswith('.ann'):

        # path to each file
        file_path = path + file_name2

        # read eah file
        with open(file_path, "r") as a_file2:

            anno_usage_strstp2 = []
            anno_purpose_strstp2 = []

            for line in a_file2:

                # grab the type of annotation
                annotataion = line.split()

                # if it is _usage annotation
                if (annotataion[1] in Usage_):

                    startstop2 = annotataion[2:4]
                    strstp2 = '_'.join(startstop2)

                    anno_usage_strstp2.append(strstp2)

                # if it is purpose_ annotation
                elif (annotataion[1] in Purpose_):

                    startstop2 = annotataion[2:4]
                    strstp2 = '_'.join(startstop2)

                    # print(strstp)

                    anno_purpose_strstp2.append(strstp2)

            Usage_annotations_set2 = set(anno_usage_strstp2)
            Purpose_annotations_set2 = set(anno_purpose_strstp2)

            # Usage_annotations_set - Purpose_annotations_set = Usage with no purpose annotation
            missing2 = Usage_annotations_set2.difference(Purpose_annotations_set2)

            # check if result is non-empty set

            if (len(missing2) != 0):
                print (file_name2, missing2)

                dict_missingAnnforUsage2[file_name2] = missing2
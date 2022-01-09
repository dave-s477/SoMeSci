import os
from os import listdir
from os.path import isfile, join

# we are interested only on annotations set of:  (software_usage and purpose annotations)

Usage_ = ['Application_Usage', 'ProgrammingEnvironment_Usage', 'PlugIn_Usage', 'OperatingSystem_Usage']

Purpose_ = ['Purpose_Analysis', 'Purpose_Modelling', 'Purpose_Stimulation', 'Purpose_DataCollection',
            'Purpose_DataPreProcss', 'Purpose_Simulation', 'Purpose_Visualization', 'Purpose_Programming']

dict_missingAnnforUsage = {}
# file path
path = '/home/beck/Desktop/Automatic-classifcation-of-purpose-of-software-in-Scientific-articles/somecode/SoMeSci/PLoS_methods/'

# iterating over all files in the dir
for file_name in os.listdir(path):

    # if the file is .ann
    if file_name.endswith('.ann'):

        # path to each file
        file_path = path + file_name

        # read eah file
        with open(file_path, "r") as a_file:

            anno_usage_strstp = []
            anno_purpose_strstp = []

            for line in a_file:

                # grab the type of annotation
                annotataion = line.split()

                # if it is _usage annotation
                if (annotataion[1] in Usage_):

                    startstop = annotataion[2:4]
                    strstp = '_'.join(startstop)

                    anno_usage_strstp.append(strstp)

                # if it is purpose_ annotation
                elif (annotataion[1] in Purpose_):

                    startstop = annotataion[2:4]
                    strstp = '_'.join(startstop)

                    # print(strstp)

                    anno_purpose_strstp.append(strstp)

            Usage_annotations_set = set(anno_usage_strstp)
            Purpose_annotations_set = set(anno_purpose_strstp)

            # Usage_annotations_set - Purpose_annotations_set = Usage with no purpose annotation
            missing = Usage_annotations_set.difference(Purpose_annotations_set)

            # check if result is non-empty set

            if (len(missing) != 0):
                print(file_name, missing)

                dict_missingAnnforUsage[file_name] = missing
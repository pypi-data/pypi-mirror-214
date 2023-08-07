from file_modules import *

import sys
import os
sys.path.insert(0, os.path.join(".."))

from cetl import DataPipeline

# zip the file with fernet
cfg = {"pipeline":[ 
                    # {"type":"generateFernetKey", "module_type":"file",
                    #     "out_file":"/home/clement/projects/cetl/sample_user_project/fernet_key.txt"},

                    # {"type":"compressDirectoryToTarWithFernet", "module_type":"file", 
                    #     "custom_fernet_key":"n0pz0JWahME9e3R8NX68eiA63brz5aV5wGytbsFiBxM=", 
                    #     "target_dir":"/home/clement/projects/cetl/sample_user_project/text_files", 
                    #     "out_dir":"/home/clement/projects/cetl/sample_user_project/out",
                    #     "out_file_prefix":"unknown"}

                    # {"type":"splitFileIntoMultiple", "module_type":"file", 
                    #     "in_file":"/home/clement/projects/cetl/sample_user_project/out/unknow.tar.gz.enc", 
                    #     "out_dir":"/home/clement/projects/cetl/sample_user_project/out", "out_file_prefix":"unknown", 
                    #     "max_size":300}

                    # {"type":"recoverFromMultipleFilesIntoOne", "module_type":"file", 
                    #     "in_dir":"/home/clement/projects/data/company_backup/sample_data", 
                    #     "in_file_prefix":"sample_data", "out_dir":"/home/clement/projects/data/company_backup", 
                    #     "out_file_ext":"tar.gz.enc"}

                    {"type":"decryptEncFileToDirectoryWithFernet", "module_type":"file", 
                        "custom_fernet_key":"n0pz0JWahME9e3R8NX68eiA63brz5aV5wGytbsFiBxM=", 
                        "target_encypt_file":"/home/clement/data/company_backup/project_codes.tar.gz.enc", 
                        "out_dir":"/home/clement/data/company_backup"}

        ]}

# cfg = {"pipeline":[ 

#                     # {"type":"decryptDirectoryToTarWithFernet", "module_type":"file", 
#                     #     "custom_fernet_key":"n0pz0JWahME9e3R8NX68eiA63brz5aV5wGytbsFiBxM=", 
#                     #     "target_encypt_file":"/home/clement/data/company_backup/unknown_1.tar.gz.enc", 
#                     #     "out_dir":"/home/clement/data/company_backup"}

#         ]}





# zip the file with pyAesCrypt
# cfg = {"pipeline":[ {"type":"generateFernetKey", "module_type":"file",
#                         "out_file":"/home/clement/projects/cetl/sample_user_project/fernet_key.txt"},
#                     {"type":"compressDirectoryToTarWithPyAesCript", "module_type":"file", 
#                         "fernet_key_file":"/home/clement/projects/cetl/sample_user_project/fernet_key.txt", 
#                         "target_dir":"/home/clement/projects/cetl/sample_user_project/text_files", 
#                         "out_dir":"/home/clement/projects/cetl/sample_user_project/out"},
#                     {"type":"decryptDirectoryToTarWithPyAesCript", "module_type":"file",
#                         "fernet_key_file":"/home/clement/projects/cetl/sample_user_project/fernet_key.txt", 
#                         "target_encypt_file":"/home/clement/projects/cetl/sample_user_project/out/text_files.tar.gz.enc", 
#                         "out_dir":"/home/clement/projects/cetl/sample_user_project/out"}
#         ]}




pipe = DataPipeline(cfg)
result = pipe.transform("")
print(result)

#  python compress_files.py
# tar -xvzf text_files.tar.gz
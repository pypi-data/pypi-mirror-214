import requests
cfg = {"pipeline":[ 
                    {"type":"splitFileIntoMultiple", "module_type":"file", 
                        "in_file":"/home/clement.cheuk/data/out/project_codes.tar.gz.enc", 
                        "out_dir":"/home/clement.cheuk/data/out", "out_file_prefix":"project_codes", 
                        "max_size":1024*1024*100}
        ]}


                    {"type":"compressDirectoryToTarWithFernet", "module_type":"file", 
                        "custom_fernet_key":"n0pz0JWahME9e3R8NX68eiA63brz5aV5wGytbsFiBxM=", 
                        "target_dir":"/home/clement.cheuk/data/out/sample_data", 
                        "out_dir":"/home/clement.cheuk/data/out",
                        "out_file_prefix":"sample_data"}

                    {"type":"compressDirectoryToTarWithFernet", "module_type":"file", 
                        "custom_fernet_key":"n0pz0JWahME9e3R8NX68eiA63brz5aV5wGytbsFiBxM=", 
                        "target_dir":"/home/clement.cheuk/xgate_projects/py-dataexport", 
                        "out_dir":"/home/clement.cheuk/data/out",
                        "out_file_prefix":"project_codes"}

                    {"type":"splitFileIntoMultiple", "module_type":"file", 
                        "in_file":"/home/clement.cheuk/data/out/sample_data.tar.gz.enc", 
                        "out_dir":"/home/clement.cheuk/data/out", "out_file_prefix":"sample_data", 
                        "max_size":1024*1024*100}


                    {"type":"splitFileIntoMultiple", "module_type":"file", 
                        "in_file":"/home/clement.cheuk/data/out/project_codes.tar.gz.enc", 
                        "out_dir":"/home/clement.cheuk/data/out", "out_file_prefix":"project_codes", 
                        "max_size":1024*1024*100}


cfg = {"pipeline":[ 
                    {"type":"decryptDirectoryToTarWithFernet", "module_type":"file", 
                        "custom_fernet_key":"n0pz0JWahME9e3R8NX68eiA63brz5aV5wGytbsFiBxM=", 
                        "target_encypt_file":"/home/clement/data/company_backup/unknown_1.tar.gz.enc", 
                        "out_dir":"/home/clement/data/company_backup"}
        ]}



api_url = "http://localhost:8099/pipeline"
res = requests.post(api_url, json=cfg, headers={'Content-Type': 'application/json'})
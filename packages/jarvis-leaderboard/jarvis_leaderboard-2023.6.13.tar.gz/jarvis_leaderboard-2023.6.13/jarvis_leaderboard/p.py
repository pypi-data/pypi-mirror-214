import os, glob
from jarvis.db.jsonutils import loadjson

root_dir = os.path.dirname(os.path.abspath(__file__))


def check_metadata_info_exists():
    search = root_dir + "/contributions/*/" + "metadata.json"
    all_dirs = []
    all_dirs_ok = []
    for i in glob.glob(search):
        meta_data = loadjson(i)
        all_dirs.append(i)
        if (
            "author_email" in meta_data
            and "project_url" in meta_data
            and "model_name" in meta_data
            and "@" in meta_data["author_email"]
            and "team_name" in meta_data
            and "time_taken_seconds" in meta_data
            and "software_used" in meta_data
            and "hardware_used" in meta_data
        ):
            all_dirs_ok.append(i)
    problem_dirs = set(all_dirs) - set(all_dirs_ok)
    return problem_dirs


def check_metadata_json_exists():

    search = root_dir + "/contributions"
    all_dirs = []
    all_dirs_meta = []
    all_dirs_with_metadata = []
    for i in os.listdir(search):
        all_dirs.append(i)
        for j in os.listdir(os.path.join(search, i)):
            if "metadata.json" in j:
                meta_path = os.path.join(search, i, j)
                if meta_path not in all_dirs_with_metadata:
                    all_dirs_with_metadata.append(meta_path)
                    all_dirs_meta.append(i)
    problem_dirs = set(all_dirs) - set(all_dirs_meta)
    return problem_dirs


def check_run_sh_exists():

    search = root_dir + "/contributions"
    all_dirs = []
    all_dirs_meta = []
    all_dirs_with_metadata = []
    for i in os.listdir(search):
        all_dirs.append(i)
        for j in os.listdir(os.path.join(search, i)):
            if "run.sh" in j:
                meta_path = os.path.join(search, i, j)
                if meta_path not in all_dirs_with_metadata:
                    all_dirs_with_metadata.append(meta_path)
                    all_dirs_meta.append(i)
    problem_dirs = set(all_dirs) - set(all_dirs_meta)
    for j in problem_dirs:  
        p = os.path.join(search, j)
        runsh = os.path.join(p,'run.sh')
        f=open(runsh,'w')
        f.write('#!/bin/bash\n')
        for k in os.listdir(p): 
          if '.py' in k:    
              print(runsh,k)
              line='python '+k+'\n'
              f.write(line)
        f.close()
    return problem_dirs


def check_at_least_one_csv_zip_exists():

    search = root_dir + "/contributions"
    all_dirs = []
    all_dirs_meta = []
    all_dirs_with_metadata = []
    for i in os.listdir(search):
        all_dirs.append(i)
        for j in os.listdir(os.path.join(search, i)):
            if "csv.zip" in j:
                meta_path = os.path.join(search, i, j)
                if meta_path not in all_dirs_with_metadata:
                    all_dirs_with_metadata.append(meta_path)
                    all_dirs_meta.append(i)
    problem_dirs = set(all_dirs) - set(all_dirs_meta)
    return problem_dirs


#p = check_metadata_json_exists()
#print(p)
#p = check_run_sh_exists()
#print(p,len(p))
p = check_at_least_one_csv_zip_exists()
print(p,len(p))
p = check_metadata_info_exists()
print("problemo", p,len(p))

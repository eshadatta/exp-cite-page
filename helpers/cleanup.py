import json

def read_pidfile(pidfile):
    data = None
    try:
        with open(pidfile, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print (e)
    return data
def cleanup(pidfile, updated_files):
    previous_files = None
    files = list(updated_files.keys())
    data = read_pidfile(pidfile)
    if data:
        previous_files = list(filter(lambda x: x['file'] in files, data))
        for f, i in updated_files.items():
            previous_file_info = list(filter(lambda x: x['file'] == f, previous_files))
            relationship = {"file_commit_id": previous_file_info[0]['file_commit_id'], "file_hash": previous_file_info[0]['file_hash'], "version": previous_file_info[0]['version']}
            if 'past_versions' and 'relationships' in i:
                i['past_versions'].append(previous_file_info[0]['version'])
                i['relationships'].append(relationship)
            else:
                i['past_versions'] = [previous_file_info[0]['version']]
                i['relationships'] = [relationship]
    print(updated_files)
    for f, i in updated_files.items():
        print(f)
        print(i)
    return updated_files


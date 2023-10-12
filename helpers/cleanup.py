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
    rest_files = []
    files = list(updated_files.keys())
    data = read_pidfile(pidfile)
    if data:
        previous_files = list(filter(lambda x: x['file'] in files, data))
        rest_files = list(filter(lambda x: not(x['file'] in files), data))
        for f, i in updated_files.items():
            previous_file_info = list(filter(lambda x: x['file'] == f, previous_files))
            if previous_file_info:
                relationship = {"file_commit_id": previous_file_info[0]['file_commit_id'], "file_hash": previous_file_info[0]['file_hash'], "version": previous_file_info[0]['version'], "id": previous_file_info[0]['current_id'], "doi": previous_file_info[0]['doi']}
                if 'past_versions' and 'past_relationships' in previous_file_info[0]:
                    i['past_versions'] = [previous_file_info[0]['version']] + previous_file_info[0]['past_versions']
                    i['past_relationships'] = [relationship] + previous_file_info[0]['past_relationships']
                else:
                    i['past_versions'] = [previous_file_info[0]['version']]
                    i['past_relationships'] = [relationship]
    return updated_files, rest_files


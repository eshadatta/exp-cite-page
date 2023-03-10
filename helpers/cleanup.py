import ijson

def cleanup(pidfile, filelist):
    file_info = {}
    for i in filelist:
        file_info[i['file']] = {"current_hash": i['file_hash'], "previous_hashes": []}
    fnames = list(file_info.keys())
    try:
        with open(pidfile, "rb") as f:
            for record in ijson.items(f, "item"):
                if record['file'] in fnames and not(record['file_hash'] == file_info[record['file']]["current_hash"]):
                    file_info[record['file']]["previous_hashes"].append((record['file_hash'], record['version']))
    except Exception as e:
        print (e)
    return file_info


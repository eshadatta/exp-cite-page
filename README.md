# static-page-id-generator

A prototype to create PIDs for static page generator

This is a prototype to create permanent identifiers for static pages such as blog posts. Eventually, the identifiers can be used to generate different types of permanent urls including DOIs.

For now, it takes a file as an argument, gets its git commit information and stores an array of json strings like so with a generated uuid:
```
[{"git_commit_id": "git commit id", "current_id": "generated uuid with a length of 10", "file": "file name and path relative to the repository root", "file_hash": "git hash of file contents" "utc_commit_date": "2022-12-14 19:26:19"}]
```

Currently, the script is run like the following:
```
python id.py -r /path/to/repo -f path/to/file -p /path/to/pid_json_file
```

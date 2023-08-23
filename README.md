# static-page-id-generator

## **This is currently in active development and may break at any time!**

## What is this?
A prototype to create PIDs for a static page generator

This is a prototype to create permanent identifiers for static pages such as blog posts. Eventually, the identifiers can be used to generate different types of permanent urls including DOIs.

This is meant to be used with markdown files and is being currently tested with Hugo.

### **Current Status**
* Needs test coverage
* I need to narrow down an argument parser library
* The scope for now is to only work with new PIDs, i.e. a file can have a new PID or be upgraded to a major version to get a new PID. It currently _does not_ work with deleted pages or tombstoning anything.
* Code needs to be abstracted out further so that a user could add more functionality for custom url construction or ID generation
* This only supports DOIs for now. A UUID option has been given as an example. 
* Currently, the config file is in an `.ini` format because I thought it would be easier for the user to enter this rather than deal with possibly malformed YAML files. This can be reverted to YAML, of course.


#### **USAGE:**
A toy example of a collection of markdown pages is available for the user to see the results of the code. The following steps will be shown with this toy example.
1. Please clone the toy example from [here](https://gitlab.com/eshadatta-crossref/tiny_static_site) 
2. Separately, please clone this [repository](https://gitlab.com/crossref/labs/static-page-id-generator.git)
3. In the root directory of the static-page-id-generator repository, please install the requirements: `pip install -r requirements.txt`

#### TL;DR:
* For a quick summary to run everything, go [here](#just-tell-me-how-to-run-everything)
* Otherwise, read on below.

##### **USAGE OVERVIEW**
* In order to use this software, the user needs to add a frontmatter tag and a version using the [semantic versioning convention](https://semver.org/) to the markdown file. The script looks for this tag and checks the version in order to generate IDs.
* The software is currently divided into three scripts: `init.py`, `id.py`, and a url generator script. The `init.py` creates a pid json file that contains the id and the git information of the file(s) to be tracked, and a config file that contains other information needed by the id and url generator script. The `id.py` script generates an id and all gathers related git information for the file. There is also a url generator script that will generate a url according to the logic of the static site generator. This can be customized by the user.

#### **USAGE EXAMPLES**:

#### **init.py**:
* creates a config file (default file name: `static.ini`) and a json file (default file name: `pid.json`)
    * The required arguments are the repository path that contains the static site, the production domain, and the id type to be used. Currently, the dry run has not yet been implemented for `init.py`.
    * `python init.py -h` gives the following:
        ```
        python init.py -h
        usage: init.py [-h] -r REPO_PATH -d DOMAIN [-p [PID_FILE_PATH]] [-cf [CONFIG_FILENAME]] [-b BRANCH] -id
               {doi,uuid} [-dry]
        Generate a permanent ID for a static site generator

        optional arguments:
        -h, --help            show this help message and exit
        -r REPO_PATH, --repo-path REPO_PATH
                            Path to repository containing the files
        -d DOMAIN, --domain DOMAIN
                            Production domain of the content, for example: https://www.crossref.org/
        -p [PID_FILE_PATH], --pid-file-path [PID_FILE_PATH]
                            Path to json file where containing all the information associated with the
                            files and their permanent IDs; relative to the repository root. If the file
                            does not exist, a new file with the specified filename will be created. An
                            existing file will not be overwritten
        -cf [CONFIG_FILENAME], --config-filename [CONFIG_FILENAME]
                            Filename for config init, has a default filename if none is specified. An
                            existing file will be overwritten
        -b BRANCH, --branch BRANCH
                            Path to branch where the file is located. The default is the active branch of
                            the repository
        -id {doi,uuid}, --id-type {doi,uuid}
        -dry, --dry-run         Dry run to generate a permanent ID of a specified file
        ```
    * The user can specify a pid file name, a config file name, and a branch, if they so choose. If the user picks an id type of `doi`, they must also provide a `--doi-prefix` option with a doi prefix. So, a command using only the required arguments using the toy example cloned to the user's machine can look like the following:
    `python init.py -r ~/tiny_static_site/ -id doi --doi-prefix 10.1212 -d https://www.crossref.org`
    * Running this command will generate a config file named `static.ini` in the root of the tiny_static_site repository and `pid.json` file with an empty dictionary: `{}`
    * Using the above commands, the config file looks like the following:
        ```
        $ cat static.ini
        [DEFAULT]
        pid_file = pid.json
        domain = https://www.crossref.org
        id_type = doi
        doi_prefix = 10.1212
        ```
#### **id.py**:
* Once the config and pid files are created, the user will run `id.py` which will generate IDs for the files.
* The user needs to add a frontmatter tag and a version number to one or more markdown files and commit them. They can then call the id generator script. 
* The required arguments are the repo path and one or more content paths; relative to the repo root:
    ```
    $ python id.py -h
    usage: id.py [-h] -r REPO -c CONTENT [CONTENT ...] [-cf [CONFIG_FILENAME]] [-d]

    Generate a permanent ID for a specific file

    optional arguments:
    -h, --help              show this help message and exit
    -r REPO, --repo REPO    Path to repository containing the files
    -c CONTENT [CONTENT ...], --content CONTENT [CONTENT ...]
                            Examples: -c filepath1 filepath2; relative to the repository root
    -cf [CONFIG_FILENAME], --config-filename [CONFIG_FILENAME]
                            Filename for config init, has a default filename if none is specified
    -b, --batch-process     batch process
    -d, --dry-run           Dry run to generate a permanent ID of a specified file or files
    ```
* This can be run with the dry run argument. If done so, this is the expected output:
  ```
  $ python id.py -r ~/tiny_static_site/ -c content/blog --dry-run
    RUNNING DRY RUN:
    At check_args: Checks if config file has been created
    At check_config_args: Checks if config values exist
    At get_file_list: Gets file list from paths
    At check_file_versions: gets a list of all files from given content paths and their versions from the pid file (if they exist) and generates a list of files to be pid-ized
    At git_info: Generate PID and git information for file to be saved in pid file
    Generates a ProcessJSON object which contains path and domain information
    Updates any PID information in the pid file, if the file already exists in the pid file or inserts PID information if the file is new
  ```
  
* **MARKDOWN EDITING**: The user needs to add a tag like the following to the frontmatter of the markdown. So, please edit `content/blog/2023/2023-05-30-our-annual-call-for-board-nominations.md` in the `tiny_static_site` repo. So, it should look like this **before**:
    ```markdown
        ---
        title: 'Our annual call for board nominations'
        author: ABC
        draft: false
        authors:
          - ABC
        date: 2023-05-30
        categories:
          - Board
          - Member Briefing
          - Governance
          - Elections
          - Crossref Live
          - Annual Meeting
        archives:
          - 2023
        ---
    ```
    * Please edit the frontmatter to add the following: `x-version: 0.0.0`. **After editing**, it should look like this:
    ```markdown
        ---
        title: 'Our annual call for board nominations'
        author: ABC
        draft: false
        authors:
          - ABC
        date: 2023-05-30
        categories:
          - Board
          - Member Briefing
          - Governance
          - Elections
          - Crossref Live
          - Annual Meeting
        x-version: 0.0.0
        archives:
            - 2023
        ---
    ```
    * It is important to commit this change. If the user doesn't, the script will error out.
* To generate an id for this file, please run the `id.py` script:
      `python id.py -r <path-to-repo>/tiny_static_site/ -c content/blog/2023/`
* It should run and create an entry in the `pid.json` file in the root of the toy example repo. 
* The pid file will look like the following:
    ```json
    [
	    {
            "file_commit_id": "b3599bfa471171961ea36226129251653d38c391",
            "file_hash": "37e9449337f968c8f27345dd09a92975b1131982",
            "utc_commit_date": "2023-06-20 22:27:12",
            "current_id": "rG6hbUs9hE",
            "version": "0.0.0",
            "url": null,
            "file": "content/blog/2023/2023-05-30-our-annual-call-for-board-nominations.md",
            "production_domain": "https://www.crossref.org",
            "doi_prefix": "10.1212"
	    }
    ]
    ```

### There are different ways to run the `id.py` script:
#### Using the toy example:
* **With one file:**
`python id.py -r  <path-to-repo>/tiny_static_site/ -c 2023-05-30-our-annual-call-for-board-nominations.md`
* **With multiple paths:**
`python id.py -r  <path-to-repo>/tiny_static_site/ -c content/blog/2023/ content/blog/2022`
* **With a mix of files and paths:**
`python id.py -r  <path-to-repo>/tiny_static_site/ -c content/blog/2023/2023-02-28-in-the-know-on-workflows.md content/blog/2022`
* **To run a batch process:**
`python id.py -r  <path-to-repo>/tiny_static_site/ -c content/blog -b`: This will run through all files and initialize a file if it is not already initialized, i.e. it will add `x-version: 0.0.0` to the frontmatter of the markdown file and add it to the pid file. It will also commit the change.
## Further information
* If the major version has been bumped up in the markdown file and the file already exists in the pid file, the file will show information about both versions. For example, if the `x-version` has changed from `0.0.0` to `1.0.0` and the file already exists in the pid json file, it will show the git information about both versions and the id for both. 
  * Frontmatter change from major version 0 to 1:
    ```
    ---
    title: 'Forming new relationships: Contributing to Open source'
    author: ABC
    draft: false
    authors:
    date: 2022-10-19
    x-version: 1.0.0
    categories:
        - DOIs
        - Linking
        - Interoperability
        - Accessibility
        - Engineering
    archives:
        - 2022
    ---
    ```
  * PID file looks like the following, provided that the file already existed in the pid json file:
    ```json
    {
		"file_commit_id": "baba78e8c26e19681042ed2d863b7d98f761295e",
		"file_hash": "7a7f12724563873874f2e35ffd4fd33940b5145c",
		"utc_commit_date": "2023-06-20 22:42:41",
		"current_id": "3zyaTDyRGf",
		"version": "1.0.0",
		"url": null,
		"file": "content/blog/2022/2022-10-19-forming-new-relationships-contributing-to-open-source.md",
		"past_versions": [
			"0.0.0"
		],
		"past_relationships": [
			{
				"file_commit_id": "7abdb96efaa0bcb52449f0856a9482e5800120d4",
				"file_hash": "221ad44858a93ce285aaa55d5a73e3d67f049258",
				"version": "0.0.0"
			}
		],
		"production_domain": "https://www.crossref.org",
		"doi_prefix": "10.1212"
	}
    ```
#### **URL GENERATION:**
* URLs pointing to the production instance need to be created and associated with the files so that the IDs can be registered with the url. Many times, the static site may have its own logic according to the use case of the institution. The given script here follows the Crossref website logic. 
* `python helper_url_generation/url_constructor.py -r  <path-to-repo>/tiny_static_site/ -cf ~/tiny_static_site/static.ini`. This populates the pid.json file with the urls.
    ```json
    [{
		"file_commit_id": "6375f0c13a42668210378e2352d447eca6fc3857",
		"file_hash": "13ef0183a59ea4624c892306100bdff71496ee9d",
		"utc_commit_date": "2023-06-20 21:04:58",
		"current_id": "W2iTVv6WNT",
		"version": "1.0.0",
		"url": "https://www.crossref.org/blog/better-preprint-metadata-through-community-participation",
		"file": "content/blog/2022/2022-11-09-preprint-schema-recommendations.md",
		"production_domain": "https://www.crossref.org",
		"doi_prefix": "10.1212"
	},
	{
		"file_commit_id": "7abdb96efaa0bcb52449f0856a9482e5800120d4",
		"file_hash": "b1206ee6d8cf91468f58362c86bb1a22aa2fab2e",
		"utc_commit_date": "2023-06-20 22:38:34",
		"current_id": "3WcMKovZou",
		"version": "1.0.0",
		"url": "https://www.crossref.org/blog/our-annual-call-for-board-nominations",
		"file": "content/blog/2023/2023-05-30-our-annual-call-for-board-nominations.md",
		"past_versions": [
			"0.0.0"
		],
		"past_relationships": [
			{
				"file_commit_id": "b3599bfa471171961ea36226129251653d38c391",
				"file_hash": "37e9449337f968c8f27345dd09a92975b1131982",
				"version": "0.0.0"
			}
		],
		"production_domain": "https://www.crossref.org",
		"doi_prefix": "10.1212"
	}]
    ```
### Just tell me how to run everything:
1. Using the toy site as an example, run the init script from the root of the static id generator script:
    * `python init.py -r <path-to-repo>/tiny_static_site/ -id doi --doi-prefix 10.1212 -d https://www.crossref.org`
2. Add the `x-version` tag to the markdown frontmatter and follow the semantic versioning convention and add `0.0.0` or bump up the major version. 
    * `x-version: 0.0.0`
3. Run `id.py` to generate IDs for the files. [Here](#using-the-toy-example) are ways to do it.
4. Run the url generator script. An example for the crossref site is here: 
   * `python helper_url_generation/url_constructor.py -r <path-to-repo>/tiny_static_site/ -cf ~/tiny_static_site/static.ini`

## Developer Information
* As of now, only integration tests are available. To run tests, after cloning the repository and installing the requirements, please run the following:
`pytest tests/functional_tests`
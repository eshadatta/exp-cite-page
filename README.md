# static-page-id-generator

## **This is currently in active development and may break at any time!**

## What is this?
A prototype to create PIDs for a static page generator

This is a prototype to create permanent identifiers for static pages such as blog posts. Eventually, the identifiers can be used to generate different types of permanent urls including DOIs. 

This is meant to be used with markdown files and is being currently tested with Hugo.

### **Current Status**
* Needs test coverage
* The scope for now is to only work with new PIDs, i.e. a file can have a new PID or be upgraded to a major version to get a new PID. It currently _does not_ work with deleted pages or tombstoning anything.
* Code needs to be abstracted out further so that a user could add more functionality for custom url construction or ID generation
* This only supports DOIs for now. A UUID option has been given as an example. 

### Quick Links
* [Usage Overview](#usage-overview)
* [Quickstart](#tldr)
* [Quick summary to run everything](#tldr)
* [Dependencies](#dependencies)
* [Installation](#installation)
* Script Steps:
  - [Init](#initialize-the-script)
  - [Run everything else](#run-the-script)
* Run scripts [individually](#individual-scripts)



### **USAGE:**
### Dependencies
* Recent version of Hugo - for the website being tracked
* Git
* curl
* Python >= 3.8



### TL;DR:
* For a quickstart, which walks through creating a small site with Hugo and using this script, please go [here](https://gitlab.com/crossref/labs/static-page-id-generator/-/blob/main/quickstart.md?ref_type=heads#quickstart)
* For a quick summary to run everything, go [here](#just-tell-me-how-to-run-everything)
* For in-depth instructions to set up everything, read on below.

### Installation
1. Please refer to quickstart [documentation](https://gitlab.com/crossref/labs/static-page-id-generator/-/blob/main/quickstart.md?ref_type=heads#create-a-new-site-and-generate-some-content) to set up a small hugo site. Once those instructions are followed, there should be `/tmp/my_science_blog` as the repository of a new example hugo site.
2. Separately, please clone this [repository](https://gitlab.com/crossref/labs/static-page-id-generator.git)
3. In the root directory of the static-page-id-generator repository, please install the requirements: `pip install -r requirements.txt`

##### **USAGE OVERVIEW**
* In order to use this software, the user needs to add a frontmatter tag and a version using the [semantic versioning convention](https://semver.org/) to the markdown file. The script looks for this tag and checks the version in order to generate IDs.
* The software has the following components:
  * sets up files and a config files with the relevant information to begin processing
  * Generates PIDs for tracked files.
  * If the user is a crossref member, there are scripts that do the following:
    * Creates a submission file to deposit the content for the user
    * Deposits the content 
    * Registers the PID as a DOI in Crossref
    * Adds the DOI back to the tagged markdown file
* All of the scripts can be run individually or together. The following examples will demonstrate the scripts that are run under one script

#### **USAGE EXAMPLES**:
#### To run all steps of the Static Site PID Genertor: use this script: `run_all.py`
* To see the commands available for the script, please run the following:
```
python run_all.py --help
Usage: run_all.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  gen-pid
  init
```
The two commands available are: `init` and `gen-pid`. `init` creates a config file and a json file with all the relevant information required for processing. `gen-pid` runs all the subsequent steps from PID genertaion to DOI registration.
Here are the steps in detail.
## Script Steps:
### Initialize the script
* creates a config file (default file name: `config.yml`) and a json file (default file name: `pid.json`)
    * The required arguments are the repository path that contains the static site, the production domain, the doi-prefix to be used. 
    * `python run_all.py init --help` gives the following:
        ```
        Usage: run_all.py init [OPTIONS]

        Options:
          -cf, --conf-file TEXT  Name of config yml file. This file will be saved and
                                should exist at the root of the repository
          -r, --repo DIRECTORY   Path to repository containing the files  [required]
          -c, --content TEXT     Examples: -c filepath1 -c filepath2; relative to the
                                repository root
          -d, --domain TEXT      Production domain of the content, for example:
                                https://www.crossref.org/  [required]
          --doi-prefix TEXT      Add doi prefix string to this argument, example:
                                --doi-prefix 'x.xxx'  [required]
          --id-type TEXT
          -p, --pid-file TEXT    Json file that keeps track of the files, stored
                                relative to the root of the repository
          --help                 Show this message and exit.
        ```
    * The user can specify a pid file name, and a config file name if they so choose. The default id type is DOI. Currently, that is the only type of id type that is in use. The user has to specify a doi-prefix. So, a command using only the required arguments using the toy example cloned to the user's machine can look like the following:
    `python run_all.py init -r /tmp/my_science_blog/ -c content -d https://production.domain.org --doi-prefix 'user-prefix'`
    * Running this command will generate a config file named `config.yml` in the root of the tiny_static_site repository and `pid.json` file with an empty dictionary: `{}`. If one does not specify the `-c` parameter, the default value is sent which is the `.`. In the default case for the content parameter, the static site pid generator will begin tracking files for everything under the `-r` path. If a content path is specified, the script will begin tracking files for everything under the `-r` + `-c` paths, so if the content path is specified as `a/b`, the script with start tracking everything under `tiny_static_site/a/b`. If the default, `.`, is given, the script will start tracking everything under `/tmp/my_science_blog/`
    * Using the above commands, the config file looks like the following:
        ```
        cat config.yml
        $ content:
          - content
          doi_prefix: 'user-prefix'
          domain: https://production.domain.org
          id_type: doi
          pid_file: pid.json
        ```
#### **run_all**:
* Once the config and pid files are created, the user would need to do the following actions to begin file tracking.
* If the user is depositing the content with Crossref, a yml file is needed for the script to generate the xml file. 
  > An example yml file is located [here](https://gitlab.com/crossref/labs/static-page-id-generator/-/raw/main/submission_workflow/submission_info.yml?ref_type=heads). Please download the file to the root of your website repository and change the values in quotes to fit the values you need to deposit the metadata. Deposit credentials will be needed to be set as environment variables to deposit the xml file to Crossref.
* In the frontmatter of the markdown file of interest, add a frontmatter tag, `x-version` and the version of the file, so to initialize files that do not have tracking, do the following:
  * Add this `x-version: 0.0.0` to the frontmatter. Here's an example frontmatter setup in yaml:
     ```
     subject:
      - 2023
      author: XYZ
      categories:
      - Users
      - Metadata
      - Community
      date: 2023-02-28
      title: 'Metadata is great'
      x-version: 0.0.0
     ```
* Once the user has added tags for the number of files needed
* The user can generate the following command to run the following actions:
  * Generate PIDs for tracked files
  * The user will specify if the submission type is crossref or custom. The crossref deposit and registration workflow is part of this codebase. If it is a custom deposit and registration, the user will need to create that workflow
  * Currently, the workflow for creating urls is hardcoded for the crossref website, but there will be functionality added to allow for custom url generation
  * The script checks for the registered DOIs and if they have been registered successfully, the script will add it to the markdown files. The frontmatter of the processed file will look like this:
  ```
     DOI: https://doi.org/10.5555/mdabn8twsw
     subject:
      - 2023
      author: XYZ
      categories:
      - Users
      - Metadata
      - Community
      date: 2023-02-28
      title: 'Metadata is great'
      x-version: 0.0.0
     ```
* The gen-pid command have the following options:
    ```
    $ python run_all.py gen-pid --help
      Usage: run_all.py gen-pid [OPTIONS]

      Options:
        -cf, --conf-file TEXT           Name of config yml file. This file will be
                                        saved and should exist at the root of the
                                        repository
        -r, --repo DIRECTORY            Path to repository containing the files
                                        [required]
        -b, --batch
        -dry, --dry-run                 Run script upto deposit but do not deposit.
                                        Creates PIDs for files and stops
        -st, --sub-type [crossref|custom]
                                        Type of submission protocol
        --info FILE                     Submission information, for crossref, please
                                        enter path to the submittor information yml
                                        file
        --help                          Show this message and exit.
    ```
### DRY RUN of the script
* Running this in DRY RUN mode as a Crossref member will generate unique ids for the tagged files, generate urls (currently hardcoded for the Crossref website), generate a xml deposit file to deposit into the Crossref system:
```
  python run_all.py gen-pid -r /tmp/my_science_blog/ -st crossref --info /tmp/my_science_blog/submission_info.yml -dry

  Running in DRY RUN mode
  In DRY RUN mode, script will generate:
  1. unique identifier for each file with a x-version tag in frontmatter
  2. URL based on website logic. Currently hardcoded for the Crossref website
  3. Create a xml deposit file (currently hardcoded for Crossref) and save it to the specified directory. 
  4. Script will NOT deposit the file
  4. Script will NOT register a DOI
  4. Script will NOT add the DOI back to the file
  Generating PID(s)
  Files in ['.'] have been processed and written to /tmp/my_science_blog/quickstart/pid.json
  Generating URLs
  Generating XML document for submission
  SUCCESS! /tmp/my_science_blog/submission_info/20231029101102_submission.xml is valid. Ready for deposit
  DRY RUN ended. Please check /tmp/my_science_blog/pid.json for information on the versioned files and /tmp/my_science_blog/submission_info/20231029101102_submission.xml for the xml deposit file
```
The pid file will look like the following:
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

## RUN THE SCRIPT
### As a Crossref Member
* Dependencies:
  - requires deposit credentials and deposit endpoint declared as env variables
  - requires the member to fill out the `submission_info.yml` file and create a xml deposit directory which will store all the xml deposit files. Please copy the example submission yml from [here](https://gitlab.com/crossref/labs/static-page-id-generator/-/raw/main/submission_workflow/submission_info.yml?ref_type=heads), change the values in the quotes to reflect your data, and save the file as `submission_info.yml` at the root of the website repository. 
  - As an example, change the `submission_info.yml` file values to this:
    ```
    depositor: 
        - name: "Test"
        - email: "t@test.org"
    registrant: Test"
    submission_path: "submission_info"
    batch_id: "test.id.batch"
    ```
  - `mkdir submission_info` at the root of the website directory. This will be the directory that contains the xml deposit files.
  - If the user wants the DOI to be displayed, add a [DOI shortcode](https://gohugo.io/templates/shortcode-templates/) so that it will be displayed on the website. Here is an example of a DOI shortcode in use on the Crossref [website](https://www.crossref.org/operations-and-sustainability/annual-report/).
* Once `x-version: 0.0.0` or `x-version = "0.0.0"` (depending on if the frontmatter is in yaml or toml), has been added to the files that the user wants tracked, running eveything as a Crossref member, the script will do the following:
  - unique identifier for each file with a x-version tag in frontmatter
  - URL based on website logic. Currently hardcoded for the Crossref website
  - Create a xml deposit file (currently hardcoded for Crossref) and save it to the specified directory. 
  - Script will deposit the file
  - Script will register a DOI
  - Script will add the DOI back to the file
* Using the quickstart [repository](https://gitlab.com/crossref/labs/static-page-id-generator/-/blob/main/quickstart.md?ref_type=heads#create-a-new-site-and-generate-some-content) as an example, if a user starts out with a markdown file in this format:
  ```
  +++
  title = 'My First Post'
  date = 2023-10-26T13:12:40-04:00
  draft = false
  +++
  test test
  ```
  and adds the `x-version = "0.0.0"` tag to this:
  ```
  +++
  title = 'My First Post'
  date = 2023-10-26T13:12:40-04:00
  draft = false
  x-version = "0.0.0"
  +++
  test test
  ```
  and commits this to git. Running the script will eventually generate this in the markdown file:
  ```
  +++
  DOI = "https://some-doi-registered"
  title = 'My First Post'
  date = 2023-10-26T13:12:40-04:00
  draft = false
  x-version = "0.0.0"
  +++
  test test
  ```
  * Here is an example of the [end result](https://www.crossref.org/operations-and-sustainability/annual-report/), where a DOI appears on the website. A DOI shortcode is implemented in this website for it to appear the way it does.
  #### Running the script:
  * First initialize the repository with the following:
    - repository path: `-r /tmp/my_science_blog/`
    - content path: `-c content` If no `-c` option is included, the content path has a default value of `.` which would be everything under the repository path: 
    - domain: `-d http://production-domain,org`
    - doi-prefix: `member-doi-prefix`

    It will create `config.yml` and `pid.json` 
    ```
    python run_all.py init -r /tmp/my_science_blog/ -c content -d "https://production-domain.org" --doi-prefix "member-doi-prefix"
    Config file created: -r /tmp/my_science_blog/config.yml
    Pid tracking file: -r /tmp/my_science_blog/pid.json created
    ```
    After the files are initialized, run the script. It will need the following:
    - repository path: `-r /tmp/my_science_blog/`
    - submission type: `-st crossref`. As a Crossref member, it will be Crossref
    - submission info: `-info /tmp/my_science_blog/submission_info.yml` which is the file that was saved for deposit purposes. For more information, please go [here](#as-a-crossref-member). The name can be whatever you want it to be, you just have to specify the full path and the filename with the `-info` option for the script
    - As a reminder, please have a directory ready to save the xml deposit files. This would be the same directory listed as the `submission_path` value in the `submission_info.yml` file
    - As a reminder, please have your deposit credentials and the deposit endpoint environment variables set. Otherwise, the deposit, DOI registration, and DOI addition to the script will fail.

    Run the script and you get the following:
    ```
    python run_all.py gen-pid -r /tmp/my_science_blog/ -st crossref --info /tmp/my_science_blog/submission_info.yml
    Generating PID(s)
    Files in ['.'] have been processed and written to website-repo/pid.json
    Generating URLs
    Generating XML document for submission
    SUCCESS! /tmp/my_science_blog/submission_info/20231026164029_submission.xml is valid. Ready for deposit
    Submitting file:  /tmp/my_science_blog/submission_info/20231026164029_submission.xml
    Submission was successful
    Updating doi status in /tmp/my_science_blog/pid.json
    DOI status updated
    Checking doi registration status
    Checking DOI URLs
    Added DOI:  /tmp/my_science_blog/content/posts/my-first-post.md
    ```

### Just tell me how to run everything:
1. Clone the static page id generator repository. Establish the virtual environment, install all the requirements. From the root of this reposiory, run the initialize step:
    * `python run_all.py init -r /path/to/website/repo/ -c /specify/path/to/content -d "https://production-domain.org" --doi-prefix "member-doi-prefix"`
2. Add the `x-version` tag to the markdown frontmatter and follow the semantic versioning convention and add `0.0.0`. 
    * `x-version: 0.0.0` for yaml or `x-version = "0.0.0"` for toml
3. If you are a Crossref member, please satisfy the [dependencies](#as-a-crossref-member). Run this:
    * `python run_all.py gen-pid -r /path/to/website/repo/ -st crossref --info /path/to/website/repo/submission_info.yml`
4. If you are NOT a Crossref member, you can run the script in the following way. This will generate file information in `pid.json` but will not generate urls, deposit files, or register the DOIs. 
    * `python run_all.py gen-pid -r /path/to/website/repo/ -st custom`

### Individual scripts
The following documentation walks through the scripts used. You can run the scripts individually but they have dependencies. The chain of dependency is as follows:
* Initialize the repository, for info: 
  - `python run_all.py init --help`
* Generate IDs in the tracked files and adds them to the PID tracking json file, for more info:
  - `python id.py --help`
* Generate URLs(currently hardcoded for the Crossref website) and add them to the PID tracking JSON file, for more info:
  - `python helper_url_generation/url_constructor.py -h`
* Generate xml files for deposit, for more info:
  - `python submit_files/create_xml_files.py -h`
* Deposit the xml files, for more info:
  - `python submit_files/submit_files.py -h`
* Add DOIs to the frontmatter of the tracked markdown files:
  - `python add_doi.py -h`

 

## Developer Information
* As of now, only integration tests are available. To run tests, after cloning the repository and installing the requirements, please run the following:
`pytest tests/functional_tests`
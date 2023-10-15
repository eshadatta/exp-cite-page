import argparse

def set_args2(argv):
    parser = argparse.ArgumentParser(description='Parses YAML files and ENV vars specified with a tag')
    parser.add_argument("-c", "--conf-file",  help="Path to config file")
    parser.add_argument('-i', '--initialize', help='Create config and pid files', action='store_true')
    parser.add_argument('-id', '--id-type', choices=['doi', 'uuid'], required=True)
    id_types, _ = parser.parse_known_args(argv)
    # adding another argparse object to process sub commands associated with a specific argument
    idtype_parser = argparse.ArgumentParser(
        description="Generate a permanent ID for a static site generator", parents=[parser], add_help=False)
    if id_types.initialize:
        idtype_parser.add_argument('--repo-path', help='Path to repository containing the files', required=True)
        idtype_parser.add_argument('--content', required=True, type=str, nargs='+', help="Examples: -c filepath1 filepath2; relative to the repository root")
        idtype_parser.add_argument('--domain', help='Production domain of the content, for example: https://www.crossref.org/', required=True)
    if id_types.id_type == "doi":
        idtype_parser.add_argument('--doi-prefix', required=True, help="Add doi prefix string to this argument, example: --doi-prefix 'x.xxx'")
    args = idtype_parser.parse_args(argv)
    return args

def set_args(argv):
    paramsDetails = {
        'inputpath': {
        '-': 'i',
        '--': '--inputpath',
        'dest': 'userinputpath',
    'type': 'str',
    'metavar': 'PATH',
    'help': 'REQUIRED, input path of base folder of the files in which to scan. ',
    'required': True
    },
    'depth': {
        '-': 'd',
        '--': '--depth',
        'dest': 'directorydepth',
    'type': 'int',
    'metavar': 'INT',
    'help': 'depth to do down in path. ',
    }}
    paramsDetails2 = {
        'initialize': {
        '-i': 'i',
        '--': '--inputpath',
        'dest': 'userinputpath',
    'type': 'str',
    'metavar': 'PATH',
    'help': 'REQUIRED, input path of base folder of the files in which to scan. ',
    'required': True
    },
    'depth': {
        '-': 'd',
        '--': '--depth',
        'dest': 'directorydepth',
    'type': 'int',
    'metavar': 'INT',
    'help': 'depth to do down in path. ',
    }}

    parser = argparse.ArgumentParser(description='My test')

    for definition in paramsDetails.values():
        flags = []
        flag_short = definition.pop("-", None)
        if flag_short:
            flags.append(f"-{flag_short}")
        flag_long = definition.pop("--", None)
        if flag_long:
            flags.append(flag_long)
        if "type" in definition:
            definition["type"] = getattr(__builtins__, definition["type"])
        parser.add_argument(*flags, **definition)
    args = parser.parse_args()
    return args

def main(argv=None):
    a = set_args(argv)
    print(a)

if __name__ == "__main__":
    main()
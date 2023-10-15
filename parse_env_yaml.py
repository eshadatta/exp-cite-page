import re
import argparse
import yaml
import os

# Credit to https://dev.to/mkaranasou/python-yaml-configuration-with-environment-variables-parsing-2ha6
# for this code
def parse_config(file, tag='!ENV'):
    pattern = re.compile('.*?\${(\w+)}.*?')
    loader = yaml.SafeLoader
    loader.add_implicit_resolver(tag, pattern, None)

    def constructor_env_variables(loader, node):
        """ 
        Extracts the environment variable from the node's value
        :param yaml.Loader loader: the yaml loader
        :param node: the current node in the yaml
        :return: the parsed string that contains the value of the environment
        variable
        """
        value = loader.construct_scalar(node)
        match = pattern.findall(value)  # to find all env variables in line
        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(
                    f'${{{g}}}', os.environ.get(g, g)
                )
            return full_value
        return value
    
    loader.add_constructor(tag, constructor_env_variables)
    with open(file, 'r') as f:
        data = yaml.load(f, Loader=loader)

    return data

def set_args():
    parser = argparse.ArgumentParser(description='Parses YAML files and ENV vars specified with a tag')
    parser.add_argument("-c", "--conf-file",  help="Path to config file")
    args = parser.parse_args()
    return args

def main():
    args = set_args()
    data = parse_config(args.conf_file)
    print(data)

if __name__ == '__main__':
    main()
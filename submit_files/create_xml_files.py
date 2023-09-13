import argparse
import os
from os.path import exists
import helpers.deposit_structure as d
import helpers.generate_xml as g
from datetime import datetime
import yaml
import xmlschema
import json

def check_path(parser, p):
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    return os.path.normpath(p)

def set_args(argv):
    parser = argparse.ArgumentParser(
                    description="Submit files for DOI registration")
    parser.add_argument('-p', '--pid_file', help='Path and name to pid json file for parsing', type=lambda p:check_path(parser,p), required=True)
    parser.add_argument('-b', '--batch_id', help='DOI Batch ID', required=True, type=str)
    parser.add_argument('-dn', '--depositor_name', help='Depositor Name', required=True, type=str)
    parser.add_argument('-de', '--depositor_email', help='Depositor Email', required=True)
    parser.add_argument('-re', '--registrant', help='Registrant', required=True, type=str)
    parser.add_argument('-f', '--xml-file-name', help='Deposit file name', required=True, type=str)
    parser.add_argument('-s', '--xml-schema', help='Crossref schema to validate deposit file', default="https://www.crossref.org/schemas/crossref5.3.0.xsd")
    args = parser.parse_args(argv)
    return args

def get_xml_structure():
    file_path = os.path.dirname(os.path.abspath(__file__))
    elements = f"{file_path}/helpers/elements.yml"
    xml_structure = None
    try:
        with open(elements, 'r') as f:
            xml_structure = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}")
    return xml_structure

def gen_deposit_structure(args, xml_structure, docs):
    batch_id = args.batch_id
    depositor_name = args.depositor_name
    depositor_email = args.depositor_email
    registrant = args.registrant
    now = datetime.now()
    timestamp = now.strftime("%Y")+now.strftime("%m")+now.strftime("%d")+now.strftime("%H")+now.strftime("%M")+now.strftime("%S")
    ds = d.DepositStructure(xml_structure, batch_id, timestamp, depositor_name, depositor_email, registrant)
    ht = ds.tree_fragment('head')
    bt = ds.tree_fragment('body')
    head_tree = ds.head_tree(ht, 'head')
    body_tree = ds.body_tree(bt, 'body', docs)
    whole_xml_structure = ds.gen_xml(head_tree, body_tree)
    return whole_xml_structure

def validate(schema, filename):
    xsd = xmlschema.XMLSchema(schema)
    try:
        xsd.validate(filename)
    except Exception as e:
        print ("ERROR: ", e)
        exit(1)
    
def gen_xml_docs(structure, name):
    tree = g.gen_xml(structure)
    try:
        tree.write(name, encoding="UTF-8", xml_declaration=True)
    except Exception as e:
        print(e)

def get_docs(pid_file):
    all_docs = None
    try:
        with open(pid_file, 'r') as f:
            all_docs = json.load(f)
    except Exception as e:
        print("ERROR: ", e)
    # getting documents which have not yet had a doi registered
    unsubmitted_doi_docs = list(filter(lambda x: not(x['doi']['submitted']), all_docs))
    return unsubmitted_doi_docs
    
def main(argv = None):
    args = set_args(argv)
    docs = get_docs(args.pid_file)
    xml_structure = get_xml_structure()
    s = gen_deposit_structure(args, xml_structure, docs)
    gen_xml_docs(s, args.xml_file_name)
    validate(args.xml_schema, args.xml_file_name)
    print(f"SUCCESS! {args.xml_file_name} is valid. Ready for deposit")
if __name__ == "__main__":
    main()
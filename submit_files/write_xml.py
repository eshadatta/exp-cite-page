import xml.etree.cElementTree as ET
import yaml

def parse_dict(d, element_to_be_attached, attribute=None):
    for k, v in d.items():
        if isinstance(v, dict):
            if k == "posted_content":
                el = ET.SubElement(element_to_be_attached, k, attribute)
            else:
                el = ET.SubElement(element_to_be_attached, k)
            parse_dict(d[k], el)
        else:
            ET.SubElement(element_to_be_attached, k).text = v





root_attributes = {
   "xmlns:xsi":  "http://www.w3.org/2001/XMLSchema-instance",
   "xsi:schemaLocation": "http://www.crossref.org/schema/5.3.0 https://www.crossref.org/schemas/crossref5.3.0.xsd",
   "xmlns": "http://www.crossref.org/schema/5.3.0",
   "version" : "5.3.0"
}

#d = {'head': {'doi_batch_id': 'Value', 'timestamp': 'Value', 'depositer': {'depositer_name': 'Value', 'email_address': 'value'}, 'registrant': 'Value'}, 'body': [{'posted_content': {'titles': {'title': 'Value'}, 'posted_date': {'month': 'Value', 'day': 'Value', 'year': 'Value'}, 'doi_data': {'doi': 'Value', 'resource': 'Value'}}},{'posted_content': {'titles': {'title': 'Vawlue'}, 'posted_date': {'month': 'Valwue', 'day': 'Valwue', 'year': 'Vawlue'}, 'doi_data': {'doi': 'Vawlue', 'resource': 'Valeue'}}}]}
d1 = {'doi_batch': {'head': {'doi_batch_id': 'test.x.e', 'timestamp': '20210831112133', 'depositor': {'depositor_name': 'test', 'email_address': 'test@t.org'}, 'registrant': 'registrations'}, 'body': [{'posted_content': {'titles': {'title': 't'}, 'posted_date': {'month': '08', 'day': '31', 'year': '2023'}, 'doi_data': {'doi': '10.5555/gKRKLTA', 'resource': 'https://www.crossref.org/xml-samples1/'}}}, {'posted_content': {'titles': {'title': 'x'}, 'posted_date': {'month': '08', 'day': '31', 'year': '2023'}, 'doi_data': {'doi': '10.5555/gKsKLTA', 'resource': 'https://www.crossref.org/xml-samples2/'}}}]}}
#d = {'head': {'doi_batch_id': 'Value', 'timestamp': 'Value', 'depositer': {'depositer_name': 'Value', 'email_address': 'value'}, 'registrant': 'Value'}}
'''
structure = {
            "doi_batch_id": "value",
            "timestamp": "value",
            "depositer": {"depositer_name": "value", "email_address": "value"},
            "registrant": "value"
            }


head = ET.SubElement(root, "head")
for k, v in structure.items():
    if isinstance(v, dict):
        el = ET.SubElement(head, k)
        for e, val in v.items():
            ET.SubElement(el, e).text = val
    else:
        ET.SubElement(head, k).text = v

'''

#ET.SubElement(doc, "field1", name="blah").text = "some value1"
#ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

#root = ET.Element("doi_batch", root_attributes)

root_el_name = list(d1.keys())[0]
root = ET.Element(root_el_name, root_attributes)
second_level_elements = list(d1[root_el_name].keys())
#with open('submit_files/elements.yml', 'r') as f:
 #   xml_structure = yaml.safe_load(f)
#head = ET.SubElement(root, "head")
#body = ET.SubElement(root, "body")
#second_level_xml_elements = {}
print(second_level_elements)

for i in second_level_elements:
    attribute = None
    sub_el = ET.SubElement(root, i)
    if i == "body":
        attribute={"type": "other"}
    if isinstance(d1[root_el_name][i], list):
        for e in d1[root_el_name][i]:
            parse_dict(e, sub_el, attribute)
    else:
        parse_dict(d1[root_el_name][i], sub_el, attribute)


""" with open('submit_files/elements.yml', 'r') as f:
    r = yaml.safe_load(f)

print(r) """
tree = ET.ElementTree(root)
tree.write("test9.xml", encoding="UTF-8", xml_declaration=True)

'''
#parse_dict(d['head'], head, attribute={"type": "other"})
#for i in d['body']:
    #parse_dict(i, body, attribute={"type": "other"})
with open('submit_files/elements.yml', 'r') as f:
    r = yaml.safe_load(f)

print(r)
tree = parse_dict2(r, root_attributes, {"type": "other"})
tree.write("test8.xml")
#tree = ET.ElementTree(root)
#tree.write("test6.xml")'''
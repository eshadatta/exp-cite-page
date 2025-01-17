import xml.etree.cElementTree as ET

def root_attributes():
    ra = {"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance", "xsi:schemaLocation":"http://www.crossref.org/schema/5.3.0 https://www.crossref.org/schemas/crossref5.3.0.xsd", "xmlns":"http://www.crossref.org/schema/5.3.0", "version":"5.3.0"}
    return ra

def process_authors(el, authors_info):
    for n in authors_info:
        for key, authors in n.items():
            el_person_name = ET.SubElement(el, key,  {"sequence": n['person_name']['sequence'], "contributor_role": "author"})
            for field, auth_info in authors.items():
                if not(field == 'sequence'):
                    attr = {"authenticated": "true"} if field == "ORCID" else {}
                    ET.SubElement(el_person_name, field, attr).text = auth_info

def parse_dict(d, element_to_be_attached, attribute=None):
    for k, v in d.items():
        if isinstance(v, dict):
            if k == "posted_content":
                el = ET.SubElement(element_to_be_attached, k, attribute)
            else:
                el = ET.SubElement(element_to_be_attached, k)
            parse_dict(d[k], el)
        elif isinstance(v, list) and k == "contributors":
            el = ET.SubElement(element_to_be_attached, k)
            process_authors(el, v)
        else:
            ET.SubElement(element_to_be_attached, k).text = v

def gen_xml(structure):
    root_element = list(structure.keys())[0]
    second_level_elements = list(structure[root_element].keys())
    root = ET.Element(root_element, root_attributes())
    for i in second_level_elements:
        attribute = None
        sub_el = ET.SubElement(root, i)
        if i == "body":
            attribute={"type": "other"}
        if isinstance(structure[root_element][i], list):
            for e in structure[root_element][i]:
                parse_dict(e, sub_el, attribute)
        else:
            parse_dict(structure[root_element][i], sub_el, attribute)
    tree = ET.ElementTree(root)
    return tree



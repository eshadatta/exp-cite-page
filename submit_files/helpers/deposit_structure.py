from datetime import datetime
from copy import deepcopy

class DepositStructure:
    def __init__(self, xml_structure, doi_batch_id, timestamp, dn, de, dr):
        self._xml_structure = xml_structure
        self._root_el_name = "doi_batch"
        self._second_level_elements = ["head", "body"]
        self.batch_id = doi_batch_id
        self.timestamp = timestamp
        self.dn = dn
        self.de = de
        self.dr = dr
    
    @property
    def xml_structure(self):
        return self._xml_structure
    
    @property
    def root_element(self):
        return self._root_el_name
    
    @property
    def second_level_elements(self):
        return self._second_level_elements
    
    def traverse_tree(self, d, doc, t):
        for k, v in d.items():
            if isinstance(v, dict):
                self.traverse_tree(d[k], doc, t)
            else:
                if k == 'month':
                    d[k] = t.strftime("%m")
                elif k == 'day':
                    d[k] = t.strftime("%d")
                elif k == 'year':
                    d[k] = t.strftime("%Y")
                elif k in list(doc.keys()):
                    d[k] = doc[k]
        return d

    def tree_fragment(self, el_name):
        tf = self.xml_structure[self.root_element][el_name]
        return tf
      
    def head_tree(self, head_tf, el_name):
        head_tree = deepcopy(head_tf)
        head_tree['doi_batch_id'] = self.batch_id
        head_tree['timestamp'] = self.timestamp
        head_tree['depositor']['depositor_name'] = self.dn
        head_tree['depositor']['email_address'] = self.de
        head_tree['registrant'] = self.dr
        return {el_name: head_tree}
    
    def convert_doc_structure(self, docs):
        struct_docs = []
        crosswalk = {
            'title': 'title',
            'doi_prefix': 'doi', 
            'url': 'resource',
        }
        for d in docs:
            info = {}
            for k, v in crosswalk.items():
                if k == 'doi_prefix':
                    info[v] = d[k] + "/" + d['current_id']
                else:
                    info[v] = d[k]
            if 'authors' in d.keys():
                info['contributors'] = []
                for a in d['authors']:
                    author_info = {}
                    author_info['sequence'] = a['sequence']
                    author_info['given_name'] = a['given_name']
                    author_info['surname'] = a['surname']
                    if 'ORCID' in a.keys():
                       author_info['ORCID'] =  a['ORCID']
                    info['contributors'].append({'person_name': author_info})
            struct_docs.append(info)
        return struct_docs

    def body_tree(self, body_tree, el_name, docs):
        now = datetime.now()
        structure = body_tree
        crosswalked_docs = self.convert_doc_structure(docs)
        xml_docs = []
        for d in crosswalked_docs:
            tmp = deepcopy(structure[0])
            t = self.traverse_tree(tmp, d, now)
            xml_docs.append(t)
        body_tree_structure = {el_name: xml_docs}
        return body_tree_structure
    
    def gen_xml(self, head, body):
        whole_structure = deepcopy(self.xml_structure)
        root_element = self.root_element
        head.update(body)
        for k, v in head.items():
            whole_structure[root_element][k] = v
        return whole_structure


    
    
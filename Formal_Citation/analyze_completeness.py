import os
import argparse
import re
import json
import csv

from pathlib import Path
from articlenizer import formatting

fields = []

class PlainEntry:
    def __init__(self, f, idx, creator=False, name=False, archive=False, pub_year=False, pub_date=False, pub_nd=False, identifier=False, url=False, version=False, date_of_access=False, type_of_citation=False, description=False, lic=False, manual=False):
        self.dict = {
            'File': f, 
            'Idx': idx, 
            'Creator': creator, 
            'Name': name, 
            'Archive': archive, 
            'PubDate_year': pub_year, 
            'PubDate_exact': pub_date, 
            'PubDate_nd': pub_nd, 
            'ID': identifier, 
            'URL': url, 
            'Version': version, 
            'Date_of_access': date_of_access, 
            'Type_of_citation': type_of_citation, 
            'Description': description, 
            'License': lic, 
            'Manual': manual
        }

class ComplexEntry:
    def __init__(self, f, idx):
        entry = PlainEntry(f, idx)
        self.dict = {
            'reference_missing': False,
            'article_missing': False
        }
        for k, v in entry.dict.items():
            self.dict[k] = v
            if k not in ['File', 'Idx']:
                for x in ['unstructured', 'incomplete_content', 'wrong_content', 'wrong_place']:
                    self.dict['{}<>{}'.format(k, x)] = v
        self.dict['duplicate'] = 0
        self.dict['wrong_content'] = 0  

def gather_files(folder_list):
    print("Loading files for {}".format(folder_list))
    combined_files = {}
    for folder in folder_list:
        combined_files.update(gather_files_folder(folder))
    return combined_files

def gather_files_folder(folder):
    all_txt_files = list(Path(folder).rglob('*.txt'))
    all_ann_files = list(Path(folder).rglob('*.ann'))
    plain_txt_names = set([p.with_suffix('') for p in all_txt_files])
    plain_ann_names = set([p.with_suffix('') for p in all_ann_files])
    only_txt_names = plain_txt_names - plain_ann_names
    only_ann_names = plain_ann_names - plain_txt_names
    if only_txt_names:
        print(RuntimeWarning("The following text files have no annotation file: {}".format([str(p) for p in only_txt_names])))
    if only_ann_names:
        print(RuntimeWarning("The following annotation files have no text file: {}".format([str(p) for p in only_ann_names])))
    all_files = plain_txt_names & plain_ann_names
    all_files = {str(p).split('/')[-1]: {'txt': Path(str(p) + '.txt'), 'ann': Path(str(p) + '.ann')} for p in all_files}
    return all_files

def handle_plain_entities(file_name, entities):
    labels = set([x['label'] for x in entities])
    file_id, ref_id = file_name.rsplit('.', maxsplit=1)[0].rsplit('/', maxsplit=1)[-1].split('_', maxsplit=1)
    entry = PlainEntry(file_id, ref_id, creator='Creator' in labels, name='Name' in labels, archive='Archive' in labels, pub_year='PubDate_year' in labels, pub_date='PubDate_exact' in labels, pub_nd='PubDate_nd' in labels, identifier='ID' in labels, url='URL' in labels, version='Version' in labels, date_of_access='Date_of_access' in labels, type_of_citation='Type_of_citation' in labels, description='Description' in labels, lic='License' in labels, manual='Manual' in labels)
    return entry

def handle_complex_entities(file_name, entities):
    file_id, ref_id = file_name.rsplit('.', maxsplit=1)[0].rsplit('/', maxsplit=1)[-1].split('_', maxsplit=1)
    if file_name == 'database_info/ready_annotated/PMC3283723_72.ann':
        print("complex case")
    entry = ComplexEntry(file_id, ref_id)
    for idx, entity in enumerate(entities):
        matching = []
        for idx_2, entity_2 in enumerate(entities):
            if idx != idx_2:
                if entity['beg'] == entity_2['beg'] or entity['end'] == entity_2['end']:
                    matching.append(entity_2)
        if entity['label'] in ['unstructured', 'incomplete_content', 'wrong_place']:
            pass
        elif entity['label'] == 'wrong_content':
            if not matching:
                entry.dict[entity['label']] += 1
        elif entity['label'] == 'duplicate':
            entry.dict[entity['label']] += 1
        else:
            entry.dict[entity['label']] = True
            for m in matching:
                entry.dict['{}<>{}'.format(entity['label'], m['label'])] = True
    return entry

def get_entities_in_range(entities, start, end):
    e = [x for x in entities.values() if x['beg'] >= start and x['end'] <= end]
    return e

def get_entry_info(file_name, entities, txt, start, end):
    file_id, ref_id = file_name.rsplit('.', maxsplit=1)[0].rsplit('/', maxsplit=1)[-1].split('_', maxsplit=1)
    entries = []
    if '<<reference missing>>' in txt[start:end]:
        entry = ComplexEntry(file_id, ref_id)
        entry.dict['reference_missing'] = True
        entries.append(entry)
    elif '<<article_missing>>' in txt[start:end]:
        entry = ComplexEntry(file_id, ref_id)
        entry.dict['article_missing'] = True
        entries.append(entry)
    elif '<<<' in txt[start:end]:
        match = re.search('<<<\w{3}_entry_\d+>>>', txt[start:end])
        start_idx = start + match.end()
        current_idx = start_idx
        for match in re.finditer('<<<\w{3}_entry_\d+>>>', txt[start_idx:end]):
            matched_entities = get_entities_in_range(entities, current_idx, start_idx + match.start())
            current_idx = start_idx + match.end() 
            entry = handle_complex_entities(file_name, matched_entities)
            entries.append(entry)
        matched_entities = get_entities_in_range(entities, current_idx, end)
        entry = handle_complex_entities(file_name, matched_entities)
        entries.append(entry)
    else:
        entry = get_entities_in_range(entities, start, end)
        entry = handle_complex_entities(file_name, entry)
        entries.append(entry)
    return entries

def to_csv(anno):
    with open('./info_summary_txt.csv', 'w') as txt_anno_out, \
            open('./info_summary_xml.csv', 'w') as xml_anno_out, \
            open('./info_summary_sem.csv', 'w') as sem_anno_out, \
            open('./info_summary_cro.csv', 'w') as cro_anno_out:
        entry = PlainEntry('t', 't')
        txt_w = csv.DictWriter(txt_anno_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=entry.dict.keys())
        entry = ComplexEntry('t', 't')
        xml_w = csv.DictWriter(xml_anno_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=entry.dict.keys())
        sem_w = csv.DictWriter(sem_anno_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=entry.dict.keys())
        cro_w = csv.DictWriter(cro_anno_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=entry.dict.keys())
        txt_w.writeheader()
        xml_w.writeheader()
        sem_w.writeheader()
        cro_w.writeheader()
        for k, v in anno.items():
            with v['ann'].open() as a_in, v['txt'].open() as t_in:
                a = a_in.read()
                t = t_in.read()
                a_dict = formatting.annotation_to_dict(a)['entities']

                m = re.search('<<<publisher>>>', t)
                txt_entities = get_entities_in_range(a_dict, 0, m.start())
                txt_entry = handle_plain_entities(str(v['ann']), txt_entities)
                txt_w.writerow(txt_entry.dict)

                m2 = re.search('<<<semantic_scholar>>>', t)
                xml_entities = get_entities_in_range(a_dict, m.end(), m2.start())
                xml_entry = handle_complex_entities(str(v['ann']), xml_entities)
                xml_w.writerow(xml_entry.dict)

                m3 = re.search('<<<crossref>>>', t)
                sem_info = get_entry_info(str(v['ann']), a_dict, t, m2.end(), m3.start())
                for x in sem_info:
                    sem_w.writerow(x.dict)
                cro_info = get_entry_info(str(v['ann']), a_dict, t, m3.end(), len(t))
                for x in cro_info:
                    cro_w.writerow(x.dict)
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Calculate IRR between BRAT annotations")
    parser.add_argument("--annotation", required=True, nargs='+', help="Path to first annotation folders.")
    args = parser.parse_args()
    
    ann = gather_files(args.annotation)
    ann = dict(sorted(ann.items()))

    to_csv(ann)
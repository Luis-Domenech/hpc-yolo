import numpy as np
import os
import xml.etree.ElementTree as ET
import pickle
import copy

def parse_voc_annotation(ann_dir, img_dir, cache_name, labels=[]):
    if os.path.exists(cache_name):
        with open(cache_name, 'rb') as handle:
            cache = pickle.load(handle)
        all_insts, seen_labels = cache['all_insts'], cache['seen_labels']
    else:
        all_insts = []
        seen_labels = {}
        
        for ann in sorted(os.listdir(ann_dir)):
            img = {'object':[]}

            try:
                tree = ET.parse(ann_dir + ann)
                root = tree.getroot()
            except Exception as e:
                print(e)
                print('Ignore this bad annotation: ' + ann_dir + ann)
                continue
            
            # for elem in tree.iter():
            #     if 'filename' in elem.tag:
            #         img['filename'] = img_dir + elem.text
            #     if 'width' in elem.tag:
            #         img['width'] = int(elem.text)
            #     if 'height' in elem.tag:
            #         img['height'] = int(elem.text)
            #     if 'object' in elem.tag or 'part' in elem.tag:
            #         obj = {}
                    
            #         for attr in list(elem):
            #             if 'name' in attr.tag:
            #                 obj['name'] = attr.text

            #                 if obj['name'] in seen_labels:
            #                     seen_labels[obj['name']] += 1
            #                 else:
            #                     seen_labels[obj['name']] = 1
                            
            #                 if len(labels) > 0 and obj['name'] not in labels:
            #                     break
            #                 else:
            #                     img['object'] += [obj]
                                
            #             if 'bndbox' in attr.tag:
            #                 for dim in list(attr):
            #                     if 'xmin' in dim.tag:
            #                         obj['xmin'] = int(round(float(dim.text)))
            #                     if 'ymin' in dim.tag:
            #                         obj['ymin'] = int(round(float(dim.text)))
            #                     if 'xmax' in dim.tag:
            #                         obj['xmax'] = int(round(float(dim.text)))
            #                     if 'ymax' in dim.tag:
            #                         obj['ymax'] = int(round(float(dim.text)))

            img['filename'] = img_dir + root.findall(".//filename")[0].text
            img['width'] = int(root.findall(".//width")[0].text)
            img['height'] = int(root.findall(".//height")[0].text)
            obj = {}

            try:
                obj['name'] = root.findall(".//name")[0].text
            except:
                obj["name"] = "palo"

            if obj['name'] in seen_labels:
                seen_labels[obj['name']] += 1
            else:
                seen_labels[obj['name']] = 1

            if len(labels) > 0 and obj['name'] not in labels:
                break
            else:
                img['object'] += [obj]

            try:
                l = len(root.findall(".//xmin"))            
            except:
                l = 0

            if l > 0:
                for box in range(l):

                    obj['xmin'] = int(round(float(root.findall(".//xmin")[box].text)))
                    obj['ymin'] = int(round(float(root.findall(".//ymin")[box].text)))
                    obj['xmax'] = int(round(float(root.findall(".//xmax")[box].text)))
                    obj['ymax'] = int(round(float(root.findall(".//ymax")[box].text)))

                    if len(img['object']) > 0:
                        all_insts += [copy.deepcopy(img)]

        cache = {'all_insts': all_insts, 'seen_labels': seen_labels}
        with open(cache_name, 'wb') as handle:
            pickle.dump(cache, handle, protocol=pickle.HIGHEST_PROTOCOL)    
                        
    return all_insts, seen_labels

# parse_voc_annotation("/home/dronicx/Documents/UPRM/2019-2020/RUMarino/yolov3/annotations/", "/home/dronicx/Documents/UPRM/2019-2020/RUMarino/yolov3/dataset/", "testing_parser.pkl", ["gate"])
import argparse
import os
import json
import yaml
import xml.etree.ElementTree as ET
import sys

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    return parser.parse_args()

def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = args.output_file
    
    if os.path.splitext(input_file)[1] == ".json":
        obj = loading_json(input_file)
    elif os.path.splitext(input_file)[1] in [".yml", ".yaml"]:
        obj = loading_yaml(input_file)
    elif os.path.splitext(input_file)[1] == ".xml":
        obj = loading_xml(input_file)
    else:
        print("Input file is not a JSON, YAML, or XML file.")
        sys.exit(1)
    
    if os.path.splitext(output_file)[1] == ".json":
        save_to_json(obj, output_file)
    elif os.path.splitext(output_file)[1] in [".yml", ".yaml"]:
        save_to_yaml(obj, output_file)
    elif os.path.splitext(output_file)[1] == ".xml":
        save_to_xml(obj, output_file)
    else:
        print("Output file is not a JSON, YAML, or XML file.")
        sys.exit(1)

def loading_json(input_file):
    if os.path.isfile(input_file):
        with open(input_file, "r") as file_js:
            file_content = file_js.read()
            json_obj = json.loads(file_content)
            return json_obj
    else:
        print("No such file")
        sys.exit(1)

def loading_yaml(input_file):
    if os.path.isfile(input_file):
        try:
            with open(input_file, "r") as file_ym:
                yaml_obj = yaml.safe_load(file_ym)
                return yaml_obj
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)
    else:
        print("No such file")
        sys.exit(1)

def loading_xml(input_file):
    if os.path.isfile(input_file):
        try:
            tree = ET.parse(input_file)
            xml_obj = tree.getroot()
            return xml_to_dict(xml_obj)
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            sys.exit(1)
    else:
        print("No such file")
        sys.exit(1)

def xml_to_dict(element):
    if len(element) > 0:
        return {element.tag: {child.tag: xml_to_dict(child) for child in element}}
    else:
        return {element.tag: element.text}

def save_to_json(obj, output_file):
    with open(output_file, "w") as file_js:
        json.dump(obj, file_js, indent=4)
        print(f"Data has been written to {output_file}")

def save_to_yaml(obj, output_file):
    with open(output_file, "w") as file_ym:
        yaml.dump(obj, file_ym, default_flow_style=False)
        print(f"Data has been written to {output_file}")

def dict_to_xml(tag, d):
    element = ET.Element(tag)
    for key, val in d.items():
        if isinstance(val, dict):
            child = dict_to_xml(key, val)
        else:
            child = ET.Element(key)
            child.text = str(val)
        element.append(child)
    return element

def save_to_xml(obj, output_file):
    if len(obj) == 1:
        root_tag = list(obj.keys())[0]
        root_element = dict_to_xml(root_tag, obj[root_tag])
    else:
        print("Error: XML root element must have a single root tag.")
        sys.exit(1)

    tree = ET.ElementTree(root_element)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Data has been written to {output_file}")

if __name__ == "__main__":
    main()

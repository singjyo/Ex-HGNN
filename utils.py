import json
import random
import string
import re
import yaml




def modify_repeating_letters(lst):
    """
    input  :  ['A', 'P', 'A']
    output :  ['A', 'P', 'A;']

    input  : ['B', 'F', 'C', 'F', 'B']
    output : ['B', 'F', 'C', 'F;', 'B;']
    """

    seen = set()  # Set to keep track of seen letters
    result = []   # Result list

    for item in lst:
        if item in seen:
            result.append(f"{item};")  # Append a semicolon if the item is repeating
        else:
            result.append(item)
            seen.add(item)  # Mark this item as seen

    return result


def generate_random_strings(count, length):
    return [''.join(random.choices(string.ascii_letters + string.digits, k=length)) for _ in range(count)]

def format_string(input_string, string_length=5):
    # Split the input string into characters, considering special cases like "P'"
    """
    input_string = ['A','P','A;']
    formatted_string = 'A stands for MWtFd, P stands for 3cDs4, A; stands for UHpQl'
    random_strings = '['MWtFd', '3cDs4', 'UHpQl']'
    string_matching_dict = '{'A': 'MWtFd', 'P': '3cDs4', 'A;': 'UHpQl'}'
    """
    elements = []
    i = 0
    while i < len(input_string):
        if i + 1 < len(input_string) and input_string[i + 1] == "'":
            elements.append(input_string[i:i+2])
            i += 2
        else:
            elements.append(input_string[i])
            i += 1

    # Generate random strings for each element
    random_strings = generate_random_strings(len(elements), string_length)
    string_matching_dict = {}
    for literal,rand_literal in zip(input_string,random_strings):
        string_matching_dict[literal] = rand_literal
    
    # Create the formatted string
    formatted_parts = [f"{element} stands for {random_string}" for element, random_string in zip(elements, random_strings)]
    formatted_string = ", ".join(formatted_parts)

    return formatted_string,random_strings,string_matching_dict

def get_regex_mapping_dict(metapath_instance,random_strings):
    """
    metapath_instance = ['Franz Baader',
      'Terminological Cycles in KL-ONE-based Knowledge Representation Languages.',
      'AAAI',
      'Old Resolution Meets Modern SLS.',
      'Abdul Sattar']

    random_strings = ['xyz','abc','def','ghi','jkl']

    regex_mapping_dict= {'xyz': 'Franz Baader',
    'abc': 'Terminological Cycles in KL-ONE-based Knowledge Representation Languages.',
    'def': 'AAAI',
    'ghi': 'Old Resolution Meets Modern SLS.',
    'jkl': 'Abdul Sattar'}

    """

    regex_mapping_dict = {}
    for metapath,rand_string in zip(metapath_instance,random_strings):
        regex_mapping_dict[rand_string] = metapath
    
    return regex_mapping_dict

def replace_with_dict_values_regex(text, replacements_dict):
    # Sort keys by length in descending order to replace longer matches first
    """
    input_text = 'Author xyz has published a paper titled abc, which has been presented at conference def. This conference also has a paper titled ghi, authored by jkl."
    replacements_dict = {
    'xyz': 'Franz Baader',
    'abc': 'Terminological Cycles in KL-ONE-based Knowledge Representation Languages.',
    'def': 'AAAI',
    'ghi': 'Old Resolution Meets Modern SLS.',
    'jkl': 'Abdul Sattar'}
    output_text : Author Franz Baader has published a paper titled Terminological Cycles in KL-ONE-based Knowledge Representation Languages., which has been presented at conference AAAI. This conference also has a paper titled Old Resolution Meets Modern SLS., authored by Abdul Sattar.
    """
    for key in sorted(replacements_dict.keys(), key=len, reverse=True):
        # Use \b for word boundary to match whole words only
        text = re.sub(r'\b' + re.escape(key) + r'\b', replacements_dict[key], text)
    return text

def generate_details_string(metapath_instance, details_dict):
    """
    metapath_instance = [
    'Franz Baader',
    'Terminological Cycles in KL-ONE-based Knowledge Representation Languages.',
    'AAAI',
    'Old Resolution Meets Modern SLS.',
    'Abdul Sattar'
     ]

    details_dict = {
        'Franz Baader': "Some details about Franz Baader",
        'Terminological Cycles in KL-ONE-based Knowledge Representation Languages.': "",
        'AAAI': "Details about AAAI conference",
        'Old Resolution Meets Modern SLS.': "Information on Old Resolution Meets Modern SLS.",
        'Abdul Sattar': ""
    }

    output_string : details related to Franz Baader: Some details about Franz Baader and details related to AAAI: Details about AAAI conference and details related to Old Resolution Meets Modern SLS.: Information on Old Resolution Meets Modern SLS.
    """
    details_string_parts = []
    for item in metapath_instance:
        if item in details_dict and details_dict[item]:  # Check if the item has non-empty details
            details_string_parts.append(f"details related to {item}: {details_dict[item]}")
    return " and ".join(details_string_parts)

def get_meta_path_context(metapath_strings,meta_path_instances_dict,metapath_in_natural_language_dict):
        meta_path_context_dict = ()
        for metapath,meta_path_instance_dict in zip(list(metapath_strings.keys()),meta_path_instances_dict):
            for key in meta_path_instance_dict.keys():
                meta_path_instances_list = meta_path_instance_dict[key]
                regex_mapping_dict_list=[get_regex_mapping_dict(metapath_instance,metapath_strings[metapath][1]) for metapath_instance in meta_path_instances_list]
                meta_path_instances_natural_language= [replace_with_dict_values_regex(metapath_in_natural_language_dict[metapath],regex_mapping_dict) for regex_mapping_dict in regex_mapping_dict_list]
                if key not in meta_path_context_dict:
                    meta_path_context_dict[key] =  meta_path_instances_natural_language
                else:
                    meta_path_context_dict[key].append(meta_path_instances_natural_language) 

        for key in meta_path_context_dict.keys():
            meta_path_context_dict[key] = [x for sub_list in meta_path_context_dict[key] for x in sub_list]
        return meta_path_context_dict


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k, v in self.__dict__.items():
            if type(v) is dict:
                setattr(self, k, Struct(**v))


def read_args(args_paths):
    final_config = {}
    with open(args_paths, "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        final_config = {**final_config, **config}

    return Struct(**final_config)


def save_artifacts(obj, output_file_path):
    with open(output_file_path, "w") as f:
        json.dump(obj, f, indent=4)


def save_args(obj, output_file_path):
    with open(output_file_path, "w") as f:
        yaml.dump(obj, f, default_flow_style=False)


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

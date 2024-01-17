
import argparse
from utils import read_args,modify_repeating_letters,generate_random_strings,replace_with_dict_values_regex,format_string
from metapath_extraction import meta_path_extraction
from neighbourhood_instance_extraction import find_generic_paths,get_k_hop_neighbours
from get_dataset import read_data









def parse_args():
    parser = argparse.ArgumentParser(description="exhgnn")
    parser.add_argument("--args-path")
    args = parser.parse_args()
    args = read_args(args.args_path)
    return args
    




def main(args):
    
    adjacency_list_info,edge_info,node_textual_attribute,edge_relations_with_example_mapping,metapath_summarization_example=read_data(args)
    meta_path_extractor= meta_path_extraction(args)
    filtered_result_simplified_only_target,filtered_result_simplified=meta_path_extractor.get_weights_by_metapath()
    node_acronyms_inv={value:key for key,value in args.node_acronyms.items()}
    required_metapaths=list(filtered_result_simplified_only_target.keys())[:args.top_metapath_needed]
    metapath_modified    = {metapath:modify_repeating_letters(metapath) for metapath in required_metapaths}
    metapath_strings     = {metapath:format_string(metapath_modified[metapath]) for metapath in required_metapaths}
    metapath_strings_with_acronyms = {metapath:metapath_modified[metapath] + ' '+ metapath_strings[metapath][0] for metapath in required_metapaths}
    path_sequence_list  =  [node_acronyms_inv[element] for element in required_metapaths]
    meta_path_instances =  [find_generic_paths(edge_info,path_sequence) for path_sequence in path_sequence_list]







if __name__ == "__main__":
    ARGS = parse_args()
    # set_logging_level(ARGS)
    main(ARGS)

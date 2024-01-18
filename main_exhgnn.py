
import argparse
from utils import read_args,modify_repeating_letters,format_string,get_meta_path_context
from metapath_extraction import meta_path_extraction
from neighbourhood_instance_extraction import find_generic_paths,get_k_hop_neighbours
from get_dataset import read_data
from llm_inference import initialize_llm_chains,chain_metapath_summary,chain_explanation_prediction
from scoring import get_scoring
import json










def parse_args():
    parser = argparse.ArgumentParser(description="exhgnn")
    parser.add_argument("--args-path")
    args = parser.parse_args()
    args = read_args(args.args_path)
    return args
    




def main(args):
    
    adjacency_list_info,edge_info,node_textual_attribute,edge_relations_with_example_mapping,metapath_summarization_example,target_categories=read_data(args)
    response_chain_prediction_explanation,response_chain_graph_summary = initialize_llm_chains(args)
    meta_path_extractor= meta_path_extraction(args)
    filtered_result_simplified_only_target,filtered_result_simplified=meta_path_extractor.get_weights_by_metapath()
    node_acronyms_inv={value:key for key,value in args.node_acronyms.items()}
    required_metapaths=list(filtered_result_simplified_only_target.keys())[:args.top_metapath_needed]
    metapath_modified    = {metapath:modify_repeating_letters(metapath) for metapath in required_metapaths}
    metapath_strings     = {metapath:format_string(metapath_modified[metapath]) for metapath in required_metapaths}
    metapath_strings_with_acronyms = {metapath:metapath_modified[metapath] + ' '+ metapath_strings[metapath][0] for metapath in required_metapaths}
    metapath_in_natural_language_dict = chain_metapath_summary(args,response_chain_graph_summary,edge_relations_with_example_mapping,metapath_summarization_example,metapath_strings_with_acronyms)
    
    path_sequence_list  =  [node_acronyms_inv[element] for element in required_metapaths]
    meta_path_instances_dict =  [find_generic_paths(edge_info,path_sequence) for path_sequence in path_sequence_list]
    meta_path_context_dict=get_meta_path_context(metapath_strings,meta_path_instances_dict,metapath_in_natural_language_dict)
    explanation_prediction_dict=chain_explanation_prediction(args,response_chain_prediction_explanation,meta_path_context_dict)
    user_llm_dict,f1_micro,f1_macro= get_scoring(args,explanation_prediction_dict,target_categories)
    with open(args.output_path + args.output_file_name,'w') as f:
        json.dump(user_llm_dict,f)


if __name__ == "__main__":
    ARGS = parse_args()
    # set_logging_level(ARGS)
    main(ARGS)

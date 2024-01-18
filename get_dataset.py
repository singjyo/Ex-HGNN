import json

def read_data(args):

    with open(args.adjacency_list_info_path,'r') as file:
       adjacency_list_info=json.load(file)

    with open(args.edge_info_path,'r') as file:
       edge_info=json.load(file)
    
    with open(args.node_textual_attribute_mapping,'r') as f:
       node_textual_attribute=json.load(f)

    with open(args.edge_relations_with_example_mapping,'r') as f:
       edge_relations_with_example_mapping=json.load(f)

    with open(args.metapath_summarization_example,'r') as f:
       metapath_summarization_example=json.load(f)

    with open(args.target_categories_mapping,'r') as f:
       target_categories=json.load(f)
    
    return adjacency_list_info,edge_info,node_textual_attribute,edge_relations_with_example_mapping,metapath_summarization_example,target_categories


    
    
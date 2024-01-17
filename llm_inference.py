import boto3
from bedrock import Bedrock
from langchain.chains import LLMChain
import config_llm_prompts as config
import re
import json
from langchain import PromptTemplate


def initialize_llm_chains(args):
            
    bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
    response_llm =Bedrock(model_id=args.bedrock_llm,client=bedrock_runtime,model_kwargs=config.GEN_HYPERPARAMETERS['anthropic.claude-v2:1'])

    response_prompt_template  = config.PROMPTS_DICT["get_explanation_and_prediction_v3"]
    summarize_prompt_template = config.PROMPTS_DICT['summarize_meta_path_v2']
    PROMPT = PromptTemplate(template=response_prompt_template, input_variables=['task-description',"node-name","context"])
    PROMPT_GRAPH_SUMMARY = PromptTemplate(template=summarize_prompt_template, input_variables=['node-type',"edge-relation","meta-path-summarization-example-1","meta-path"])

    response_chain_prediction_explanation = LLMChain(llm=response_llm,prompt=PROMPT,verbose=False)
    response_chain_graph_summary = LLMChain(llm=response_llm,prompt=PROMPT_GRAPH_SUMMARY,verbose=False)
    return response_chain_prediction_explanation,response_chain_graph_summary

def chain_metapath_summary(args,response_chain_graph_summary,edge_relations_with_example_mapping,metapath_summarization_example,metapath_strings_with_acronyms):
    
    node_acronyms_inv={value:key for key,value in args.node_acronyms.items()}
    node_acronyms_inv_list = [key+':'+value for key,value in node_acronyms_inv.items()]
    node_schema = '\n'.join(node_acronyms_inv_list)
    edge_relations = [key+':='+value for key,value in edge_relations_with_example_mapping.items()]
    edge_relation_schema = '\n'.join(edge_relations)
    metapath_summarization_example_list=list(metapath_summarization_example.values())
    metapath_summary_example_string = '\n'.join(metapath_summarization_example_list)
    #metapath_strings_with_acronyms_json_string = json.dumps(metapath_strings_with_acronyms)
    metapath_list_example_string = list(metapath_strings_with_acronyms.values())
    meta_path_summary_inputs = {'node-type':node_schema, 'edge-relation':edge_relation_schema,'meta-path-summarization-example-1':metapath_summary_example_string,'meta-path':metapath_list_example_string}
    generated_summary = response_chain_graph_summary.run(meta_path_summary_inputs)
    metapath_meanings = re.search(r"<meaning>(.*?)</meaning>", generated_summary, re.DOTALL)
    metapath_meanings_dict = {metapath:metapath_meanings[index] for index,metapath in enumerate(list(metapath_strings_with_acronyms.keys()))}
    return metapath_meanings_dict


def chain_explanation_prediction_summary(args,response_chain_prediction_explanation,meta_path_context_dict):
    
    for key in meta_path_context_dict:
        if len(meta_path_context_dict[key]['context']):
            try:
                source_documents= meta_path_context_dict[key]['context']
                source_documents_truncated = source_documents[:40]
                context = "\n•".join(source_documents_truncated)
                generated_response=response_chain_prediction_explanation.run({'task-description':args.task_description,'node-name':key,'context':context})
                meta_path_context_dict[key]['generated_response'] = generated_response
            except:
                print ("")
    return meta_path_context_dict






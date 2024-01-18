PROMPTS_DICT = {'summarize_meta_path_v1':'''

Human:You are a human whose goal is to generate the meaning of different meta-paths in heterogeneous graph network. You are provided with all the node types and edge-type and the underlying relation between them.  

A : Author
P : Paper
C: Conference

AP (A stands for {author-1}, P stands for {paper-1}) : Author {author-1} has published a paper with title and abstract as {paper-1}.
PA (P stands for {paper-1}, A stands for {author-1}):  Paper with title and abstract as {paper-1} has been published by an author {author-1}.
PC (P stands for {paper-1}, C stands for {conference-1}) :  Paper with title and abstract as {paper-1} has been published in conference titled as {conference-1}.
CP (C stands for {conference-1}, P stands for {paper-1}) :  Conference {conference-1} has paper with title and abstract as {paper-1} in its list of publications.

{meta-path-summarization-example-1}

Can u generate the meaning of following meta-paths :
APCP’A’ (A stands for {author-1}, P stands for {paper-1}, C stands for {conference-1}, P’ stands for {paper-2},A’ stands for {author-2})?
APCP’   (A stands for {author-1}, P stands for {paper-1}, C stands for {conference-1}, P’ stands for {paper-2})?

Write the meaning inside xml tags <meaning> </meaning>?

Assistant:''',

'summarize_meta_path_v2':'''

Human:You are a human whose goal is to generate the meaning of different meta-paths in heterogeneous graph network. You are provided with all the node types and edge-type and the underlying relation between them.  

Please find the node types enclosed inside the xml tags <node-type>,</node-type>
<node-type>{node-type}</node-type>

Edge-type and their underlying relation is enclosed between xml tags <edge-relation>,</edge-relation>
<edge-relation>{edge-relation}</edge-relation>

Please find one meta-path summarization example below:
{meta-path-summarization-example-1}

Can you generate the meaning of the following meta-paths enclosed inside xml tags <meta-path>,</meta-path>
<meta-path>{meta-path}</meta-path>

Write the meaning inside xml tags <meaning> </meaning>?

Assistant:''',
                
'get_explanation_and_prediction_v1':'''

You are a scientist who is required to read the academic details of an author such as the papers published by him and list of conferences and co-authors and provide the reasoning logic or methodology to get the prediction for the research of the author.  Post obtaining the prediction, you have to provide the justification and explanation.

The name of the author for which you have to predict the research area and provide explanation is enclosed in xml tags <author-name>{author-name}</author-name>
Please find the academic information of this author enclosed in xml tags <academic-information> , </academic-information>:
<academic-information>{context}</academic-information>
This academic information will help you in predicting the research area and providing the explanation and justification for it.

Human:

Provide the methodology to get the prediction for the research area of the author. Enclose the methodology in xml tags <methodology>,</methodology>. This is just the space for your notes and not meant to be shown to the user.
Get the prediction of the research area of the author, enclose the prediction in xml tags. <prediction>,</prediction>
Get the explanation behind the prediction for the research area of the author. Enclose it in xml tags <explanation>,</explanation>
 
 
Assistant:
''',
'get_explanation_and_prediction_v3':'''

Human: {task-description}
-provide the reasoning logic or methodology to get the prediction for the node.  Post obtaining the prediction, you have to provide the justification and explanation.

The name of the node for which you have to predict the label and provide explanation is enclosed in xml tags <node-name>{node-name}</node-name>
Please find the relevant context for this node enclosed in xml tags <relevant-context> , </relevant-context>:
<relevant-context>{context}</relevant-context>

This context will help you in predicting the label and providing the explanation and justification for it.

Assistant: Thanks for providing the task-description and relevant context. Do you have any other instructions.

Human: Provide the methodology to get the prediction for the label of the node. Enclose the methodology in xml tags <methodology>,</methodology>. This is just the space for your notes and not meant to be shown to the user.
Get the prediction of the label of the node, enclose the prediction in xml tags. <prediction>,</prediction>
Get the explanation behind the prediction for the label of the node. Enclose it in xml tags <explanation>,</explanation>

# think in terms of steps to get the prediction of the node, and mention your steps in <explanation></explanation>
 
Assistant:
''',
'get_explanation_v3':'''

Human: {task-description}
-You are given the prediction of the label of the node, you have to provide the justification and explanation.

Prediction of the node for which you have to provide explanation is enclosed in xml tags <node-prediction>{node-prediction}</node-prediction>
Please find the relevant context for this node enclosed in xml tags <relevant-context> , </relevant-context>:
<relevant-context>{context}</relevant-context>

This context will help you in providing the explanation and justification for it.

Assistant: Thanks for providing the task-description and relevant context. Do you have any other instructions?

Human: Get the explanation behind the prediction for the label of the node. Enclose it in xml tags <explanation>,</explanation>
 
Assistant:
''',
'get_explanation_and_prediction_v2':'''

Human: {task-description}
-provide the reasoning logic or methodology to get the prediction for the node.  Post obtaining the prediction, you have to provide the justification and explanation.

-The name of the node for which you have to predict the label and provide explanation is enclosed in xml tags <node-name>{node-name}</node-name>

Assistant: Thanks for providing the task-description and relevant context. Do you have any other instructions?

Human: Provide the methodology to get the prediction for the label of the node. Enclose the methodology in xml tags <methodology>,</methodology>. This is just the space for your notes and not meant to be shown to the user.
Get the prediction of the label of the node, enclose the prediction in xml tags. <prediction>,</prediction>
Get the explanation behind the prediction for the label of the node. Enclose it in xml tags <explanation>,</explanation>

 
Assistant:
''',
'get_explanation_v2':'''

Human: {task-description}
-You are given the prediction of the label of the node, you have to provide the justification and explanation.

Prediction of the node for which you have to provide explanation is enclosed in xml tags <node-prediction>{node-prediction}</node-prediction>

Assistant: Thanks for providing the task-description and relevant context. Do you have any other instructions?

Human: Get the explanation behind the prediction for the label of the node. Enclose it in xml tags <explanation>,</explanation>
 
Assistant:
'''
}


GEN_HYPERPARAMETERS = {
'amazon.titan-tg1-large': {"maxTokenCount": 1600,
      "stopSequences": [],
      "temperature":0,
      "topP":1, 
     },
'anthropic.claude-instant-v1' : {"max_tokens_to_sample": 500,
      "stop_sequences": [],
      "temperature":0,
      "top_p":1, 
     },
 'anthropic.claude-v1' : {"max_tokens_to_sample": 500,
      "stop_sequences": [],
      "temperature":0,
      "top_p":1, 
     },
 'anthropic.claude-v2' : {"max_tokens_to_sample": 500,
      "stop_sequences": [],
      "temperature":0,
      "top_p":1, 
     },
  'anthropic.claude-v2:1' : {"max_tokens_to_sample": 500,
      "stop_sequences": [],
      "temperature":0,
      "top_p":1, 
     },
}

CONTEXT_LENGTH = {
    'amazon.titan-tg1-large': 8000,
    'anthropic.claude-instant-v1':100000,
    'anthropic.claude-v1': 100000,
    'anthropic.claude-v2': 100000,
    'anthropic.claude-v2:1':100000,
}


PROMPTS_DICT = {

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

Assistant: Thanks for providing the task-description. Do you have any other instructions?

Human: Provide the methodology to get the prediction for the label of the node. Enclose the methodology in xml tags <methodology>,</methodology>. This is just the space for your notes and not meant to be shown to the user.
Get the prediction of the label of the node, enclose the prediction in xml tags. <prediction>,</prediction>
Get the explanation behind the prediction for the label of the node. Enclose it in xml tags <explanation>,</explanation>

 
Assistant:
''',
'get_explanation_v2':'''

Human: {task-description}
-You are given the prediction of the label of the node, you have to provide the justification and explanation.

Prediction of the node for which you have to provide explanation is enclosed in xml tags <node-prediction>{node-prediction}</node-prediction>

Assistant: Thanks for providing the task-description. Do you have any other instructions?

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

# sample input summarize_meta_path_v2 #
'''
Human:You are a human whose goal is to generate the meaning of different meta-paths in heterogeneous graph network. You are provided with all the node types and edge-type and the underlying relation between them.  

Please find the node types enclosed inside the xml tags <node-type>,</node-type>
<node-type>A: Author
P:Paper
C:Conference</node-type>

Edge-type and their underlying relation is enclosed between xml tags <edge-relation>,</edge-relation>
<edge-relation>AP (A stands for xyz, P stands for abc) : Author xyz has published a paper titled abc
PA (P stands for abc, A stands for xyz):  Paper abc has been published by an author xyz
PC (P stands for abc,C stands for def) :  Paper abc has been published in conference titled as def
CP (C stands for def, P stands for ghi) : Conference DEF has paper titled ABC in its list of publications.</edge-relation>

Please find one meta-path summarization example below:
APA (A stands for xyz, P stands for abc, A’ def) : Author xyz has published a paper abc together with def

Can you generate the meaning of the following meta-paths enclosed inside xml tags <meta-path>,</meta-path>
<meta-path>APCP’A’ (A stands for xyz,P stands for abc, C stands for def, P’ stands for ghi,A’ stands for jkl)
APCP (A stands for xyz, P stands for abc, C stands for mno, P’ stands for pqr)</meta-path>

Write the meaning inside xml tags <meaning> </meaning>?

Assistant:
'''

# sample output summarize_meta_path_v2 #
'''
Certainly! I'll generate the meanings of the specified meta-paths in your heterogeneous graph network, adhering to the node and edge types you've provided.

1. Meta-Path: APCP’A’ (A stands for xyz, P stands for abc, C stands for def, P’ stands for ghi, A’ stands for jkl)

   Meaning:
   `<meaning>Author xyz has published a paper titled abc, which has been presented at conference def. This conference also has a paper titled ghi, authored by jkl.</meaning>`

2. Meta-Path: APCP (A stands for xyz, P stands for abc, C stands for mno, P’ stands for pqr)

   Meaning:
   `<meaning>Author xyz has published a paper titled abc, which has been presented at conference mno. This conference also has a paper titled pqr.</meaning>`
'''



import re
from sklearn.metrics import f1_score

def get_scoring(args,inputs_to_llm_dict,target_categories):
    """
    # y_true are the true class labels
    # y_pred are the predicted class labels by your model


    # For binary classification, labels=None by default
    # For multiclass classification, specify the labels
    """
    user_llm_dict = {}
    for key in inputs_to_llm_dict:
        if len(inputs_to_llm_dict[key]['context']):
            
            try:
            
                generated_response = inputs_to_llm_dict[key]['generated_response']

                match_explanation = re.search(r"<explanation>\n(.*?)\n</explanation>", generated_response, re.DOTALL)
                # need to make the lines 23 to 26 generic to capture as many unique labels as available.
                pattern_1 = r"<label1>(.*?)</label1>"
                pattern_2 = r"<label2>(.*?)</label2>" 
                pattern_3 = r"<label3>(.*?)</label3>"
                pattern_4 = r"<label4>(.*?)</label4>"
                pattern_5 = r"<prediction>(.*?)</prediction>"

                match_prediction_1 = re.search(pattern_1, generated_response, re.DOTALL)
                match_prediction_2 = re.search(pattern_2, generated_response, re.DOTALL)
                match_prediction_3 = re.search(pattern_3, generated_response, re.DOTALL)
                match_prediction_4 = re.search(pattern_4, generated_response, re.DOTALL)
                match_prediction_5 = re.search(pattern_5, generated_response, re.DOTALL)
                
                
                match_prediction = [match_prediction_1,match_prediction_2,match_prediction_3,match_prediction_4,match_prediction_5,match_prediction_7]
                relevant_matches=[relevant_match for relevant_match in match_prediction if relevant_match!= None]
                
                ground_truth = target_categories[key]
                if key not in user_llm_dict:
                    user_llm_dict[key] = {}
                    user_llm_dict[key]['node-name'] = key
                    user_llm_dict[key]['prediction'] = relevant_matches[0].group(1)
                    user_llm_dict[key]['explanation']  = match_explanation.group(1)
                    user_llm_dict[key]['ground_truth'] = target_categories[key]
                    if (ground_truth in relevant_matches[0].group(1)):
                        user_llm_dict[key]['is_prediction_correct'] = True
                    else:
                        user_llm_dict[key]['is_prediction_correct'] = False
            except Exception as e:
                print("An error occurred:", e)
                print (generated_response)

        
    count = 0
    y_true = []
    y_pred = []
    for key in user_llm_dict.keys():
        if 'is_prediction_correct' in user_llm_dict[key]:
            if (user_llm_dict[key]['is_prediction_correct']):
                count=count + 1
                
            y_pred.append(user_llm_dict[key]['prediction'])
            y_true.append(user_llm_dict[key]['ground_truth'])




    # Micro F1 Score
    f1_micro = f1_score(y_true, y_pred, average='micro')

    # Macro F1 Score
    f1_macro = f1_score(y_true, y_pred, average='weighted')

    print("Micro F1 Score:", f1_micro)
    print("Macro F1 Score:", f1_macro)

    return user_llm_dict,f1_micro,f1_macro



import torch.nn.functional as F
import torch
from collections import defaultdict


class meta_path_extraction():

    def __init__(self,args):
        self.keys = args.model_keys
        self.model = torch.load(args.gtn_model_path)
        self.node_acronyms = args.node_acronyms
        self.target_node = args.target_node_type
        self.edge_types = args.edge_types
     

    def get_weights_for_edges(self,model,keys):
        weights_for_metapath = []
        for key in keys:
            F.softmax(model[key],dim=1)
            weights_for_metapath.append(F.softmax(model[key],dim=1))
        
        return weights_for_metapath



    def get_polynomials(self,list_keys,weight_tensors):
        polynomial_list = []
        for tensor_value in weight_tensors:
            polynomial_list.append({((key,1),): value for key, value in zip(list_keys, tensor_value[0].tolist())})
        return polynomial_list


    def multiply_terms(self,term1,term2):
        result = defaultdict(int)
        
        for var, power in term1:
            result[var] = power
        
        for var, power in term2:
            result[var] += power
            
        return tuple(result.items())

    def multiply_two_polynomials(self,poly1,poly2):
        product = defaultdict(int)

        for term1, coef1 in poly1.items():
            for term2, coef2 in poly2.items():
                multiplied_term = self.multiply_terms(term1, term2)
                product[multiplied_term] += coef1 * coef2

        # Removing terms with 0 coefficient
        product = {term: coef for term, coef in product.items() if coef != 0}
        
        return product

    def multiply_polynomials(self,polynomials):
        result = polynomials[0]

        for poly in polynomials[1:]:
            result = self.multiply_two_polynomials(poly,result)

        return result


    def terms_with_degree_one(self,poly):
        return [term for term in poly if all(degree == 1 for _, degree in term if _!='I')]
    
    def get_weights_by_metapath(self):
        weights_for_metapath=self.get_weights_for_edges(self.model,self.keys)
        short_form_list = ['_' + self.node_acronyms.get(item.split('_')[0], '') + self.node_acronyms.get(item.split('_')[1], '') + '_' for item in self.edge_types]
        short_form_list.append('_I_')
        polynomials=self.get_polynomials(short_form_list,weights_for_metapath)
        result = self.multiply_polynomials(polynomials)
        filtered_keys = self.terms_with_degree_one(result)
        string_match_list = []
        for key in filtered_keys:
            string_match_sublist = []
            
            for index,term in enumerate(key):
                if term[0] != 'I':
                    string_match_sublist.append(term)
            string_match_list.append(tuple(string_match_sublist))

        req_strings = []            
        for index_2,sub_list in enumerate(string_match_list):       
            for index,term in enumerate(sub_list):
                        
                if ((index > 0 and sub_list[index][0][1] == sub_list[index-1][0][2])):
                        flag = 1            
                else:
                        flag = 0
                        if (index !=0):
                            break                    
            if (flag):            
                req_strings.append(sub_list)
                
        updated_dict = dict()
        for key in filtered_keys:
            string_match_sublist = []
            
            for index,term in enumerate(key):
                if term[0] != 'I':
                    string_match_sublist.append(term)
            if (tuple(string_match_sublist) in updated_dict):
                updated_dict[tuple(string_match_sublist)] += result[key]
            else:
                updated_dict[tuple(string_match_sublist)] = result[key]

        filtered_result = {k: updated_dict[k] for k in req_strings if k in updated_dict}
        filtered_result = dict(sorted(filtered_result.items(), key=lambda item: item[1], reverse=True))


        filtered_result_simplified  =dict()
        for key in filtered_result.keys():

            combined_string = ''.join([tup[0].replace('_', '')[0] for tup in key])
            filtered_result_simplified[combined_string] = filtered_result[key]

        filtered_result_simplified_only_target = dict()
        for key in filtered_result_simplified.keys():
            if key[0] ==self.node_acronyms[self.target_node] and key[-1] == self.node_acronyms[self.target_node]:
                filtered_result_simplified_only_target[key] = filtered_result_simplified[key]

        filtered_result_simplified_only_target = dict(sorted(filtered_result_simplified_only_target.items(), key=lambda item: item[1], reverse=True))

        return filtered_result_simplified_only_target,filtered_result_simplified

    

    





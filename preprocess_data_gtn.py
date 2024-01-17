from collections import Counter
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix
import json

# to be done: needs a generic pre-processing to be input for gtn.


index_list = []
feature_list = [book2feature,author2feature,publisher2feature,shelf2feature,format2feature,language_code_2feature]
for index,feature in enumerate(feature_list):
    if index==0:
        index_list.append(index)
    else:
        index_list.append(index_list[index-1]+feature_list[index-1].shape[0])


feature_sequence = ['book','author','publisher','shelf','format','lc']
feature_list = [book2list,author2list,publisher2list,shelf2list,format2list,language2list]
edges = ['book_shelf','shelf_book','book_lc','lc_book','book_publisher','publisher_book','book_author','author_book','book_format','format_book']
mapping_nodes={'book_shelf':book_to_shelf,'shelf_book':shelf_to_book,'book_lc':book_to_language_code,'lc_book':language_code_to_book,'book_publisher':book_to_publisher,'publisher_book':publisher_to_book,'book_author':book_to_author,'author_book':author_to_book,'book_format':book_to_format,'format_book':format_to_book}


edge_csr = []
for edge in edges:
        edge_matrix = csr_matrix(np.zeros((n, n)))  
        source_node =edge.split("_")[0]
        destination_node = edge.split("_")[1]
        source_node_type_index=feature_sequence.index(source_node)
        destination_node_type_index=feature_sequence.index(destination_node)
        source_node_index = index_list[source_node_type_index]
        destination_node_index = index_list[destination_node_type_index]
        source_node_list = feature_list[source_node_type_index]
        destination_node_list = feature_list[destination_node_type_index]
        mapping_dict = mapping_nodes[edge]
        for key in mapping_dict.keys():
            x = source_node_list.index(key) + source_node_index
            if type(mapping_dict[key]) == list:
                for value in mapping_dict[key]:
                    y = destination_node_list.index(value) + destination_node_index
                    edge_matrix[x,y]= 1
            else:   
                    if (mapping_dict[key]!=''):
                        y = destination_node_list.index(mapping_dict[key]) + destination_node_index
                        edge_matrix[x,y]= 1
        edge_csr.append(edge_matrix)


labels = []
for index,book in enumerate(book2list):
    labels.append([index,book_dict[book]['genres']])
    
label_genres=[label[1] for label in labels]
dict_from_set = {element: index for index, element in enumerate(set(label_genres))}

labels_v2 = []
for index,book in enumerate(book2list):
    labels_v2.append([index,dict_from_set[book_dict[book]['genres']]])
    
labels_train = labels_v2[:400]
labels_val = labels_v2[400:600]
labels_test = labels_v2[600:]
labels_final = [labels_train,labels_val,labels_test]


with open('./goodsreads_preprocessed_data/edges.pkl', 'wb') as file:
    pickle.dump(edge_csr, file)
    
with open('./goodsreads_preprocessed_data/node_features.pkl', 'wb') as file:
    pickle.dump(vstacked_array, file)


    



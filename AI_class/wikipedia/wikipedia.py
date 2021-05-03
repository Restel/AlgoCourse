__author__ = 'Lina Brilliantova'

import csv
import math
from Node import Node
import sys

def load_data(file):  # todo fix to vanilla python
    data = []
    file = open(file, mode="r", encoding='utf-8')
    wiki_reader = csv.reader(file)
    for row in wiki_reader:
        data.append(row)
    return data

def prepare_data(data, type = 'train'):
    """Prepare data for training and prediction : expands the features, delete the text, returns colnames, label index and text"""
    features = feature_expansion(data)
    text = select_column(data, 0)
    for x in data:
        del x[0]
    if type == 'train':
        colnames = ['label'] + features #  FIX this !!!
        label_index = 0
    else:
        colnames = features
        label_index = None
    #colnames = features #  FIX this !!!
    # label_index = colnames.index('label')

    return colnames, label_index, text


def entropy(p):  #todo TEST
    res = -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)
    return res


def estimate_entropy(data, label_index): #todo TEST
    if len(data) == 0:
        return 0
    p = len([x for x in data if x[label_index] in ['it', 'Y']])/len(data)
    if p == 1 or p == 0:
        return 10 ** -100
    else:
        return entropy(p)


def unique_answers(data, attr_ind):
    attr_data = [x[attr_ind] for x in data]
    a_set = set(attr_data)
    # unique_list = []
    # attr_data = [x[attr_ind] for x in data] # get a vector of data's attribute (located at attr_ind column in data)
    # for x in attr_data:
    #     if x not in unique_list:
    #         unique_list.append(x)
    return a_set

def select_column(data, label_ind):
    return [y[label_ind] for y in data]

def filter(data, attr_ind, answer):
    new_data = []
    for elem in data:
        if elem[attr_ind] == answer:
            new_data.append(elem)
    return new_data

def majority_output(data):
    count = {}
    for key in data:
        if key not in count.keys():
            count[key] = 1
        else:
            count[key] += 1
    max_key = None
    max_counter = 0
    for key in count:
        if count[key] > max_counter:
            max_counter = count[key]
            max_key = key
    return max_key


def weighted_sum(data, answers, attr_ind, label_ind):
    sum = 0
    for ans in answers:
        subset = [x for x in data if x[attr_ind] == ans]
        sum += len(subset)/len(data) * estimate_entropy(subset, label_ind)
    return sum


def get_answer(obs, question, colnames):
    ind = colnames.index(question)
    return obs[ind]


def predict_all(obs_list, dtree, colnames):
    res_list = []
    for obs in obs_list:
        res = predict(obs, dtree, colnames)
        #print(res)
        res_list += [res]
    return res_list


def predict(obs, dtree, colnames):
    """Predict a language based on textual observation (obs). """
    curr_node = dtree # initialize to the rootnode
    question = curr_node.attr
    while question not in ['it', 'nl']:
        answer = get_answer(obs, question, colnames)
        curr_node = curr_node._find_by_answer(answer)
        question = curr_node.attr
    return question

def best_attribute(data, colnames, label_index):
    #label_index = colnames.index('label')
    best_gain = 0
    best_attr = None
    best_ind = None
    best_answers = []
    attr_list = [x for x in colnames if x != 'label']
    for attr in attr_list:
        attr_ind = colnames.index(attr)
        answers = unique_answers(data, attr_ind)
        sum = weighted_sum(data, answers, attr_ind, label_index)
        gain = estimate_entropy(data, label_index) - sum
        if gain > best_gain:
            best_attr = attr
            best_gain = gain
            best_answers = answers
            best_ind = attr_ind
    #print("Best attribute: ", best_attr, "Best infogain: ", best_gain, " Answers: ", best_answers, " Attribute index ", best_ind)
    return best_attr, best_answers, best_ind

def dtree_build(data, list_attr, label_index, eps = 10 ** -4):
    if len(data) == 0: # no examples
        return None
    if estimate_entropy(data, label_index) < eps:
        #print("test")
        column = select_column(data, label_index)
        test = Node(majority_output(column))
        return test
    if len(list_attr) == 0: # asked all questions
        #print("test")
        test = Node(majority_output(select_column(data, label_index)))
        return Node(majority_output(select_column(data, label_index)))

    attr, answers, attr_ind  = best_attribute(data, list_attr, label_index)

    if attr is None:
        return Node(majority_output(select_column(data, label_index)))

    rnode = Node(attr)
    for answer in answers:
        subset = filter(data, attr_ind, answer)
        subtree = dtree_build(subset, list_attr, label_index, eps)
        if subtree is None:
            subtree = Node(majority_output(select_column(data, label_index)))
        rnode.add_child(subtree, answer)
    return rnode


def count_end_vowels(list_words):
    count = 0
    for word in list_words:
        if word[-1] in ['i', 'a', 'e', 'è', 'o', 'é', 'ŭ', 'ò', 'ù']:
            count += 1
    return count

def expand(data, type):
    for obs in data:
        if type == "vowel_ending":
            splitted = obs[0].split() #split to list of words
            feature = count_end_vowels(splitted) >= 10
        else:
            feature = obs[0].count(type) > 0
        obs.append(feature)

def feature_expansion(data):
    """Returns the original data with additional feature columns for language identification
    :param data: list of lists in format [[Text_i, label_i]]
    :return data_exp: expanded data in format [[Text_i, label_i, feature1_i ... featurek_i]
    """
    #feature_list = ['vowel_ending', 'ooi', 'aa', 'ee', 'aai', 'auw', 'eu', 'euw', 'uu', 'è', 'é', 'ei', '\'', 'ŭ', 'ò', 'ù', 'vv']  # future attribute names
    feature_list = ['vowel_ending',  'aa', 'ee', 'uu', 'è', 'ei', '\'', 'ò', 'vv'] # FIX: remove uu, vv?
    for f in feature_list:
        expand(data, f)
    return feature_list


def accuracy(data, label_index, results):
    correct = 0
    if len(data) != len(results):
        raise IndexError("The number of observations in data and labels do not match!")
    labels = select_column(data, label_index)
    for i in range(len(data)):
        if labels[i] == results[i]:
            correct += 1
    return correct/len(data)

def testing():
    print("==========Testing best attribute and information gain on the example of coffee data")
    data_file = "coffee.csv"
    data = []
    file = open(data_file, mode="r")
    wiki_reader = csv.reader(file, delimiter = ';')
    for row in wiki_reader:
        data.append(row)
    colnames = data[0]
    colnames[0] = 'Student'
    colnames[len(colnames)-1] = 'label'
    label_index = colnames.index('label')
    data = data[1:len(data)] #remove headers
    b_attr, answers, attr_ind = best_attribute(data, colnames, label_index)

    print("#######Testing filter #######")
    print("print Student (first column) == Yes")
    print(filter(data, 0, 'Y'))
    print("print Drinks Coffee (last column) == No")
    print(filter(data, 4, 'N'))
    #print("THe results of subset:", print(select_column(data,0)), "Should be ", print([y[0] for y in data]))
    #print(majority_output(['Y', 'N', 'S', 'Y', 'S', 'N', 'S']))
    #print(majority_output(select_column(data, 0)))

    #label_index = colnames.index('label')
    list_attr = [x for i, x in enumerate(colnames) if i != label_index]  # create a list of attribute names
    tree = dtree_build(data, list_attr, label_index)
    print("#############Testing Decision tree build#############")
    print("#### FIRST LEVEL")
    print("# VEGETARIAN", tree)
    print("#### RIGHT SUBTREE")
    print("STUDENT", tree.children[1])
    print("OWNS IPHONE", tree.children[1].children[0])

    print("#### LEFT SUBTREE")
    print("AMERICAN", tree.children[0])
    print('STUDENT LEFT', tree.children[0].children[0])
    print('STUDENT RIGHT', tree.children[0].children[1])

    print("########  TESTING ON WIKIPEDIA TRAIN DATA ###########")
    data = load_data("wikipedia_data_train.csv")
    colnames, label_index, text = prepare_data(data)
    tree = dtree_build(data, colnames, label_index, 0.4)
    print(tree.children[0].attr)
    # b_attr, answers, attr_ind = best_attribute(data, colnames, label_index)
    # list_attr = [x for i, x in enumerate(colnames) if i != label_index]  # create a list of attribute names

    print("Test dataset")
    test_data = load_data("wikipedia_data_test.csv")
    colnames, label_index, text = prepare_data(test_data)
    results = predict_all(test_data, tree, colnames)
    acc = accuracy(test_data, label_index, results)
    print(acc)

    print("#### TEST CONSISTENCY WITH SPECS")
    r_s_data = load_data("data_right_spec.txt")
    colnames, _, _ = prepare_data(r_s_data, 'predict')
    predicted_labels = predict_all(r_s_data, tree, colnames)
    print(predicted_labels)


def infer_tree():
    train_data = load_data("wikipedia_data_train.csv")
    colnames, label_index, _ = prepare_data(train_data)
    valid_data = load_data("wikipedia_data_valid.csv")
    _, _, _ = prepare_data(valid_data)
    best_eps = None
    best_acc = 0
    for eps in range(5, 95, 5):
        tree = dtree_build(train_data, colnames, label_index, eps/100)
        predicted_labels = predict_all(valid_data, tree, colnames)
        acc = accuracy(valid_data, label_index, predicted_labels)
        if acc > best_acc:
            best_acc = acc
            best_eps = eps
    print("Best entropy threshold on the validation set is", best_eps/100, " with accuracy ", best_acc)
    print("But the second best entropy threshold is chosen (see report)", 0.3, " with accuracy ", '0.958')

    tree = dtree_build(train_data, colnames, label_index, 0.4)
    test_data = load_data("wikipedia_data_test.csv")
    _, _, _ = prepare_data(test_data)
    predicted_labels = predict_all(test_data, tree, colnames)
    acc = accuracy(test_data, label_index, predicted_labels)
    print("Accuracy of the best tree with eps = 0.3 on test data: ", acc)

def make_best_tree():
    #  feature_list = ['vowel_ending',  'aa', 'ee', 'uu', 'è', 'ei', '\'', 'ò', 'vv']
    node1 = Node('uu', False, children = [Node('nl', answer=False), Node('nl', answer=True)])
    node2 = Node('ò', True, children = [Node('it', answer=False), Node('it', answer=True)])
    node3 = Node('\'', False, children=[node1, node2])
    node4 = Node('\'', True, children=[Node('nl', answer=False), Node('nl', answer=True)])
    node5 = Node('ei', False, children=[node3, node4])
    node6 = Node('è', False, children=[node5, Node('it', answer = True)])
    node7 = Node('ee', False, children=[node6, Node('nl', True)])
    node8 = Node('aa', False, children=[node7, Node('nl', True)])
    root = Node('vowel_ending', children=[node8, Node('it', True)])
    return root

if __name__ == '__main__':
    mode = sys.argv[1]

    if mode == "predict":
        type = sys.argv[2]
        filename = sys.argv[3]

    if mode == 'train':
        infer_tree()

    elif mode == 'predict':
        data = load_data(filename)
        tree = make_best_tree()
        colnames, _, _ = prepare_data(data, 'predict')
        #colnames, label_index, text = prepare_data(data, 'predict') #fiX!
        predicted_labels = predict_all(data, tree, colnames)
        #acc = accuracy(data, label_index, predicted_labels)
        for label in predicted_labels:
            if label == 'it':
                print('Italian')
            elif label =='nl':
                print('Dutch')
    else:
        raise ValueError("Unsupported argument. Correct usage: python3 wiki.py [train/predict] [model-type] [datafile] (last two arguments only for predict mode)")

# def best_attribute(, A)
# colnames = ['text', 'label']
# data = load_data()
# filtered = [x for x in data if x[1] == "it"]
# estimate_entropy(data, 1)
# a = 'è'

####TRAINING####


# with open('t.csv', 'r') as f:
#     results = []
#     for line in f:
#             words = line.split(',')
#             results.append((words[0], words[1:]))
#     print results

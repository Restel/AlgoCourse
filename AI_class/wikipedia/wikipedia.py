__author__ = 'Lina Brilliantova'

import csv
import math
from Node import Node

def load_data():  # todo fix to vanilla python
    data = []
    file = open("wikipedia_data.csv", mode="r", encoding='utf-8')
    wiki_reader = csv.reader(file)
    for row in wiki_reader:
        data.append(row)
    return data


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
    print("Best attribute: ", best_attr, "Best infogain: ", best_gain, " Answers: ", best_answers, " Attribute index ", best_ind)
    return best_attr, best_answers, best_ind

def dtree_build(data, list_attr, label_index, eps = 10 ** -4):
    if len(data) == 0: # no examples
        return None
    if estimate_entropy(data, label_index) < eps:
        print("test")
        column = select_column(data, label_index)
        test = Node(majority_output(column))
        return test
    if len(list_attr) == 0: # asked all questions
        print("test")
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

    # Do not forget to remove the label colums in colnames when passing to best_attribute()!!!
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

    # print('STUDENT RIGHT', tree.children[0].children[1])
    # print('STUDENT RIGHT', tree.children[0].children[1].children[0])

    # print("STUDENT", tree.children[1])
    # print("#### THIRD LEVEL (LEFT TO RIGHT)")
    # print("STUDENT", tree.children[0].children[0])
    # print("STUDENT", tree.children[0].children[1])
    # print("PHONE", tree.children[1].children[0])
    # print("YES", tree.children[1].children[1])
if __name__ == '__main__':
    testing()

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

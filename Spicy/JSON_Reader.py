import json

# reads the json file and returns the whole data
def read_json(file_name):

    with open(file_name) as json_data:
        TEST_DATA = json.load(json_data)
        # print(TEST_DATA)

        return TEST_DATA


# parse the JSON data and returns a list of sentences
def get_sentences(data_json, out_filename):

    sentences_str = []
    sentences_list = []
    heads = []
    dependencies = []

    for data in data_json:
        tokens = data["paragraphs"][0]["sentences"][0]["tokens"]
        # print(type(tokens))
        sent = []
        head = []
        dep= []
        individual_line = ""
        for token in tokens:
            individual_line += (token['orth']+" ")
            sent.append(token['orth'])
            head.append(token['head'])
            dep.append(token['dep'])

        # taking the actual head string from the relative distance
        head_str = []
        for i, head_num in enumerate(head):
            # print(i, " ", head_num, " "+sent[i+head_num])
            head_str.append((sent[i+head_num]))

        # appending the values into lists
        sentences_str.append(individual_line)
        sentences_list.append(sent)
        heads.append(head_str)
        dependencies.append(dep)

        # print(sent)
        # print(head)
        # print(head_str)
        # print(dep)
        # print("\n")


    # converting the gold label from json to rel(head,dep) format
    create_test_doc(sentences_str, sentences_list, heads, dependencies, out_filename)

    return sentences_str, sentences_list, heads, dependencies

# Writing the output to a file
def create_test_doc(sentences_str, sentences_list, heads, dependencies, out_filename):

    file = open(out_filename, 'w', encoding='utf-8')
    id = 0

    for sentence_str, sent, head, dep in zip(sentences_str, sentences_list, heads, dependencies):

        file.write("#id_"+str(id)+": "+sentence_str+"\n\n")
        for rel, head_text, tok_text  in zip(dep, head, sent):
            file.write(rel+"("+tok_text+" ,"+head_text+")\n")

        file.write("\n")
        id+=1



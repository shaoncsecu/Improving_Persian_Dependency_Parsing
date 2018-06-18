#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
import json
import codecs
import JSON_Reader

# training data
# TRAIN_DATA = [
#     ("They trade mortgage-backed securities.", {
#         'heads': [1, 1, 4, 4, 5, 1, 1],
#         'deps': ['nsubj', 'ROOT', 'compound', 'punct', 'nmod', 'dobj', 'punct']
#     }),
#     ("I like London and Berlin.", {
#         'heads': [1, 1, 1, 2, 2, 1],
#         'deps': ['nsubj', 'ROOT', 'dobj', 'cc', 'conj', 'punct']
#     })
# ]



def run_spacy(model, sentences_str):

    """Load the model, set up the pipeline and train the parser."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # add the parser to the pipeline if it doesn't exist
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'parser' not in nlp.pipe_names:
        parser = nlp.create_pipe('parser')
        nlp.add_pipe(parser, first=True)
    # otherwise, get it, so we can add labels to it
    else:
        parser = nlp.get_pipe('parser')

    # # add labels to the parser
    # with open('single.json') as json_data:
    #     TRAIN_DATA = json.load(json_data)
    #     # print(TRAIN_DATA)
    #
    #     for _, annotations in TRAIN_DATA:
    #         print(annotations)
    #         for dep in annotations.get('dep', []):
    #             parser.add_label(dep)
    #
    #     # get names of other pipes to disable them during training
    #     other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']
    #     with nlp.disable_pipes(*other_pipes):  # only train parser
    #         optimizer = nlp.begin_training()
    #         for itn in range(n_iter):
    #             random.shuffle(TRAIN_DATA)
    #             losses = {}
    #             for text, annotations in TRAIN_DATA:
    #                 nlp.update([text], [annotations], sgd=optimizer, losses=losses)
    #             print(losses)


    file = open('spacy_out.txt', 'w', encoding='utf-8')
    id = 0

    sentences_list_spacy = []
    heads_spacy = []
    dependencies_spacy = []

    for sentence in sentences_str:
        # print(sentence)
        # test the trained model
        # test_text = "نظامی می‌گوید که در سال ۵۱۰ تربت او را زیارت کرده"
        # doc = nlp(test_text)
        doc = nlp(sentence)

        # print('Dependencies', [(t.text, t.dep_, t.head.text) for t in doc])

        # save model to output directory
        # if output_dir is not None:
        #     output_dir = Path(output_dir)
        #     if not output_dir.exists():
        #         output_dir.mkdir()
        #     nlp.to_disk(output_dir)
        #     print("Saved model to", output_dir)
        #
        #     # test the saved model
        #     print("Loading from", output_dir)
        #     nlp2 = spacy.load(output_dir)
        #     # doc = nlp2(test_text)

        sent = []
        head = []
        dep= []

        # Writing the output to a file and saving them in variables
        file.write("#id_"+str(id)+": "+sentence+"\n\n")
        for t in doc:
            sent.append(t.text)
            head.append(t.head.text)
            dep.append(t.dep_)

            file.write(t.dep_+"("+t.text+" ,"+t.head.text+")\n")

        sentences_list_spacy.append(sent)
        heads_spacy.append(head)
        dependencies_spacy.append(dep)

        file.write("\n")
        id+=1

    file.close()

    return sentences_str, sentences_list_spacy, heads_spacy, dependencies_spacy


# expected result:
# #id_0: نظامی می‌گوید که در سال ۵۱۰ تربت او را زیارت کرده .
#
# nsubj(نظامی ,می‌گوید)
# ROOT(می‌گوید ,می‌گوید)
# mark(که ,کرده)
# case(در ,سال)
# obl(سال ,کرده)
# nummod(۵۱۰ ,سال)
# amod(تربت ,سال)
# obj(او ,کرده)
# case(را ,او)
# compound:lvc(زیارت ,کرده)
# ccomp(کرده ,می‌گوید)
# punct(. ,می‌گوید)

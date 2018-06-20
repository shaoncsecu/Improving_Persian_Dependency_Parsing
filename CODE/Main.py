'''
Run the program like this:

python Main.py -m best_model -t fa_seraji-ud-test.json -ud ud_parsed.json

'''

import plac
import random
from pathlib import Path

import Test_Spacy
import JSON_Reader
import  Evaluation_Combine

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    input_file=("Test File Name JSON format.", "option", "t", str),
    ud_parsed=("UDpipe parsed File Name JSON format.", "option", "ud", str))
def main(model, input_file, ud_parsed):

    # Reading the Test JSON file and converting it as rel(head, dep) format
    TEST_DATA = JSON_Reader.read_json(input_file)
    sentences_str_gold, sentences_gold, heads_gold, dependencies_gold = JSON_Reader.get_sentences(TEST_DATA, 'gold_out.txt')

    # Running Spacy with a model and the Test JSON file
    sentences_str_spacy, sentences_list_spacy, heads_spacy, dependencies_spacy = Test_Spacy.run_spacy(model, sentences_str_gold)

    # for sent, head, dep in zip(sentences_list_spacy, heads_spacy, dependencies_spacy):
    #     print(sent)
    #     print(head)
    #     print(dep)
    #     print("\n")

    # Reading the UD parsed JSON file and converting it as rel(head, dep) format
    ud_out = JSON_Reader.read_json(ud_parsed)
    sentences_str_ud, sentences_ud, heads_ud, dependencies_ud = JSON_Reader.get_sentences(ud_out, 'ud_out.txt')

    # To generate A combination of both the parsers and to evaluate the combined results (macro & micro LAS)
    Evaluation_Combine.run_evaluation(sentences_str_gold, sentences_gold,
                                      heads_gold, dependencies_gold,
                                      heads_spacy, dependencies_spacy,
                                      heads_ud, dependencies_ud)

if __name__ == '__main__':
    plac.call(main)

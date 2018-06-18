import JSON_Reader

def combine_macro_LAS(heads_gold, dependencies_gold,
                   heads_spacy, dependencies_spacy,
                   heads_ud, dependencies_ud):

    heads = []
    dependencies = []

    total_LAS = 0

    for dep_line_gold, dep_line_spacy, dep_line_ud, head_line_spacy, head_line_ud in zip(
            dependencies_gold, dependencies_spacy, dependencies_ud, heads_spacy, heads_ud):

        correct_spacy = 0
        correct_ud = 0

        for dep_g, dep_s, dep_u in zip(dep_line_gold, dep_line_spacy, dep_line_ud):
            if dep_g == dep_s:
                correct_spacy += 1

            if dep_g == dep_u:
                correct_ud += 1

        LAS_sentence = 0
        if(correct_spacy > correct_ud):
            LAS_sentence = correct_spacy/len(dep_line_gold)

            heads.append(head_line_spacy)
            dependencies.append(dep_line_spacy)

        else:
            LAS_sentence = correct_ud/len(dep_line_gold)

            heads.append(head_line_ud)
            dependencies.append(dep_line_ud)

        total_LAS += LAS_sentence

        # print("#Sentence - "+str(i))
        # i+=1
        # print(dep_line_gold)
        # print("Correct Spacy = "+str(correct_spacy))
        # print("Correct UD = "+str(correct_ud))
        # print("Length = "+str(len(dep_line_gold)))
        # print("LAS = "+str(LAS_sentence))
        # print("\n")

    print("\n\n")
    print("Processed Sentences: ",len(heads_gold))

    macro_LAS = total_LAS/len(heads_gold)
    print("Combined Macro LAS = ",round(macro_LAS,4))

    return heads, dependencies


def run_evaluation(sentences_str_gold, sentences_gold,
                   heads_gold, dependencies_gold,
                   heads_spacy, dependencies_spacy,
                   heads_ud, dependencies_ud):

    heads, dependencies = combine_macro_LAS(heads_gold, dependencies_gold,
                                            heads_spacy, dependencies_spacy,
                                            heads_ud, dependencies_ud)

    # Creating the modified results in rel(head,dep) format - best sentences from each parser
    JSON_Reader.create_test_doc(sentences_str_gold, sentences_gold, heads, dependencies, 'best_out_macro.txt')

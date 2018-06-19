import JSON_Reader

def combine_micro_LAS(heads_gold, dependencies_gold,
                   heads_spacy, dependencies_spacy,
                   heads_ud, dependencies_ud):

    heads = []
    dependencies = []

    correct = 0
    incorrect =0
    total_tokens = 0

    for dep_line_gold, dep_line_spacy, dep_line_ud, head_line_gold, head_line_spacy, head_line_ud in zip(
            dependencies_gold, dependencies_spacy, dependencies_ud, heads_gold, heads_spacy, heads_ud):

        head = []
        dep_rel = []

        # print("\n#id:,\n")

        # here dep means dependency relations
        for dep_g, dep_s, dep_u, head_g, head_s, head_u in zip(
                dep_line_gold, dep_line_spacy, dep_line_ud, head_line_gold, head_line_spacy, head_line_ud):

            # if head and rel_label of spacy is correct select that
            if dep_g == dep_s and head_g == head_s:
                correct += 1
                dep_rel.append(dep_s)
                head.append(head_s)
                # print("Spacy: Rel = ",dep_s,"Head = "+head_s)

            # else if head and rel_lable of udpipe is correct select that
            elif dep_g == dep_u and head_g == head_u:
                correct += 1
                dep_rel.append(dep_u)
                head.append(head_u)
                # print("UDpipe: Rel = ",dep_u,"Head = "+head_u)

            # if both of them are incorrect
            else:
                incorrect += 1
                # take any one of those *we can use statistics here for main implementation of search*
                dep_rel.append(dep_s)
                head.append(head_s)
                # print("Incorrect Taking Spacy: Rel = ",dep_s,"Head = "+head_s)

            total_tokens += 1

        heads.append(head)
        dependencies.append(dep_rel)

    print("\n\n")
    print("Processed Tokens: ",total_tokens)

    print("Correct Annotation: ",correct)

    print("Incorrect Annotation: ",incorrect)

    micro_LAS = correct/total_tokens
    print("Combined Micro LAS = ",round(micro_LAS,4))

    return heads, dependencies



def combine_macro_LAS(heads_gold, dependencies_gold,
                   heads_spacy, dependencies_spacy,
                   heads_ud, dependencies_ud):

    heads = []
    dependencies = []

    total_LAS = 0

    for dep_line_gold, dep_line_spacy, dep_line_ud, head_line_gold, head_line_spacy, head_line_ud in zip(
            dependencies_gold, dependencies_spacy, dependencies_ud, heads_gold, heads_spacy, heads_ud):

        correct_spacy = 0
        correct_ud = 0

        # here dep means dependency relations
        for dep_g, dep_s, dep_u, head_g, head_s, head_u in zip(
                dep_line_gold, dep_line_spacy, dep_line_ud, head_line_gold, head_line_spacy, head_line_ud):

            if dep_g == dep_s and head_g == head_s:
                correct_spacy += 1

            if dep_g == dep_u and head_g == head_u:
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

    print("########## LAS Score ###########")
    # Macro LAS calculations
    heads_macro, dep_rel_macro = combine_macro_LAS(heads_gold, dependencies_gold,
                                            heads_spacy, dependencies_spacy,
                                            heads_ud, dependencies_ud)

    # Creating the modified results in rel(head,dep) format - best sentences from each parser
    JSON_Reader.create_test_doc(sentences_str_gold, sentences_gold, heads_macro, dep_rel_macro, 'best_out_macro.txt')


    # Macro LAS calculations
    heads_micro, dep_rel_micro = combine_micro_LAS(heads_gold, dependencies_gold,
                                            heads_spacy, dependencies_spacy,
                                            heads_ud, dependencies_ud)

    # Creating the modified results in rel(head,dep) format - best sentences from each parser
    JSON_Reader.create_test_doc(sentences_str_gold, sentences_gold, heads_micro, dep_rel_micro, 'best_out_micro.txt')

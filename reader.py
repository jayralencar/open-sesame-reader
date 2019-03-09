from io import open
from conllu import parse_incr
import pprint
import json
from optparse import OptionParser

optpr = OptionParser()
optpr.add_option("--input", type="str", metavar="FILE")
optpr.add_option("--output", type="str", metavar="FILE")

(options, args) = optpr.parse_args()

sentences = []

data_file = open(options.input, "r", encoding="utf-8")
sentence_list = data_file.read().split("\n\n")

current_sentence = {
    "sentence_id" : 0,
    'frames':[]
}
sentences = []
for sent in sentence_list:
    _frame = {}
    for line in sent.split("\n"):
        if len(line.split("\t")) == 15:
            line_id, form, misc1, lemma,misc2,pos,sentence_id, misc3, misc4, misc5, misc7, misc8,lu, frame, argument = line.split('\t')
            if current_sentence['sentence_id'] != int(sentence_id):
                sentences.append(current_sentence)
                current_sentence = {
                    'sentence_id' : int(sentence_id),
                    'frames':[]
                }
            if frame != '_':
                # print(frame)
                _frame['target'] = {
                    "frame" : frame,
                    "word" : form,
                    "word_id" : int(line_id),
                    "pos": pos,
                    "lemma": lemma
                }
            if argument != "_" and argument != "O":
                if 'frame_elements' not in _frame:
                    _frame['frame_elements'] = []
                _frame['frame_elements'].append({
                    "frame_element" : argument,
                    "word":form,
                    'word_id':int(line_id),
                    'pos': pos,
                    "lemma": lemma
                })
                

    if _frame != {}:
        current_sentence['frames'].append(_frame)   
            
sentences.append(current_sentence)
# pprint.pprint(sentences)
# with open('output.json', 'w') as outfile:
    # json.dump(sentences, outfile)
with open(options.output, 'w', encoding='utf-8') as f:
    f.write(json.dumps(sentences, ensure_ascii=False))
# print(json.dumps(sentences))
print("DONE")
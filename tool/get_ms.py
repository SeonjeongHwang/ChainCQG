import sys

import json
from typing import List, Union, Iterable
from itertools import zip_longest
import sacrebleu
from moverscore_v2 import word_mover_score
from collections import defaultdict
import numpy as np

def sentence_score(hypothesis: str, references: List[str], trace=0):
    
    idf_dict_hyp = defaultdict(lambda: 1.)
    idf_dict_ref = defaultdict(lambda: 1.)
    
    hypothesis = [hypothesis] * len(references)
    
    sentence_score = 0 

    scores = word_mover_score(references, hypothesis, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=False)
    
    sentence_score = np.mean(scores)
    
    if trace > 0:
        print(hypothesis, references, sentence_score)
            
    return sentence_score

def corpus_score(sys_stream: List[str],
                     ref_streams:Union[str, List[Iterable[str]]], trace=0):

    if isinstance(sys_stream, str):
        sys_stream = [sys_stream]

    if isinstance(ref_streams, str):
        ref_streams = [[ref_streams]]

    fhs = [sys_stream] + ref_streams

    corpus_score = 0
    for lines in zip_longest(*fhs):
        if None in lines:
            raise EOFError("Source and reference streams have different lengths!")
            
        hypo, *refs = lines
        corpus_score += sentence_score(hypo, refs, trace=0)
        
    corpus_score /= len(sys_stream)

    return corpus_score


refs_list = []
sys_list = []

tag = str(sys.argv[1])
test = str(sys.argv[2])

with open(tag+"/"+test+"/new_result.json", "r") as reader:
    items = json.load(reader)
    for item in items:
        refs_list.append(item["label"])
        sys_list.append(item["result"])

bleu = sacrebleu.corpus_bleu(sys_list, [refs_list])
moverscore = corpus_score(sys_list, [refs_list])

print(bleu)
print(moverscore)

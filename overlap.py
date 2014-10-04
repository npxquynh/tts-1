#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import time
import doc_handling

import pdb

QUERY_FILE  = './qrys.txt'
DOC_FILE    = './docs.txt'
OVERLAP_FILE = './overlap.top'

class Overlap():
    def __init__(self, query_file, doc_file):
        self.queries    = doc_handling.parse_doc(query_file)
        self.docs       = doc_handling.parse_doc(doc_file)
        self.overlap_score = []
    
    def compute_score(self):
        for (query_id, query) in self.queries.iteritems():
            for (doc_id, doc) in self.docs.iteritems():
                score = self.compute_overlap_score(query, doc)
                self.overlap_score.append((query_id, doc_id, score))

    def compute_overlap_score(self, query, doc):
        return len(set(query).intersection(set(doc)))

    def print_overlap_score(self, output_file):
        doc_handling.write_output(self.overlap_score, output_file)

if __name__ == '__main__':
    time_1 = time.time()

    task1 = Overlap(QUERY_FILE, DOC_FILE)
    task1.compute_score()
    task1.print_overlap_score(OVERLAP_FILE)

    print "running time: %f\n" % (time.time() - time_1)
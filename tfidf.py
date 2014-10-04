#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
from __future__ import division

import time
import os.path
import pdb
from math import log

import doc_handling

QUERY_FILE  = './qrys.txt'
DOC_FILE    = './docs.txt'
TFIDF_FILE  = './tfidf.top'

class Tfidf():
    def __init__(self, query_file, doc_file, k_constant, preprocessing_option = 1):
        self.k_constant             = k_constant
        self.preprocessing_option   = preprocessing_option
        self.docs                   = doc_handling.parse_doc(doc_file, preprocessing_option)
        self.queries                = doc_handling.parse_doc(query_file, preprocessing_option)

    def build_dict(self):
        dictionary = set()
        for doc in self.docs.values():
            dictionary = dictionary.union(set(doc))

        self.dictionary = dictionary

    def compute_idf(self):
        print "Running: compute_idf()Comput IDF"
        t = time.time()

        idf = dict()
        C = self.no_of_documents
        for token in self.dictionary:
            try:
                idf[token] = log(C / self.compute_df(token))
            except:
                # Given zero for unrecognized token
                idf[token] = 0
                print "ERROR: tfidf.py - compute_idf()"

        self.idf = idf
        print "************* %f seconds" % (time.time() - t)

    def read_idf(self, input_file):
        print "Read IDF"
        error_count = 0
        with open(input_file) as f:
            for line in f:
                try:
                    items = line.strip().split('\t')
                    token = items[0]
                    value = float(items[1])
                    self.idf[token] = value
                except IndexError:
                    error_count += 1
        print "error count idf.temp %d" % error_count

    def write_idf(self, output_file):
        with open(output_file, 'w') as output:
            for (token, value) in self.idf.iteritems():
                output.write('%s\t%f\n' % (token, value))

    def handle_idf(self):
        # IMPORTANT NOTE: Enable those lines in the real running

        # Check if the temporary file for the preprocessing option existed?
        file_path = 'idf_%d.temp' % self.preprocessing_option
        if os.path.isfile(file_path):
            self.read_idf(file_path)
        else:
            self.compute_idf()
            self.write_idf(file_path)

    def compute_df(self, token):
        """
        Return the number of documents a token appears in the collection
        """
        if token not in self.df:
            count = 0
            for doc in self.docs.values():
                if token in doc:
                    count += 1
            self.df[token] = count
        else:
            count = self.df[token]

        return count

    def compute_tf(self, tokens):
        """
        The number of times a token appears in a document
        tokens: array
        """
        return dict((token, tokens.count(token)) for token in set(tokens))
    
    def compute_Dw(self):
        print "Running: compute_Dw()"
        t = time.time()

        for (doc_id, doc) in self.docs.iteritems():
            tf_D = self.compute_tf(doc)

            # Normalization: k|D| / avg |D|
            # It's the same for one document
            normalized_constant = self.k_constant * len(doc) / self.avg_D 
            try:
                for (token, value) in tf_D.iteritems():
                    tf_D[token] = (value / (value + normalized_constant)) * self.idf[token]
            except KeyError:
                print "ERROR: tfidf.py - compute_Dw"
            # Save result for the fture
            self.Dw[doc_id] = tf_D

        print "************* %f seconds" % (time.time() - t)

    def compute_Qw(self):
        for (query_id, query) in self.queries.iteritems():
            self.Qw[query_id] = self.compute_tf(query)

    def score_query_document(self):
        """
        One of the most important function in TfIdf
        """
        print "Running: score_query_document()"
        t = time.time()

        # Step 0: Preparation step
        self.no_of_documents = len(self.docs)
        self.avg_D = sum([len(i) for i in self.docs.values()]) / self.no_of_documents
        
        self.dictionary = set()
        self.build_dict()

        self.df = dict()
        self.idf = dict()
        self.handle_idf()

        self.Dw = dict() # dw hold value of tf_D * idf
        self.compute_Dw()

        self.Qw = dict()
        self.compute_Qw()
        
        # Step 1: Computing the score from the weight of documents & queries
        self.scoreQD = []
        scoreQD = []
        for (query_id, query) in self.queries.iteritems():
            for (doc_id, doc) in self.docs.iteritems():
                # common words between query and document
                common_words = set(query).intersection(set(doc))
                score = 0
                for word in common_words:
                    score += self.Qw[query_id][word] * self.Dw[doc_id][word]

                if score != 0:
                    scoreQD.append((query_id, doc_id, score))
        
        # save the result
        self.scoreQD = scoreQD
        print "************* %f seconds" % (time.time() - t)

    def write_tfidf(self, output_file):
        doc_handling.write_output(self.scoreQD, output_file)

if __name__ == '__main__':
    time_1 = time.time()

    K = 2
    # preprocessing
    # = 1: normal case
    preprocessing_option = 1

    task2 = Tfidf(QUERY_FILE, DOC_FILE, K, preprocessing_option)
    task2.score_query_document()
    task2.write_tfidf(TFIDF_FILE)

    print "Total Running time: %f seconds" % (time.time() - time_1)

    # ./trec_eval
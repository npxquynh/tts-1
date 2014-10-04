#!/usr/bin/python2.6
import re
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

import pdb

def parse_doc(file_name, preprocessing_option = 1):
    parsed_doc = dict()

    with open(file_name) as doc:
        regex = r'(\d+)[\s](.+)'

        for line in doc:
            try:
                match_obj = re.match(regex, line)
                _id = match_obj.group(1)
                text = match_obj.group(2)

                parsed_doc[_id] = preprocessing(text, preprocessing_option)  
            except AttributeError:
                # the file is not in correct format
                print "incorrect format"

        return parsed_doc

def preprocessing(text, option = 1):
    """
    Input: text
    Output: array of tokens
    """
    tokens = []

    # remove any non-word character at the beginning of text
    text = re.sub('^[^\w]*', '', text)

    if option == 1:
        # lower + tokenize string
        splitter = re.compile(r'\W+') # any non-word character = delimeter
        tokens = splitter.split(text.strip().lower())
    elif option in [2, 3, 4, 5]:
        text = remove_references(text)
        tokens = tokenize(text)
        if option == 3:
            st = LancasterStemmer()
            tokens = [st.stem(token) for token in tokens]
        elif option == 4:
            st = SnowballStemmer("english")
            tokens = [st.stem(token) for token in tokens]
        elif option == 5:
            wnl = WordNetLemmatizer()
            tokens = [wnl.lemmatize(token) for token in tokens]
    elif option in [6, 7]:
        text = remove_references(text)
        tokens = tokenize(text)

        stop = stopwords.words('english')
        try:
            tokens = [token for token in tokens if token not in stop]
        except:
            pdb.set_trace()
            a = 2

        if option == 7:
            st = LancasterStemmer()
            tokens = [st.stem(token) for token in tokens]

    return tokens    

def remove_references(text):
    regex = '(.+)(References: .+)$'
    try:
        text = re.match(regex, text).group(1) # remove references
    except AttributeError: 
        text = text # keep the original text

    return text

def tokenize(text):
    # lower + tokenize string
    splitter = re.compile(r'\W+') # any non-word character = delimeter
    tokens = splitter.split(text.strip().lower())
    
    return tokens

def line_format(number_tuple):
    line = ""
    for i in range(len(number_tuple)):
        line = line + str(number_tuple[i]) + "\t0\t"

    return line.strip()

def write_output(output_data, output_file):
    with open(output_file, 'w') as out:
        for item in output_data:
            if item[2] != 0:
                out.write(line_format(item) + "\n")

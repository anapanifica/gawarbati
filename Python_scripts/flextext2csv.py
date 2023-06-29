#for some reason the title of the text is not correct in the resulting csv

import re
from xml.etree import ElementTree


def get_clean_data_from_flextext (corpus_file):
    csv = ""
    tree = ElementTree.parse(corpus_file)
    root = tree.getroot()

    for text in root.findall("./interlinear-text"):
        text_title = text.find('item').text
        print(text_title)
    
        for phrase in root.findall("./interlinear-text/paragraphs/paragraph/phrases/phrase"):
            sentence = phrase.find('item').text
            transl = phrase.find("item[@type='gls']").text

            
            phrase_gwt = ""
            words_gwt = ""
            gls = ""


            
            for word in phrase.findall("words/word"):

                clean_word = ""
                clean_word_gl = ""
                
                for word_txt in word.findall("item[@type='txt']"):
                    phrase_gwt += word_txt.text + " "
                
                for morph in word.findall("morphemes/morph/item[@type='txt']"):
                    clean_word += morph.text
                for morph in word.findall("morphemes/morph/item[@type='gls']"):
                    clean_word_gl += morph.text + "-"



                clean_word_gl = clean_word_gl.strip("-")

                words_gwt += clean_word + " "
                gls += clean_word_gl + " "

        
            
            words_gwt = words_gwt.strip()
            gls = gls.strip()


            #print(phrase_gwt)
            #print(words_gwt)
            #print(gls)
            #print(transl)

            csv = str(csv) + str(text_title) + "\t" + str(phrase_gwt) + "\t" + str(words_gwt) + "\t" + str(gls) + "\t" + str(transl) + "\n"
            #print(csv)

    
    return csv


def main ():

    corpus_file = "corpus_for_LocExist.flextext"
    csv = get_clean_data_from_flextext (corpus_file)
    #type(clean_txt)

    path = 'corpus.csv'
    f = open (path, 'w', encoding = 'utf-8')
    f.write (csv)
    f.close

if __name__ == '__main__':
    main ()

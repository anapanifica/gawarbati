import re
from lxml import etree as ElementTree



def get_the_glossed_word (word):
    glossed_word = ""
    glossed_word_gl = ""



    for morph in word.findall("morphemes/morph/item[@type='txt']"):
        glossed_word += morph.text

    for morph in word.findall("morphemes/morph/item[@type='gls']"):
        glossed_word_gl += morph.text + "-"

    glossed_word_gl = glossed_word_gl.strip("-")
    
    return glossed_word, glossed_word_gl


def get_the_glossed_sentence (phrase):

    sentence = phrase.find('item').text
    transl = phrase.find("item[@type='gls']").text
    sentence_number = phrase.find("item[@type='segnum']").text

    phrase_gwt = ""
    words_gwt = ""
    gls = ""

    for word in phrase.findall("words/word"):

        words_gwt += get_the_glossed_word (word) [0] + " "
        gls += get_the_glossed_word (word) [1] + " "

    words_gwt = words_gwt.strip()
    gls = gls.strip()


    glossed_sentence = str(sentence_number) + "\t" + str(phrase_gwt) + "\t" + str(words_gwt) + "\t" + str(gls) + "\t" + str(transl)

    return glossed_sentence

def edit_light_verbs (tree):
    
    #add translation of the verb to the glosses of lvc
    for morph in tree.findall(".//morph[item='com.pred']"):
        lvc = morph.find("item[@type='cf']").text
        if lvc.split(' ')[1] == "ke" or lvc.split(' ')[1] == "ker":
            morph.find("item[@type='gls']").text = 'do.' + morph.find("item[@type='gls']").text


                
        #print(morph.find("item[@type='gls']").text)
    

    return tree

def find_LVCs (corpus_file):
    csv = ""
    tree = ElementTree.parse(corpus_file)
    tree = edit_light_verbs (tree)
    root = tree.getroot()

    for text in root.findall("./interlinear-text"):
        text_title = text.find("item[@type='title']").text
        print(text_title)
    
        for phrase in text.findall("paragraphs/paragraph/phrases/phrase"):
            for word in phrase.findall("words/word"):

                for morph in word.findall("morphemes/morph/item[@type='gls']"):



                    #if morph.text == 'do' or 'do.' in morph.text:
                    if morph.text == 'give' or 'give.' in morph.text:
                        word_text = word.find('item').text
                        word_glossed = get_the_glossed_word (word) [0]
                        word_glossed_gl = get_the_glossed_word (word) [1]


                        # get the preceding word
                        for preceding_word in word.xpath("preceding-sibling::*[1]"):
                            pos = preceding_word.find("morphemes/morph/item[@type='msa']")
                            if pos != None: # is the part of speech indicated?
                                if pos.text == 'n' or pos.text == 'nm' or pos.text == 'nf' or pos.text == 'adj' or pos.text == '<Not Sure>':
                                    preceding_word_text = preceding_word.find('item').text
                                    preceding_word_pos = pos.text
                                    preceding_word_glossed = get_the_glossed_word (preceding_word) [0]
                                    preceding_word_glossed_gl = get_the_glossed_word (preceding_word) [1]


                                    csv = csv + text_title + '\t' + preceding_word_text + '\t' + preceding_word_pos + '\t' + preceding_word_glossed + '\t' + preceding_word_glossed_gl + '\t' + word_text + '\t' + word_glossed + '\t' + word_glossed_gl + '\t' + get_the_glossed_sentence (phrase) + '\n'

    return csv


def main ():    
    corpus_file = "../BACKUP 2024-02-09/all_texts.flextext"
    csv = find_LVCs (corpus_file)
    


    path = 'LVCs.csv'
    f = open (path, 'w', encoding = 'utf-8')
    f.write (csv)
    f.close


if __name__ == '__main__':
    main ()

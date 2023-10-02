import re
from xml.etree import ElementTree
import pandas as pd
import numpy as np



def get_all_verbs_from_flextext (corpus_file):
    csv = ""
    tree = ElementTree.parse(corpus_file)
    tree = edit_light_verbs (tree)
    root = tree.getroot()
    
    df = pd.DataFrame(columns=('word', 'gls'))
    
    for word_info in root.findall("./interlinear-text/paragraphs/paragraph/phrases/phrase/words/word"):
        
        word = ""
        word_gls = ""


        #if the word contains at least one morpheme annotated as verb (v, vt, vi, cop), this word is taken to the df
        for morph in word_info.findall("morphemes/morph/item[@type='msa']"):            
            if morph.text == "v" or morph.text == "vt" or morph.text == "vi" or morph.text == "cop" or morph.text == "com.pred" :
                for morph in word_info.findall("morphemes/morph/item[@type='txt']"):
                    word += morph.text
                #print(word)
                for morph in word_info.findall("morphemes/morph/item[@type='gls']"):
                    morph_text = morph.text
                    
                    morph_text = morph_text.replace(".afraid", "_afraid")
                    morph_text = morph_text.replace(".away", "_away")
                    morph_text = morph_text.replace(".birth", "_birth")
                    morph_text = morph_text.replace(".caus", "_caus")
                    morph_text = morph_text.replace(".down", "_down")
                    morph_text = morph_text.replace(".in", "_in")
                    morph_text = morph_text.replace(".injured", "_injured")
                    morph_text = morph_text.replace(".into", "_into")
                    morph_text = morph_text.replace(".off", "_off")
                    morph_text = morph_text.replace(".out", "_out")
                    morph_text = morph_text.replace(".sth", "_sth")
                    morph_text = morph_text.replace(".the.night", "_the_night")
                    morph_text = morph_text.replace(".the.river", "_the_river")
                    morph_text = morph_text.replace(".tired", "_tired")
                    morph_text = morph_text.replace(".up", "_up")

                    
                    
                    word_gls += morph_text + "-"
                #print(word_gls)
                
                df.loc[len(df.index)] = [word, word_gls.strip("-")] 
                

        #print(df)

    return df

def edit_light_verbs (tree):
    
    #add translation of the verb to the glosses of lvc
    for morph in tree.findall(".//morph[item='com.pred']"):
        lvc = morph.find("item[@type='cf']").text
        if lvc.split(' ')[1] == "ke" or lvc.split(' ')[1] == "ker":
            morph.find("item[@type='gls']").text = 'do.' + morph.find("item[@type='gls']").text
        if lvc.split(' ')[1] == "ɬi":
            morph.find("item[@type='gls']").text = 'give.' + morph.find("item[@type='gls']").text
        if lvc.split(' ')[1] == "foʈa":
            morph.find("item[@type='gls']").text = 'break.' + morph.find("item[@type='gls']").text
        if lvc.split(' ')[1] == "dar":
            morph.find("item[@type='gls']").text = 'stay.' + morph.find("item[@type='gls']").text
                
        #print(morph.find("item[@type='gls']").text)
    

    return tree


def identify_stem_and_inflection_in_glosses (df):

    # I remove the prefix neg- in glosses, so that the first element of the gloss would always be the stem
    df = df.replace('neg-','', regex=True)

    #unite entries for polysemious verbs
    df = df.replace('hit','give', regex=True)
    df = df.replace('take_out','pull_out', regex=True)
    df = df.replace('give_birth','pull_out', regex=True)
    
    df['stem'] = df['gls'].str.split('[-.]').str[0] #the first element of gloss is copied to the column 'stem'
    df['affixes'] = df['gls'].str.split('[-.]').str[1:] #the rest elements found in the gloss are copied to the column 'inflection' as lists
    df['affixes'] = [', '.join(map(str, l)) for l in df['affixes']] #list to string

    temp=df.affixes.fillna("0")
    df['nonfinite.affixes'] = np.where(temp.str.contains('cv'), 'cv',
                                       np.where(temp.str.contains("vn"), "vn", ""))


    #print(df)

    return df


def make_a_freq_list (tokens_list):

    tokens_freq = {}
    for i in tokens_list:
        if (i in tokens_freq.keys()):
            tokens_freq[i] += 1
        else:
            tokens_freq[i] = 1

    #dict to list
    tokens_freq_list = []
    for i in tokens_freq:
        tokens_freq_list.append([i, tokens_freq[i]])

    tokens_freq_list.sort(key = lambda x:x[1], reverse = True)
    print (tokens_freq_list[:20])

    freq = pd.DataFrame(tokens_freq_list, columns = ['verb', 'frequency'])

    return freq


def main ():    
    corpus_file = "../BACKUP 2023-05-24/all_texts.flextext"
    #corpus_file = "corpus_fragment.flextext"
    df = get_all_verbs_from_flextext (corpus_file)
    df = identify_stem_and_inflection_in_glosses (df)
    df_without_nonfinites = df[df['nonfinite.affixes']=='']

    freq = make_a_freq_list (df['stem'].values.tolist())
    freq_without_nonfinite_forms = make_a_freq_list (df_without_nonfinites['stem'].values.tolist())


    
    #type(clean_txt)


    df.to_csv('verbs.csv')
    freq.to_csv('verbs_freq_list.csv')
    freq_without_nonfinite_forms.to_csv('verbs_freq_list_without_nonfinite_forms.csv')


if __name__ == '__main__':
    main ()

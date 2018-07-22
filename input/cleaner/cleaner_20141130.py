'''
Created on 2014-11-30

@author: XingZhe
'''

import time
import csv
import re
import os

class Cleaner:
    
    lyric_file = "metadata/lyrics.csv"
    clean_lyric_file = "metadata/clean_lyrics_20141130.txt"
    hyphen_rule_file = "rules/hyphen_rules.txt"
    misspell_rule_file = "rules/misspell_rules.txt"
    variant_rule_file = "rules/variant_rules.txt"
    manual_rule_replace_file = "rules/manual_rules_new.txt"
    
    hyphen_rules = []
    misspell_rules = []
    variant_rules = []
    manual_rules_replace = []
    manual_rules_ignorecase = []
    
    
    def __init__(self):
        self.load_hyphen_rules()
        self.load_misspell_rules()
        self.load_variant_rules()
        self.load_manual_rules()
    
    def load_hyphen_rules(self):
        lines = open(self.hyphen_rule_file).readlines()
        for line in lines:
            line = line.replace("\r\n", "")
            line = line.replace("\n", "")
            tokens = line.split("\t")
            self.hyphen_rules.append((tokens[0], tokens[1]))
       
            
    def deal_with_hyphen(self, text):
        for (before, after) in self.hyphen_rules:
            text = text.replace(before, after)
        text = text.replace("-", " ")
        return text
    
    
    def load_misspell_rules(self):  # this rule is all lower case
        lines = open(self.misspell_rule_file).readlines()
        for line in lines:
            line = line.replace("\r\n", "")
            line = line.replace("\n", "")
            tokens = line.split("\t")
            self.misspell_rules.append((tokens[0], tokens[1]))
        
            
    def check_misspelling(self, text):
        for (before, after) in self.misspell_rules:
            text = re.sub(before, after, text, flags = re.I)
        return text
    
    
    def load_variant_rules(self):
        lines = open(self.variant_rule_file).readlines()
        for line in lines:
            line = line.replace("\r\n", "")
            line = line.replace("\n", "")
            tokens = line.split("\t")
            self.variant_rules.append((tokens[0], tokens[1]))
       
            
    def check_variants(self, text):
        for (before, after) in self.variant_rules:
            text = text.replace(before, after)
        return text
    
    
    def load_manual_rules(self):
        lines = open(self.manual_rule_replace_file).readlines()
        for line in lines:
            line = line.replace("\r\n", "")
            line = line.replace("\n", "")
            tokens = line.split("\t")
            self.manual_rules_replace.append((tokens[0], tokens[1]))
                    
    
    def check_manual(self, text):
        text = text.lower()
        for (before, after) in self.manual_rules_replace:
            text = text.replace(before, after)
        return text
    
    
    def deal_with_spelling(self, text):
        text = self.check_misspelling(text)
        text = self.check_variants(text)
        text = self.check_manual(text)
        return text
    
    
    def clean(self, text):
        text = text.replace("\r\n", " ")  # flatten
        text = text.replace("\n", " ")
        text = " " + text + " "
        
        # remove special, except for hyphen sign
        text = re.sub(r"[^a-zA-Z.'\- ]", " ", text)
        
        # apply the hyphen rule, no special signs any more, only punctuation left
        text = self.deal_with_hyphen(text)
        
        # apply the spelling checking rule: misspell, variant, manual check
        text = self.deal_with_spelling(text)
        
        return text
    
    
    def clean_lyric_for_tagging(self):
        candidate_lfids = {}  # only need to re-clean 275905 lyrics
        for line in open("metadata/metadata_for_275905_lyrics_20141105.txt").readlines():
            tokens = line.strip().split("\t")
            candidate_lfids[tokens[0]] = 1

        count = 0
        fout = open(self.clean_lyric_file, "w")
        fin = open(self.lyric_file, "rb")
        reader = csv.reader(fin, delimiter = ';', quotechar = '"', doublequote = False, escapechar = '\\')
        for row in reader:
            lyric_id = row[0]
            if lyric_id not in candidate_lfids:
                continue
            lyric = row[1]
            lyric = self.clean(lyric)
            fout.write("%s\t%s\n" % (lyric_id, lyric))
            count += 1
            if (count % 1000 == 0):
                print "%s done!" % count
        fin.close()
        fout.close()


def main():
    os.chdir("D:/smc/lyriq_20141130")   
    cleaner = Cleaner()
    start = time.clock()
    cleaner.clean_lyric_for_tagging()
    end = time.clock()
    print "running time: " + str((end -start) / 60.0) + " min"
    
        
if __name__ == "__main__":
    print "running as main...\n"
    main()
else:
    print "loaded as module...\n"
    
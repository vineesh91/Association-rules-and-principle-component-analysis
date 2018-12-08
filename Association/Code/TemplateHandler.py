import RuleGenerator as rg
import pandas as pd
from itertools import combinations
import sys
import argparse

def main(min_sup,min_conf):
    asso_rule = Asso_rule(min_sup,min_conf)
    print('Shape:')
    print(len(asso_rule.frequent_items))
    print('Results for queries')
    result11,cnt,fltr = asso_rule.template1("RULE", "ANY", ['G59_UP'])
    print(cnt)
    result12,cnt,fltr = asso_rule.template1("RULE", "NONE", ['G59_UP'])
    print(cnt)
    result13,cnt,fltr = asso_rule.template1("RULE", 1, ['G59_UP', 'G10_Down'])
    print(cnt)
    result14,cnt,fltr = asso_rule.template1("HEAD", "ANY", ['G59_UP'])
    print(cnt)
    result15,cnt,fltr = asso_rule.template1("HEAD", "NONE", ['G59_UP'])
    print(cnt)
    result16,cnt,fltr = asso_rule.template1("HEAD", 1, ['G59_UP', 'G10_Down'])
    print(cnt)
    result17,cnt,fltr = asso_rule.template1("BODY", "ANY", ['G59_UP'])
    print(cnt)
    result18,cnt,fltr = asso_rule.template1("BODY", "NONE", ['G59_UP'])
    print(cnt)
    result19,cnt,fltr = asso_rule.template1("BODY", 1, ['G59_UP', 'G10_Down'])
    print(cnt)
    result21,cnt,fltr = asso_rule.template2("RULE", 3)
    print(cnt)
    result22,cnt,fltr = asso_rule.template2("HEAD", 2)
    print(cnt)
    result23,cnt,fltr = asso_rule.template2("BODY", 1)
    print(cnt)
    result31,cnt,fltr = asso_rule.template31("1or1", "HEAD", "ANY", ['G10_Down'],"BODY", 1, ['G59_UP'])
    print(cnt)
    result32,cnt,fltr = asso_rule.template31("1and1", "HEAD", "ANY",['G10_Down'], "BODY", 1, ['G59_UP'])
    print(cnt)
    result33,cnt,fltr = asso_rule.template32("1or2", "HEAD", "ANY", ['G10_Down'],"BODY", 2)
    print(cnt)
    result34,cnt,fltr = asso_rule.template32("1and2", "HEAD", "ANY",['G10_Down'], "BODY", 2)
    print(cnt)
    result35,cnt,fltr = asso_rule.template33("2or2", "HEAD", 1, "BODY", 2)
    print(cnt)
    result36,cnt,fltr = asso_rule.template33("2and2", "HEAD", 1, "BODY", 2)

    print(cnt)

    print('done')

class Asso_rule:

    def __init__(self, min_sup, min_conf):
        self.temp_rules = []
        self.all_rules,self.frequent_items = rg.main_func(min_sup,min_conf)

    #
    def template1(self,part,quant,item_set):
        item_set = [item.upper() for item in item_set]
        part = part.upper()
        if type(quant) == str:
            quant = quant.upper()
        new_df = pd.DataFrame(columns=('Head', 'Body', 'Confidence'))
        if quant == 1:
            if part == 'HEAD':
                item = item_set[0]
                lst = item_set.copy()
                del lst[0]
                if len(item_set) == 1:
                    filter = self.all_rules['Head'].str.contains(item)
                else:
                    filter = ~self.all_rules['Head'].str.contains('|'.join(lst)) & self.all_rules['Head'].str.contains(
                        item)
                    for i in range(1, len(item_set)):
                        item = item_set[i]
                        lst = item_set.copy()
                        del lst[i]
                        sub_filter = ~self.all_rules['Head'].str.contains('|'.join(lst)) & self.all_rules[
                            'Head'].str.contains(item)
                        filter = filter | sub_filter

            if part == 'BODY':
                item = item_set[0]
                lst = item_set.copy()
                del lst[0]
                if len(item_set) == 1:
                    filter = self.all_rules['Body'].str.contains(item)
                else:
                    filter = ~self.all_rules['Body'].str.contains('|'.join(lst)) & self.all_rules['Body'].str.contains(
                        item)
                    for i in range(1, len(item_set)):
                        item = item_set[i]
                        lst = item_set.copy()
                        del lst[i]
                        sub_filter = ~self.all_rules['Body'].str.contains('|'.join(lst)) & self.all_rules[
                            'Body'].str.contains(item)
                        filter = filter | sub_filter

            if part == 'RULE':
                item = item_set[0]
                lst = item_set.copy()
                del lst[0]
                if len(item_set) == 1:
                    filter = (self.all_rules['Body'].str.contains(item) | self.all_rules['Head'].str.contains(item))
                else:
                    filter = ~(self.all_rules['Body'].str.contains('|'.join(lst)) | self.all_rules['Head'].str.contains(
                        '|'.join(lst))) & (self.all_rules['Body'].str.contains(item) | self.all_rules[
                        'Head'].str.contains(item))
                    for i in range(1, len(item_set)):
                        item = item_set[i]
                        lst = item_set.copy()
                        del lst[i]
                        sub_filter = ~(self.all_rules['Body'].str.contains('|'.join(lst)) | self.all_rules[
                            'Head'].str.contains('|'.join(lst))) & (
                                                 self.all_rules['Body'].str.contains(item) | self.all_rules[
                                             'Head'].str.contains(item))
                        filter = filter | sub_filter

        if quant == 'ANY':
            if part == 'HEAD':
                filter = self.all_rules['Head'].str.contains('|'.join(item_set))
            if part == 'BODY':
                filter = self.all_rules['Body'].str.contains('|'.join(item_set))
            if part == 'RULE':
                filter = self.all_rules['Head'].str.contains('|'.join(item_set)) | self.all_rules['Body'].str.contains('|'.join(item_set))


        if quant == 'NONE':
            if part == 'HEAD':
                filter = ~(self.all_rules['Head'].str.contains('|'.join(item_set)))

            if part == 'BODY':
                filter = ~(self.all_rules['Body'].str.contains('|'.join(item_set)))

            if part == 'RULE':
                filter = ~(self.all_rules['Head'].str.contains('|'.join(item_set)) | self.all_rules['Body'].str.contains('|'.join(item_set)))

        new_df = self.all_rules[filter]
        new_df.to_csv('template1.csv')
        return new_df,new_df.shape[0],filter

    def template2(self,part,quant):
        part = part.upper()
        new_df = pd.DataFrame(columns=('Head', 'Body', 'Confidence'))
        if part == 'HEAD':
            filter = self.all_rules['Head'].str.count(',')+1 >= quant
            new_df = self.all_rules[filter]
        if part == 'BODY':
            filter = self.all_rules['Body'].str.count(',')+1 >= quant
            new_df = self.all_rules[filter]
        if part == 'RULE':
            filter = self.all_rules['Body'].str.count(',')+1 + self.all_rules['Head'].str.count(',')+1 >= quant
            new_df = self.all_rules[filter]

        new_df.to_csv('template2.csv')
        return new_df, new_df.shape[0], filter

    def template31(self,operator,part1,quant1,item_set1,part2,quant2,item_set2):
        temp1 = operator[0]
        res1,cnt,filter1 = self.template1(part1, quant1, item_set1)
        res2,cnt,filter2 =self.template1(part2, quant2, item_set2)
        if ((operator[1] == 'o') | (operator[1] == 'O')):
            filter = filter1 | filter2
        else:
            filter = filter1 & filter2
        new_df = self.all_rules[filter]

        new_df.to_csv('template31.csv')
        return new_df, new_df.shape[0], filter

    def template32(self,operator,part1,quant1,item_set1,part2,quant2):
        temp1 = operator[0]
        res1,cnt,filter1 = self.template1(part1, quant1, item_set1)
        res2,cnt,filter2 = self.template2(part2, quant2)
        if ((operator[1] == 'o') | (operator[1] == 'O')):
            filter = filter1 | filter2
        else:
            filter = filter1 & filter2
        new_df = self.all_rules[filter]

        new_df.to_csv('template32.csv')
        return new_df, new_df.shape[0], filter

    def template33(self,operator,part1,quant1,part2,quant2):
        temp1 = operator[0]
        res1,cnt,filter1 = self.template2(part1, quant1)
        res2,cnt,filter2 = self.template2(part2, quant2)
        if ((operator[1] == 'o') | (operator[1] == 'O')):
            filter = filter1 | filter2
        else:
            filter = filter1 & filter2
        new_df = self.all_rules[filter]

        new_df.to_csv('template33.csv')
        return new_df, new_df.shape[0], filter


#Provide the parameters


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Association Rule Generator')
    parser.add_argument('--support', default=0.5, type=float,help='Minimum support')
    parser.add_argument('--confidence', default=0.7, type=float, help='Minimum confidence')
    args = parser.parse_args()
    main(args.support,args.confidence)

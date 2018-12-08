import DMProj1Apriory as item_generator
import pandas as pd
from itertools import combinations
from itertools import chain

def main_func(min_sup,min_conf):
    input_data = data_loader()
    H1 = []
    freq_itemsets = item_generator.Apriori(input_data, min_sup)
    asso_rule_generator = AssociationRuleGenerator(freq_itemsets,min_sup,min_conf)
    reslt = asso_rule_generator.generate_rules()
    reslt.to_csv('Rules_Generated.csv')
    with open('Frequent_ItemSets.csv', 'w') as f:
        for key in freq_itemsets.keys():
            f.write("%s,%s\n" % (key, freq_itemsets[key]))
    return reslt,freq_itemsets


def data_loader():
    data = pd.read_csv('C:/Users/vinee/Documents/Fall2018/DataMining/Proj1/associationruletestdata.txt', \
                       header=None, sep='\t')
    print(data.info())
    # change the data to the format as "G0_Up"
    for i in range(data.shape[1] - 1):
        for j in range(data.shape[0]):
            data[i][j] = 'G%s_' % (i + 1) + data[i][j].upper()
    data = data.values
    return data

class AssociationRuleGenerator:
    def __init__(self, freq_item_sets, min_sup, min_conf):
        self.freq_item_sets = freq_item_sets
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.rules = []
        self.rule_frame = pd.DataFrame(columns=('Head','Body','Confidence'))

    def item_set_diff(self,orig, sub):
        orig = list(orig)
        for item in sub:
            orig.remove(''.join(item))
        return orig

    def generate_rules(self):
        for item_set, support in self.freq_item_sets.items():
            if type(item_set) == frozenset:
                conseq_list = [x for x in list(item_set)]
                # one length consequent:
                self.ap_gen_rules(item_set,conseq_list,1)
        return self.rule_frame


    #method  from itertools
    def powerset(self,iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(1,2))

    def ap_gen_rules(self, item_set, hm,conseq_len):
        set_len = len(item_set)
        if set_len >= conseq_len + 1:
            #take all subsets of size conseq_len
            hm_new_set = set(combinations(hm, conseq_len))
            for hm_new in hm_new_set:
                diff = self.item_set_diff(item_set, list(hm_new))
                diff_list = list(diff)
                if len(diff_list) > 1:
                    rem_set = frozenset(diff_list)
                else:
                    rem_set = ''.join(diff_list)
                conf = self.freq_item_sets.get(frozenset(item_set)) / self.freq_item_sets.get(rem_set)
                if(conf >= self.min_conf):
                    if type(rem_set) != str:
                        rem_set = ','.join(rem_set)
                    if type(hm_new) != str:
                        new_val = ''
                        for ind_vals in hm_new:
                            if type(ind_vals) == str:
                                new_val = new_val+ ind_vals + ','
                            else:
                                new_val = new_val + ''.join([i for i in ind_vals]) + ','

                        new_val = new_val[:-1]
                    self.rules.append(''.join(rem_set) + '->' + ''.join(new_val))
                    self.rule_frame = self.rule_frame.append({'Head': rem_set,'Body':''.join(new_val),'Confidence':conf}, ignore_index=True)
                else:
                    hm_new_set = list(hm_new_set)
                    hm_new_set.remove(hm_new)
            self.ap_gen_rules(item_set, list(hm_new_set),conseq_len + 1)

# main_func()
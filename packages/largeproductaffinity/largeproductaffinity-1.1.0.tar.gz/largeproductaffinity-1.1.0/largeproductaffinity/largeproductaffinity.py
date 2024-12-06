# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 21:19:29 2022

@author: sarathbabu.karunanit
"""

import pandas as pd

from itertools import combinations,product

class large_product_affinity:
    
    def __init__(self,__df,support):
        self.__df=__df
        self.support=support
        tran,prod=self.__df.columns.values
        self.__df=self.__df.rename(columns={tran:'tran',prod:'prod'})
        self.total=self.__df.tran.nunique()

    def __mutual_support(self,x,y):
        return x&y
    
    def __cllc(self,x):
        x['confidence']=x['support']/x['antecedent_support']
        x['lift']=x['confidence']/x['consequent_support']
        x['leverage']=x['support']-(x['antecedent_support']*x['consequent_support'])
        x['conviction']=(1-x['consequent_support'])/(1-x['confidence'])
        return x
    
    def __post_processing(self):
        self.__mba=self.__cllc(self.__mba)

        self.__mba.drop(['antecedent_tran','consequent_tran','support_tran'],axis=1,inplace=True)

        self.__mba=self.__mba.sort_values(by=['confidence','lift'],ascending=False,ignore_index=True)
    
    def __individual_support(self):
        self.__df=self.__df.groupby(['prod']).agg(tran=pd.NamedAgg(column='tran',aggfunc=lambda x:set(list(x))),\
                            support=pd.NamedAgg(column='tran',aggfunc=lambda x:len(set(list(x)))/self.total)).reset_index()
        self.__df=self.__df.loc[self.__df['support']>=self.support]
        
        if len(self.__df)>0:
            self.__df=self.__df.sort_values(by=['support'],ascending=False)
            self.__flag=True    
        else:
            print('No Products available for the specified support')
            self.__flag=False

    def __perm_merge(self):
        self.__df_comb=pd.merge(self.__df_comb,self.__df,on=['consequent'],how='inner')
    
        self.__df_perm=self.__df_comb.copy()
        self.__df_perm.columns=[i.replace('antecedent','consequent') if 'antecedent' in i else i.replace('consequent','antecedent') \
        for i in self.__df_comb.columns.values]
        self.__df_perm=self.__df_perm[self.__df_comb.columns.values]

        self.__df_comb=pd.concat([self.__df_comb,self.__df_perm],axis=0,ignore_index=True)

        self.__df_comb['support_tran']=self.__df_comb.apply(lambda x:self.__mutual_support(x['antecedent_tran'],x['consequent_tran']),axis=1)

        self.__df_comb['support']=self.__df_comb['support_tran'].apply(lambda x:len(x)/self.total)
        self.__df_comb=self.__df_comb.loc[self.__df_comb['support']>=self.support]
        self.__df_comb=self.__df_comb.sort_values(by=['support'],ascending=False,ignore_index=True)
    
    def __perm_merge_two(self):
        self.__df_comb_two=pd.merge(self.__df_comb_two,self.__df_comb_pair,on=['consequent'],how='inner')
    
        self.__df_perm=self.__df_comb_two.copy()
        self.__df_perm.columns=[i.replace('antecedent','consequent') if 'antecedent' in i else i.replace('consequent','antecedent') \
        for i in self.__df_comb_two.columns.values]
        self.__df_perm=self.__df_perm[self.__df_comb_two.columns.values]

        self.__df_comb_two=pd.concat([self.__df_comb_two,self.__df_perm],axis=0,ignore_index=True)

        self.__df_comb_two['support_tran']=self.__df_comb_two.apply(lambda x:self.__mutual_support(x['antecedent_tran'],x['consequent_tran']),axis=1)

        self.__df_comb_two['support']=self.__df_comb_two['support_tran'].apply(lambda x:len(x)/self.total)
        self.__df_comb_two=self.__df_comb_two.loc[self.__df_comb_two['support']>=self.support]
        self.__df_comb_two=self.__df_comb_two.sort_values(by=['support'],ascending=False,ignore_index=True)
        
    
    def __perm_merge_three(self):
        self.__df_balance=pd.merge(self.__df_balance,self.__mba_copy,on=['consequent'],how='inner')
    
        self.__df_perm=self.__df_balance.copy()
        self.__df_perm.columns=[i.replace('antecedent','consequent') if 'antecedent' in i else i.replace('consequent','antecedent') \
        for i in self.__df_balance.columns.values]
        self.__df_perm=self.__df_perm[self.__df_balance.columns.values]

        self.__df_balance=pd.concat([self.__df_balance,self.__df_perm],axis=0,ignore_index=True)

        self.__df_balance['support_tran']=self.__df_balance.apply(lambda x:self.__mutual_support(x['antecedent_tran'],x['consequent_tran']),axis=1)

        self.__df_balance['support']=self.__df_balance['support_tran'].apply(lambda x:len(x)/self.total)
        self.__df_balance=self.__df_balance.loc[self.__df_balance['support']>=self.support]
        self.__df_balance=self.__df_balance.sort_values(by=['support'],ascending=False,ignore_index=True)
    
        
    def __two_combinations(self):
        self.__individual_support()
        
        if self.__flag:
            self.__df_comb=pd.DataFrame(list(combinations(self.__df['prod'].unique(),2)),columns=['antecedent','consequent'])
            self.__df=self.__df.rename(columns={'prod':'antecedent','tran':'antecedent_tran','support':'antecedent_support'})
            self.__df_comb=pd.merge(self.__df_comb,self.__df,on=['antecedent'],how='inner')
            self.__df.columns=[i.replace('antecedent','consequent') for i in self.__df.columns.values]

            self.__perm_merge()
            
            if len(self.__df_comb)>0:
                self.__mba=self.__df_comb.copy()

                #self.post_processing()

                return self.__mba
            else:
                print('No Two Products available for the specified support')
                self.__flag=False
                self.__df_one=self.__df.copy()
                self.__df_one.columns=['Product','Product_tran','Support']
                return self.__df_one.reset_index(drop=True)
                
 
    def __two_two_combinations(self):
            
        self.__df_comb_two=pd.DataFrame([(i,j) for i,j in list(combinations(self.__df_comb['antecedent'].unique(),2)) \
                          if len(set(i.split(','))&set(j.split(',')))==0],columns=['antecedent','consequent'])

        self.__df_comb_two=pd.merge(self.__df_comb,self.__df_comb_two,on=['antecedent'],how='inner')

        self.__df_comb_pair=self.__df_comb.copy()
        self.__df_comb_pair.columns=[i.replace('antecedent','consequent') for i in self.__df_comb_pair.columns.values]

        if len(self.__df_comb_two)>0:
            self.__perm_merge_two()
        
    def __three_two_combinations(self):
        self.__mba_copy=self.__mba.copy()


        self.__mba_copy['ant_len']=self.__mba_copy['antecedent'].apply(lambda x:len(x.split(',')))

        self.__mba_copy=self.__mba_copy.loc[self.__mba_copy['consequent_support']>=self.__mba_copy['antecedent_support']].\
        sort_values(by=['consequent_support'])


        self.__mba_copy=self.__mba_copy.loc[self.__mba_copy['ant_len']>1,['antecedent','antecedent_tran','antecedent_support']]


        self.__mba_copy['antecedent']=self.__mba_copy['antecedent'].apply(lambda x:",".join(sorted(x.split(','))))

        self.__mba_copy=self.__mba_copy.drop_duplicates(subset=['antecedent'],keep='first')


        self.__df_balance=pd.DataFrame([(i,j) for i,j in list(product(self.__df_comb['antecedent'].unique(),self.__mba_copy['antecedent'].unique())) \
                    if len(set(i.split(','))&set(j.split(',')))==0],columns=['antecedent','consequent'])


        self.__df_balance=pd.merge(self.__df_comb,self.__df_balance,on=['antecedent'],how='inner')


        self.__mba_copy.columns=[i.replace('antecedent','consequent') for i in self.__mba_copy.columns.values]

        if len(self.__df_balance)>0:
            self.__perm_merge_three()

        
   
    def calc(self):
        
        self.__two_combinations()
        
        if self.__flag:
            while len(self.__df_comb)>0:
                self.__df_comb=self.__df_comb.loc[self.__df_comb['consequent_support']>=self.__df_comb['antecedent_support']].\
                sort_values(by=['consequent_support'])

                self.__df_comb['antecedent']=self.__df_comb['antecedent']+','+self.__df_comb['consequent']

                self.__df_comb['antecedent']=self.__df_comb['antecedent'].apply(lambda x:",".join(sorted(x.split(','))))

                self.__df_comb=self.__df_comb.drop_duplicates(subset=['antecedent'],keep='first')


                self.__df_comb=self.__df_comb[['antecedent','support_tran','support']]
                self.__df_comb.columns=['antecedent','antecedent_tran','antecedent_support']

                self.__two_two_combinations()
                self.__three_two_combinations()

                self.__df_comb_three=pd.DataFrame([(i,j) for i,j in list(product(self.__df_comb['antecedent'],self.__df['consequent'])) if j not in i],\
                                          columns=['antecedent','consequent'])

                self.__df_comb=pd.merge(self.__df_comb,self.__df_comb_three,on=['antecedent'])

                self.__perm_merge()

                self.__mba=pd.concat([self.__mba,self.__df_comb],axis=0,ignore_index=True)
                self.__mba=pd.concat([self.__mba,self.__df_comb_two],axis=0,ignore_index=True)
                self.__mba=pd.concat([self.__mba,self.__df_balance],axis=0,ignore_index=True)

            self.__post_processing()

            return self.__mba
        
        else:
            self.__flag=False
            if len(self.__df)>0:
                self.__df_one=self.__df.copy()
                self.__df_one.columns=['Product','Product_tran','Support']
                return self.__df_one.reset_index(drop=True)
    
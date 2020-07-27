from .objects import dataset
import numpy as np
import pandas as pd
from tabulate import tabulate


def get_country_weekly_stat(MDlist, pops, key, timeoffset=0):
    def subfill(M, subs, key, rd, timeoffset):
        adata = dataset(M[key], key)
        rd[subs] = adata.y[-1-timeoffset] 
        rd['%s_perpop'%subs] = rd[subs] / rd['population']
        y_lastweek = adata.y[-8-timeoffset]
        y_twoweeksago = adata.y[-15-timeoffset]
        rd['%s_delta'%subs] = rd[subs] - y_lastweek
        rd['%s_delta_perpop'%subs] = rd['%s_delta'%subs] / rd['population']
        rd['%s_delta_relative'%subs] = rd['%s_delta'%subs] / y_lastweek
        rd['%s_ratechange'%subs] = (rd[subs] - y_lastweek) / (y_lastweek-y_twoweeksago)-1
        return rd
    rd = {}    
    Md = MDlist[0].copy()
    Mdea = MDlist[1].copy()
    Mdact = MDlist[2].copy()
    Mdrec = MDlist[3].copy()
    rd['key'] = key
    rd['population'] = pops[key]    
    rd = subfill(Md, 'cases', key, rd,timeoffset)
    rd = subfill(Mdea, 'dead', key, rd,timeoffset)
    rd = subfill(Mdact, 'active', key, rd,timeoffset)
    rd = subfill(Mdrec, 'recovered', key, rd,timeoffset)
    return rd

def get_country_weekly_stat_table(MDlist, pops, key, timeoffset=0, tableformat = 'simple'):
    rd = get_country_weekly_stat(MDlist, pops, key, timeoffset=timeoffset)
    L = [["cases",
          "%.0f k"%(rd['cases']/1e3),
          "%.1f k"%(rd['cases_delta']/1e3),
          "%.0f%%"%(rd['cases_delta_relative']*100),
          "%.0f%%"%(rd['cases_ratechange']*100)],
        ["",
         "%.1f /k"%(rd['cases_perpop']*1e3),
         "%.0f /m"%(rd['cases_delta_perpop']*1e6)],
        ["dead",
         "%.1f k"%(rd['dead']/1e3),
          "%.2f k"%(rd['dead_delta']/1e3),
          "%.0f%%"%(rd['dead_delta_relative']*100),
          "%.0f%%"%(rd['dead_ratechange']*100)],
        ["",
         "%.0f /m"%(rd['dead_perpop']*1e6),
         "%.0f /m"%(rd['dead_delta_perpop']*1e6)],]
    
    return(tabulate(L,
                   headers=["weekly","num","diff","diff %","acc %"],
                   tablefmt=tableformat,
                   colalign=("right","right","right","right"),
                   ))
    
def get_metatable(MDlist, pops, keyl, ignorelist=[], timeoffset=0):
    """pandas dataframe with get_country_stat values for key in keyl"""
    newDF = pd.DataFrame() 
    for k in keyl:
        if k not in ignorelist:        
            s = get_country_weekly_stat( MDlist, pops, k, timeoffset=timeoffset)
            if len(k)>10: # make abbrieviation of long names
                s['key10'] = k[0:10]
            else:
                s['key10'] = k
            tmpdf = pd.DataFrame([[s[x] for x in s.keys()]],
                                columns=[x for x in s.keys()])
            newDF=newDF.append(tmpdf,ignore_index=True)
    return newDF

def get_metatable124(MDlist, pops, keyl, ignorelist=[], timeoffset=0):
    """ get metatables for 1, 2 and 4 weeks """
    mt = get_metatable(MDlist, pops, keyl, ignorelist=ignorelist,  timeoffset = timeoffset )
    mt2 = get_metatable(MDlist, pops, keyl, ignorelist=ignorelist,  timeoffset = timeoffset + 15)
    mt4 = get_metatable(MDlist, pops, keyl, ignorelist=ignorelist,  timeoffset = timeoffset + 29)
    return mt, mt2, mt4

def sort_df_and_get_keys(dF, sortkey, num=10, ascending=False):
    """ sort dataframe by sortkey, return num keys in ascending(descending) order"""
    newDF = dF.sort_values(by=sortkey, ascending=ascending)
    return [x for x in newDF['key'][0:num] ]





def get_rank_table_from_df2(dF, dF2, dF4, sortkey, 
                           columns, factors,
                           columnalias = None,
                           num=10, ascending=False,
                           mininf=2000,
                           tableformat = 'github',
                           floatfmt='.1f'):
    keyranks = sort_df_and_get_keys(dF[dF['cases']>mininf], sortkey, num=num, ascending=ascending)
    if columnalias is None:
        cla = [x for x in columns]
    else:
        cla = [x for x in columnalias]
    cla.insert(0,'country')
    cla.insert(0,'')
    LL = []
    srtd2 = dF2[dF2['cases']>mininf].sort_values(by=sortkey, ascending=ascending, ignore_index=True)[['key',sortkey]]
    srtd4 = dF4[dF4['cases']>mininf].sort_values(by=sortkey, ascending=ascending, ignore_index=True)[['key',sortkey]]
    for i, kk in enumerate(keyranks):
        key10 =  dF[dF['key']==kk]['key10'].to_numpy()[0] #abbriev.keys
        # list index 2 and 4 weeks ago, -1 else
        i2l = srtd2[srtd2['key']==kk].index.to_list()
        i4l = srtd4[srtd4['key']==kk].index.to_list()
        if len(i4l)==0:
            i4 = 199
        else:
            i4 = i4l[0]
        if len(i2l) ==0:
            i2 = 199
        else:
            i2 = i2l[0]
    
        def diffsym(i1, i2):
            if i1-i2<0:
                return '\u25b2'
            elif i1==i2:
                return '\u25a0'
            else:
                return '\u25bc'
        r = "%d (%d, %d)  %s %s"%(i+1, i2+1,
               i4+1, diffsym(i, i2), diffsym(i2, i4))
        newl = [r,  key10]
        for ii,key2 in enumerate(columns):
            newl.append(dF[dF['key']==kk][key2] * factors[ii])
        LL.append(newl)
    return tabulate(LL, headers = cla, floatfmt=floatfmt, tablefmt=tableformat)


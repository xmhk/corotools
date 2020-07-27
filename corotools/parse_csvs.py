import numpy as np
import pandas as pd
import datetime as dt

from .base_data import dict_keyreplace, list_africancountries,  list_northamericancountries,list_asiancountries,list_southamericancountries,list_europeancountries, list_oceaniancountries


def get_populations(popfile):
    """get populations of countries from csv
    
    required csv format: country, number
    
    creates a dict with country as key"""
    pops = pd.read_csv(popfile, engine='python')
    popr = {}
    for x in pops['country']:
        popr[x] = pops[pops.country==x].to_numpy()[0][1]
    return popr



def parse_hopkins(csvfile):
    """parse time series files from Johns Hopkin University
    
    works for e.g. time_series_covid19_confirmed_global.csv
    
    Arguments : 
        - csvfile : csv file path"""
    df = pd.read_csv(csvfile)
    dtlist = [dt.datetime.strptime(x,"%m/%d/%y") for x in df.columns[4::]]
    years = np.array([x.year for x in dtlist])
    months = np.array([x.month for x in dtlist])
    days = np.array([x.day for x in dtlist])
    countrylist = set(df['Country/Region'])
    Md = {}
    world = np.zeros(len(dtlist))
    africa = np.zeros(len(dtlist))
    southamerica = np.zeros(len(dtlist))
    europe = np.zeros(len(dtlist))
    asia = np.zeros(len(dtlist))
    northamerica= np.zeros(len(dtlist))
    oceania = np.zeros(len(dtlist))
    for country in countrylist:
        newkey = country
        npa = df[df['Country/Region']==country].to_numpy()
        cases = np.sum(npa[:,4::],axis=0)  # cumulative countries, no regions
        tmpm = np.zeros((len(dtlist),4));    tmpm[:,0] = years[:];    tmpm[:,1] = months;    tmpm[:,2] = days
        tmpm[:,3] = cases[:]
        if newkey in dict_keyreplace.keys():
                newkey = dict_keyreplace[newkey]
        world = world + cases
        if newkey in list_africancountries:
            africa = africa + cases
        if newkey in list_asiancountries:
            asia = asia + cases
        if newkey in list_europeancountries:
            europe = europe + cases
        if newkey in list_northamericancountries:
            northamerica = northamerica + cases
        if newkey in list_southamericancountries:
            southamerica = southamerica + cases
        if newkey in list_oceaniancountries:
            oceania = oceania + cases

        Md[newkey] = tmpm
    tmpm = np.zeros((len(dtlist),4));    tmpm[:,0] = years[:];    tmpm[:,1] = months;    tmpm[:,2] = days
    tmpm2 = tmpm.copy()
    tmpm3 = tmpm.copy()
    tmpm5 = tmpm.copy()
    tmpm6 = tmpm.copy()
    tmpm7 = tmpm.copy()
    tmpm8 = tmpm.copy()
    tmpm[:,3] = world
    tmpm2[:,3] = africa
    tmpm3[:,3] = southamerica
    tmpm5[:,3] = europe
    tmpm6[:,3] = asia
    tmpm7[:,3] = oceania
    tmpm8[:,3] = northamerica
    Md['World'] = tmpm.copy()
    Md['Africa'] = tmpm2.copy()
    Md['South America'] = tmpm3.copy()
    Md['Asia'] = tmpm6.copy()
    Md['Europe'] = tmpm5.copy()
    Md['Oceania'] = tmpm7.copy()
    Md['North America'] = tmpm8.copy()
    return Md

def get_jhu_data(datadir='example_data/'):
    """parse cases, death, active, recovered from JHU data in one run
    
    * optional parameter: datadir: dir which contains
        'time_series_covid19_....csv' files
    * returns list of dictionaries:
        [ Cases, Dead, Recovered, Active ]
        """
    Md = parse_hopkins(datadir+'time_series_covid19_confirmed_global.csv')
    Mdea = parse_hopkins(datadir+'time_series_covid19_deaths_global.csv')
    Mdrec = parse_hopkins(datadir+'time_series_covid19_recovered_global.csv')
    Mact = {}
    for k in [x for x in Md.keys()]:
        Mact[k] = Md[k].copy()
        Mact[k][:,3] = Md[k][:,3] - Mdea[k][:,3] - Mdrec[k][:,3]
    return [Md, Mdea, Mact, Mdrec]
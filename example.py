import corotools as ct

popfilepath = "example_data/worldpop.csv"

all_jhu_dicts = ct.get_jhu_data()
population_dict = ct.get_populations(popfilepath)

# print stat for one country
countrykey = 'Japan'

print( ct.get_country_weekly_stat_table(all_jhu_dicts,population_dict, countrykey) )

# get the meta tables
mt, mt2, mt4= ct.get_metatable124(all_jhu_dicts,population_dict,ct.list_europeancountries)

# print example table
mytable = ct.get_rank_table_from_df2(mt,mt2, mt4, 'cases', columns=['cases', 'cases_perpop'],
                                     factors=[1.0/1000, 1000],
                                     columnalias=['cases (k)','rel. cases (1/k)'])
print(mytable)


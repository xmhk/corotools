import corotools as ct

popfile = "example_data/worldpop.csv"

all_jhu_dicts = ct.get_jhu_data()
population_dict = ct.get_populations(popfile)

# print stat for one country
countrykey = 'Japan'

print( ct.get_country_weekly_stat_table(all_jhu_dicts,population_dict, countrykey) )

# print the metatable
mt1 = ct.get_metatable124(all_jhu_dicts,population_dict,ct.list_europeancountries)
print(mt1)


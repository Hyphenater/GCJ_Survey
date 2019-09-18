import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load the previously-cleaned dataframe
filename = 'GCJ_Data-Cleaned.csv'
df = pd.read_csv(filename) 

# construct filtering masks and a name list for the different age groups
age_masks = {"younger than 12" : df['Age'].str.contains('younger') == True, "12 to 17" : df['Age'].str.contains('12') == True, "18 to 24" : df['Age'].str.contains('18', regex=False) == True, "25 to 34" : df['Age'].str.contains('25', regex=False) == True, "35 and up" : df['Age'].str.contains('35', regex=False) == True}
age_groups = [key for key in age_masks]

# produce a list of all the regions reported in the study and total populations for each
regions_list = df.Region.unique()
region_totals = {'Total (Age)': 0}
for region in regions_list:
    region_totals[region] = df.loc[df['Region'] == region]['Region'].count()
    region_totals['Total (Age)'] = region_totals['Total (Age)'] + region_totals[region]
print(region_totals)

# define the empty dictionary, and produce total populations, for each age group defined in age_masks
age_groups_total = [df.loc[age_masks[key]]['Age'].count() for key in age_masks]

# extract the age column for each region using the list of regions as a filter
region_age_data = {}
for item in regions_list:
    region_age_data[item] = df.loc[df['Region'] == item][['Age']]

# set up a dictionary of age group population by region, adding the total and age group names in the initial step
age_groups_by_region = {'Total (Age)': age_groups_total, 'Age Group': age_groups}
for region in regions_list:
    age_groups_by_region[region] = [region_age_data[region].loc[age_masks[key]]['Age'].count() for key in age_masks]

# convert the age group population dictionary into a pandas dataframe, assigning the index manually
age_groups_by_region = pd.DataFrame(age_groups_by_region)
print(age_groups_by_region)

# produce a new dataframe from age_groups_by_region to yield percentages
age_perc_by_region = age_groups_by_region
age_perc_by_region = age_perc_by_region.set_index('Age Group')
for name, content in age_perc_by_region.items():
    region_total = sum(age_perc_by_region[name])
    age_perc_by_region[name] = [entry / region_total * 100 for entry in age_perc_by_region[name]]
print(age_perc_by_region)
age_perc_by_region.to_csv('age_groups_data_melt.csv')

# re-shape the age_groups and age_perc dataframes to show the age group breakdown per region, then merge
age_groups_melt = pd.melt(age_groups_by_region, id_vars='Age Group', var_name='Region', value_name='Population')
age_perc_by_region = age_perc_by_region.reset_index()
age_perc_melt = pd.melt(age_perc_by_region, id_vars='Age Group', var_name='Region', value_name='Percentage of Population')
age_groups_melt = pd.merge(age_groups_melt, age_perc_melt, on=['Region', 'Age Group'])
age_groups_melt = age_groups_melt.set_index(['Region', 'Age Group'])
print(age_groups_melt)
age_groups_melt.to_csv('region_population_and_percentages.csv')

# pivot the population percentages data to a format for pyplot to work with
age_groups_melt = age_groups_melt.reset_index()
age_groups_pivot = age_groups_melt.pivot_table(index='Region', columns='Age Group', values='Percentage of Population', margins=True, aggfunc=sum)
print(age_groups_pivot)
age_groups_pivot.to_csv('region_percentage_pivot_table.csv')

# create a breakdown of region population by age group from a transpose of the initial age group dataframe
age_groups_by_region = age_groups_by_region.set_index('Age Group')
print(age_groups_by_region)
regions_by_age_group = age_groups_by_region.transpose()
regions_by_age_group = regions_by_age_group.reset_index()
print(regions_by_age_group)
regions_by_age_group.to_csv('region_age_group_data.csv', index_label='Region')

# plot data
#_ = age_groups_pivot.iloc[:-1,:-1].plot(kind='bar', stacked=True)
#_ = plt.title('Regional Age Group Distribution (% of total)')
#_ = plt.xlabel('Region')
#_ = plt.ylabel('Percentage of Population')
#_ = plt.show()

# use groupby to demonstrate an easy way to get age/region breakdowns, and why I tried to do things differently
groupby_ex = df.groupby(['Age', 'Region'])
groupby_ex = groupby_ex['Region'].count()
print(groupby_ex)

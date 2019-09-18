import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = 'GCJ_Data-Cleaned.csv'
df = pd.read_csv(filename)

# set up filter masks for each platform to be searched for
platform_masks = {'Desktop' : df['Platforms Owned'].str.contains('Desktop') == True, 'PS4' : df['Platforms Owned'].str.contains('Playstation 4') == True, 'Xbone' : df['Platforms Owned'].str.contains('XBox One') == True, 'Switch' : df['Platforms Owned'].str.contains('Nintendo Switch') == True, 'Retros' : df['Platforms Owned'].str.contains('retro') == True, 'Laptop' : df['Platforms Owned'].str.contains('Laptop') == True}

# create dictionary of total counts for each platform
platforms_total = {key : platform_masks[key].sum() for key in platform_masks}
print(platforms_total)

# create dictionaries of total population by region and age group
age_masks = {"younger than 12" : df['Age'].str.contains('younger') == True, "12 to 17" : df['Age'].str.contains('12') == True, "18 to 24" : df['Age'].str.contains('18', regex=False) == True, "25 to 34" : df['Age'].str.contains('25', regex=False) == True, "35 and up" : df['Age'].str.contains('35', regex=False) == True}
age_groups = [key for key in age_masks]
age_groups_total = {key : df.loc[age_masks[key]]['Age'].count() for key in age_masks}

regions_list = df.Region.unique()
region_totals = {'Total (Age)': df['Region'].count()}
for region in regions_list:
    region_totals[region] = df.loc[df['Region'] == region]['Region'].count()
print(region_totals)

# create a dictionary of questionaire responses for each listed platform, broken down by age group
platform_age_data = {'Platform' : [platform for platform in platform_masks.keys()]}
for group in age_masks:
    platform_age_data[group] = [df.loc[platform_masks[platform] & age_masks[group]]['Age'].count() for platform in platform_masks]

# convert the platform ownership by age group dictionary into a dataframe and index by age group
platforms_by_age = pd.DataFrame(platform_age_data)
print(platforms_by_age)

# produce a new dataframe, expressing platform ownership as percentage of the age group population total
platforms_by_age = platforms_by_age.set_index('Platform')
platforms_by_age_perc = platforms_by_age
for group, content in platforms_by_age_perc.items():
    platforms_by_age_perc[group] = [entry / age_groups_total[group] * 100 for entry in platforms_by_age_perc[group]]
print(platforms_by_age_perc)
#platforms_by_age_perc = platforms_by_age_perc.reset_index()
#platforms_by_age_perc.to_csv('platform_ownership-by_age-percent.csv')

# create a dictionary of questionaire responses for each listed platform, broken down by region
platform_region_data = {'Platform' : [platform for platform in platform_masks.keys()]}
for region in regions_list:
    platform_region_data[region] = [df.loc[platform_masks[platform] & df['Region'].isin([region])]['Region'].count() for platform in platform_masks]
platforms_by_region = pd.DataFrame(platform_region_data)
platforms_by_region = platforms_by_region.set_index('Platform')
print(platforms_by_region)

# produce a new dataframe, expressing platform ownership as a percentage of the region population total
platforms_by_region_perc = platforms_by_region
for region, content in platforms_by_region_perc.items():
    platforms_by_region_perc[region] = [entry / region_totals[region] * 100 for entry in platforms_by_region_perc[region]]
print(platforms_by_region_perc)

# plot the data
_ = platforms_by_age_perc.plot(kind='bar')
_ = plt.title('Gaming Platform Ownership by Age Group')
_ = plt.xlabel('Gaming Platform')
_ = plt.ylabel('Ownership (% of Age Group Population)')
_ = plt.yticks(range(0, 101, 10))
_ = plt.grid(True, which='major', axis='y')
_ = plt.show()

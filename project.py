#!/usr/bin/env python
# coding: utf-8

# ## Project: Clean and Analyze Employee Exit Surveys

# In this project,stakeholders want to know the following:
# 
# - Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
# 
# - Are younger employees resigning due to some kind of dissatisfaction? What about older employees?

# ## import libraries

# In[1]:


import pandas as pd
import numpy as np


# ## Creating new dataset's

# In[2]:


dete_survey = pd.read_csv("dete_survey.csv")
tafe_survey = pd.read_csv("tafe_survey.csv")


# # Analyse both dataset's 

# In[3]:


dete_survey.info()


# So above we can see that in "dete_survey" there is total 55 columns and some of them have missing values

# In[4]:


tafe_survey.info()


# So above we can see that in "tafe_survey" there is total 72 columns and some of them have missing values 

# ### lets see how dataset's are looks like

# In[5]:


dete_survey.head()


# In[6]:


tafe_survey.head()


# ## Frequency of  values

# ### dete_survey dataset

# In[7]:


dete_survey["Region"].value_counts()


# In[8]:


dete_survey["SeparationType"].value_counts()


# From above we can say that most of office employees are resigning beacause of their retirement and other 150 employees who resigning are not give their specific reasons.

# In[9]:


dete_survey["Age"].value_counts()


# From above we can see that younger employee are not the one who are resigning.
# the employee are resigning th most are older employee's
# 

# ### tafe_survey dataset

# In[10]:


tafe_survey["Reason for ceasing employment"].value_counts()


# In[11]:


tafe_survey["Gender. What is your Gender?"].value_counts()


# from above we can see that most of the Females are resigning. 

# In[12]:


tafe_survey["CESSATION YEAR"].value_counts().sort_index()


# ### Checking Null Values in both datasets 

# In[13]:


dete_survey.isnull().sum()


# - Aboriginal
# - Torres Strait
# - South Sea
# - Disability
# - NESB
# 
# Above listed columns have too much null values!

# In[14]:


tafe_survey.isnull().sum()


# In[15]:


dete_survey = pd.read_csv("dete_survey.csv",na_values="Not Stated")


# we can first make the following observations:
# 
# - The dete_survey dataframe contains 'Not Stated' values that indicate values are missing, but they aren't represented as NaN.
# - Both the dete_survey and tafe_survey dataframes contain many columns that we don't need to complete our analysis.
# - Each dataframe contains many of the same columns, but the column names are different.
# - There are multiple columns/answers that indicate an employee resigned because they were dissatisfied.

# In[16]:


tafe_survey = pd.read_csv("tafe_survey.csv",na_values="Not Stated")


# ## Droping Columns

# let's drop some columns from each dataframe that we won't use in our analysis to make the dataframes easier to work with.

# In[17]:


dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49],axis = 1)


# In[18]:


tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66],axis = 1)


# ## Renaming columns

# In[19]:


dete_survey_updated.columns = dete_survey_updated.columns.str.lower().str.strip().str.replace(" ","_")


# In[20]:


rename_col = {"Record ID":"ID","Reason for ceasing employment":"SeparationType","CESSATION YEAR":"Cease Date","LengthofServiceOverall.Overall Length of Service at Institute (in years)":"DETE Start Date","CurrentAge.Current Age":"Age","Gender.What is your Gender?":"Gender"}
tafe_survey_updated= tafe_survey.rename(rename_col,axis=1)


# In[21]:


tafe_survey_updated.columns = tafe_survey_updated.columns.str.lower().str.strip().str.replace(" ","_")


# In[22]:


dete_survey_updated["separationtype"].value_counts()


# In[23]:


tafe_survey_updated["separationtype"].value_counts()


# In[24]:


# Update all separation types containing the word "resignation" to 'Resignation'
dete_survey_updated['separationtype'] = dete_survey_updated['separationtype'].str.split('-').str[0]

# Check the values in the separationtype column were updated correctly
dete_survey_updated['separationtype'].value_counts()


# In[25]:


# Select only the resignation separation types from each dataframe
dete_resignations = dete_survey_updated[dete_survey_updated['separationtype'] == 'Resignation'].copy()
tafe_resignations = tafe_survey_updated[tafe_survey_updated['separationtype'] == 'Resignation'].copy()


# ## Verify the Data

# In[26]:


dete_resignations["cease_date"].value_counts()


# In[27]:


dete_resignations["cease_date"] = dete_resignations["cease_date"].str.split("/").str[-1]
dete_resignations["cease_date"] = dete_resignations["cease_date"].astype(float)


# In[28]:


dete_resignations["cease_date"].value_counts()


# In[29]:


# Check the unique values and look for outliers
dete_resignations['dete_start_date'].value_counts().sort_values()


# In[30]:


# Check the unique values
tafe_resignations['cease_date'].value_counts().sort_values()


# Below are our findings:
# 
# - The years in both dataframes don't completely align. The tafe_survey_updated dataframe contains some cease dates in 2009, but the dete_survey_updated dataframe does not. The tafe_survey_updated dataframe also contains many more cease dates in 2010 than the dete_survey_updaed dataframe. Since we aren't concerned with analyzing the results by year, we'll leave them as is.

# ## Create a New Column

# The years in the dete_resignations dataframe, we'll use them to create a new column. Recall that our end goal is to answer the following question:
# 
# - Are employees who have only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been at the job longer? 

# In[31]:


dete_resignations["cease_date"]


# In[32]:


dete_resignations["institute_service"] = dete_resignations["cease_date"] - dete_resignations["dete_start_date"]
dete_resignations["institute_service"].head()


# ## Identify Dissatisfied Employees

# Next, we'll identify any employees who resigned because they were dissatisfied. Below are the columns we'll use to categorize employees as "dissatisfied" from each dataframe:
# 
# 1.tafe_survey_updated:
#  - Contributing Factors. Dissatisfaction
#  - Contributing Factors. Job Dissatisfaction
#  
# 2.dafe_survey_updated:
#  - job_dissatisfaction
#  - dissatisfaction_with_the_department
#  - physical_work_environment
#  - lack_of_recognition
#  - lack_of_job_security
#  - work_location
#  - employment_conditions
#  - work_life_balance
#  - workload

# If the employee indicated any of the factors above caused them to resign, we'll mark them as dissatisfied in a new column. After our changes, the new dissatisfied column

# In[33]:


tafe_resignations.columns


# In[34]:


tafe_resignations['contributing_factors._dissatisfaction'].value_counts()


# In[35]:


tafe_resignations['contributing_factors._job_dissatisfaction'].value_counts()


# ## Create function to make new column
# 

# In[38]:


# Update the values in the contributing factors columns to be either True, False, or NaN
def update_vals(x):
    if x == '-':
        return False
    elif pd.isnull(x):
        return np.nan
    else:
        return True
tafe_resignations['dissatisfied'] = tafe_resignations[['contributing_factors._dissatisfaction', 'contributing_factors._job_dissatisfaction']].applymap(update_vals).any(1, skipna=False)
tafe_resignations_up = tafe_resignations.copy()

# Check the unique values after the updates
tafe_resignations_up['dissatisfied'].value_counts(dropna=False)


# In[39]:


# Update the values in columns related to dissatisfaction to be either True, False, or NaN
dete_resignations['dissatisfied'] = dete_resignations[['job_dissatisfaction',
       'dissatisfaction_with_the_department', 'physical_work_environment',
       'lack_of_recognition', 'lack_of_job_security', 'work_location',
       'employment_conditions', 'work_life_balance',
       'workload']].any(1, skipna=False)
dete_resignations_up = dete_resignations.copy()
dete_resignations_up['dissatisfied'].value_counts(dropna=False)


# we've accomplished the following:
# 
# - Renamed our columns
# - Dropped any data not needed for our analysis
# - Verified the quality of our data
# - Created a new institute_service column
# - Cleaned the Contributing Factors columns
# - Created a new column indicating if an employee resigned because they were - - - dissatisfied in some way

# In[40]:


dete_resignations_up["institute"] = "DETE"


# In[42]:


tafe_resignations_up["institute"] = "TAFE"


# In[58]:


combined = pd.concat([dete_resignations_up,tafe_resignations_up],ignore_index=True)


# In[66]:


combined


# We can perform some kind of analysis! First, though, we'll have to clean up the institute_service column. This column is tricky to clean because it currently contains values in a couple different forms

# In[69]:


combined["institute_service"].value_counts(dropna=False)


# In[71]:


# Extract the years of service and convert the type to float
combined['institute_service_up'] = combined['institute_service'].astype('str').str.extract(r'(\d+)')
combined['institute_service_up'] = combined['institute_service_up'].astype('float')

# Check the years extracted are correct
combined['institute_service_up'].value_counts()


# In[73]:



# Convert years of service to categories
def transform_service(val):
    if val >= 11:
        return "Veteran"
    elif 7 <= val < 11:
        return "Established"
    elif 3 <= val < 7:
        return "Experienced"
    elif pd.isnull(val):
        return np.nan
    else:
        return "New"
combined['service_cat'] = combined['institute_service_up'].apply(transform_service)

# Quick check of the update
combined['service_cat'].value_counts()


# ## Perform Some Initial Analysis

# In[76]:


# Verify the unique values
combined['dissatisfied'].value_counts(dropna=False)


# In[77]:


# Replace missing values with the most frequent value, False
combined['dissatisfied'] = combined['dissatisfied'].fillna(False)


# In[78]:



# Calculate the percentage of employees who resigned due to dissatisfaction in each category
dis_pct = combined.pivot_table(index='service_cat', values='dissatisfied')

# Plot the results
get_ipython().run_line_magic('matplotlib', 'inline')
dis_pct.plot(kind='bar', rot=30)


# From the initial analysis above, we can tentatively conclude that employees with 7 or more years of service are more likely to resign due to some kind of dissatisfaction with the job than employees with less than 7 years of service. 

# In[ ]:





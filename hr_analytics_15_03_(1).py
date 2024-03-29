# -*- coding: utf-8 -*-
"""HR Analytics_15-03 (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YMorbiK29wIJDAINNPvvFzAPWIC3u1ig

## HR Analytics
"""

import pandas as pd #importing the required libraries

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("drive/MyDrive/people.csv")

df

df.shape

#EDA - Exploratory Data Analysis
#->Null values
#->Duplicate values
#->Outliers
#->#Multicollinearity - vif
#->Visualisation

#Data Preprocessing -

#Identify NUll values

df.head()

#isnull()
df.isnull()

df.info()

df.describe(include='all')

df.isnull().sum()

#Handling the null values
#-> df.dropna()
#-> df.fillna(0)

df.info()

#duplicate rows

df.duplicated()

df[df.duplicated()]

#removing the duplicated records
df = df.drop_duplicates()

df.shape #14999 - 3008 = 11991

#Data Correlation -

#Positive correlation - directly proportional
#Negative correlation - Inversly proportional
#Zero correlation - Not related to each other -> ex: Age, Gender

df.corr()

import matplotlib.pyplot as plt
import seaborn as sns

#Heat map

sns.heatmap(df.corr(),cmap='rainbow')

for col in df.columns:
  print(pd.DataFrame(df[col].value_counts()))

sns.heatmap(df.corr(),annot=True,cmap='rainbow')

#Data Visualization

df

a = ['dept','numberOfProjects','timeSpent.company','workAccident','promotionInLast5years','salary']

a

fig = plt.subplots(figsize=(20,25))
#for i in range(a): #enumerate
for i,j in enumerate(a):
    print(i,j)
    #i -> index values
    #j -> Data
    #i=0, j=Dept; i=1, j= numberOfProjects,......
    plt.subplot(3,2,i+1)
    #(3,2,1), (3,2,2), (3,2,3) ,.....
    sns.countplot(x=j, data=df) #categories and their count
plt.show()

fig = plt.subplots(figsize=(20,25))
#for i in range(a): #enumerate
for i,j in enumerate(a):
    print(i,j)
    #i -> index values
    #j -> Data
    #i=0, j=Dept; i=1, j= numberOfProjects,......
    plt.subplot(3,2,i+1)
    #(3,2,1), (3,2,2), (3,2,3) ,.....
    sns.countplot(x=j, data=df, hue='left') #categories and their count
plt.show()

#attrition rate = no.of employees those are leaving / total no.of rmp's

#Conclusions:

#Dept: Sales, Support, Technical: depts are having the high attrition rate
   # -> Incentives, Increments, training, bonus

#Projects -> Employees are leaving when they either have highest or lowest no.of projects
    #-> 3, 4 is the optimal no.of projects

#Time spent -> 3-5 years is the most crucial time for the company
    #-> Increment, Annual Incentives, Promotions, appreciation bonus

#Work Accident -> Most of the employees who are leaving, are not invloved in any work accident
    # Work accident and attrition rate are not related

#Promotion in last 5 years -> Most of the employees who are leaving the company haven't been promoted in last 5 yaers

#Salary -> Most of the employees who are leaving are from ramge low and medium salaries.

"""**t-test**

A t test is a statistical test that is used to compare the means of two groups. It is often used in hypothesis testing to determine whether a process or treatment actually has an effect on the population of interest, or whether two groups are different from one another.

The null hypothesis (H0) is that the true difference between these group means is zero.
The alternate hypothesis (Ha) is that the true difference is different from zero.
"""

#The average monthly hours of an employee having 2 years experience is 167.
#Is it same for employees having more than 2 years experience?
#CONDITION: satisfactory level of an employee is from 0-0.5 and AvgMonthlyHours =130-200

df.columns

emp = df[(df['satisfactoryLevel']<=0.5)  & (df['avgMonthlyHours']>=130) & (df['avgMonthlyHours']<=200)]

emp.head(3)

#H0 - Average Monthly Hours of an employee having 2 or more than 2 years experience is 167 hours
#H1 - Average Monthly Hours of an employee having 2 or more than 2 years experience is not 167 hours

#selecting a random sample
sample_size =100
sample1 = emp.sample(sample_size,random_state=1)

pop_mean =167
#sample mean
print("Sample Mean - ",sample1["avgMonthlyHours"].mean(),", Population Mean - ",pop_mean)

from scipy.stats import ttest_1samp
statistics, p_value = ttest_1samp(sample1["avgMonthlyHours"],pop_mean)
print(p_value)

#The given value is less than 0.05 and thus reject the null hypothesis.
#Average Monthly Hours of an employee having 2 or more than 2 years experience is not 167 hours

"""**z-test**

Z test is a statistical test that is conducted on data that approximately follows a normal distribution. The z test can be performed on one sample, two samples, or on proportions for hypothesis testing. It checks if the means of two large samples are different or not when the population variance is known.

A z test can further be classified into left-tailed, right-tailed, and two-tailed hypothesis tests depending upon the parameters of the data.
"""

# The percentage of employee leaving the company is 3% having experience of 2 years.
#Is it same for employees having more than 2 years experience?

#H0 - The percentage of employee leaving the company is 3% having experience of 2 years and  same as
#more than 2 years experience.
#H1 - The percentage of employee leaving the company is 3% having experience of 2 years and is not same as
#more than 2 years experience employees.

from statsmodels.stats.proportion import proportions_ztest
sample_size = 100
sample1 = emp.sample(sample_size,random_state=1)
sample1['left'].value_counts()
nobs = len(sample1['left'])
p0 = 0.03
count = sample1['left'].value_counts()/nobs
statistic_oneprop,p_value_oneprop = proportions_ztest(count = count,nobs = nobs ,value =p0)

p_value_oneprop

#pvalue <0.05 reject the null hypothesis
#The percentage of employee leaving the company is 3% having experience of 2 years and is not same as
#more than 2 years experience employees.

#Is the mean avg monthly hours of an employee having experience of 2-5 yrs is the same as that for employee
#having exp of 6-10 yrs?

"""**f-test**

The F test is a statistical technique that determines if the variances of two samples or populations are equal using the F test statistic. Both the samples and the populations need to be independent and fit into an F-distribution. The null hypothesis can be rejected if the results of the F test during the hypothesis test are statistically significant; if not, it stays unchanged.

We can use this test when:
The population is normally distributed.
The samples are taken at random and are independent samples.
"""

e1 = df[(df['timeSpent.company']>2) & (df['timeSpent.company']<5)]
e2 = df[(df['timeSpent.company']>6) & (df['timeSpent.company']<10)]

s1 = e1.sample(100,random_state = 0)
s2 = e2.sample(100,random_state=0)

print(s1.avgMonthlyHours.var())
print(s2.avgMonthlyHours.var())
df1 = len(s1)-1
df2 = len(s2)-1

from scipy.stats import f
f = s1.avgMonthlyHours.mean()/s2.avgMonthlyHours.mean()
print(f)

import scipy
scipy.stats.f.cdf(f,df1,df2)

#The mean avg monthly hours of an employee having experience of 2-5 yrs is the same as that for employee
#having exp of 6-10 yrs.


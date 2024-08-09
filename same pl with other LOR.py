import pandas as pd
import numpy as np
#read sql
data1= pd.read_csv('C:/Users/mfernando/OneDrive - Wiley/Documents/product line- LOB,LOR/data/product_line_all.csv')

#read sales data
sales= pd.read_excel('C:/Users/mfernando/OneDrive - Wiley/Documents/product line- LOB,LOR/data/net_sales.xlsx')
#join with sales data
data= data1.merge(sales, on=['ISBN10'], how='left')
data["NET_SALES"].fillna(0, inplace = True)
data["ABS_NET_SALES"]= abs(data["NET_SALES"])
#remove exclusions
data= data[data["ABS_NET_SALES"]> 100]

df1= data[data['SC_LOB'].isin(['Advanced Content','Courseware'])]
df1= df1[~df1['SC_LOR'].isin(['Advanced Business','Advanced Math','Accounting','Business & Finance Foundations','Computer Science',
                             'Data Science','Engineering Foundations','IT','Mathematics'])]

df1= df1[(df1['PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])) | (df1['PROJ_LEVEL_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1']))]
# df2= df1[(df1['PRODUCT_LINE'].isin(['AM','I','4','D','W','C1']))]
#consistent in project level?
df1.loc[df1['PRODUCT_LINE']==df1['PROJ_LEVEL_PRODUCT_LINE'],'PROJECT_LEVEL_CONSISTENT']= 'YES'
df1.loc[df1['PRODUCT_LINE']!=df1['PROJ_LEVEL_PRODUCT_LINE'],'PROJECT_LEVEL_CONSISTENT']= 'NO'

df1.loc[(~df1['PROJ_LEVEL_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])), 'NEED REVIEW']= 'NO'
df1.loc[(~df1['PROJ_LEVEL_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])) & (df1['PROJ_LEVEL_PRODUCT_LINE'].isnull()), 'NEED REVIEW']= 'YES'
df1.loc[(~df1['PROJ_LEVEL_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])), 'PREDICTED_PRODUCT_LINE']= df1['PROJ_LEVEL_PRODUCT_LINE']
df1.loc[(~df1['PROJ_LEVEL_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])) & (df1['PROJ_LEVEL_PRODUCT_LINE'].isnull()), 'PREDICTED_PRODUCT_LINE']= 'NEED REVIEW'
df1.loc[(df1['PROJ_LEVEL_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])), 'NEED REVIEW']= 'YES'
df1.loc[(df1['PROJ_LEVEL_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])), 'PREDICTED_PRODUCT_LINE']= 'NEED REVIEW'

#add new column to get predicted values
data_count = df1.groupby(['SC_LOB','SC_LOR','PRODUCT_LINE'], as_index = False)['ISBN10'].nunique()
data_count.rename(columns={'ISBN10':'NO_ISBNS'},inplace=True,)

top_3_prod_line= data_count.sort_values('NO_ISBNS',ascending= False).groupby(['SC_LOB','SC_LOR']).head(3)
top_3_prod_line['order_row'] = top_3_prod_line.sort_values('NO_ISBNS',ascending= False).groupby(['SC_LOB','SC_LOR']).cumcount()+1
top_3_prod_line.rename(columns={'PRODUCT_LINE':'PDG_PRODUCT_LINE'},inplace=True,)

#get 1st df
df_1= top_3_prod_line[top_3_prod_line['order_row']==1]
df_1.rename(columns={'PDG_PRODUCT_LINE':'PDG1_PRODUCT_LINE'},inplace=True,)
df_1=df_1.drop(['NO_ISBNS','order_row'], axis= 1)
#get 2nd df
df_2= top_3_prod_line[top_3_prod_line['order_row']==2]
df_2.rename(columns={'PDG_PRODUCT_LINE':'PDG2_PRODUCT_LINE'},inplace=True,)
df_2= df_2.drop(['NO_ISBNS','order_row'], axis= 1)

#get 3rd df
df_3= top_3_prod_line[top_3_prod_line['order_row']==3]
df_3.rename(columns={'PDG_PRODUCT_LINE':'PDG3_PRODUCT_LINE'},inplace=True,)
df_3= df_3.drop(['NO_ISBNS','order_row'], axis= 1)

#merge as separate columns
f1= df1.merge(df_1, on=['SC_LOB','SC_LOR'], how='left')
f2= f1.merge(df_2, on=['SC_LOB','SC_LOR'], how='left')
f3= f2.merge(df_3, on=['SC_LOB','SC_LOR'], how='left')

#add PDF suggestion
f3.loc[~f3['PDG1_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1']),'PDG_SUGGESTION']= f3['PDG1_PRODUCT_LINE']
f3.loc[(f3['PDG1_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])) & (~f3['PDG2_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])),'PDG_SUGGESTION']= f3['PDG2_PRODUCT_LINE']
f3.loc[(f3['PDG1_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])) & (f3['PDG2_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])) & (~f3['PDG3_PRODUCT_LINE'].isin(['AM','I','4','D','W','C1'])),'PDG_SUGGESTION']= f3['PDG3_PRODUCT_LINE']
f3.loc[f3['PREDICTED_PRODUCT_LINE']!= 'NEED REVIEW','PDG_SUGGESTION']= f3['PREDICTED_PRODUCT_LINE']

f3.rename(columns={'PRODUCT_LINE':'ISBN_LEVEL_PRODUCT_LINE'},inplace=True,)
f3= f3.drop(['PDG1_PRODUCT_LINE','PDG2_PRODUCT_LINE','PDG3_PRODUCT_LINE'], axis= 1)


print(f3.head())
f3.to_csv('C:/Users/mfernando/OneDrive - Wiley/Documents/product line- LOB,LOR/reports/new/Product_lines_with_different_LOR_ALL_08-08-2024.csv', index= False)

print('...............done................')
exit()
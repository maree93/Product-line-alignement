import pandas as pd
import numpy as np
#read sql
data1= pd.read_csv('C:/Users/mfernando/OneDrive - Wiley/Documents/product line- LOB,LOR/data/product_line_all.csv')

data1= data1[data1['SC_LOR'].isin(['Advanced Business','Advanced Math','Accounting','Business & Finance Foundations',
                                'Computer Science','Data Science','Engineering Foundations','IT','Mathematics'])]

#read sales data
sales= pd.read_excel('C:/Users/mfernando/OneDrive - Wiley/Documents/product line- LOB,LOR/data/net_sales.xlsx')
#join with sales data
data= data1.merge(sales, on=['ISBN10'], how='left')
data["NET_SALES"].fillna(0, inplace = True)
data["ABS_NET_SALES"]= abs(data["NET_SALES"])
#remove exclusions
data= data[data["ABS_NET_SALES"]> 100]

# data= data[data['PROJECT_ID'].isin(data_proj_list)]
# data.dropna(subset = ['PROJECT_ID'], inplace=True)
#add a new column as predicted_pl
data.loc[(data['SC_LOB']=='Advanced Content') & (data['SC_LOR']=='Advanced Business'),'PREDICTED_PRODUCT_LINE']= 'AM'
data.loc[(data['SC_LOB']=='Advanced Content') & (data['SC_LOR']=='Advanced Math'),'PREDICTED_PRODUCT_LINE']= 'I'
data.loc[(data['SC_LOB']=='Courseware') & (data['SC_LOR']=='Accounting'),'PREDICTED_PRODUCT_LINE']= '4'
data.loc[(data['SC_LOB']=='Courseware') & (data['SC_LOR']=='Business & Finance Foundations'),'PREDICTED_PRODUCT_LINE']= 'D'
data.loc[(data['SC_LOB']=='Courseware') & (data['SC_LOR']=='Computer Science'),'PREDICTED_PRODUCT_LINE']= 'W'
data.loc[(data['SC_LOB']=='Courseware') & (data['SC_LOR']=='Data Science'),'PREDICTED_PRODUCT_LINE']= 'W'
data.loc[(data['SC_LOB']=='Courseware') & (data['SC_LOR']=='Engineering Foundations'),'PREDICTED_PRODUCT_LINE']= 'W'
data.loc[(data['SC_LOB']=='Courseware') & (data['SC_LOR']=='IT'),'PREDICTED_PRODUCT_LINE']= 'W'
data.loc[(data['SC_LOB']=='Courseware') & (data['SC_LOR']=='Mathematics'),'PREDICTED_PRODUCT_LINE']= 'C1'

data.loc[(data['PRODUCT_LINE']== data['PREDICTED_PRODUCT_LINE']),'Required Change ISBN level']= 'No'
data.loc[(data['PRODUCT_LINE']!= data['PREDICTED_PRODUCT_LINE']),'Required Change ISBN level']= 'Yes'

data.loc[(data['PROJ_LEVEL_PRODUCT_LINE']== data['PREDICTED_PRODUCT_LINE']),'Required Change PROJ level']= 'No'
data.loc[(data['PROJ_LEVEL_PRODUCT_LINE']!= data['PREDICTED_PRODUCT_LINE']),'Required Change PROJ level']= 'Yes'

#consistent in project level?
data.loc[data['PRODUCT_LINE']==data['PROJ_LEVEL_PRODUCT_LINE'],'PROJECT_LEVEL_CONSISTENT']= 'YES'
data.loc[data['PRODUCT_LINE']!=data['PROJ_LEVEL_PRODUCT_LINE'],'PROJECT_LEVEL_CONSISTENT']= 'NO'

#Add 2 columns like additional operation
reg_pl= pd.read_excel('C:/Users/mfernando/OneDrive - Wiley/Documents/product line- LOB,LOR/data/productline_Origin.xlsx')
data= data.merge(reg_pl, on='PREDICTED_PRODUCT_LINE', how='left')

data.loc[data['PRODUCT_SPONSOR_B']!=data['SPONSOR_CODE'],'Additional operation-due to sponsor']= 'YES'
data.loc[data['PRODUCT_SPONSOR_B']==data['SPONSOR_CODE'],'Additional operation-due to sponsor']= 'NO'

data.loc[data['ORIGIN_PRODUCT_LINE_BELONGS_TO']!=data['ORIGINATING_LOCATION'],'Additional operation-due to region']= 'YES'
data.loc[data['ORIGIN_PRODUCT_LINE_BELONGS_TO']==data['ORIGINATING_LOCATION'],'Additional operation-due to region']= 'NO'

data.to_csv('C:/Users/mfernando/OneDrive - Wiley/Documents/product line- LOB,LOR/reports/new/Predicted_product_line_all_08-08-2024_old.csv', index= False)

print('...............done................')
exit()
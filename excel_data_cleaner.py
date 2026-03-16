import os
import pandas as pd

#folders
input_folder='input_files'
output_folder='output_files'

#go through every file in input folder
for file in os.listdir(input_folder):

    if file.endswith('.csv'):

        file_path=os.path.join(input_folder,file)

        print('\nProcessing file:',file)
        data=pd.read_csv(file_path)

#column names
        if 'Item' not in data.columns:
            data.columns=['Date','Item','Amount']

        print('\nFirst few rows:')
        print(data.head())

        print('\nMissing values in each column:')
        print(data.isnull().sum())

        negative=data[data['Amount']<0]
        print('\nNegative expenses found:')
        print(negative)

        print('\nUnique categories found:')
        print(data['Item'].unique())

#removes rows with missing values
        data=data.dropna()

#fixes inconsistent item names
        data['Item']=data['Item'].str.capitalize()

#removes negative expense
        data=data[data['Amount']>0]

        category_total=data.groupby('Item')['Amount'].sum().sort_values(ascending=False)
        print('\nTotal spending by category:')
        print(category_total)

        output_path=os.path.join(output_folder,file.replace('.csv','.xlsx'))

        with pd.ExcelWriter(output_path)as writer:
            data.to_excel(writer,sheet_name='Cleaned Data',index=False)
            category_total.to_excel(writer,sheet_name='Category Summary')
            print('Report saved:',output_path)

import pandas as pd

def cleanse_and_extract(file):
    df = pd.read_excel(file)
    
    if df.empty:
        raise ValueError("The uploaded Excel file is empty.")
    
    while df.shape[1] > 0 and df.iloc[:, 0].isnull().all():
        df = df.iloc[:, 1:]
    
    if df.empty:
        raise ValueError("The Excel file has no valid data columns.")

    df_cleaned = df.dropna(how='all').reset_index(drop=True)
    

    if df_cleaned.shape[0] < 2:
        raise ValueError("The Excel file doesn't have enough data.")

    main_title = df_cleaned.iloc[0, 0]
    
    df_cleaned.columns = df_cleaned.iloc[1]
    
    df_cleaned = df_cleaned.drop([0, 1]).reset_index(drop=True)
    
    # print(df_cleaned)
    # raise Exception('this is debug')
    
    return df_cleaned, main_title

import pandas as pd

def cleanse_and_extract(file):
    df = pd.read_excel(file)
    
    # Drop rows with all NaN values and reset index
    df_cleaned = df.dropna(how='all').reset_index(drop=True)
    
    if df_cleaned.shape[0] < 2:
        raise ValueError("The Excel file does not have enough rows to extract data properly.")
    
    # Extract the main title from the first row and first column
    main_title = df_cleaned.iloc[0, 0]
    
    # Set the second row as the header
    df_cleaned.columns = df_cleaned.iloc[1]
    
    # Drop the first two rows (main title and header) and reset index
    df_cleaned = df_cleaned.drop([0, 1]).reset_index(drop=True)
    
    return df_cleaned, main_title

import pandas as pd
import numpy as np
import random

# Generate random company title
def generate_random_title():
    companies = ['Acme', 'Global', 'Vertex', 'Nexus', 'Omega']
    return f"{random.choice(companies)}_LTD"

# Generate random mineral names with their symbols
def generate_random_minerals():
    minerals = [
        ('Gold', 'Au'), ('Silver', 'Ag'), ('Copper', 'Cu'), ('Iron', 'Fe'),
        ('Lead', 'Pb'), ('Zinc', 'Zn'), ('Nickel', 'Ni'), ('Cobalt', 'Co'),
        ('Platinum', 'Pt'), ('Aluminium', 'Al')
    ]
    return [symbol for name, symbol in random.sample(minerals, k=10)]

# Generate years range
years = list(range(2000, 2015))

# Generate random data
def generate_random_data(num_cells):
    return np.random.randint(1000, 5000001, size=num_cells).tolist()

# Create DataFrame
company_title = generate_random_title()
mineral_symbols = generate_random_minerals()
num_years = len(years)
num_minerals = len(mineral_symbols)

# Initialize DataFrame with predefined rows and columns
data = pd.DataFrame(index=[company_title, ''] + years, columns=[''] + mineral_symbols)

# Fill in the first row with the company name
data.iloc[0] = [company_title] + [''] * num_minerals

# Fill in the second row with mineral names
data.iloc[1] = [''] + mineral_symbols

# Fill in the remaining rows with years and random values
for i, year in enumerate(years):
    data.iloc[i + 2] = [year] + generate_random_data(num_minerals)

# Save to Excel

data.to_excel('output/random_data01.xlsx', index=False, engine='openpyxl')

print("sucessfully created 'random_data01.xlsx'")
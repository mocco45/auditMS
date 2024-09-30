# tasks.py
from celery import shared_task
from .models import company, minerals, mineralsYear
from .dataprocess import cleanse_and_extract

@shared_task
def process_excel(file_path):
    try:
        df_cleaned, main_title = cleanse_and_extract(file_path)
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}
    
    companie, created = company.objects.get_or_create(name=main_title)
    mineral_years = []

    for index, row in df_cleaned.iterrows():
        year = row[df_cleaned.columns[0]]
        
        for mineral_name in df_cleaned.columns[1:]:
            value = row[mineral_name]
            mineral, created = minerals.objects.get_or_create(name=mineral_name)
            mineral_years.append(mineralsYear(
                companie=companie,
                mineral=mineral,
                year=year,
                value=value
            ))

    mineralsYear.objects.bulk_create(mineral_years)
    return {'status': 'success'}

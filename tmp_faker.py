import pandas as pd
from faker import Faker
import random

def generate_persons_data(num_records):
    fake = Faker()
    Faker.seed(0)
    data = {
        'id': [i for i in range(1, num_records + 1)],
        'name': [fake.name() for _ in range(num_records)],
        'age': [random.randint(18, 70) for _ in range(num_records)],
        'nationality': [fake.country() for _ in range(num_records)]
    }
    return pd.DataFrame(data)

def generate_data_companies(num_records):
    fake = Faker()
    Faker.seed(0)
    data = {
        'companyId': [i for i in range(1, num_records + 1)],
        'companyName': [fake.company() for _ in range(num_records)],
        'employeeId': [random.randint(1, num_records) for _ in range(num_records)]
    }
    return pd.DataFrame(data)

def save_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False, sep=';')

num_records = 1000 
persons_data = generate_persons_data(num_records)
save_to_csv(persons_data, 'data/persons.csv')
company_data = generate_data_companies(num_records)
save_to_csv(company_data, 'data/companies.csv')

print(f"Generated {num_records} records and saved to 'persons.csv' and 'companies.csv'.")

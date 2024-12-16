import csv
import random
import faker

fake = faker.Faker()
unique_emails = set()

with open('import_test_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Email', 'First Name', 'Last Name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    while len(unique_emails) < 5:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@test.com"
        if email not in unique_emails:
            unique_emails.add(email)
            writer.writerow({'Email': email, 'First Name': first_name, 'Last Name': last_name})
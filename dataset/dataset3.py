import csv
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# List of random university names and corresponding cities in the USA
us_universities = [
    ("Harvard University", "Cambridge"),
    ("Massachusetts Institute of Technology (MIT)", "Cambridge"),
    ("Stanford University", "Stanford"),
    ("Yale University", "New Haven"),
    ("Princeton University", "Princeton"),
    ("California Institute of Technology (Caltech)", "Pasadena"),
    ("Columbia University", "New York"),
    ("University of Chicago", "Chicago"),
    ("University of Pennsylvania (UPenn)", "Philadelphia"),
    ("Johns Hopkins University", "Baltimore"),
    ("Northwestern University", "Evanston"),
    ("Duke University", "Durham"),
    ("University of California, Berkeley (UC Berkeley)", "Berkeley"),
    ("University of California, Los Angeles (UCLA)", "Los Angeles"),
    ("University of Michigan, Ann Arbor", "Ann Arbor"),
    ("University of Texas at Austin", "Austin"),
    ("Cornell University", "Ithaca"),
    ("University of Washington", "Seattle"),
    ("New York University (NYU)", "New York"),
    ("University of Southern California (USC)", "Los Angeles"),
    ("Brown University", "Providence"),
    ("Rice University", "Houston"),
    ("Vanderbilt University", "Nashville"),
    ("Emory University", "Atlanta"),
    ("Washington University in St. Louis", "St. Louis"),
    ("Georgetown University", "Washington, D.C."),
    ("University of Notre Dame", "Notre Dame"),
    ("University of Virginia", "Charlottesville"),
    ("University of California, San Diego (UCSD)", "San Diego"),
    ("University of Wisconsin-Madison", "Madison"),
    ("University of Illinois at Urbana-Champaign", "Urbana and Champaign"),
    ("Carnegie Mellon University", "Pittsburgh"),
    ("University of North Carolina at Chapel Hill (UNC Chapel Hill)", "Chapel Hill"),
    ("Boston University", "Boston"),
    ("University of Florida", "Gainesville"),
    ("University of Miami", "Coral Gables"),
    ("University of Georgia", "Athens"),
    ("University of Maryland, College Park", "College Park"),
    ("University of Arizona", "Tucson"),
    ("Ohio State University", "Columbus"),
    ("San Jose State University", "San Jose")
]

# List of unique priorities
priorities = ['Priority 1', 'Priority 2', 'Priority 3', 'Priority 4']

def generate_data(n):
    data = []
    email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com']
    start_date = datetime.strptime("10/28/2023 16:57:46", "%m/%d/%Y %H:%M:%S")
    end_date = datetime.now()

    for _ in range(n):
        timestamp = fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%m/%d/%Y %H:%M:%S')
        first_name = fake.first_name()
        last_name = fake.last_name()
        email_prefix = f"{first_name.lower()}.{last_name.lower()}"
        
        # Bias towards 'gmail.com'
        email_domain = 'gmail.com' if random.random() > 0.2 else random.choice(email_domains)
        
        email = f"{email_prefix}@{email_domain}"
        name = f"{first_name} {last_name}"

        gender = random.choice(['Male', 'Female'])
        age = fake.random_int(min=18, max=30)

        # Introduce some missing values
        university, city = random.choice(us_universities) if random.random() > 0.1 else (None, None)

        monthly_budget = fake.random_int(min=500, max=1500) if random.random() > 0.1 else None
        rent = fake.random_int(min=350, max=1000) if random.random() > 0.1 else None
        grocery = fake.random_int(min=20, max=100) if random.random() > 0.1 else None
        transportation = fake.random_int(min=0, max=120) if random.random() > 0.1 else None
        personal = fake.random_int(min=0, max=200) if random.random() > 0.1 else None
        misc = fake.random_int(min=20, max=100) if random.random() > 0.1 else None
        ef_knowledge = random.choice(['Yes', 'No']) if random.random() > 0.1 else None

        # Ensure unique priorities for each record
        unique_priorities = random.sample(priorities, len(priorities))
        subway, starbucks, tacobell, walmart = unique_priorities

        # Ensure 'Wage_per_hour' is between 10 and 20
        wage_per_hour = fake.random_int(min=10, max=20)

        # Ensure 'target_saving' is above 200 and less than 'monthly_budget'
        if monthly_budget is not None:
            target_saving = fake.random_int(min=201, max=monthly_budget-1, step=5) if random.random() > 0.1 else None
        else:
            target_saving = None

        tuition_fees_due_date = (datetime.now() + timedelta(days=fake.random_int(min=1, max=30))).strftime('%m/%d/%Y') if random.random() > 0.1 else None
        insurance_due_date = (datetime.now() + timedelta(days=fake.random_int(min=1, max=30))).strftime('%m/%d/%Y') if random.random() > 0.1 else None

        contact_method = random.choice(['Email', 'SMS text']) if random.random() > 0.1 else None

        row = [timestamp, email, name, gender, age, university, city, monthly_budget, rent, grocery, transportation, personal,
               misc, ef_knowledge, target_saving, wage_per_hour, tuition_fees_due_date, insurance_due_date,
               subway, starbucks, tacobell, walmart, contact_method]

        # Check for null values in university, city, name, email, timestamp, gender, age, and priority
        if None not in [university, city, name, email, timestamp, gender, age, subway, starbucks, tacobell, walmart]:
            data.append(row)

    return data








def write_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Email", "Name", "Gender", "Age", "University", "City", "monthly_budget", "rent",
                         "grocery", "transportation", "personal", "misc", "ef_knowledge", "target_saving", "wage_per_hour",
                         "tuition_fees_due_date", "insurance_due_date", "subway", "starbucks", "tacobell", "walmart", "Contact_Method"])
        writer.writerows(data)

if __name__ == "__main__":
    num_records = 5000
    generated_data = generate_data(num_records)
    write_to_csv(generated_data, 'new_datset.csv')

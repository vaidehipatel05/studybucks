import psycopg2
from decimal import Decimal

def fetch_user_data(user_id):
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        database="studybucks",
        user="vaidehipatel",
        password="root"
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Fetch user details, budget, total expense, and discounts
    query = """
    SELECT u.user_id, u.name_stud, u.email, u.university, u.city, u.age, u.gender,
       b.budget_id, b.monthly_budget, b.target_saving,
       COALESCE(SUM(e.grocery), 0) AS grocery_expense,
       COALESCE(SUM(e.rent), 0) AS rent_expense,
       COALESCE(SUM(e.personal), 0) AS personal_expense,
       COALESCE(SUM(e.transportation), 0) AS transportation_expense,
       COALESCE(SUM(e.misc), 0) AS misc_expense,
       b.monthly_budget - COALESCE(SUM(e.grocery + e.rent + e.personal + e.transportation + e.misc), 0) AS total_saving,
       d.walmart_discount, d.subway_discount, d.starbucks_discount, d.tacobell_discount,
       lsd.subway AS subway_deal,
       lsd.starbucks AS starbucks_deal,
       lsd.tacobell AS tacobell_deal,
       lsd.walmart AS walmart_deal
FROM "User" u
LEFT JOIN "budget" b ON u.user_id = b.user_id
LEFT JOIN "expense" e ON u.user_id = e.user_id
LEFT JOIN final_discounts d ON true
LEFT JOIN "Local Student Deals" lsd ON u.user_id = lsd.user_id
WHERE u.user_id = %s
GROUP BY u.user_id, u.name_stud, u.email, u.university, u.city, u.age, u.gender,
         b.budget_id, b.monthly_budget, b.target_saving,
         d.walmart_discount, d.subway_discount, d.starbucks_discount, d.tacobell_discount,
         lsd.subway, lsd.starbucks, lsd.tacobell, lsd.walmart;

    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return result




def apply_discounts(grocery, personal, misc, walmart_discount, subway_discount, starbucks_discount, tacobell_discount,subway_deal,starbucks_deal,tacobell_deal):
    # Convert discount percentages to Decimal
    walmart_discount = Decimal(str(walmart_discount))
    subway_discount = Decimal(str(subway_discount))
    starbucks_discount = Decimal(str(starbucks_discount))
    tacobell_discount = Decimal(str(tacobell_discount))

    # Convert expense values to Decimal
    grocery = Decimal(str(grocery))
    personal = Decimal(str(personal))
    misc = Decimal(str(misc))

    # Apply Walmart discount to grocery and misc expenses
    grocery_discounted = grocery * (1 - walmart_discount / 100)
    misc_discounted = misc * (1 - walmart_discount / 100)

    # Determine the highest priority deal among subway, starbucks, and tacobell
    deal_priorities = {
        'subway': subway_deal,
        'tacobell': tacobell_deal,
        'starbucks': starbucks_deal
    }

    # Find the deal with the highest priority
    highest_priority_deal = max(deal_priorities, key=deal_priorities.get)

    # Now you have the highest priority deal, you can apply the corresponding discount to personal expense
    if highest_priority_deal == 'subway':
        personal_discounted = personal * (1 - subway_discount / 100)
    elif highest_priority_deal == 'starbucks':
        personal_discounted = personal * (1 - starbucks_discount / 100)
    elif highest_priority_deal == 'tacobell':
        personal_discounted = personal * (1 - tacobell_discount / 100)
    else:
        personal_discounted = personal  # No discount if no deal is found


    # Calculate total expense after discounts
    total_expense_discounted = grocery_discounted + personal_discounted + misc_discounted  
    """print("grocery_discounted", grocery_discounted)
    print("misc_discounted", misc_discounted)
    print("personal_discounted",personal_discounted)
"""
    return total_expense_discounted


user_id_to_fetch = 8808
result = fetch_user_data(user_id_to_fetch)

# Extract relevant information
user_id, name_stud, email, university, city, age, gender, budget_id, monthly_budget, target_saving, grocery_expense, rent_expense, personal_expense, transportation_expense, misc_expense, total_saving, walmart_discount, subway_discount, starbucks_discount, tacobell_discount, subway_deal, starbucks_deal, tacobell_deal, walmart_deal = result


# Apply discounts to individual expenses and calculate new total expense and total savings
total_expense_discounted = apply_discounts(grocery_expense, personal_expense, misc_expense, walmart_discount, subway_discount, starbucks_discount, tacobell_discount,subway_deal,starbucks_deal, tacobell_deal)

total_expense_discounted = total_expense_discounted + rent_expense + transportation_expense

# Example: Displaying personalized details after applying discounts
#print(f"User ID: {user_id}")
print(f"Name: {name_stud}")
print(f"Email: {email}")
print(f"University: {university}")
print(f"City: {city}")
print(f"Age: {age}")
print(f"Gender: {gender}")
#print(f"Budget ID: {budget_id}")
print(f"Monthly Budget: ${monthly_budget}")
print(f"Target Saving: ${target_saving}")
"""print(f"Grocery Expense: ${grocery_expense}")
print(f"Rent Expense: ${rent_expense}")
print(f"Personal Expense: ${personal_expense}")
print(f"Transportation Expense: ${transportation_expense}")
print(f"Misc Expense: ${misc_expense}")"""
print(f"Total Expense before discounts: ${grocery_expense + rent_expense + personal_expense + transportation_expense + misc_expense}")
print(f"Total Savings before discounts: ${total_saving}")
"""print(f"Walmart Discount: {walmart_discount}% off")
print(f"Subway Discount: {subway_discount}% off")
print(f"Starbucks Discount: {starbucks_discount}% off")
print(f"Taco Bell Discount: {tacobell_discount}% off")
print("subway_deal", subway_deal)
print("tacobell_deal", tacobell_deal)
print("starbucks_deal", starbucks_deal)"""

print(f"\nTotal Expense after discounts: ${total_expense_discounted}")
print(f"Total Savings after discounts: ${monthly_budget - total_expense_discounted}")

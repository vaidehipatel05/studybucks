import matplotlib
matplotlib.use('Agg')
import os
from flask import Flask, render_template, request
import psycopg2
from decimal import Decimal
from flask import Flask, render_template, request
import psycopg2
from decimal import Decimal
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.express as px
from plotly.io import to_html

app = Flask(__name__)

def fetch_user_data(user_id):
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        database="studybucks",
        user="root",
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

import psycopg2

def get_due_dates(user_id):
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        database="studybucks",
        user="vaidehipatel",
        password="root"
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Fetch tuition and insurance due dates from "Academic Calendar Events" table
    query = """
    SELECT tuition_fees_due_date, insurance_due_date
    FROM "Academic Calendar Event"
    WHERE user_id = %s;
    """

    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Check if the result is not None before extracting values
    if result:
        tuition_fees_due_date, insurance_due_date = result
    else:
        tuition_fees_due_date, insurance_due_date = 'N/A', 'N/A'

    return tuition_fees_due_date, insurance_due_date


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
    return total_expense_discounted, grocery_discounted, personal_discounted, misc_discounted


def plot_expenses(grocery_expense, rent_expense, personal_expense, transportation_expense, misc_expense, total_expense_before_discounts, total_expense_after_discounts, grocery_discounted, personal_discounted, misc_discounted):
    categories = ['Grocery', 'Rent', 'Personal', 'Transportation', 'Misc']
    expenses_before_discounts = [grocery_expense, rent_expense, personal_expense, transportation_expense, misc_expense]
    expenses_after_discounts = [grocery_discounted, rent_expense, personal_discounted, transportation_expense, misc_discounted]

    fig, ax = plt.subplots()
    bar_width = 0.35
    bar1 = ax.bar(categories, expenses_before_discounts, bar_width, label='Before Discounts')
    bar2 = ax.bar(categories, expenses_after_discounts, bar_width, label='After Discounts', bottom=expenses_before_discounts)

    ax.set_ylabel('Expense ($)')
    ax.set_title('Expenses Before and After Discounts')
    ax.legend()

    static_path = os.path.join(app.root_path, 'static')
    chart_filename = 'expenses_chart.png'
    chart_filepath = os.path.join(static_path, chart_filename)

    plt.savefig(chart_filepath, format='png')
    plt.close()

    return chart_filename

def plot_expenses_chart(grocery_expense, rent_expense, personal_expense, transportation_expense, misc_expense,
                        total_expense_before_discounts, total_expense_after_discounts, grocery_discounted,
                        personal_discounted, misc_discounted):
    categories = ['Grocery', 'Rent', 'Personal', 'Transportation', 'Miscellaneous']
    labels = ['Expenses Before Discounts', 'Expenses After Discounts']

    values_before_discounts = [grocery_expense, rent_expense, personal_expense, transportation_expense, misc_expense]
    values_after_discounts = [grocery_discounted, rent_expense, personal_discounted, transportation_expense, misc_discounted]

    data = {
        'Categories': categories * 2,  # Repeat each category for both before and after discounts
        'Expenses': values_before_discounts + values_after_discounts,
        'Label': labels * len(categories)  # Repeat labels for each category
    }

    fig = px.bar(data, x='Categories', y='Expenses', color='Label',
                 title='Grouped Bar Chart of Expenses', barmode='group')

    # Convert the Plotly chart to HTML
    chart_html = to_html(fig, full_html=False)

    return chart_html

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id_to_fetch = request.form['user_id']
        result = fetch_user_data(user_id_to_fetch)

        if result:
            user_id, name_stud, email, university, city, age, gender, budget_id, monthly_budget, target_saving, grocery_expense, rent_expense, personal_expense, transportation_expense, misc_expense, total_saving, walmart_discount, subway_discount, starbucks_discount, tacobell_discount, subway_deal, starbucks_deal, tacobell_deal, walmart_deal = result

            total_expense_discounted,grocery_discounted, personal_discounted, misc_discounted = apply_discounts(
                grocery_expense, personal_expense, misc_expense,
                walmart_discount, subway_discount, starbucks_discount, tacobell_discount,
                subway_deal, starbucks_deal, tacobell_deal
            )

            total_expense_discounted = total_expense_discounted + rent_expense + transportation_expense
            total_expense_before_discounts=grocery_expense + rent_expense + personal_expense + transportation_expense + misc_expense
            total_expense_after_discounts=total_expense_discounted
            chart_image = plot_expenses(grocery_expense, rent_expense, personal_expense, transportation_expense, misc_expense, total_expense_before_discounts, total_expense_after_discounts, grocery_discounted, personal_discounted, misc_discounted)

            chart_html = plot_expenses_chart(grocery_expense, rent_expense, personal_expense,
                                      transportation_expense, misc_expense,
                                      total_expense_before_discounts,
                                      total_expense_after_discounts, grocery_discounted,
                                      personal_discounted, misc_discounted)

            tuition_fees_due_date, insurance_due_date = get_due_dates(user_id_to_fetch)

            return render_template('result_combine1.html', user_id=user_id, name_stud=name_stud, email=email,
                                   university=university, city=city, age=age, gender=gender,
                                   monthly_budget=monthly_budget, target_saving=target_saving,
                                   total_expense_before_discounts=total_expense_before_discounts,
                                   total_saving_before_discounts=total_saving,
                                   total_expense_after_discounts=total_expense_discounted,
                                   total_saving_after_discounts=monthly_budget - total_expense_discounted,
                                   chart_html=chart_html,
                                   tuition_fees_due_date=tuition_fees_due_date, insurance_due_date=insurance_due_date)
        else:
            return render_template('error.html', message="User not found. Please enter a valid user ID.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

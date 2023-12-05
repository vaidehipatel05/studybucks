# studybucks
For college and university students to successfully navigate the complexities of student life, they must learn effective money management techniques. To address the financial challenges this demographic encounters, we provide ’StudyBucks,’ an innovative money management and budgeting tool designed with students in mind. StudyBucks provides a comprehensive suite of tools for tracking spending, making budgets, and gaining insight into students’ spending habits, giving them the financial management tools, they need. StudyBucks offers personalized solutions for both financial and academic achievement, going beyond traditional budgeting tools. Offering local student discounts and deals, integrating with the academic calendar, offering emergency fund building, and integrating parttime job income integration are few examples of innovative features. The best tool for tracking daily spending, creating a college budget, or making plans is StudyBucks.

Tables
1. User:
   - Attributes: 
     - `user_id` (Primary Key)
     - `Name`
     - `email`
     - `University’
     - `City`
     - `Age`
     - ‘Gender’

2. Expense:
   - Attributes:
     - `expense_id` (Primary Key)
     - `user_id` (Foreign Key to User)
     - `grocery`
     - `rent`
     - `personal`
     - `transportation`
     - ‘Misc’
    - ‘Total expense’
    - 
3. Budget:
   - Attributes:
     - `budget_id` (Primary Key)
     - `user_id` (Foreign Key to User)
     - `monthly_budget`
     - ‘target_saving’
     -  total_saving

4. Emergency Fund:
   - Attributes:
     - `emergency_fund_id` (Primary Key)
     - `user_id` (Foreign Key to User)
     - `EF_amount`
     - `EF_knowledge`

5. Academic Calendar Event:
   - Attributes:
     - `event_id` (Primary Key)
     - `user_id` (Foreign Key to User)
     - `Tuition_fees_due_date`
     - `Insurance_due_date`

6. Local Student Deals:
   - Attributes:
     - `deal_id` (Primary Key)
     - `user_id` (Foreign Key to User)
     - `subway`
     - `starbucks`
     - `tacobell`
     - `walmart`

7. User Preferences:
   - Attributes:
     - `preferences_id` (Primary Key)
     - `user_id` (Foreign Key to User)
     - `notification_preferences`

8. Part time
   -Attributes:
     - ‘User_id’ (foreign Key)
     - ‘Wage_per_hour’
     - ‘Total’




-------------

1. Flask and python code:

create a new folder named 'templates'
Under this folder, upload all html files
index.html
error.html
result*.html

Main file is app.py, on cmd run python app.py
you will see output similar to

Project % python3 app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!

Go to link http://127.0.0.1:5000 and you will see the project.

2. To see analysis on geograph, run code geo.py
   It will generate heatmap ("student_concentration_heatmap.html") and save on local machine.

3. localdeals_final.py
   (check local_discount.txt file for more details)

import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from expense_tracker.models import Budget, CategoryColors, Expense
from . import app, db
from .functions import AuthenticateUser, CreateBudget, CreateExpense, CreateUser, GetBudgets, GetProfileDetails, HashPassword, SearchExpense
from .validations import ValidateEmail, ValidatePassword, ValidateUsername

# expenses is the handler for the expenses page
@app.route("/", methods=["GET", "POST"])
@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():    
    expense_list = []
    labels = []
    values = []
    colors = []

    expenses = Expense.query.filter_by(user=current_user.id).all()
    for expense in expenses:
        color_row = CategoryColors.query.filter_by(category=expense.category, user=current_user.id).first()
        expense_dict = {
            "id": expense.id,
            "name": expense.name,
            "category": expense.category,
            "color": color_row.color,
            "amount": expense.amount,
            "time": expense.time.strftime("%H:%M"),
            "date": expense.date,
            "user": expense.user,
        }

        expense_list.append(expense_dict)

    expense_list = expense_list[::-1]

    category_list = []
    categories = db.session.query(Expense.category).filter_by(user=current_user.id).distinct().all()
    
    for category in categories:
        category_row = Expense.query.filter_by(category=category[0], user=current_user.id).all()
        total_amount = 0
        for each in category_row:
            total_amount += each.amount
        category_dict = {
            "category": category[0],
            "amount": total_amount,
        }
        labels.append(category[0])
        values.append(total_amount)
        color_row = CategoryColors.query.filter_by(category=category[0], user=current_user.id).first()
        colors.append(color_row.color)
        category_list.append(category_dict)
    
    if request.method == "POST":
        if "addExpense" in request.form:
            name = request.form.get("expenseName")
            category = request.form.get("expenseCategory").upper()
            amount = int(request.form.get("expenseAmount"))
            color = request.form.get("expenseColor")
            time = datetime.datetime.now()
            date = datetime.datetime.now().strftime("%d %b %Y")
            user = current_user.id

            msg, category = CreateExpense(name, category, color, time, date, amount, user)

            flash(message=msg, category=category)

            return redirect(url_for('expenses'))
        elif "deleteExpenseID" in request.form:
            id = request.form.get("deleteExpenseID")
            to_delete = Expense.query.filter_by(id=id).first()

            db.session.delete(to_delete)
            db.session.commit()

            flash(message="Expense has been deleted.", category="info")

            return redirect(url_for('expenses'))
        
        elif "searchExpense" in request.form:
            query = str(request.form.get("search-expense"))
            length, results = SearchExpense(query, current_user.id)

            if length == 0:
                flash(message="No results found", category="info")

            return render_template("expenses.html", expenses=expense_list, categories=category_list, labels=labels, values=values, colors=colors, length=length, results=results)

    return render_template("expenses.html", expenses=expense_list, categories=category_list, labels=labels, values=values, colors=colors)

@app.route("/expenses-table", methods=["GET", "POST"])
def expenses_table():
    expense_list = []
    labels = []
    values = []
    colors = []

    expenses = Expense.query.filter_by(user=current_user.id).all()
    for expense in expenses:
        color_row = CategoryColors.query.filter_by(category=expense.category, user=current_user.id).first()
        expense_dict = {
            "id": expense.id,
            "name": expense.name,
            "category": expense.category,            
            "color": color_row.color,
            "amount": expense.amount,
            "time": expense.time.strftime("%H:%M"),
            "date": expense.date,
            "user": expense.user,
        }

        expense_list.append(expense_dict)

    expense_list = expense_list[::-1]

    category_list = []
    categories = db.session.query(Expense.category).filter_by(user=current_user.id).distinct().all()
    
    for category in categories:
        category_row = Expense.query.filter_by(category=category[0], user=current_user.id).all()
        total_amount = 0
        for each in category_row:
            total_amount += each.amount
        category_dict = {
            "category": category[0],
            "amount": total_amount,
        }
        color_row = CategoryColors.query.filter_by(category=category[0], user=current_user.id).first()
        colors.append(color_row.color)
        labels.append(category[0])
        values.append(total_amount)        
        category_list.append(category_dict)
    
    if request.method == "POST":
        if "addExpense" in request.form:
            name = request.form.get("expenseName")
            category = request.form.get("expenseCategory").upper()
            color = request.form.get("expenseColor")
            amount = int(request.form.get("expenseAmount"))
            time = datetime.datetime.now()
            date = datetime.datetime.now().strftime("%d %b %Y")
            user = current_user.id

            msg, category = CreateExpense(name, category, color, time, date, amount, user)

            flash(message=msg, category=category)

            return redirect(url_for('expenses_table'))
        
        elif "deleteExpenseID" in request.form:
            id = request.form.get("deleteExpenseID")
            to_delete = Expense.query.filter_by(id=id).first()
            
            db.session.delete(to_delete)
            db.session.commit()

            flash(message="Expense has been deleted.", category="info")

            return redirect(url_for('expenses_table'))
        
        elif "searchExpense" in request.form:
            query = str(request.form.get("search-expense"))
            length, results = SearchExpense(query, current_user.id)

            if length == 0:
                flash(message="No results found", category="info")

            return render_template("expenses-table.html", expenses=expense_list, categories=category_list, labels=labels, values=values, colors=colors, length=length, results=results)

    return render_template("expenses-table.html", expenses=expense_list, categories=category_list, labels=labels, values=values, colors=colors)

@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    categories = db.session.query(Expense.category).filter_by(user=current_user.id).distinct().all()
    category_expenses_list = []
    labels_category = []
    values_category = []
    labels_date = []
    values_date = []

    # graph for expenses by category
    for category in categories:
        total_amount = 0
        category_rows = Expense.query.filter_by(category=category[0], user=current_user.id).all()
        for row in category_rows:
            total_amount += row.amount
        category_dict = {
            "category": category[0],
            "amount": total_amount,
        }
        category_expenses_list.append(category_dict)

        labels_category.append(category_dict["category"])
        values_category.append(category_dict["amount"])

    n = 10

    # graph for only expenses by date
    while n >= 0:
        day_before = datetime.date.today() - datetime.timedelta(days=n)
        day_before = day_before.strftime("%d %b %Y")
        rows = Expense.query.filter_by(date=day_before, user=current_user.id).all()
        total = 0
        for row in rows:
            total+=row.amount

        values_date.append(total)

        labels_date.append(day_before)
        
        n-=1

    if request.method == "POST":
        if "categoryName" in request.form:
            category = request.form.get("categoryName")
            expenses = Expense.query.filter_by(category=category, user=current_user.id).all()

            expenses_list = []

            if expenses:
                for expense in expenses:
                    expense_dict = {
                        "id": expense.id,
                        "name": expense.name,
                        "date": expense.date,
                        "time": datetime.datetime.strftime(expense.time, "%H:%M"),
                        "amount": expense.amount,
                        "category": expense.category,
                    }       

                    expenses_list.append(expense_dict)

                return render_template("tracker-category.html", category=category, expenses=expenses_list)
        
        elif "graphDate" in request.form:
            recieved_date = request.form.get("graphDate")
            date = datetime.datetime.strptime(recieved_date, "%Y-%m-%d")
            converted_date = date.strftime("%d %b %Y")
            search_expenses = Expense.query.filter_by(user=current_user.id, date=converted_date).all()          

            search_expenses_list = []

            for expense in search_expenses:
                search_expense_dict = {
                    "id": expense.id,
                    "name": expense.name,
                    "category": expense.category,
                    "time": datetime.datetime.strftime(expense.time, "%H:%M"),
                    "date": expense.date,
                    "amount": expense.amount,
                    "user": expense.user,
                }

                search_expenses_list.append(search_expense_dict)
            
            length = len(search_expenses_list)
            if length == 0:
                flash(message=f"No expenses found on {converted_date}", category="info")

            return render_template("tracker.html", category_expenses=category_expenses_list, labels_category=labels_category, values_category=values_category, labels_date=labels_date, values_date=values_date, search_expenses=search_expenses_list, length_search=length, date=converted_date, recieved_date=recieved_date)

        elif "dateRangeOne" in request.form:
            dateOne = request.form.get("dateRangeOne")
            dateTwo = request.form.get("dateRangeTwo")

            dateOneConverted = datetime.datetime.strptime(dateOne, "%Y-%m-%d")
            dateTwoConverted = datetime.datetime.strptime(dateTwo, "%Y-%m-%d")

            query = db.session.query(Expense).filter((Expense.time < dateTwoConverted) & (Expense.time > dateOneConverted)).all()
            query_list = []
            for each in query:
                dict = {
                    "id": each.id,
                    "name": each.name,
                    "category": each.category,
                    "amount": each.amount,
                    "time": each.time.strftime("%H:%M"),
                    "date": each.date,
                    "user": each.user,
                }

                query_list.append(dict)

            length = len(query_list)

            if length > 0:
                return render_template("tracker.html", category_expenses=category_expenses_list, labels_category=labels_category, values_category=values_category, labels_date=labels_date, values_date=values_date, dateranges=query_list, daterange_length=length)
            else:
                flash(message=f"No results for expenses between {dateOne} and {dateTwo}", category="info")

    return render_template("tracker.html", category_expenses=category_expenses_list, labels_category=labels_category, values_category=values_category, labels_date=labels_date, values_date=values_date)

@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    if request.method == "POST":
        if "defineBudget" in request.form:
            category = request.form.get("budgetCategory")
            amount = request.form.get("budgetAmount")
            user = current_user.id

            msg = CreateBudget(category, amount, user)

            flash(message=msg, category="info")

            return redirect(url_for('budget'))
        
    budgets, labels, expense_values, budget_values, total_expense, total_budget, total_difference = GetBudgets(current_user.id)

    return render_template("budget.html", budgets=budgets, labels=labels, expense_values=expense_values, budget_values=budget_values, total_expense=total_expense, total_budget=total_budget, total_difference=total_difference)

@app.route("/profile")
def profile():
    user_details = GetProfileDetails(current_user.id)
    return render_template("profile.html", user=user_details)

# login is the handler for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "loginForm" in request.form:
            username = request.form.get("username")
            pwd = request.form.get("pwd")

            user = AuthenticateUser(username, pwd)
            
            if user != False:
                login_user(user)
                flash(message="You have been logged in successfully!", category="success")
                return redirect(url_for('expenses'))
            else:
                flash(message="Invalid credentials", category="danger")

    return render_template("login.html")

# register is the handler for the register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if "registerForm" in request.form:
            username = request.form.get("username")
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            pwd_confirm = request.form.get("pwd-confirm")

            username_validation =  ValidateUsername(username)
            email_validation = ValidateEmail(email)
            pwd_validation = ValidatePassword(pwd, pwd_confirm)

            results = [username_validation, email_validation, pwd_validation]

            if results[0] == True and results[1] == True and results[2] == True:
                hash_pwd = HashPassword(pwd)
                msg, category = CreateUser(username, email, hash_pwd)

                flash(message=msg, category=category)
                return redirect(url_for('expenses'))
            else:
                for result in results:
                    if result != True:
                        flash(f"{result}", category="danger")
                    else:
                        print(result)

    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    flash(message="You have been logged out", category="info")
    return redirect(url_for('login'))
    
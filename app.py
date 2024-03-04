from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

# hardcoded as of now, will connect flask to mysql
expenses = [
    {"id": 1, "description": "Groceries", "amount": 60.5, "date": "2024-03-01", "category": "Food"},
    {"id": 2, "description": "Internet", "amount": 30.0, "date": "2024-03-02", "category": "Utilities"},
    {"id": 3, "description": "Rent", "amount": 1200, "date": "2024-03-03", "category": "Housing"}
]

@app.route("/")
def home():
    total_expense = sum(expense["amount"] for expense in expenses)
    return render_template("index.html", expenses=expenses, total_expense=total_expense)

@app.route("/add", methods=["POST"])
def add():
    # New id for every expense that arises
    new_id = max(expense["id"] for expense in expenses) + 1 if expenses else 1
    new_expense = {
        "id": new_id,
        "description": request.form["description"],
        "amount": float(request.form["amount"]),
        "date": request.form["date"],
        "category": request.form["category"]
    }
    expenses.append(new_expense)
    return redirect(url_for("home"))

@app.route("/update/<int:expense_id>", methods=["POST"])
def update(expense_id):
    for expense in expenses:
        if expense["id"] == expense_id:
            expense["description"] = request.form.get("description", expense["description"])
            expense["amount"] = float(request.form.get("amount", expense["amount"]))
            expense["date"] = request.form.get("date", expense["date"])
            expense["category"] = request.form.get("category", expense["category"])
            break
    return redirect(url_for("home"))

@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    global expenses
    expenses = [expense for expense in expenses if expense["id"] != expense_id]
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

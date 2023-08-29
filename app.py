# Import libraries
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template('transactions.html', transactions = transactions)

# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(transaction)

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Render the form template to display the add transaction form
    return render_template("form.html")

# Update operation
@app.route("/edit/<int:transaction_id>", methods = ["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])

        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = date
                transaction["amount"] = amount
                break
        
        return redirect(url_for("get_transactions"))

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction = transaction)

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

@app.route("/search", methods = ["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        max = float(request.form["max_amount"])
        min = float(request.form["min_amount"])
        filtered_transactions = []

        for transaction in transactions:
            if transaction["amount"] >= min and transaction["amount"] <= max:
                filtered_transactions.append(transaction)
    
        return render_template("transactions.html", transactions = filtered_transactions)

    return render_template("search.html")

@app.route("/balance")
def total_balance():
    total_amount = 0
    for transaction in transactions:
        total_amount = total_amount + transaction["amount"]
    return "Total Balance: {total_amount}"


# Run the Flask app
if __name__ == "__main__":
    app.run(debug = True)
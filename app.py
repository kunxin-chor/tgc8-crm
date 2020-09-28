from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
import random

app = Flask(__name__)
app.secret_key = b'6853-6789-5905$#)(%$x-57-605h)'

database = {}
with open('customers.json') as fp:
    database = json.load(fp)


# returns the customer by a required customer_id
# if no customer with that id, return None
def find_customer_by_id(customer_id):
    for customer in database:
        if customer["id"] == customer_id:
            return customer
    return None


def save_database():
    with open('customers.json', 'w') as fp:
        json.dump(database, fp)


@app.route('/')
def home():
    return render_template('home.template.html')


@app.route('/customers')
def show_customers():
    return render_template('customers.template.html', all_customers=database)


@app.route('/customers/add')
def show_add_customer():
    return render_template('add_customer.template.html', old_values={})


@app.route('/customers/add', methods=["POST"])
def process_add_customer():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    # use a dictionary to store the error messages
    errors = {}

    # check if the first_name is provided
    if not first_name:
        errors["first_name"] = "Please provide a valid first name"

    if not last_name:
        errors["last_name"] = "Please provide a valid last name"

    if not email:
        errors["email"] = "Please provide a valid email address"

    # check if `can_send` checkbox is checked
    if 'can_send' in request.form:
        can_send = True
    else:
        can_send = False

    if len(errors) == 0:
        new_customer = {
            'id': random.randint(1000, 9999),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'can_send': can_send
        }

        database.append(new_customer)

        with open('customers.json', 'w') as fp:
            json.dump(database, fp)

        flash(
            f"The customer with the name {new_customer['first_name']}"
            f" {new_customer['last_name']} has been created successfully")
        return redirect(url_for('show_customers'))
    else:
        for key, value in errors.items():
            flash(value, "error")

        return render_template('add_customer.template.html', old_values=request.form)


@app.route('/customers/<int:customer_id>/edit')
def show_edit_customer(customer_id):
    # 1. find the customer that we are supposed to edit
    customer_to_edit = find_customer_by_id(customer_id)

    if customer_to_edit:
        return render_template('edit_customer.template.html',
                               customer=customer_to_edit)
    else:
        return f"The customer with the id of {customer_id} is not found"


@app.route('/customers/<int:customer_id>/edit', methods=["POST"])
def process_edit_customer(customer_id):
    customer_to_edit = None
    for each_customer in database:
        if each_customer["id"] == customer_id:
            customer_to_edit = each_customer
            break

    if customer_to_edit:
        customer_to_edit["first_name"] = request.form.get('first_name')
        customer_to_edit["last_name"] = request.form.get('last_name')
        customer_to_edit["email"] = request.form.get('email')

        if 'can_send' in request.form:
            print("send marketing material true")
            customer_to_edit['send_marketing_material'] = True
        else:
            print('send marketing material false')
            customer_to_edit['send_marketing_material'] = False

        with open('customers.json', 'w') as fp:
            json.dump(database, fp)

        flash(
            f"The customer {customer_to_edit['first_name']}"
            f" {customer_to_edit['last_name']} has been updated.")
        return redirect(url_for('show_customers'))
    else:
        return f"The customer with the id {customer_id} does not exist"


@app.route('/customers/<int:customer_id>/delete')
def show_delete_customer(customer_id):
    customer_to_delete = find_customer_by_id(customer_id)

    if customer_to_delete:
        return render_template('confirm_to_delete_customer.template.html',
                               customer=customer_to_delete)
    else:
        return f"The customer with the id of {customer_id} is not found"


@app.route('/customers/<int:customer_id>/delete', methods=['POST'])
def process_delete_customer(customer_id):
    customer_to_delete = find_customer_by_id(customer_id)

    if customer_to_delete:
        database.remove(customer_to_delete)
        save_database()
        return redirect(url_for('show_customers'))
    else:
        return f"The customer with the id of {customer_id} is not found"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

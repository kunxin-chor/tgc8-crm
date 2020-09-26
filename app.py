from flask import Flask, render_template, request, redirect, url_for
import os
import json
import random

app = Flask(__name__)
database = {}
with open('customers.json') as fp:
    database = json.load(fp)


@app.route('/')
def home():
    return render_template('home.template.html')


@app.route('/customers')
def show_customers():
    return render_template('customers.template.html', all_customers=database)


@app.route('/customers/add')
def show_add_customer():
    return render_template('add_customer.template.html')


@app.route('/customers/add', methods=["POST"])
def process_add_customer():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    if first_name == "" or last_name == "" or email == "":
        return redirect(url_for('show_add_customer'))

    # check if `can_send` checkbox is checked
    if 'can_send' in request.form:
        can_send = True
    else:
        can_send = False

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

    return redirect(url_for('show_customers'))


@app.route('/customers/<int:customer_id>/edit')
def show_edit_customer(customer_id):
    # 1. find the customer that we are supposed to edit
    customer_to_edit = None
    for each_customer in database:
        if each_customer["id"] == customer_id:
            customer_to_edit = each_customer
            break

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
        return redirect(url_for('show_customers'))
    else:
        return f"The customer with the id {customer_id} does not exist"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

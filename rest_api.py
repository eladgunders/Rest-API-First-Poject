import json
from flask import Flask, request, render_template
from Customer import Customer
from CustomerDataAccess import CustomerDataAccess


app = Flask(__name__)
dao = CustomerDataAccess('rest_api_first_project_db.db')


@app.route("/")
def home():
    print('hi')
    return '''
        <html>
            Ready!
        </html>
    '''


@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    if request.method == 'GET':
        customers = dao.get_all_customers()
        return json.dumps(customers)
    if request.method == 'POST':
        customer_data = request.get_json()
        inserted_customer = Customer(id_=None, name=customer_data["name"], city=customer_data["city"])
        return dao.insert_new_customer(inserted_customer)


@app.route('/customers/<int:id_>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def get_customer_by_id(id_):
    if request.method == 'GET':
        customer = dao.get_customer_by_id(id_)
        return json.dumps(customer)
    if request.method == 'PUT':
        values_dict = request.get_json()
        return dao.update_put_customer(id_, values_dict)
    if request.method == 'DELETE':
        return dao.delete_customer(id_)
    if request.method == 'PATCH':
        values_dict = request.get_json()
        return dao.update_patch_customer(id_, values_dict)


app.run()

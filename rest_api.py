from flask import Flask, request, jsonify, make_response
from Customer import Customer
from User import User
from RestDataAccess import RestDataAccess
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'I took this code from Elad Gunders'

dao = RestDataAccess('rest_api_first_project_db.db')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is not valid'}), 401

        return f(*args, **kwargs)
    return decorated


@app.route("/")
def home():
    return '''
        <html>
            Best home page!
        </html>
    '''


@app.route('/customers', methods=['GET', 'POST'])
@token_required
def get_or_post_customer():
    if request.method == 'GET':
        customers = dao.get_all_customers()
        return jsonify(customers)
    if request.method == 'POST':
        customer_data = request.get_json()
        inserted_customer = Customer(id_=None, name=customer_data["name"], city=customer_data["city"])
        answer = dao.insert_new_customer(inserted_customer)
        if answer:
            return make_response('Customer Created!', 201)
        else:
            return jsonify({'answer': 'failed'})


@app.route('/customers/<int:id_>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@token_required
def get_customer_by_id(id_):
    if request.method == 'GET':
        customer = dao.get_customer_by_id(id_)
        return jsonify(customer)
    if request.method == 'PUT':
        values_dict = request.get_json()
        answer = dao.update_put_customer(id_, values_dict)
        if answer:
            return make_response('Put done!', 201)
        else:
            return jsonify({'answer': 'failed'})
    if request.method == 'DELETE':
        answer = dao.delete_customer(id_)
        if answer:
            return make_response('Delete done!', 201)
        else:
            return jsonify({'answer': 'failed'})
    if request.method == 'PATCH':
        values_dict = request.get_json()
        answer = dao.update_patch_customer(id_, values_dict)
        if answer:
            return make_response('Patch done!', 201)
        else:
            return jsonify({'answer': 'failed'})


@app.route('/signup', methods=['POST'])
def signup():
    form_data = request.form

    username = form_data.get('username')
    password = form_data.get('password')

    user = dao.get_user_by_username(username)

    if user:
        return make_response('User already exists. Please Log in.', 202)

    else:
        inserted_user = User(id_=None, username=username, password=generate_password_hash(password))
        dao.insert_new_user(inserted_user)
        return make_response('Successfully registered.', 201)


@app.route('/login', methods=['POST'])
def login():
    form_data = request.form

    if not form_data or not form_data.get('username') or not form_data.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required."'})

    user = dao.get_user_by_username(form_data.get('username'))
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required."'})

    if not check_password_hash(user.password, form_data.get('password')):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required."'})

    token = jwt.encode({'id': user.id_, 'exp': datetime.now() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return make_response(jsonify({'token': token.decode('UTF-8')}), 201)


if __name__ == '__main__':
    app.run(debug=True)

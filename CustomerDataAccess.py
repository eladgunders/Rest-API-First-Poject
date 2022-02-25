from Customer import Customer
import sqlite3


class CustomerDataAccess:

    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
        self.con = sqlite3.connect(db_file_path, check_same_thread=False)
        self.db_cursor = self.con.cursor()

    def get_all_customers(self):
        customers_ls = []
        self.db_cursor.execute("select * from customers")
        customers = self.db_cursor.fetchall()
        for customer in customers:
            customers_ls.append(Customer(id_=customer[0], name=customer[1], city=customer[2]))
        return_ls = [customer.__dict__ for customer in customers_ls]
        print(return_ls)
        return return_ls

    def get_customer_by_id(self, id_):
        self.db_cursor.execute(f"select * from customers where id = {id_}")
        customer = self.db_cursor.fetchall()
        if customer:
            selected_customer = Customer(id_=customer[0][0], name=customer[0][1], city=customer[0][2])
            return selected_customer.__dict__
        else:
            return []

    def insert_new_customer(self, customer):
        if not isinstance(customer, Customer):
            return {'process': 'failed'}
        if not hasattr(customer, "name") or not hasattr(customer, "city"):
            return {'process': 'failed'}
        self.db_cursor.execute(f'insert into customers (name, city) values ("{customer.name}", "{customer.city}")')
        self.con.commit()
        return {'process': 'success'}

    def update_put_customer(self, id_, values_dict):
        updated_values_dict = {}
        for key, value in values_dict.items():
            if key == 'name' or key == 'city':
                updated_values_dict[key] = value
        if len(list(updated_values_dict.keys())) == 2:
            self.db_cursor.execute(f'update customers set name="{updated_values_dict["name"]}", '
                                   f'city="{updated_values_dict["city"]}" where id={id_}')
            self.con.commit()
            return {'process': 'success'}
        else:
            return {'process': 'failed'}

    def update_patch_customer(self, id_, values_dict):
        updated_values_dict = {}
        for key, value in values_dict.items():
            if key == 'name' or key == 'city':
                updated_values_dict[key] = value
        if len(list(updated_values_dict.keys())) == 2:
            self.db_cursor.execute(f'update customers set name="{updated_values_dict["name"]}", '
                                   f'city="{updated_values_dict["city"]}" where id={id_}')
            self.con.commit()
            return {'process': 'success'}
        if 'name' in updated_values_dict:
            self.db_cursor.execute(f'update customers set name="{updated_values_dict["name"]}" where id={id_}')
            self.con.commit()
            return {'process': 'success'}
        if 'city' in updated_values_dict:
            self.db_cursor.execute(f'update customers set city="{updated_values_dict["city"]}" where id={id_}')
            self.con.commit()
            return {'process': 'success'}
        else:
            return {'process': 'failed'}

    def delete_customer(self, id_):  # can do it with try catch but not rasing any errors if id not exists in the db
        self.db_cursor.execute(f'delete from customers where id={id_}')
        self.con.commit()
        return {'process': 'success'}

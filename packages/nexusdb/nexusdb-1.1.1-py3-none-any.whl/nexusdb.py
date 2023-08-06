import os
import json
import hashlib
import shutil
from datetime import datetime
from pprint import pprint
import bcrypt
import secrets
import uuid
import pytz


class JSONDatabase:
    def __init__(self, database_dir):
        self.database_dir = database_dir

    def create_database(self, database_name):
        database_path = os.path.join(self.database_dir, database_name)
        os.makedirs(database_path, exist_ok=True)
        operation = f"Create database {database_name}"
        self.log_operation(operation)

    def remove_database(self, database_name):
        database_path = os.path.join(self.database_dir, database_name)
        if os.path.exists(database_path):
            confirm = input(f"Are you sure you want to remove database '{database_name}'? (y/n): ")
            if confirm.lower() == 'y':
                shutil.rmtree(database_path)
                operation = f"Remove database {database_name}"
                self.log_operation(operation)

    def create_table(self, database_name, table_name):
        database_path = os.path.join(self.database_dir, database_name)
        table_path = os.path.join(database_path, f"{table_name}.json")
        if os.path.exists(database_path):
            if not os.path.exists(table_path):
                with open(table_path, 'w') as f:
                    f.write("[]")
        operation = f"Create table {table_name} in {database_name}"
        self.log_operation(operation)

    def remove_table(self, database_name, table_name):
        database_path = os.path.join(self.database_dir, database_name)
        table_path = os.path.join(database_path, f"{table_name}.json")
        if os.path.exists(database_path):
            if os.path.exists(table_path):
                confirm = input(f"Are you sure you want to remove table '{table_name}' from database '{database_name}'? (y/n): ")
                if confirm.lower() == 'y':
                    os.remove(table_path)
                    operation = f"Remove table {table_name} from {database_name}"
                    self.log_operation(operation)

    def insert_record(self, database_name, table_name, record):
        database_path = os.path.join(self.database_dir, database_name)
        table_path = os.path.join(database_path, f"{table_name}.json")
        if os.path.exists(database_path):
            if os.path.exists(table_path):
                with open(table_path, 'r+') as f:
                    data = json.load(f)
                    record['_id'] = secrets.token_hex(8)
                    data.insert(0, record)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()

        operation = f"Insert record into {database_name}/{table_name}"
        self.log_operation(operation)

    def update_record(self, database_name, table_name, record_id, new_values):
        database_path = os.path.join(self.database_dir, database_name)
        table_path = os.path.join(database_path, f"{table_name}.json")
        if os.path.exists(database_path):
            if os.path.exists(table_path):
                with open(table_path, 'r+') as f:
                    data = json.load(f)
                    for record in data:
                        if record.get('_id') == record_id:
                            record.update(new_values)
                            break
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()

        operation = f"Update record in {database_name}/{table_name}"
        self.log_operation(operation)

    def delete_record(self, database_name, table_name, record_id):
        database_path = os.path.join(self.database_dir, database_name)
        table_path = os.path.join(database_path, f"{table_name}.json")
        if os.path.exists(database_path):
            if os.path.exists(table_path):
                with open(table_path, 'r+') as f:
                    data = json.load(f)
                    data = [record for record in data if record.get('_id') != record_id]
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()

        operation = f"Delete record from {database_name}/{table_name}"
        self.log_operation(operation)

    def get_table(self, database_name, table_name):
        database_path = os.path.join(self.database_dir, database_name)
        table_path = os.path.join(database_path, f"{table_name}.json")
        if os.path.exists(database_path):
            if os.path.exists(table_path):
                with open(table_path, 'r') as f:
                    table = json.load(f)
                return table

    def count_records(self, database_name, table_name):
        table = self.get_table(database_name, table_name)
        if table:
            count = len(table)
            return count

    def aggregate(self, database_name, table_name, field, operation):
        table = self.get_table(database_name, table_name)
        if table:
            if operation == 'sum':
                result = sum(record[field] for record in table)
                return result
            elif operation == 'average':
                result = sum(record[field] for record in table) / len(table)
                return result
            elif operation == 'min':
                result = min(record[field] for record in table)
                return result
            elif operation == 'max':
                result = max(record[field] for record in table)

    def sort_table(self, database_name, table_name, field, reverse=False):
        table = self.get_table(database_name, table_name)
        if table:
            sorted_table = sorted(table, key=lambda x: x.get(field), reverse=reverse)
            return sorted_table

    def create_index(self, database_name, table_name, field):
        table = self.get_table(database_name, table_name)
        if table:
            index = {}
            for record in table:
                value = record.get(field)
                if value not in index:
                    index[value] = []
                index[value].append(record)
            index_file = os.path.join(self.database_dir, database_name, f"{table_name}_{field}_index.json")
            with open(index_file, 'w') as f:
                json.dump(index, f, indent=4)

    def backup_database(self, database_name, backup_file):
        database_path = os.path.join(self.database_dir, database_name)
        if os.path.exists(database_path):
            shutil.make_archive(backup_file, 'zip', database_path)

    def restore_database(self, backup_file, database_dir):
        shutil.unpack_archive(backup_file, database_dir)

    def begin_transaction(self, database_name):
        database_path = os.path.join(self.database_dir, database_name)
        transaction_path = os.path.join(database_path, 'transaction')
        if os.path.exists(database_path):
            if not os.path.exists(transaction_path):
                os.makedirs(transaction_path)

    def commit_transaction(self, database_name):
        database_path = os.path.join(self.database_dir, database_name)
        transaction_path = os.path.join(database_path, 'transaction')
        if os.path.exists(database_path):
            if os.path.exists(transaction_path):
                shutil.rmtree(transaction_path)

    def rollback_transaction(self, database_name):
        database_path = os.path.join(self.database_dir, database_name)
        transaction_path = os.path.join(database_path, 'transaction')
        if os.path.exists(database_path):
            if os.path.exists(transaction_path):
                shutil.rmtree(transaction_path)

    def log_operation(self, operation):
        logs_path = os.path.join(self.database_dir, 'logs')
        log_file = os.path.join(logs_path, 'logs.json')
        log = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"),
            'operation': operation
        }
        os.makedirs(logs_path, exist_ok=True)
        if os.path.exists(log_file):
            with open(log_file, 'r+') as f:
                logs = json.load(f)
                logs.append(log)
                f.seek(0)
                json.dump(logs, f, indent=4)
                f.truncate()
        else:
            with open(log_file, 'w') as f:
                json.dump([log], f, indent=4)

    def create_user(self, username, password):
        hashed_password = self.hash_password(password)
        users_path = os.path.join(self.database_dir, 'auth', 'users.json')
        unique_id = str(uuid.uuid4())

        if not os.path.exists(users_path):
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(users_path), exist_ok=True)
            current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

            user_data = {
                "id": unique_id,
                "username": username,
                "password": hashed_password,
                "role": "admin",
                "status": "active",
                "encryption": True,
                "ssl": "OFF",
                "created_at": current_time
            }

            with open(users_path, 'w') as f:
                json.dump([user_data], f, indent=4)
        else:
            with open(users_path, 'r+') as f:
                users = json.load(f)
                current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

                user_data = {
                    "id": unique_id,
                    "username": username,
                    "password": hashed_password,
                    "role": "admin",
                    "status": "active",
                    "encryption": True,
                    "ssl": "OFF",
                    "created_at": current_time
                }

                users.append(user_data)
                f.seek(0)
                json.dump(users, f, indent=4)
                f.truncate()

    def authenticate(self, username, password):
        users_path = os.path.join(self.database_dir, 'auth', 'users.json')
        if os.path.exists(users_path):
            with open(users_path, 'r') as f:
                users = json.load(f)
                for user in users:
                    if user["username"] == username and self.verify_password(password, user["password"]):
                        return True
        return False

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def query_record(self, database_name, table_name, condition):
        table = self.get_table(database_name, table_name)
        if table:
            query_result = [record for record in table if all(record.get(key) == value for key, value in condition.items())]
            return query_result
        
    def drop_database(self, database_name):
        confirm = input(f"Are you sure you want to drop the entire database '{database_name}'? (y/n): ")
        if confirm.lower() == 'y':
            database_path = os.path.join(self.database_dir, database_name)
            if os.path.exists(database_path):
                shutil.rmtree(database_path)
                operation = f"Drop database {database_name}"
                self.log_operation(operation)

    def drop_table(self, database_name, table_name):
        confirm = input(f"Are you sure you want to drop the table '{table_name}' from database '{database_name}'? (y/n): ")
        if confirm.lower() == 'y':
            self.remove_table(database_name, table_name)

    def get_record(self, database_name, table_name, record_id):
        table = self.get_table(database_name, table_name)
        if table:
            for record in table:
                if record.get('_id') == record_id:
                    return record

    def query_records(self, database_name, table_name, condition):
        table = self.get_table(database_name, table_name)
        if table:
            query_result = [record for record in table if all(record.get(key) == value for key, value in condition.items())]
            return query_result

    def create_unique_index(self, database_name, table_name, field):
        index_file = os.path.join(self.database_dir, database_name, f"{table_name}_{field}_index.json")
        if not os.path.exists(index_file):
            table = self.get_table(database_name, table_name)
            if table:
                unique_index = {}
                for record in table:
                    value = record.get(field)
                    if value not in unique_index:
                        unique_index[value] = record
                    else:
                        raise ValueError(f"Duplicate value '{value}' found for field '{field}'. Unique index creation failed.")
                with open(index_file, 'w') as f:
                    json.dump(unique_index, f, indent=4)
                operation = f"Create unique index for field '{field}' in {database_name}/{table_name}"
                self.log_operation(operation)
            else:
                raise ValueError(f"Table '{table_name}' does not exist in database '{database_name}'.")
        else:
            raise ValueError(f"Unique index already exists for field '{field}' in {database_name}/{table_name}.")

    def get_record_by_index(self, database_name, table_name, field, value):
        index_file = os.path.join(self.database_dir, database_name, f"{table_name}_{field}_index.json")
        if os.path.exists(index_file):
            with open(index_file, 'r') as f:
                index = json.load(f)
            return index.get(value)

    def update_record_by_index(self, database_name, table_name, field, value, new_values):
        index_file = os.path.join(self.database_dir, database_name, f"{table_name}_{field}_index.json")
        if os.path.exists(index_file):
            with open(index_file, 'r+') as f:
                index = json.load(f)
                record = index.get(value)
                if record:
                    record.update(new_values)
                    f.seek(0)
                    json.dump(index, f, indent=4)
                    f.truncate()
                else:
                    raise ValueError(f"No record found with value '{value}' for field '{field}'.")
        else:
            raise ValueError(f"Unique index does not exist for field '{field}' in {database_name}/{table_name}.")

    def delete_record_by_index(self, database_name, table_name, field, value):
        index_file = os.path.join(self.database_dir, database_name, f"{table_name}_{field}_index.json")
        if os.path.exists(index_file):
            with open(index_file, 'r+') as f:
                index = json.load(f)
                record = index.get(value)
                if record:
                    table_path = os.path.join(self.database_dir, database_name, f"{table_name}.json")
                    if os.path.exists(table_path):
                        with open(table_path, 'r+') as table_file:
                            table = json.load(table_file)
                            table = [r for r in table if r.get('_id') != record.get('_id')]
                            table_file.seek(0)
                            json.dump(table, table_file, indent=4)
                            table_file.truncate()
                            del index[value]
                            f.seek(0)
                            json.dump(index, f, indent=4)
                            f.truncate()
                else:
                    raise ValueError(f"No record found with value '{value}' for field '{field}'.")
        else:
            raise ValueError(f"Unique index does not exist for field '{field}' in {database_name}/{table_name}.")

    def get_table_size(self, database_name, table_name):
        table = self.get_table(database_name, table_name)
        if table:
            table_size = os.path.getsize(os.path.join(self.database_dir, database_name, f"{table_name}.json"))
            return table_size

    def optimize_table(self, database_name, table_name):
        table_path = os.path.join(self.database_dir, database_name, f"{table_name}.json")
        if os.path.exists(table_path):
            with open(table_path, 'r+') as f:
                table = json.load(f)
                table = [record for record in table if record.get('_id') is not None]
                f.seek(0)
                json.dump(table, f, indent=4)
                f.truncate()
                operation = f"Optimize table {database_name}/{table_name}"
                self.log_operation(operation)
        else:
            raise ValueError(f"Table '{table_name}' does not exist in database '{database_name}'.")
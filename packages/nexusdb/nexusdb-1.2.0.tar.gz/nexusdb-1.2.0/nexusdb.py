import json
import os
import uuid
import hashlib
import datetime
import shutil
import zipfile
from pprint import pprint


class JSONDatabase:
    def __init__(self, db_folder):
        self.db_folder = db_folder
        self.db_path = os.path.join('database', self.db_folder)
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        self.logs_path = os.path.join(self.db_path, 'logs', 'logs.json')
        if not os.path.exists(self.logs_path):
            os.makedirs(os.path.join(self.db_path, 'logs'))

    def create_collection(self, collection_name):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if os.path.exists(collection_path):
            raise ValueError('Collection already exists')
        with open(collection_path, 'w') as f:
            json.dump([], f, indent=4)
            f.write('\n')
        self._log_action('create_collection', collection_name)

    def insert_document(self, collection_name, document):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        with open(collection_path, 'r+') as f:
            data = json.load(f)
            document['_id'] = str(uuid.uuid4().hex)
            data.append(document)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        pprint(document, indent=4)
        self._log_action('insert_document', collection_name, document)

    def find_documents(self, collection_name, query):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            results = [doc for doc in data if self._match_query(doc, query)]
            self._log_action('find_documents', collection_name, query, results)
            return results

    def remove_document(self, collection_name, document_id):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        with open(collection_path, 'r+') as f:
            data = json.load(f)
            filtered_data = [doc for doc in data if doc['_id'] != document_id]
            f.seek(0)
            json.dump(filtered_data, f, indent=4)
            f.truncate()
        self._log_action('remove_document', collection_name, document_id)

    def create_user(self, name, email, password, role):
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            os.makedirs(os.path.join(self.db_path, 'users'))
            with open(users_path, 'w') as f:
                json.dump([], f, indent=4)
                f.write('\n')

        with open(users_path, 'r+') as f:
            users = json.load(f)
            salt = os.urandom(16)
            hashed_password = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000
            )
            user = {
                '_id': str(uuid.uuid4().hex),
                'name': name,
                'email': email,
                'password': hashed_password.hex(),
                'role': role,
                'status': 'active',
                'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'salt': salt.hex()
            }
            users.append(user)
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()
        pprint(user, indent=4)
        self._log_action('create_user', name, email, role)

    def remove_user(self, user_id):
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError('Users collection does not exist')
        with open(users_path, 'r+') as f:
            users = json.load(f)
            filtered_users = [user for user in users if user['_id'] != user_id]
            f.seek(0)
            json.dump(filtered_users, f, indent=4)
            f.truncate()
        self._log_action('remove_user', user_id)

    def block_user(self, user_id):
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError('Users collection does not exist')
        with open(users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user['_id'] == user_id:
                    user['status'] = 'blocked'
                    break
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()
        self._log_action('block_user', user_id)

    def revoke_user(self, user_id):
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError('Users collection does not exist')
        with open(users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user['_id'] == user_id:
                    user['status'] = 'revoked'
                    break
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()
        self._log_action('revoke_user', user_id)

    def update_document(self, collection_name, document_id, update_data):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        with open(collection_path, 'r+') as f:
            data = json.load(f)
            updated = False
            for doc in data:
                if doc['_id'] == document_id:
                    doc.update(update_data)
                    updated = True
                    break
            if updated:
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                print('Document updated successfully.')
            else:
                print('Document not found.')
        self._log_action('update_document', collection_name, document_id, update_data)

    def get_all_documents(self, collection_name):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            self._log_action('get_all_documents', collection_name)
            return data

    def count_documents(self, collection_name):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            self._log_action('count_documents', collection_name)
            return len(data)

    def drop_collection(self, collection_name):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        os.remove(collection_path)
        print(f'Collection {collection_name} dropped successfully.')
        self._log_action('drop_collection', collection_name)

    def drop_database(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
            print(f'Database {self.db_folder} dropped successfully.')
        else:
            raise ValueError('Database does not exist.')
        self._log_action('drop_database', self.db_folder)

    def import_database(self, zip_path):
        if not zipfile.is_zipfile(zip_path):
            raise ValueError('Invalid zip file')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.db_path)
        print('Database imported successfully.')
        self._log_action('import_database', zip_path)

    def import_collection(self, collection_name, zip_path):
        if not zipfile.is_zipfile(zip_path):
            raise ValueError('Invalid zip file')
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(collection_path))
        print(f'Collection {collection_name} imported successfully.')
        self._log_action('import_collection', collection_name, zip_path)

    def export_database(self, export_path):
        with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, dirs, files in os.walk(self.db_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_ref.write(file_path, os.path.relpath(file_path, self.db_path))
        print('Database exported successfully.')
        self._log_action('export_database', export_path)

    def export_collection(self, collection_name, export_path):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            zip_ref.write(collection_path, os.path.basename(collection_path))
        print(f'Collection {collection_name} exported successfully.')
        self._log_action('export_collection', collection_name, export_path)

    def _match_query(self, document, query):
        for key, value in query.items():
            if key not in document or document[key] != value:
                return False
        return True

    def _log_action(self, function_name, *args):
        logs = []
        if os.path.exists(self.logs_path):
            with open(self.logs_path, 'r') as f:
                logs = json.load(f)
        log_entry = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'function_name': function_name,
            'args': args
        }
        logs.append(log_entry)
        with open(self.logs_path, 'w') as f:
            json.dump(logs, f, indent=4)
        print(f'Logged action: {function_name} {args}')

    def create_index(self, collection_name, field):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        index_path = os.path.join(self.db_path, collection_name + '_' + field + '_index.json')
        if os.path.exists(index_path):
            raise ValueError('Index already exists')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            index_data = {}
            for doc in data:
                if field in doc:
                    value = doc[field]
                    if value not in index_data:
                        index_data[value] = []
                    index_data[value].append(doc['_id'])
        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=4)
            f.write('\n')
        pprint(index_data, indent=4)
        self._log_action('create_index', collection_name, field)

    def drop_index(self, collection_name, field):
        index_path = os.path.join(self.db_path, collection_name + '_' + field + '_index.json')
        if not os.path.exists(index_path):
            raise ValueError('Index does not exist')
        os.remove(index_path)
        print(f'Index {collection_name}_{field}_index dropped successfully.')
        self._log_action('drop_index', collection_name, field)

    def get_index(self, collection_name, field):
        index_path = os.path.join(self.db_path, collection_name + '_' + field + '_index.json')
        if not os.path.exists(index_path):
            raise ValueError('Index does not exist')
        with open(index_path, 'r') as f:
            index_data = json.load(f)
            self._log_action('get_index', collection_name, field)
            return index_data

    def backup_database(self, backup_path):
        if os.path.exists(backup_path):
            raise ValueError('Backup path already exists')
        shutil.copytree(self.db_path, backup_path)
        print('Database backup created successfully.')
        self._log_action('backup_database', backup_path)

    def restore_database(self, backup_path):
        if not os.path.exists(backup_path):
            raise ValueError('Backup path does not exist')
        shutil.rmtree(self.db_path)
        shutil.copytree(backup_path, self.db_path)
        print('Database restored successfully.')
        self._log_action('restore_database', backup_path)

    def compact_database(self):
        compact_db_path = os.path.join(self.db_path, 'compact')
        if os.path.exists(compact_db_path):
            shutil.rmtree(compact_db_path)
        os.makedirs(compact_db_path)

        for root, dirs, files in os.walk(self.db_path):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    compact_file_path = os.path.join(compact_db_path, file)
                    with open(compact_file_path, 'w') as f:
                        json.dump(data, f, separators=(',', ':'))
        shutil.rmtree(self.db_path)
        shutil.move(compact_db_path, self.db_path)
        print('Database compacted successfully.')
        self._log_action('compact_database')
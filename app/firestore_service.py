import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

class Todo:
    def __init__(self, description, done, todo_id, email=None, company=None, job_title=None, client=None):
        self.description = description
        self.done = done
        self.id = todo_id
        self.email = email
        self.company = company
        self.job_title = job_title
        self.client = client

    def to_dict(self):
        return {
            'description': self.description,
            'done': self.done,
            'email': self.email,
            'company': self.company,
            'job_title': self.job_title,
            'client': self.client,
        }

    @staticmethod
    def from_firestore(todo_doc):
        data = todo_doc.to_dict()
        description = data.get('description', '')
        done = data.get('done', False)
        email = data.get('email', '')
        company = data.get('company', '')
        job_title = data.get('job_title', '')
        client = data.get('client', '')

        return Todo(
            description=description,
            done=done,
            todo_id=todo_doc.id,
            email=email,
            company=company,
            job_title=job_title,
            client=client,
        )

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})

def get_todos(user_id):
    todos_docs = db.collection('users')\
        .document(user_id)\
        .collection('todos').get()
    
    todos = [Todo.from_firestore(todo) for todo in todos_docs]
    return todos

def put_todo(user_id, description, email, company, job_title, client):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    
    try:
        new_todo_ref = todos_collection_ref.document()
        new_todo_ref.set({
            'description': description,
            'done': False,
            'email': email,
            'company': company,
            'job_title': job_title,
            'client': client,
        })
    except Exception as e:
        print(f"Error al agregar el todo: {e}")
        raise

def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, description=None, email=None, company=None, job_title=None, client=None):
    todo_ref = db.collection('users').document(user_id).collection('todos').document(todo_id)
    updates = {
        'description': description,
        'email': email,
        'company': company,
        'job_title': job_title,
        'client': client
    }
    todo_ref.update(updates)

def _get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')


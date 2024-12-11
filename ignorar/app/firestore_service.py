import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

class Todo:
    def __init__(self, description, done, todo_id):
        self.description = description
        self.done = done
        self.id = todo_id

    def to_dict(self):
        return {'description': self.description, 'done': self.done}

    @staticmethod
    def from_firestore(todo_doc):
        data = todo_doc.to_dict()
        description = data.get('descripción') or data.get('description')
        done = data.get('done', False)
        return Todo(description=description, done=done, todo_id=todo_doc.id)


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

def put_todo(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    
    try:
        new_todo_ref = todos_collection_ref.document()  
        new_todo_ref.set({'description': description, 'done': False})
        print(f"Tipo de new_todo_ref: {type(new_todo_ref)}")
        print(f"Contenido de new_todo_ref: {new_todo_ref}")
    except Exception as e:
        print(f"Error al agregar el todo: {e}")
        raise
    
    if not isinstance(new_todo_ref, firestore.DocumentReference):
        raise ValueError("new_todo_ref no es un DocumentReference")
    
    new_todo_doc = new_todo_ref.get()
    return Todo.from_firestore(new_todo_doc)




def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done': todo_done})
    updated_todo = todo_ref.get()
    return Todo.from_firestore(updated_todo)

def _get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')

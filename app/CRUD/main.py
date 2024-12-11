import os
import csv
import uuid

CLIENT_TABLE = '.clients.csv'
CLIENT_SCHEMA = ['name', 'company', 'email', 'position', 'id']
clients = []

def _initialize_clients_from_storage():
    with open(CLIENT_TABLE, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=CLIENT_SCHEMA)
        for row in reader:
            clients.append(row)

def _save_clients_to_storage():
    tmp_table_name = f'{CLIENT_TABLE}.tmp'
    with open(tmp_table_name, mode='w') as f:
        writer = csv.DictWriter(f, fieldnames=CLIENT_SCHEMA)
        writer.writerows(clients)
    os.remove(CLIENT_TABLE)
    os.rename(tmp_table_name, CLIENT_TABLE)

def _exist_client(client):
    for idx, existing_client in enumerate(clients):
        if client['name'] == existing_client['name']:
            return True, idx
    return False, None

def create_client(client):
    client['id'] = str(uuid.uuid4())  
    clients.append(client)

def client_not_list():
    print('El cliente no esta en la lista.')

def list_clients():
    print('| id | name | company | email | position |')
    print('*' * 50)
    for idx, client in enumerate(clients):
        print('{uid} | {name} | {company} | {email} | {position}'.format(
            uid=client['id'],
            name=client['name'],
            company=client['company'],
            email=client['email'],
            position=client['position']
        ))

def update_client(client_name, updated_client_name, idx):
    clients[idx]['name'] = updated_client_name
    clients[idx]['company'] = _get_client_field('company')
    clients[idx]['email'] = _get_client_field('email')
    clients[idx]['position'] = _get_client_field('position')

def delete_client(idx):
    clients.pop(idx)

def search_client(client):
    for idx, existing_client in enumerate(clients):
        if client['name'] == existing_client['name']:
            return True, idx
    return False, None

def _print_welcome():
    print('Bienvenido a mi Platzi Ventas')
    print('*' * 50)
    print('¿Qué te gustaría hacer hoy?')
    print('(C) Crear cliente')
    print('(L) Listar clientes')
    print('(A) Actualizar cliente')
    print('(E) Eliminar cliente')
    print('(B) Buscar cliente')

def _get_client_field(field_name):
    field = None
    while not field:
        field = input(f'¿Cuál es el {field_name} del cliente? ')
    return field

def _get_client_name():
    client_name = None
    while not client_name:
        client_name = input('¿Cual es el nombre del cliente? ')
        if client_name.lower() == 'salir':
            sys.exit()
    return client_name

if __name__ == '__main__':
    _initialize_clients_from_storage()
    _print_welcome()

    command = input().upper()

    if command == 'C':
        client = {
            'name': _get_client_name(),
            'company': _get_client_field('company'),
            'email': _get_client_field('email'),
            'position': _get_client_field('position')
        }
        exists, idx = _exist_client(client)
        if not exists:
            create_client(client)
        else:
            print('El cliente ya está en la lista.')

        list_clients()

    elif command == 'L':
        list_clients()

    elif command == 'E':
        client = {'name': _get_client_name()}
        exists, idx = _exist_client(client)
        if exists:
            delete_client(idx)
        else:
            print(f'El cliente {client["name"]} no está en la lista.')

        list_clients()

    elif command == 'B':
        client = {'name': _get_client_name()}
        exists, idx = search_client(client)
        if exists:
            print('El cliente está en la lista:')
            print('{uid} | {name} | {company} | {email} | {position}'.format(
                uid=clients[idx]['id'],
                name=clients[idx]['name'],
                company=clients[idx]['company'],
                email=clients[idx]['email'],
                position=clients[idx]['position']
            ))
        else:
            print(f'El cliente {client["name"]} no está en la lista.')

    elif command == 'A':
        client = {'name': _get_client_name()}
        exists, idx = _exist_client(client)
        if not exists:
            client_not_list()
        else:
            updated_client_name = input('¿Cual es el nombre actualizado del cliente? ')
            update_client(client, updated_client_name, idx)
            list_clients()

    else:
        print('Comando invalido.')

    _save_clients_to_storage()

import psycopg2

def create_db(conn):

    query = '''
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                family_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL);
                '''
    conn.execute(query)

    query = '''
                CREATE TABLE IF NOT EXISTS tel (
                id SERIAL PRIMARY KEY,
                tel VARCHAR(40) NOT NULL,
                user_id INTEGER REFERENCES users (id));
                '''
    conn.execute(query)
    print('Таблицы созданы')

def add_client(conn, first_name, last_name, email, phone):
    conn.execute('''INSERT INTO users (name, family_name, email) 
    VALUES (%s, %s, %s) RETURNING id, name;''', (first_name, last_name, email))
    print(conn.fetchone())
    if phone is not None:
        conn.execute('''SELECT id FROM users 
        WHERE name = %s and family_name = %s and email = %s;''', (first_name, last_name, email))
        client_id = conn.fetchone()[0]
        add_phone(conn, client_id, phone)

def add_phone(conn, client_id, phone):
    conn.execute('''INSERT INTO tel (tel, user_id) 
    VALUES (%s, %s) RETURNING id, tel;''', (phone, client_id))
    print(conn.fetchone())

def change_client(conn, client_id, table, column, data):
    query = f'UPDATE {table} SET {column} = %s WHERE id = %s'
    conn.execute(query, (data, client_id))
    query = f'SELECT * FROM {table}'
    conn.execute(query)
    print(conn.fetchone())

def delete_phone(conn, client_id, phone):
    conn.execute('''DELETE FROM tel WHERE tel = %s and user_id = %s;''', (phone, client_id))
    print(f'телефон {phone} удален')

def delete_client(conn, client_id):
    conn.execute('''DELETE FROM users WHERE id = %s''', (client_id,))
    print(f'клиент {client_id} удален')

def find_client(conn, table, column, data:str):
    query = f'SELECT * FROM {table} WHERE {column}=%s'
    conn.execute(query, (data,))
    print(conn.fetchmany())


if __name__ == "__main__":
    connect = psycopg2.connect(host='localhost', port='5432', database="net_db_1", user="postgres", password="912@greP")

    print('Введите цифру для выбора функции:')
    print('1 - создать таблицы' + '\n' + '2 - добавить клиента' + '\n' + '3 - добавить телефон клиента' + '\n' + '4 - изменить данные клиента'
          + '\n' + '5 - удалить телефон клиента' + '\n' + '6 - удалить клиента' + '\n' + '7 - найти клиента' + '\n')

    d = int(input())
    with connect.cursor() as conn:
        if d == 1:
            create_db(conn)
        if d == 2:
            first_name = str(input('Введите Имя клиента '+ '\n'))
            last_name = str(input('Введите Фамилию клиента '+ '\n'))
            email = str(input('Введите E-mail клиента '+ '\n'))
            phone = str(input('Введите телефон клиента ' + '\n'))
            add_client(conn, first_name, last_name, email, phone)
        if d == 3:
            client_id = int(input('Введите ID клиента '+ '\n'))
            phone = str(input('Введите Телефон клиента '+ '\n'))
            add_phone(conn, client_id, phone)
        if d == 4:
            client_id = int(input('Введите ID клиента '+ '\n'))
            n = int(input('Если хотите поменять имя нажмите 1 '+ '\n' + 'Если хотите поменять Фамилию нажмите 2 '+ '\n'
                                   + 'Если хотите поменять email  нажмите 3 '+ '\n' + 'Если хотите поменять телефон нажмите 4 '+ '\n'))
            if n == 1:
                data = str(input('Введите новое имя клиента ' + '\n'))
                table = 'users'
                column = 'name'
                change_client(conn, client_id, table, column, data)
            if n == 2:
                data = str(input('Введите новую фамилию клиента ' + '\n'))
                table = 'users'
                column = 'family_name'
                change_client(conn, client_id, table, column, data)
            if n == 3:
                data = str(input('Введите новый email клиента ' + '\n'))
                table = 'users'
                column = 'email'
                change_client(conn, client_id, table, column, data)
            if n == 4:
                data = str(input('Введите новый телефон клиента ' + '\n'))
                table = 'tel'
                column = 'tel'
                change_client(conn, client_id, table, column, data)
        if d == 5:
            client_id = int(input('Введите ID клиента ' + '\n'))
            phone = str(input('Введите Телефон клиента '+ '\n'))
            delete_phone(conn, client_id, phone)
        if d == 6:
            client_id = int(input('Введите ID клиента ' + '\n'))
            delete_client(conn, client_id)
        if d == 7:
            n = int(
                input('Если хотите найти по имени нажмите 1 ' + '\n' + 'Если хотите найти по Фамилии нажмите 2 ' + '\n'
                      + 'Если хотите найти по email  нажмите 3 ' + '\n' + 'Если хотите найти по телефону нажмите 4 ' + '\n'))
            if n == 1:
                data = str(input('Введите  имя клиента ' + '\n'))
                table = 'users'
                column = 'name'
                find_client(conn, table, column, data)
            if n == 2:
                data = str(input('Введите  фамилию клиента ' + '\n'))
                table = 'users'
                column = 'family_name'
                find_client(conn, table, column, data)
            if n == 3:
                data = str(input('Введите  email клиента ' + '\n'))
                table = 'users'
                column = 'email'
                find_client(conn, table, column, data)
            if n == 4:
                data = str(input('Введите  телефон клиента ' + '\n'))
                table = 'tel'
                column = 'tel'
                find_client(conn, table, column, data)

    connect.close()
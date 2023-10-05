import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
           CREATE TABLE IF NOT EXISTS client(
               client_id SERIAL PRIMARY KEY,
               first_name VARCHAR(40) NOT NULL,
               last_name VARCHAR(40) NOT NULL,
               email VARCHAR(100) NOT NULL
           );
           """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
               phone_id SERIAL PRIMARY KEY,
               phone VARCHAR(20) NOT NULL,
               id_client INTEGER REFERENCES client(client_id)
            );
            """)

        conn.commit()


def add_client(conn, client_id, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(client_id, first_name, last_name, email) VALUES(%s,%s, %s, %s);
            """, (client_id, first_name, last_name, email))

        # conn.commit()
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())


def add_phone(conn, id_client, phone_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(phone_id, phone, id_client) VALUES(%s, %s, %s);
            """, (phone_id, phone, id_client))

        cur.execute("""
                SELECT * FROM phone;
                """)
        print(cur.fetchall())


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                UPDATE client SET first_name=%s WHERE client_id=%s;
                """, (first_name, client_id))

        if last_name is not None:
            cur.execute("""
                UPDATE client SET last_name=%s WHERE client_id=%s;
                """, (last_name, client_id))

        if email is not None:
            cur.execute("""
                UPDATE client SET email=%s WHERE client_id=%s;
                """, (email, client_id))

        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())


def delete_phone(conn, id_client, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE id_client=%s or phone=%s;
            """, (id_client, phone))
        cur.execute("""
             SELECT * FROM phone;
             """)
        print(cur.fetchall())


def delete_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                SELECT * FROM client WHERE first_name=%s;
                """, (first_name,))
            print(cur.fetchone())

        if last_name is not None:
            cur.execute("""
                SELECT * FROM client WHERE last_name=%s;
                """, (last_name,))
            print(cur.fetchone())

        if email is not None:
            cur.execute("""
                SELECT * FROM client WHERE email=%s;
                """, (email,))
            print(cur.fetchone())


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    create_db(conn)

    add_client(conn, 1, 'Tatiana', 'Molchanova', 'tatuka.08@mail.ru')

    add_phone(conn, 1, 1, '+5491150184099')

    change_client(conn, 1, None, None, 'molchanovatatiana33@gmail.com')

    find_client(conn, last_name='Molchanova')

    delete_phone(conn, 1, '5491150184099')

    delete_client(conn, 1)

conn.close()

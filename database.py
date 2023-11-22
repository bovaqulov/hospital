import psycopg2


class DataBase:
    def __init__(self, dbname, user, host, password):
        self.database=psycopg2.connect(
            database=dbname,
            user=user,
            host=host,
            password=password
        )

    def manager(self, sql, *args, commit:bool=False, fetchone:bool=False, fetchall:bool=False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                return db.commit()
            elif fetchone:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()


    def create_users_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            name VARCHAR(30),
            lastname VARCHAR(30),
            contact VARCHAR(15) UNIQUE,
            birthdate DATE
        )'''
        self.manager(sql, commit=True)

    def find_user_id(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = %s'''
        return None not in self.manager(sql, telegram_id, fetchone=True)

    def insert_telegram_id(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES(%s) ON CONFLICT DO NOTHING'''
        self.manager(sql, (telegram_id,), commit=True)

    def update_user_info(self, name, lastname, contact, birthdate, address, telegram_id):
        sql = '''UPDATE users SET name=%s, lastname=%s, contact=%s, birthdate=%s, address=%s WHERE telegram_id=%s'''
        self.manager(sql, name, lastname, contact, birthdate, address, telegram_id, commit=True)

    def create_patients(self):
        sql = """CREATE TABLE IF NOT EXISTS patients(
            patient_id SERIAL PRIMARY KEY,
            telegram_id INTEGER REFERENCES users(telegram_id),
            category_id INTEGER REFERENCES categories(category_id)
        )"""
        self.manager(sql, commit=True)


    def create_categories(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
            category_id SERIAL PRIMARY KEY,
            category VARCHAR(50) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def insert_category(self, category):
        sql = '''INSERT INTO categories(category) VALUES (%s) ON CONFLICT DO NOTHING'''
        self.manager(sql, (category,), commit=True)

    def get_all_categories(self):
        sql = '''SELECT * FROM categories'''
        return [item for item in self.manager(sql, fetchall=True)]

    def get_telegram_id_by_category_id_from_patients(self, telegram_id):
        sql = '''SELECT * FROM patients WHERE telegram_id=%s'''
        return self.manager(sql, telegram_id, fetchall=True)

    def insert_patients(self, telegram_id, category_id):
        sql = '''INSERT INTO patients(telegram_id, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING'''
        self.manager(sql, telegram_id, category_id, commit=True)

    def get_all_patients_by_category_id(self, category_id):
        sql = '''SELECT * FROM users WHERE telegram_id IN (SELECT telegram_id FROM patients WHERE category_id=%s)'''
        return [item[0:4] for item in self.manager(sql, category_id, fetchall=True)]

    def get_category_by_telegram_id(self, telegram_id):
        sql = """SELECT category FROM categories WHERE category_id IN (SELECT category_id FROM patients WHERE telegram_id=%s)"""
        return self.manager(sql, telegram_id, fetchone=True)[0]

    def delete_patient_by_telegam_id(self,  telegram_id):
        sql = """DELETE FROM patients WHERE telegram_id=%s"""
        self.manager(sql, telegram_id, commit=True)

    def get_queues_patients(self, telegram_id):
        sql = """SELECT category_id FROM patients WHERE telegram_id=%s"""
        return self.manager(sql, telegram_id, fetchone=True)[0]

    def count_users(self):
        sql = '''SELECT count(telegram_id) FROM users'''
        return self.manager(sql, fetchone=True)[0]

    def get_all_users(self):
        sql = '''SELECT telegram_id FROM users'''
        return [item[0] for item in self.manager(sql, fetchall=True)]

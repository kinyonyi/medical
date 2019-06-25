import psycopg2
con = psycopg2.connect(
    database = "medical",
    user = "postgres",
    port = "5432",
    host = "localhost",
    password = "david"
)
cur = con.cursor()
con.autocommit = True
#user registration table creation
def create_table_register_user():
    register = "CREATE TABLE IF NOT EXISTS register_user(id SERIAL PRIMARY KEY, firstname VARCHAR(30), lastname VARCHAR(30), password VARCHAR(30), telephone INT, email VARCHAR(30) UNIQUE);"
    cur.execute(register)
#doctor registration table creation
def create_table_register_doc():
    register = "CREATE TABLE IF NOT EXISTS register_doc(id SERIAL PRIMARY KEY, doc_id VARCHAR(30), doc_type VARCHAR(30), firstname VARCHAR(30), lastname VARCHAR(30),password VARCHAR(30), qualification VARCHAR(30), telephone INT, email VARCHAR(30) UNIQUE);"
    cur.execute(register)
#insertion of new users/patients to the database table for users
def save_registered_user(fname, lname, pword, tel, email):
    values = (fname, lname, pword, tel, email)
    saved = "INSERT INTO register_user (firstname, lastname, password, telephone, email) VALUES (%s, %s, %s, %s, %s);"
    cur.execute(saved, values)
#insertion of new doctors to the database table for doctors registration
def save_registered_doctor(doc_id, doc_type, fname, lname, pword, qualification, tel, email):
    values = (doc_id, doc_type, fname, lname, pword, qualification, tel, email)
    saved = "INSERT INTO register_doc (doc_id, doc_type, firstname, lastname, password, qualification, telephone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    cur.execute(saved, values)
#querrying database table for all users currently registered
def query_registered_user():
    queried = "SELECT * FROM {} ORDER BY firstname DESC;".format('register_user')
    cur.execute(queried)
    registered = cur.fetchall()
    return registered
#querrying database table for all doctors currently registered
def query_registered_doc():
    queried = "SELECT * FROM {} ORDER BY firstname ASC;".format('register_doc')
    cur.execute(queried)
    registered = cur.fetchall()
    return registered
def query_login_user():
    querried = "SELECT firstname, password FROM {} WHERE id = id;".format('register_user')
    cur.execute(querried)
    items = cur.fetchall()
    users_registered = {}
    for fname, pword in items:
        users_registered[fname] = '{}'.format(pword)
    return users_registered
def query_login_doc():
    querried = "SELECT firstname, password FROM {} WHERE id = id;".format('register_doc')
    cur.execute(querried)
    items = cur.fetchall()
    docs_registered = {}
    for fname, pword in items:
        docs_registered[fname] = '{}'.format(pword)
    return docs_registered
def update_doc_details(telephone1, email1, variable):
    values = (telephone1, email1, variable)
    update = "UPDATE register_doc SET telephone = '{}', email = '{}' WHERE firstname = '{}' ;".format(telephone1, email1, variable)
    cur.execute(update, values)

def update_user_details(password,telephone, email, variable):
    values = (password,telephone, email, variable)
    update = "UPDATE register_user SET password = '{}', telephone = '{}', email = '{}' WHERE firstname = '{}';".format(password,telephone, email, variable)
    cur.execute(update, values)

#messaging tables and querries
def create_table_messsage_general_doc():
    creation = "CREATE TABLE IF NOT EXISTS general_physician(id SERIAL PRIMARY KEY, Cough VARCHAR(10), Headache VARCHAR(20), Fever VARCHAR(10), Stomachpain VARCHAR(20), LowerAbdominalPain VARCHAR(20), Vomiting VARCHAR(15), Diarrhea VARCHAR(10), Flue VARCHAR(10), Chest_pain VARCHAR(10), other_comments VARCHAR(300), email VARCHAR(50))"
    cur.execute(creation)
def create_table_messsage_bones_doc():
    creation = "CREATE TABLE IF NOT EXISTS bones(id SERIAL PRIMARY KEY, Cough VARCHAR(10), Headache VARCHAR(20), Fever VARCHAR(10), Stomachpain VARCHAR(20), LowerAbdominalPain VARCHAR(20), Vomiting VARCHAR(15), Diarrhea VARCHAR(10), Flue VARCHAR(10), Chest_pain VARCHAR(10), other_comments VARCHAR(300),email VARCHAR(50));"
    cur.execute(creation)
def create_table_messsage_womens_doc():
    creation = "CREATE TABLE IF NOT EXISTS women(id SERIAL PRIMARY KEY, Cough VARCHAR(10), Headache VARCHAR(20), Fever VARCHAR(10), Stomachpain VARCHAR(20), LowerAbdominalPain VARCHAR(20), Vomiting VARCHAR(15), Diarrhea VARCHAR(10), Flue VARCHAR(10), Chest_pain VARCHAR(10), other_comments VARCHAR(300),email VARCHAR(50));"
    cur.execute(creation)
def create_table_admin_messsage():
    creation = "CREATE TABLE IF NOT EXISTS message_admin(id SERIAL PRIMARY KEY, firstname VARCHAR(30), lastname VARCHAR(30), email VARCHAR(30), message VARCHAR(300));"
    cur.execute(creation)

#insertion of messages to the database 
def insert_messages(doc_type,Cough, Headache, Fever, Stomachpain,LowerAbdominalPain,Vomiting,Diarrhea,Flue, Chest_pain, other_comments, email):
    values = (Cough, Headache,Fever, Stomachpain,LowerAbdominalPain,Vomiting,Diarrhea,Flue,Chest_pain, other_comments, email[0])
    inserted = "INSERT INTO {} (Cough, Headache, Fever, Stomachpain, LowerAbdominalPain, Vomiting, Diarrhea, Flue, Chest_pain, other_comments, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(doc_type)
    cur.execute(inserted, values)

def insert_message_admin(fname, lname,email, message):
    values = (fname, lname, email, message)
    inserted = "INSERT INTO message_admin(firstname, lastname, email, message) VALUES (%s, %s, %s, %s);"
    cur.execute(inserted, values)

#viewing of the messages
def query_message(table_name):
    query = "SELECT message FROM '{}' ;".format(table_name)
    cur.execute(query)
    messages = cur.fetchall()
    return messages

create_table_messsage_general_doc()
create_table_messsage_bones_doc()
create_table_messsage_womens_doc()
create_table_admin_messsage()
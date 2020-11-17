import sqlite3
database = 'big_bazar.db'
menu_file = "Menu.cfg"
record_not_found = 'Record not found.'

connection = sqlite3.connect(database)

tables = []

def get_count_of_tables():
	count_of_tables = 0

	cursor = connection.cursor()

	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

	tables = cursor.fetchall()

	for table in tables:
		count_of_tables = count_of_tables + 1

	print(count_of_tables)

def get_tables():


	cursor = connection.cursor()

	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

	tables = cursor.fetchall()

	connection.commit()
	return tables

tables = get_tables()

def show_tables():

	counter = 1

	for table in tables:
		print(str(counter) + "." + str(tables[counter - 1][0]))
		counter = counter + 1

def select_table():

	try:
		user_option = int(input("Enter option: "))

	except:
		print("INVALID INPUT")

	table = tables[user_option - 1][0]

	return table

def get_no_of_fields():
	count_of_fields = 0
	for column_name in column_names:
		count_of_fields = count_of_fields + 1
	return count_of_fields

show_tables()

table = select_table()
print(table)

try:
	with open(menu_file) as f_menu:
		menu = f_menu.read()
	f_menu.close()
except FileNotFoundError:
	print(file_not_found_message)

try:
	get_column_names = connection.execute("select * from %s limit 1" %(table))
except sqlite3.OperationalError:
	print("Table not found.")

column_names = [i[0] for i in get_column_names.description]

max_length_column_name = column_names[0]
for column_name in column_names:
	if(len(max_length_column_name) < len(column_name)):
		max_length_column_name = column_name

max_length_column_name = column_names[0]

for column_name in column_names:
	if(len(max_length_column_name) < len(column_name)):
		max_length_column_name = column_name

def print_pipe():
	count_of_fields = get_no_of_fields()
	print("-" * (((len(max_length_column_name) + 12) * count_of_fields) + 1) )

def get_column_names():
	print("|", end = "")
	for column_name in column_names:
		print(column_name, end ="")
		print(" " * (len(max_length_column_name) - len(column_name) + 11), end = "")
		print("|", end = "")
	print("\t")

def column_names_string():
	columns_string = "("
	for column_name in column_names:
		columns_string = columns_string +  column_name + ","
	columns_string = columns_string.rstrip(",") + ")"
	return columns_string

def insert_record():

	field_values = []
	for column_name in column_names:
		if column_name == 'STATUS':
			status = 'ACTIVE'
			field_values.append(status)
		else:
			field_value = input("Enter " + column_name + ": ")
			field_values.append(field_value)
	record = tuple(field_values)
	duple_of_column_names = tuple(column_names)
	columns_string = column_names_string()
	try:
		is_record_saved = connection.execute("INSERT INTO " + table + " "+ columns_string + "VALUES" + str(record) ).rowcount
	except sqlite3.IntegrityError:
		is_record_saved = 0
		print("Id already exist")
	if is_record_saved > 0:
		print("Record saved successfully.")
	connection.commit()

def show_records():
	cursor = connection.execute("SELECT * from %s WHERE STATUS = 'ACTIVE'" %(table))
	data = cursor.fetchall()
	print_pipe()
	get_column_names()
	print_pipe()
	for record in data:
		print("|", end ="")
		for counter in range(0,len(record)):
			print(record[counter], end= "")
			print(" " * (len(max_length_column_name) - int(len(str(record[counter]))) + 11), end = "")
			print("|", end="")
		print("\t")
	print_pipe()

def show_record():
	user_input_id = int(input("Enter ID: "))
	id = connection.execute("SELECT ID from %s WHERE STATUS = 'ACTIVE'" %(table))
	ids = id.fetchall()
	is_record_found = False
	for id in ids:
		if (id[0]) == user_input_id:
			is_record_found = True
			cursor = connection.execute("SELECT * from %s WHERE STATUS = 'ACTIVE' AND ID =" %(table) + str(user_input_id))
			data = cursor.fetchall()
			print_pipe()
			get_column_names()
			print_pipe()
			for record in data:
				print("|", end ="")
				for counter in range(0,len(record)):
					print(record[counter], end= "")
					print(" " * (len(max_length_column_name) - int(len(str(record[counter]))) + 11), end = "")
					print("|", end = "")
				print("\t")
			print_pipe()
			break
		else:
			is_record_found = False
	if is_record_found == False:
		print(record_not_found)

def delete_record():
	user_input_id =int(input("Enter ID: "))
	is_record_deleted = connection.execute("UPDATE %s set STATUS = 'INACTIVE' where ID =" %(table) + str(user_input_id)).rowcount
	print(is_record_deleted)
	connection.commit()

def update_record():
	count_of_fields = get_no_of_fields()
	user_input_id = int(input("Enter ID: "))
	id = connection.execute("SELECT ID from %s WHERE STATUS = 'ACTIVE'" %(table))
	ids = id.fetchall()
	is_record_found = False
	for id in ids:
		if id[0] == user_input_id:
			is_record_found = True
			for counter in range(2, count_of_fields):
				print(str(counter - 1) + ".Update " + column_names[counter])
			user_input = int(input("Enter option: "))
			if user_input >= 1 and user_input <= count_of_fields - 2:
				user_input_data = input("Enter "+ column_names[user_input + 1] + ": ")
				is_record_updated =  connection.execute("UPDATE %s set %s = '%s' where id = %s" %(table, column_names[user_input + 1], user_input_data, user_input_id))
				connection.commit()
				print("Record updated successfully.")
				break
		else:
			is_record_found = False
	if is_record_found == False:
		print(record_not_found)

functions_list = [insert_record, show_records, show_record, update_record, delete_record, exit]

while True:
	print(menu)
	try:
		user_option = int(input("Enter option: "))
	except ValueError:
		print("INVALID INPUT")
		continue
	if user_option >= 1 and user_option <= 5:
		functions_list[user_option - 1]()
	elif user_option == 6:
		print("Press Y to exit.")
		quit_option = input("Enter option: ")
		if quit_option.upper() == 'Y':
			functions_list[user_option - 1]()
	else:
		print("INVALID INPUT")

connection.close()

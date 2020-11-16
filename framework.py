import sqlite3
data_base = 'bank.db'

table = input("Enter table: ").upper()

connection = sqlite3.connect(data_base)
menu_file = "Menu.cfg"
record_not_found = 'Record not found.'

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


column_name_names = [i[0] for i in get_column_names.description]

max_length_column_name = column_name_names[0]
for column_name in column_name_names:
	if(len(max_length_column_name) < len(column_name)):
		max_length_column_name = column_name

def get_no_of_fields():
	count_of_fields = 0
	for column_name in column_name_names:
		count_of_fields = count_of_fields + 1
	return count_of_fields

def print_pipe():
	count_of_fields = get_no_of_fields()
	print("-" * (((len(max_length_column_name) + 6) * count_of_fields) + 1) )

def get_column_names():
	print("|", end = "")
	for column_name in column_name_names:
		print(column_name, end ="")
		print(" " * (len(max_length_column_name) - len(column_name) + 5), end = "")
		print("|", end = "")
	print("\t")

def insert_record():
	connection = sqlite3.connect(data_base)
	query = ('INSERT INTO %s (STATUS, ID, NAME, BALANCE) '
	         'VALUES (:STATUS, :ID, :NAME, :BALANCE);' %(table))
	params = {
	        'STATUS': 'ACTIVE',
	        'ID': input("Enter ID:"),
	        'NAME': input("Enter name: "),
	        'BALANCE': input("Enter balance: "),
	    	}
	try:
		connection.execute(query, params)
		connection.commit()
		print("Record saved successfully.")
	except sqlite3.IntegrityError:
		print("ID already exist.")
	connection.close()

def show_records():
	connection = sqlite3.connect(data_base)
	cursor = connection.execute("SELECT * from %s WHERE STATUS = 'ACTIVE'" %(table))
	data = cursor.fetchall()
	print_pipe()
	get_column_names()
	print_pipe()
	for record in data:
		print("|", end ="")
		for counter in range(0,len(record)):
			print(record[counter], end= "")
			print(" " * (len(max_length_column_name) - int(len(str(record[counter]))) + 5), end = "")
			print("|", end="")
		print("\t")
	print_pipe()
	connection.close()

def deactivate_record():
	connection = sqlite3.connect(data_base)
	user_input_id =int(input("Enter ID: "))
	id = connection.execute("SELECT ID from %s WHERE STATUS = 'ACTIVE'" %(table))
	is_record_found = False
	ids = id.fetchall()
	is_record_found = False
	for id in ids:
		if (id[0]) == user_input_id:
			is_record_found = True
			connection.execute("UPDATE %s set STATUS = 'INACTIVE' where ID =" %(table) + str(user_input_id))
			connection.commit()
			connection.close()
			print("Record deleted successfully.")
			break
		else:
			is_record_found = False
	if is_record_found == False:
		print(record_not_found)

def show_record():
	connection = sqlite3.connect(data_base)
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
					print(" " * (len(max_length_column_name) - int(len(str(record[counter]))) + 5), end = "")
					print("|", end="")
				print("\t")
			print_pipe()
			connection.close()
			break
		else:
			is_record_found = False
	if is_record_found == False:
		print(record_not_found)
			
def update_record():
	connection = sqlite3.connect(data_base)
	count_of_fields = get_no_of_fields()
	user_input_id = int(input("Enter ID: "))
	count_of_fields = get_no_of_fields()
	id = connection.execute("SELECT ID from %s WHERE STATUS = 'ACTIVE'" %(table))
	ids = id.fetchall()
	is_record_found = False
	for id in ids:
		if id[0] == user_input_id:
			is_record_found = True
			for counter in range(2, count_of_fields):
				print(str(counter - 1) + ".Update " + column_name_names[counter])
			user_input = int(input("Enter option: "))
			if user_input >= 1 and user_input <= count_of_fields - 2:
				user_input_data = input("Enter "+ column_name_names[user_input + 1] + ": ")
				connection.execute("UPDATE %s set %s = '%s' where id = %s" %(table, column_name_names[user_input + 1], user_input_data, user_input_id))
				connection.commit()
				connection.close()
				print("Record updated successfully.")
				break
		else:
			is_record_found = False
	if is_record_found == False:
		print(record_not_found)

functions_list = [insert_record, show_records, show_record, update_record, deactivate_record, exit]

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


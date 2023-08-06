#!python

try:
	import argparse
	import getpass
	import json
	import requests
	import sys
except Exception as e:
	print()
	print('Error ...')
	print('Message: Could not import the required modules, exiting script!')
	print()
	
	exit(1)

try:
	import passpy
	pass_available = True
except Exception as e:
	pass_available = False

def choose_cyberark_account(cyberark_accounts_list: list):
	print('> Choose Account <')
	print()

	cyberark_accounts_dict = {}
	
	for account in cyberark_accounts_list:  
		cyberark_account_id = account['id']
		
		try:
			cyberark_account_name = account['name']
		except:
			cyberark_account_name = 'No Name'
			
		try:
			cyberark_account_username = account['userName']
		except:
			cyberark_account_username = 'No Username'
			
		cyberark_accounts_dict[cyberark_account_username] = []
		cyberark_accounts_dict[cyberark_account_username] = [cyberark_account_id, cyberark_account_name]
			
	cyberark_accounts_id_list = []
	
	for username in sorted(cyberark_accounts_dict): 
		cyberark_account_id, cyberark_account_name = cyberark_accounts_dict[username]
		cyberark_accounts_id_list.append(cyberark_account_id)

	if len(cyberark_accounts_id_list) == 1:
		print('Good news! Account found ...')
		print()
		
		choose_cyberark_account_input = 0
	else:
		print('Displaying choices ...')
		print()
		
		print(f"{'Choice:' :<10}{'Account:' :<25}{'Name/Description:'}")
		
		cyberark_accounts_id_count = 0
		
		for username in sorted(cyberark_accounts_dict):
			cyberark_accounts_id_count += 1
			cyberark_account_id, cyberark_account_name = cyberark_accounts_dict[username]
			print(f"{cyberark_accounts_id_count :<10}{username[0:24] :<25}{cyberark_account_name[:44]}")
			
		print()
		
		print(f'Choice: 1-{cyberark_accounts_id_count}')
		print('r: Return to the main menu')
		print()
		
		choose_cyberark_account_quit_flag = False
	
		while choose_cyberark_account_quit_flag is False:
			choose_cyberark_account_input = input(f'Enter your choice: ')
			print()
		
			if choose_cyberark_account_input == 'r':
				break
			else:
				try:	
					choose_cyberark_account_choice = int(choose_cyberark_account_input) - 1
					if (choose_cyberark_account_choice > -1) and (choose_cyberark_account_choice < len(cyberark_accounts_id_list)):
						return cyberark_accounts_id_list[choose_cyberark_account_choice]
				except:
					choose_cyberark_account_choice = -1
					print('Your choice was not a number in the specified range.')
					print()

def do_webservice_request(requests_method: str, requests_url: str, requests_headers: dict, requests_json: dict or None):
	try:	
		webservice_response = requests.request(
			method=requests_method,
			url=requests_url,					   
			headers=requests_headers,
			json=requests_json
		)
		
		webservice_response.raise_for_status()

		return json.loads(webservice_response.text)	 
	except (ConnectionError, requests.exceptions.HTTPError, Exception) as e:
		print('Error ...') 
		print(f'Message: {str(e)}')
		print()
		
		exit(1)
	
def get_auth_userinfo_from_commandline():
	parser = argparse.ArgumentParser(description='VaultPass: Search for CyberArk accounts, then display or save their passwords')
	
	parser.add_argument('--uniqname', '-u', type=str, required=True, help='Your uniqname')
	parser.add_argument('--password', '-p', type=str, required=True, help='Your UMICH Level 1 password')
	
	args = parser.parse_args()
	
	uniqname = args.uniqname
	password = args.password
	
	return uniqname, password
	
def get_auth_userinfo_from_directinput():
	print('> Enter Credentials <')
	print() 
	
	uniqname = input('uniqname: ')
	print()
	
	password = getpass.getpass(prompt='UMICH Level 1 Password: ')
	print()
	
	if uniqname == '':
		print('Error ...')
		print('Message: You did not enter a uniqname!')
		
	if password == '':	
		print('Error ...')
		print('Message: You did not enter a UMICH Level 1 password!')
		print()
		
		exit(1)
		
	return uniqname, password
	
def get_cyberark_auth_header(uniqname: str, password: str):
	print('> Authenticating ... <')
	print()
	
	cyberark_generic_header = {'content-type': 'application/json', 'accept': 'application/json'}
	cyberark_auth_userinfo_dict = {'username': uniqname, 'password': password}
	
	try:	
		cyberark_auth_token_string = do_webservice_request('POST', 'https://cyberark.its.umich.edu/PasswordVault/api/auth/RADIUS/Logon', cyberark_generic_header, cyberark_auth_userinfo_dict)
		
		cyberark_auth_header = cyberark_generic_header
		cyberark_auth_header['Authorization'] = cyberark_auth_token_string
		
		print('Success!')
		print()
		
		return cyberark_auth_header		 
	except: 
		print('Error ...')
		print('Message: There was a problem logging into CyberArk!')
		print()
		
		exit(1)
		
# This function uses a CyberArk object ID to retrieve the account, e.g., 84_3.
def output_cyberark_password(cyberark_auth_header: dict, cyberark_account: str):
	print('> Display or Save Password <')
	print()
	
	cyberark_password = do_webservice_request('POST', f'https://cyberark.its.umich.edu/PasswordVault/api/Accounts/{cyberark_account}/Password/Retrieve', cyberark_auth_header, {})

	output_cyberark_password_quit_flag = False
	
	while output_cyberark_password_quit_flag is False:
		print('d: Display the password on the screen')
		if pass_available is True: print('s: Save the password in the pass password store')
		print('r: Return to the main menu')
		print('!q: Exit the script')
		print()
		
		output_cyberark_password_input = input('Enter your choice: ')
		output_cyberark_password_choice = output_cyberark_password_input.lower()
		print()
		
		if output_cyberark_password_choice == 'd':	
			print(' Display Password '.center(50, "-"))
		
			if len(cyberark_password) > 0:		 
				print(' Success! '.center(50, '-'))
				print(f' {cyberark_password} '.center(50, "-"))
				
			else:	   
				print(' Error! '.center(50, "-"))
				
			print('-' * 50)
			print()
			
			output_cyberark_password_quit_flag = True
		elif output_cyberark_password_choice == 's':	  
			cyberark_password_pass_name_input = input('Enter the name of the password: ')
			print()
			
			try:
				password_store = passpy.Store()
				password_set = password_store.set_key(cyberark_password_pass_name_input, cyberark_password, force=True)
			
				print(' Save Password '.center(50, "-"))
			
				if password_set is None:		
					print(' Success! '.center(50, "-"))			 
				else:	   
					print(' Error! '.center(50, "-"))
				
				print('-' * 50)
				print()
			except:
				print('Error ...')
				print('Message: You do not have the pass password store configured!')
				print()
			
			output_cyberark_password_quit_flag = True
		elif output_cyberark_password_choice == 'r':
			output_cyberark_password_quit_flag = True
		elif output_cyberark_password_choice == '!q':
			return True
		else:   
			print('You did not choose d, s, r, or !q.')
			print()

def search_cyberark_accounts(cyberark_auth_header: dict):
	print('> Search for Accounts <')
	print()

	print('Search accounts: Enter a search term')
	print('r: Return to the main menu')
	print()
	
	search_cyberark_accounts_input = input('Enter your choice: ')
	print()
	
	search_cyberark_accounts_choice = search_cyberark_accounts_input.lower()
	
	if search_cyberark_accounts_choice == '':  
		print('You did not enter a search term.')
		print()
	elif search_cyberark_accounts_choice == 'r':
		pass
	else:
		search_cyberark_accounts_dict = do_webservice_request('GET', f'https://cyberark.its.umich.edu/PasswordVault/api/Accounts?search={search_cyberark_accounts_choice}', cyberark_auth_header, {})
		
		try:	
			search_cyberark_accounts_return_value = search_cyberark_accounts_dict['value']
		except:
			search_cyberark_accounts_return_value = []
		
		return search_cyberark_accounts_return_value

def main():	
	print()
	print('>> VaultPass <<')
	print('>> Search for CyberArk accounts, then display or save their passwords <<')
	print()
	
	if len(sys.argv) > 1:
		uniqname, password = get_auth_userinfo_from_commandline()		   
	else:   
		uniqname, password = get_auth_userinfo_from_directinput()

	cyberark_auth_header = get_cyberark_auth_header(uniqname, password)
	
	main_quit_flag = False
	main_choice = 's'
	
	while main_quit_flag is False:
		if main_choice == 's':		   
			cyberark_accounts = search_cyberark_accounts(cyberark_auth_header)
			
			if len(cyberark_accounts) == 0:
				print('Your search produced no results.')
				print()
			else:			   
				cyberark_account = choose_cyberark_account(cyberark_accounts)
				
				if not(cyberark_account is None):
					script_output_password_quit_flag = output_cyberark_password(cyberark_auth_header, cyberark_account)
					
					if script_output_password_quit_flag is True:
						script_quit_flag = True
	
		elif main_choice == '!q':
			main_quit_flag = True
		else:
			print('You did not choose s or !q.')
			print()
			
		if main_quit_flag is False:
			print('Do you want to search again for another account or exit the script?')
			print()		 
			print('s: Search again')
			print('!q: Exit the script')
			print()
			
			main_input = input('Enter your choice: ')
			main_choice = main_input.lower()
			
			print()
				
	print('>> Exit VaultPass <<')
	print()
			
	print('Buh-Bye Now! Y\'all have a GREAT DAY!')
	print()

if __name__ == "__main__":
	main()


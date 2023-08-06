#!python

DEFAULT_PASSPY_VAULT = 'umich'

try:
	import argparse
	import json
	import passpy
	import requests
	import sys
except Exception as e:
	print()
	print('Error ...')
	print('Message: Could not import the required modules, exiting script!')
	print()
	
	exit(1)

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
	parser = argparse.ArgumentParser(description='VaultPass Direct: Add one or more CyberArk account passwords to the pass password store')
	
	parser.add_argument('--uniqname', '-u', type=str, required=True, help='Your uniqname')
	parser.add_argument('--password', '-p', type=str, required=True, help='Your UMICH Level 1 password')
	parser.add_argument('--accounts', '-a', type=str, required=True, help='The colon-separated list of CyberArk accounts for which you want to retrieve passwords')
	parser.add_argument('--vault', '-v', type=str, required=False, help='The pass password store location where CyberArk account passwords will be added', default=DEFAULT_PASSPY_VAULT)
	
	args = parser.parse_args()
	
	username = args.uniqname
	password = args.password
	accounts = args.accounts
	vault = args.vault
	
	return username, password, accounts, vault

def get_cyberark_auth_header(username: str, password: str):
	print('> Authenticating ... <')
	print()
	
	cyberark_generic_header = {'content-type': 'application/json', 'accept': 'application/json'}
	cyberark_auth_userinfo_dict = {'username': username, 'password': password}
	
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
def output_cyberark_password(cyberark_auth_header: dict, account: str, cyberark_account: str, vault: str):
	cyberark_password = do_webservice_request('POST', f'https://cyberark.its.umich.edu/PasswordVault/api/Accounts/{cyberark_account}/Password/Retrieve', cyberark_auth_header, {})
	
	# print(f'Type: {type(cyberark_password)}')
	# print()
	
	# print(f'cyberark_password: {cyberark_password}')
	# print()
	
	if cyberark_password == '':
		print(f'Account \'{account}\': No password was found in CyberArk.')
	else:	
		try:
			password_store = passpy.Store()
			password_store.set_key(vault + '/' + account, cyberark_password, force=True)
			print(f'Account \'{account}\': The password was added to the pass vault {vault}.')
		except:
			print(f'Account \'{account}\': Could not save the password to the pass vault {vault}.')
		
def search_cyberark_account(cyberark_auth_header: dict, cyberark_account: str):
	cyberark_account_dict = do_webservice_request('GET', f'https://cyberark.its.umich.edu/PasswordVault/api/Accounts?search={cyberark_account}', cyberark_auth_header, {})
	
	# print(f'Type: {type(cyberark_account_dict)}')
	# print()
	
	# print(f'cyberark_account_dict: {cyberark_account_dict}')
	# print()
	
	try:	
		cyberark_account = cyberark_account_dict['value'][0]['id']
	except:
		cyberark_account = ''
	
	# print(f'cyberark_account: {cyberark_account}')
	# print()
		
	return cyberark_account

def main():	
	print()
	print('>> VaultPass Direct <<')
	print('>> Add one or more CyberArk account passwords to the pass password store <<')
	print()
	
	if len(sys.argv) > 1:
		username, password, accounts, vault = get_auth_userinfo_from_commandline()
	else:
		print()
		print('Error ...')
		print('Message: You did not supply any command line arguments!')
		print()
		print('Usage: vaultpass-direct.py')
		print('--uniqname uniqname')
		print('--password \'password\'')
		print('--accounts username:username:username ...')
		print('--vault vault')
		print()
		
		exit(1)
	
	cyberark_auth_header = get_cyberark_auth_header(username, password)

	accounts_split = accounts.split(':')
	
	print('> Retrieving and storing CyberArk account passwords ... <')
	print()
	
	for account in accounts_split:
		# print(account)
		# print()
		
		cyberark_account = search_cyberark_account(cyberark_auth_header, account)
		
		# print(f'cyberark_account: {cyberark_account}')
		# print()
		
		if cyberark_account == '':
			print(f'Account \'{account}\': Value not found.')
		else:
			output_cyberark_password(cyberark_auth_header, account, cyberark_account, vault)
		
		# print()
			
	print()
	print('>> Exit VaultPass Direct <<')
	print()
			
	print('Buh-Bye Now! Y\'all have a GREAT DAY!')
	print()

if __name__ == "__main__":
	main()


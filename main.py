import os
import csv
import string
import random
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SERVICE_ACCOUNT_FILE = 'service-account.json'
DOMAIN = 'your-company-domain.com'  # Replace with your domain
ADMIN_EMAIL = 'admin@your-company-domain.com'  # Replace with admin email
CSV_FILENAME = 'created_accounts.csv'

def generate_password(length=12):
    """Generate a random strong password"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(length))

def get_directory_service():
    """Authenticate and return directory service"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/admin.directory.user'],
        subject=ADMIN_EMAIL
    )
    return build('admin', 'directory_v1', credentials=credentials)

def create_account(service, base_username, index):
    """Create a single user account"""
    account_data = {
        "primaryEmail": f"{base_username}{index}@{DOMAIN}",
        "name": {
            "givenName": f"{base_username.capitalize()}",
            "familyName": f"{index}"
        },
        "password": generate_password(),
        "changePasswordAtNextLogin": True,
        "orgUnitPath": "/"
    }

    try:
        result = service.users().insert(body=account_data).execute()
        return {
            'email': result['primaryEmail'],
            'password': account_data['password'],
            'status': 'success'
        }
    except HttpError as error:
        return {
            'email': account_data['primaryEmail'],
            'password': account_data['password'],
            'status': f'error: {error.content.decode()}'
        }

def create_accounts(num_accounts, base_username):
    """Main account creation function"""
    service = get_directory_service()
    results = []
    
    for i in range(1, num_accounts + 1):
        result = create_account(service, base_username, i)
        results.append(result)
        print(f"Account {i}/{num_accounts}: {result['email']} - {result['status']}")
        time.sleep(1)  # Rate limit protection

    # Save results
    with open(CSV_FILENAME, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['email', 'password', 'status'])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nProcess completed. Results saved to {CSV_FILENAME}")

if __name__ == "__main__":
    try:
        num = int(input("Number of accounts to create: "))
        base = input("Base username (e.g., 'employee'): ").strip()
        
        if num < 1 or num > 1000:
            raise ValueError("Number must be between 1-1000")
            
        if not base.isalnum():
            raise ValueError("Username base must be alphanumeric")
            
        create_accounts(num, base)
        
    except ValueError as e:
        print(f"Input error: {str(e)}")
    except Exception as e:
        print(f"Fatal error: {str(e)}")

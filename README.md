---

### Implementation Steps:

1. **Enable Admin SDK API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to **APIs & Services** > **Library**
   - Search for "Admin SDK" and enable it

2. **Create Service Account**
   - In Cloud Console: **IAM & Admin** > **Service Accounts**
   - Create new service account with domain-wide delegation
   - Download JSON credentials

3. **Configure Domain-Wide Delegation**
   - In Google Workspace Admin Console:
     - **Security** > **API Controls**
     - Add new client ID (from service account)

4. **Set Required Scopes**
   - Ensure the service account has:
     - `https://www.googleapis.com/auth/admin.directory.user`

---

# Google Workspace Account Creator

## Setup Instructions

1. **Prerequisites**
   - Google Workspace Admin account
   - Domain-wide delegation enabled
   - Admin SDK API enabled

2. **Configuration**
   - Replace in `main.py`:
     - `DOMAIN`: Your organization's domain
     - `ADMIN_EMAIL`: Your admin email
   - Add valid `service-account.json`

3. **Installation**
   ```bash
   pip install -r requirements.txt

### Usage Example:
```bash
$ python main.py
Number of accounts to create: 5
Base username (e.g., 'employee'): staff

Account 1/5: staff1@your-domain.com - success
Account 2/5: staff2@your-domain.com - success
...
Process completed. Results saved to created_accounts.csv


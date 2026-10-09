# Page Turner

Page Turner is a Django-based book platform that brings together book browsing, digital reading, physical book rentals, and subscription management. It includes user authentication and Razorpay integration for payments.

The project demonstrates how multiple Django applications work together to handle users, books, rentals, subscriptions, and payment records.

## Features

### User Accounts
- User registration and login.
- User profiles.
- Authentication for account-based features.

### Book Management
- Browse available books and view their details.
- Add and edit book information.
- Display book cover images.
- Read uploaded PDF books using an integrated PDF.js viewer.

### Physical Book Rentals
- Request physical book rentals.
- Check subscription eligibility before renting.
- Track rental and return information.
- Manage rental requests through administrative pages.
- Calculate and manage late-return fines.

### Subscriptions
- View subscription plans.
- Maintain user subscription records.
- Check subscription validity when accessing rental features.

### Payments
- Razorpay payment integration.
- Payment and transaction records.

### Email Notifications
- Send email notifications using SendGrid.
- Use Mailinator inboxes to receive and verify test emails during development.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript, Django Templates |
| Local Database | SQLite |
| Payment Integration | Razorpay |
| PDF Viewer | PDF.js |
| Version Control | Git and GitHub |

## Project Structure

The repository contains an outer project folder and an inner `page_turner` directory containing `manage.py`.

| Path | Purpose |
|------|---------|
| `.gitignore` | Excludes local environments, secrets, database files, and uploaded media |
| `README.md` | Project overview and setup instructions |
| `page_turner/manage.py` | Django management commands |
| `page_turner/requirements.txt` | Python dependencies |
| `page_turner/page_turner/` | Django settings and main URL configuration |
| `page_turner/authentication/` | User authentication and profile functionality |
| `page_turner/books/` | Book models, views, and forms |
| `page_turner/rentals/` | Rental requests, returns, and fine management |
| `page_turner/subscriptions/` | Subscription plans and user subscriptions |
| `page_turner/payments/` | Payment integration and transaction records |
| `page_turner/templates/` | HTML templates |
| `page_turner/static/` | CSS, JavaScript, images, and PDF.js assets |

Each Django application's migration files are included in the repository.

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Akash-shaijan/Page-Turner.git
cd Page-Turner
```

### 2. Create a Virtual Environment

```bash
python -m venv env
```

Activate it using the command for your operating system.

**Windows PowerShell:**

```powershell
.\env\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
env\Scripts\activate.bat
```

**macOS or Linux:**

```bash
source env/bin/activate
```

### 3. Install Dependencies

Move into the directory containing `manage.py`:

```bash
cd page_turner
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the location expected by the project's configuration loader.

Environment variable names must match the names referenced in the source code. Check `settings.py` and the payment-related modules for calls such as `config(...)` or `os.getenv(...)`.

The following is an example only:

```dotenv
SECRET_KEY=replace_with_a_random_local_secret_key
RAZORPAY_KEY_ID=replace_with_your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=replace_with_your_razorpay_test_key_secret
```

Add any other variables required by the project's configuration.

Use Razorpay test credentials for local payment testing. Do not commit the `.env` file or place actual credentials in source code.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

This creates the database tables using the migration files included in the repository.

The original local SQLite database is excluded from Git, so a fresh installation starts with a new database.

### 6. Create an Administrator Account

```bash
python manage.py createsuperuser
```

Follow the terminal prompts to create an account for the Django administration panel.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

Open the Django administration panel:

```text
http://127.0.0.1:8000/admin/
```

## Initial Data

The repository includes application code and migrations. It does not include the original database or user-uploaded media.

After installation:

1. Create an administrator account.
2. Add books and subscription plans through the available management pages or Django admin, where registered.
3. Upload book covers and PDF files as required.
4. Create a regular user account to explore the user-facing features.
5. Configure Razorpay test credentials before testing payment flows.

Use books and other files that you have permission to upload and distribute.

## Typical User Flow

1. Register an account and log in.
2. Browse books and open a book's details.
3. View the available subscription plans.
4. Complete the applicable subscription payment flow.
5. Request a physical book rental.
6. Track the rental and return process.
7. Settle any applicable late-return fines.

Digital books can be opened through the integrated PDF viewer where available and permitted by the application.

## Static Files and Uploaded Media

The project handles two different types of files:

- **Static files:** Application assets such as CSS, JavaScript, icons, and PDF.js files. These are included in the repository.
- **Uploaded media:** Files such as uploaded book covers and PDFs. These are stored locally and excluded from Git.

A fresh clone will not contain previously uploaded books or cover images. Add new records and upload their associated files after setting up the database.

## Configuration and Security

- Keep secret values in environment variables.
- Keep `.env` excluded from version control.
- Use Razorpay test mode during development.
- Do not upload personal user data or payment credentials.
- Review Django settings before deploying the application.

The setup instructions above are intended for local development. Production deployment requires separate configuration for hosting, HTTPS, database access, static files, media storage, and application secrets.

## Useful Commands

Run these commands from the directory containing `manage.py`.

**Check Django configuration:**

```bash
python manage.py check
```

**Create migrations after changing models:**

```bash
python manage.py makemigrations
```

**Apply migrations:**

```bash
python manage.py migrate
```

**Run available tests:**

```bash
python manage.py test
```

**Start the development server:**

```bash
python manage.py runserver
```

## Author

**Akash Shaijan**

- GitHub: [Akash-shaijan](https://github.com/Akash-shaijan)
- Repository: [Page-Turner](https://github.com/Akash-shaijan/Page-Turner)

## Acknowledgements

- Django for the web framework.
- Razorpay for payment integration.
- Mozilla PDF.js for PDF rendering.
- The creators of the third-party frontend assets included in this project. Their applicable licenses remain in effect.
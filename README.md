```markdown
# Syrian Development Association – Aid Management API

A production‑grade Django REST Framework (DRF) backend powering the Syrian Development Association’s digital aid platform.  
The API serves two main audiences:

- **Administrative Dashboard** – For managers and staff to review, approve, and track beneficiary requests, manage aid categories, and monitor operational metrics.
- **User Portal** – For beneficiaries to request financial assistance, medical support, or funding for small business projects, and track application status.

## 🚀 Features
- Fully implemented with **Class‑Based Views (CBVs)** for clean, maintainable, DRF‑idiomatic architecture.
- Explicit read/write serializer separation for predictable data handling.
- Secure authentication and role‑based access control.
- POST‑based filtering and search for complex queries without breaking client compatibility.
- Secrets management via environment variables (no hard‑coded credentials).

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<Ranc0/Syrian-Development-Association.git
cd Syrian-Development-Association
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your_django_secret_key
DEBUG=True

EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_email@example.com...
```
> **Never commit `.env` to version control.** Add it to `.gitignore`.

### 5. Apply database migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```
The API will be available at:  
`http://127.0.0.1:8000/`
---

## 🔒 Security Notes
- All secrets are stored in environment variables.
- Use HTTPS in production.
- Rotate any credentials if they were ever committed to history.

---

## 📜 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
```

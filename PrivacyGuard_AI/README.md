# PrivacyGuard AI — Personal Data Exposure Monitor

PrivacyGuard AI is a portfolio-focused cybersecurity web application that demonstrates privacy-risk analysis, permission-risk assessment, machine-learning risk classification, personalized security recommendations, and local scan history.

> **Portfolio/demo limitation:** Exposure findings in this version are simulated. The application does **not** query real breach databases or the dark web, and it does not collect passwords, OTPs, or payment information.

## Features

- Privacy score calculation
- Simulated email/phone exposure analysis
- Machine-learning risk classification using scikit-learn
- Personalized security recommendations
- Application permission risk checker
- SQLite scan history
- REST API endpoints
- Responsive cybersecurity dashboard
- Exposure trend visualization with Chart.js

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **AI/ML:** scikit-learn, Logistic Regression
- **Database:** SQLite
- **Visualization:** Chart.js

## Project Structure

```text
PrivacyGuard-AI/
├── app.py
├── ml_model.py
├── recommendations.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/PrivacyGuard-AI.git
cd PrivacyGuard-AI
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

The SQLite database is created automatically as `privacyguard.db` and is ignored by Git.

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/scan` | POST | Analyze demo exposure data and return risk results |
| `/api/history` | GET | Return recent local scan history |
| `/api/permissions` | POST | Analyze application permission risk |

## Example Demo Input

Use non-sensitive test data such as:

```text
Email: demo@example.com
Phone: 9876500000
```

Do not enter real passwords, OTPs, payment details, or other sensitive credentials.

## Machine Learning Component

The project includes a small synthetic training dataset and a Logistic Regression classifier. The model converts exposure indicators into a low/medium/high risk assessment. This is an educational portfolio implementation rather than a production security model.

## Security & Privacy Notes

- No passwords or OTPs are requested.
- No real breach or dark-web lookup is performed.
- Demo exposure results are generated locally.
- For production use, a verified breach-data provider, authentication, rate limiting, secure secrets management, HTTPS, and stronger model validation would be required.

## Future Scope

- Integrate a legitimate breach-notification API where permitted
- Add user authentication and secure account management
- Add PostgreSQL for production persistence
- Improve model training with validated datasets
- Add automated security reports
- Deploy with a production WSGI server and HTTPS

## Disclaimer

PrivacyGuard AI is an educational cybersecurity portfolio project. It is not a real breach-monitoring or threat-intelligence service.

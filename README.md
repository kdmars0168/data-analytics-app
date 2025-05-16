# HealthWhisper

A data analytics web application that allows users to upload personal datasets, view insightful automated visualizations, and selectively share results with trusted users.

---

## ✨ Purpose and Design

## Health Data Analytics App

### Purpose

- Help users make sense of their personal health data through automated analysis and visualization.
- Enable secure and selective sharing of health insights with trusted individuals (e.g., doctors, family).

### Design & Features

- **Frontend**: Clean, responsive interface built with **HTML**, **TailwindCSS**,**CSS** and **JavaScript** (with some **jQuery**).
- **Backend**: Developed using **Flask** with **SQLAlchemy ORM** and an **SQLite** database.
- **User Capabilities**:
  - Register and manage a personal account.
  - Upload CSV files containing health data (e.g., steps, sleep hours, mood).
  - Automatically generate **bar**, **line**, and **pie charts** to visualize trends.
  - Manage sharing preferences for individual data types.
- **Focus Areas**:
  - Simplicity and clarity in user interaction.
  - Strong data **privacy** and **selective sharing**.
  - **Mobile-responsive** design for cross-device accessibility.

---

## 👥 Group Members

| UWA ID   | Name               | GitHub Username |
| -------- | ------------------ | --------------- |
| 24117314 | Mohaimen Al Rashid | kdmars0168      |
| 24343523 | Boyu Shen          | Ethan-zzz-zzz   |
| 24103568 | Silvia Gao         | SilviaRuth      |

---

## 🚀 How to Launch the Application

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/data-analytics-app.git
   cd data-analytics-app
   ```

2. **Create a Python virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On MacOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations** (only first time):

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db migrate -m "Add Dataset table"
   flask db upgrade
   ```

6. **Launch the application**:

   ```bash
   python run.py
   ```

7. **Open the app in your browser**:
   ```
   http://127.0.0.1:5000/
   ```

---

Unit tests are designed to verify the correctness of individual functions, methods, or modules in isolation without relying on a browser or UI. They are lightweight and fast to run, usually focusing on the business logic or backend code. Unit tests are commonly written using testing frameworks such as pytest and can be executed quickly to catch regressions early in the development cycle.
`pytest tests -v`

Selenium tests, on the other hand, automate real user interactions within a web browser to test the frontend functionality and user interface. These tests simulate actions like logging in, navigating pages, uploading files, and submitting forms, ensuring that the whole application behaves as expected from the user’s perspective. While more comprehensive, Selenium tests require a configured browser environment and are slower to run compared to unit tests.
`pytest tests_selenium -v`

---

## 📂 Project Structure

```
data-analytics-app/
│
├── app/
│ ├── init.py # App factory
│ ├── forms.py # WTForms definitions
│ ├── models.py # SQLAlchemy models
│ ├── routes.py # Flask routes/views
│ ├── utils.py # Utility functions
│ ├── new_utils.py # (Additional helper logic)
│ ├── static/
│ │ ├── css/ # Tailwind/CSS styles
│ │ ├── js/ # Custom JS scripts
│ │ │ ├── dashboard.js
│ │ │ ├── main.js
│ │ │ ├── share.js
│ │ │ ├── shared_with_me.js
│ │ │ └── upload.js
│ │ └── assets/ # Image/assets if used
│ ├── uploads/ # Sample CSVs for dev/test
│ │ ├── sample.csv
│ │ ├── sample_valid.csv
│ │ └── ...
│ └── templates/
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── profile.html
│ ├── edit_profile.html
│ ├── upload.html
│ ├── dashboard.html
│ ├── shared_with_me.html
│ ├── share.html
│ └── partials/
│ └── sidebar.html
│
├── instance/
│ └── app.db # Local SQLite DB
│
├── migrations/ # Alembic DB migrations
│ ├── versions/
│ ├── env.py
│ ├── README
│ └── script.py.mako
│
├── tests/ # Unit tests (uses in-memory DB)
│ ├── conftest.py
│ ├── test_routes.py
│ ├── test_models.py
│ ├── test_upload.py
│ ├── test_utils.py
│ ├── ...
│ └── uploads/ # CSV files for testing uploads
│
├── tests_selenium/ # Selenium UI tests
│ ├── conftest.py
│ ├── test_login.py
│ ├── test_register.py
│ ├── test_profile.py
│ ├── test_upload.py
│ ├── test_dashboard.py
│ └── uploads/ # Selenium test CSVs
│
├── venv/ # Virtual environment (excluded via .gitignore)
├── config.py # App configuration
├── run.py # App entry point
├── requirements.txt # Pip dependencies
├── create_demo_user.py # (Optional: setup script)
├── .gitignore
└── README.md
```

---

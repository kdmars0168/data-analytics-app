
# DataWhisper

A data analytics web application that allows users to upload personal datasets, view insightful automated visualizations, and selectively share results with trusted users.

---

## ✨ Purpose and Design

- **Purpose**: 
  - To help users better understand their private data by providing automated visualization and analysis tools.
  - To allow secure and selective sharing of insights with trusted individuals.
  
- **Design and Use**:
  - The application features a clean, intuitive frontend built with HTML, TailwindCSS, and JavaScript (with some JQuery).
  - The backend uses Flask with SQLAlchemy ORM connected to an SQLite database.
  - Users can create an account, upload CSV files, visualize patterns (using bar, line, pie charts), and manage sharing settings.
  - Strong focus on privacy, simplicity, and user experience.
  - Mobile responsive design ensures accessibility across devices.

---

## 👥 Group Members

| UWA ID   | Name               | GitHub Username   |
|----------|--------------------|-------------------|
| 24117314 | Mohaimen Al Rashid  | kdmars0168         |
| 24343523 | Boyu Shen           | Ethan-zzz-zzz |
| 24103568 | Silvia Gao          | (GitHub username pending) |

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

## 🧪 How to Run Tests

(Currently, testing is manual.)

- After launching the application, manually verify:
  - User registration
  - User login
  - Data upload
  - Data visualization
  - Data sharing functionality

(Automated tests can be added later using `pytest`.)

---

## 📂 Project Structure 

```
data-analytics-app/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── utils.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── upload.html
│       ├── visualize.html
│       └── share.html
│
├── migrations/
│
├── instance/
│   └── app.db
│
├── venv/ (virtual environment — not pushed to GitHub)
│
├── config.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

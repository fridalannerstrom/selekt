# Cleo – Candidate Management for Recruiters

Cleo is a web-based tool designed to help recruiters structure and store all information about their candidates in one place. The project was developed as part of the Full Stack Developer Diploma and focuses on simple, accessible candidate data management.

---

## 🔍 Project Purpose

In many recruitment processes, information about candidates is scattered – resumes in folders, interview notes in Word, test results in PDFs, and feedback in email threads. Cleo solves this by acting as a digital "candidate binder" where everything can be organized and accessed through one interface.

---

## 👤 Target Audience

Recruiters and HR professionals who work with multiple candidates and need a structured, user-friendly tool to manage their pipeline.

---

## ⚙️ Included Features

- User login and authentication (admin via Django)
- Candidate list overview
- Create candidates via admin
- Candidate model with:
  - Name
  - Email
  - Notes
  - Top skills (comma-separated)
  - Upload date
- Responsive frontend using Bootstrap
- Custom static file support (`assets/` folder for CSS/JS)
- Homepage using `index.html` with routing to candidate views

---

## 🛠️ Technologies

- Python 3.12
- Django 5.2
- HTML, CSS, Bootstrap 5
- JavaScript
- SQLite (local development)
- Django Templates
- Git & GitHub

---

## 📁 Project Structure

```
cleo-school/
├── candidates/           # Django app for candidate data
├── cleoproject/          # Project configuration
├── templates/            # HTML templates
├── assets/               # Custom static files (CSS/JS)
│   ├── css/
│   └── js/
├── db.sqlite3            # Database
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started (Local)

1. Clone the repo:
```bash
git clone https://github.com/your-username/cleo-school.git
cd cleo-school
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

5. Visit `http://127.0.0.1:8000/` in your browser

---

## 🔐 Create Superuser (for admin)

```bash
python manage.py createsuperuser
```

---

## ✅ Status

- [x] Basic project structure ready
- [x] Authentication and admin
- [x] Candidate model implemented
- [x] Bootstrap and custom static files connected
- [x] Templates for index and candidate list created
- [ ] Add candidate via frontend form
- [ ] File uploads (CVs/test results)
- [ ] Role-based permissions
- [ ] Testing and README improvements

---

## 📌 TODO (Next Steps)

- Frontend form for adding candidates
- File uploads for documents (CV, test results)
- Candidate detail views
- Filtering/search functionality
- Testing and deployment readiness
- Deploy to Render

---

## ✍️ Author

This project was created by **Frida Lannerström** as part of Portfolio Project 4 in the Full Stack Developer Diploma at Code Institute.

---

## Daily log

### April 15

✅ What I did today
Reflected on the project scope and decided to split Cleo into two parts:
a school-appropriate version (cleo-school) and a more advanced product version (cleo-pro) for future development and commercial use.

Created a new GitHub repository (cleo-school) and started fresh to keep the school project focused and clean.

Set up a new Django project with virtual environment, Django installation, and initial server test.

Created the candidates app to manage candidate data.

Built the initial Candidate model with the following fields:

name, email, notes, top_skills (comma-separated), and uploaded_at.

Performed migrations to set up the database using SQLite.

Registered the model in the Django admin panel and verified that it works.

Created a candidate_list view and connected it via a new urls.py.

Built a set of templates: base.html, index.html, candidate_list.html, and login.html.

Integrated Bootstrap via CDN for responsive design and created a custom assets/ folder for CSS and JavaScript files.

Configured STATICFILES_DIRS in Django to serve custom static assets.

Created both Swedish and English versions of the project README.md file with full structure and project documentation.

💡 Why I did it
To meet the school’s requirements with a simplified version of my broader product idea.

To stay within the scope of a realistic and testable full-stack MVP.

To keep the school version clean, modular, and easier to document, test, and submit.

To establish good habits around structure, reusability, and version control from day one.

🤔 Challenges and reflections
Letting go of the earlier version and previous commits was tough, but starting fresh has been freeing and helpful.

Had a minor issue with activating the virtual environment on Windows, which I resolved by using the correct script path.

Realized the importance of focusing on core functionality and resisting feature creep – the simpler version is not only easier to build but likely to get a better grade.

📌 Next up
Build a frontend form for adding candidates

Add file upload functionality (CVs, test results)

Implement detail views for each candidate

Introduce role-based access

Prepare for testing and deployment

💬 Keeping this log directly in the README helps me stay focused and track decisions and progress. It will likely be removed or moved later.
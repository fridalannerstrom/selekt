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

## 🔄 Agile Working Methodology

This project is developed using an **Agile-inspired workflow** with GitHub Projects.

All functionality is broken down into **user stories**, written from the user's perspective in the format:

> *As a user, I want to... so that...*

Each user story includes:
- **Type:** User Story or Epic Story
- **Priority:** Assigned using the [MoSCoW method](https://en.wikipedia.org/wiki/MoSCoW_method) (Must Have, Should Have, Could Have, Won’t Have)
- **Acceptance Criteria:** Clear conditions to define when a story is complete

I use **GitHub Projects (Kanban board view)** to visually organize and track my work:
- `Backlog`: All user stories and epics are added here initially
- `Ready`: Tasks that are prioritized and ready to begin
- `In Progress`: Tasks currently being worked on
- `In Review`: Stories ready for testing or feedback
- `Done`: Completed work

### 🏷️ Labels
Each issue is tagged with:
- **Type** (e.g., `user story`, `epic story`)
- **Priority** (e.g., `must-have`, `should-have`)

### 🧩 Epic Stories
Larger themes are grouped into *epic stories*. Each epic includes links to related user stories and acts as a checklist of progress.  
Example epics: `User Authentication`, `Candidate Management`, `File Uploads`.

This structure helps me:
- Keep focus and prioritize correctly
- Demonstrate planning and iterative work
- Track progress clearly, even on a solo project

---


## Daily log

### April 15

#### ✅ What I did today

- Reflected on the project scope and decided to split Cleo into two parts:  
  a school-appropriate version (`cleo-school`) and a more advanced product version (`cleo-pro`) for future development and commercial use.
- Created a new GitHub repository (`cleo-school`) and started fresh to keep the school project focused and clean.
- Set up a new Django project with virtual environment, Django installation, and initial server test.
- Created the `candidates` app to manage candidate data.
- Built the initial `Candidate` model with the following fields:
  - `name`, `email`, `notes`, `top_skills` (comma-separated), and `uploaded_at`.
- Performed migrations to set up the database using SQLite.
- Registered the model in the Django admin panel and verified that it works.
- Created a `candidate_list` view and connected it via a new `urls.py`.
- Built a set of templates: `base.html`, `index.html`, `candidate_list.html`, and `login.html`.
- Integrated Bootstrap via CDN for responsive design and created a custom `assets/` folder for CSS and JavaScript files.
- Configured `STATICFILES_DIRS` in Django to serve custom static assets.
- Created both Swedish and English versions of the project `README.md` file with full structure and project documentation.

---

#### 💡 Why I did it

- To meet the school’s requirements with a simplified version of my broader product idea.
- To stay within the scope of a realistic and testable full-stack MVP.
- To keep the school version clean, modular, and easier to document, test, and submit.
- To establish good habits around structure, reusability, and version control from day one.

---

#### 🤔 Challenges and reflections

- Letting go of the earlier version and previous commits was tough, but starting fresh has been freeing and helpful.
- Had a minor issue with activating the virtual environment on Windows, which I resolved by using the correct script path.
- Realized the importance of focusing on core functionality and resisting feature creep – the simpler version is not only easier to build but likely to get a better grade.

---

#### 📌 Next up

- Build a frontend form for adding candidates
- Add file upload functionality (CVs, test results)
- Implement detail views for each candidate
- Introduce role-based access
- Prepare for testing and deployment

### April 16

#### ✅ What I did today

- Created a signup page with Django's `UserCreationForm`, custom template, and post-signup redirection to dashboard.
- Enabled **automatic login after signup** using `login(request, user)`.
- Fixed URL issues: adjusted routing so dashboard is at `/dashboard/` instead of `/candidates/dashboard/`.
- Ensured login and signup redirects work using `LOGIN_REDIRECT_URL` and `LOGIN_URL` in `settings.py`.
- Created a form (`CandidateForm`) and view (`add_candidate`) for adding new candidates via the frontend.
- Built a template `add_candidate.html` with Bootstrap layout and connection to dashboard.
- Improved the dashboard layout with a list of candidates and connection to "Add Candidate" functionality.
- Added a `user` field to the `Candidate` model to ensure that candidates are linked to the logged-in user.
- Updated the dashboard view to only show candidates for the currently logged-in user.
- Handled `IntegrityError` and migration issues caused by the new `user` field by resetting migrations and database when needed.
- Verified candidate privacy: users now only see their own added candidates.

---

#### 💡 Why I did it

- To build a real MVP-level system where users can manage their own data securely.
- To prepare the project for individual user accounts and future features like uploads, file attachments, etc.
- To learn best practices around Django forms, models, and user authentication.

---

#### 🤔 Challenges and reflections

- Encountered an issue where the wrong `login()` function was used (naming conflict with a view) – solved by renaming the view and importing Django’s login method.
- Faced migration errors due to the new `user` field, but resolved them through a full reset of the database and migrations.
- Important realization: Form fields like `user` should not be exposed in the form, but handled manually in the view.

---

#### 📌 Next up

- Implement file upload support for CVs and test results
- Display uploaded files in the candidate detail view
- Improve candidate list and dashboard with more metadata and styling
- Add edit/delete functionality for candidates


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

---

### April 19

#### Completed Features & Stories

##### 🔐 User Authentication (Epic Completed)
- ✅ User signup with validation and automatic login
- ✅ User login redirects to dashboard, with clear error messages on failure
- ✅ User logout redirects to homepage
- ✅ Dashboard access is restricted to logged-in users only

##### 👤 Candidate Management (Epic In Progress)
- ✅ Candidate list displays name, email, and top skills (only current user's candidates)
- ✅ Clicking a candidate opens their detailed profile
- ✅ Candidate detail view is protected — users cannot access other users’ data
- ✅ Edit candidate functionality implemented using a form

##### ⚠️ Custom 404 Page
- ✅ Custom 404 page shown when trying to access a candidate that doesn’t belong to the user
- ✅ Helpful message: “This candidate does not belong to you.”

#### 🔧 Technical Improvements

- ✅ Switched to Django **class-based generic views**:
  - `ListView`, `DetailView`, `CreateView`, `UpdateView`
  - `get_queryset()` and `get_object()` properly scoped to current user
- ✅ **URL structure cleaned up**:
  - Most routes now live in `candidates/urls.py`
  - Project-level `urls.py` simplified
  - Removed duplicate route definitions

#### ✅ Testing & Verification
- All user flows in the **User Authentication** epic tested and verified
- Candidate list and detail views only show current user's data
- All redirects, logins, logouts, and access restrictions confirmed working

### April 25

#### Design changes
- The current template is too much "dashboard" and will be to much for this project.. 
- Decided to build my own template with Bootstrap. Custom CSS etc. Based on sketches in Adobe XD.

#### Features implemented:
Grid layout of candidate cards with dynamic data from the database, showing name, title, email, and top skills.

Candidate profile modal popup, displaying full profile info (name, contact, skills, notes, etc.) without leaving the page.

Animated slide-up modal from the bottom of the screen – 90% height, 80% width, scrollable.

Separate delete confirmation modal – centered, small, no dark backdrop, and closes when clicking outside.

Delete functionality via JavaScript, correctly linked to each candidate and confirmed before deletion.

Improved routing & user protection – candidate view/edit/delete only accessible to the associated user.

Layout and animation improvements for both modals; responsive positioning and UI polishing.

GitHub comments added to reflect current status and what remains on each relevant user story.

#### Still to do / improve:
Candidate profile layout needs further design polish.

More data fields (education, work experience, links, etc.) to be added to the model and views.

Delete button currently only available in candidate profile view – not yet in list/grid view.


### April 26

Today's Focus:
Major improvements to the Candidate Form layout, editing experience, and user interactions.

Tasks Completed:

Rebuilt the Candidate Form with a modern WYSIWYG editor for fields like Profile, Work Experience, Education, and Other (using Trumbowyg).

Added skills input with Tagify for a smoother and faster skills management experience.

Redesigned the Links section: planned a dynamic system where users can add multiple link buttons (e.g., GitHub, LinkedIn) easily.

Improved the visual layout of the form:

Main fields (Profile, Work experience, etc.) on the left side

Contact info, Skills, and Links on the right side

Created a new system to display success messages when a candidate is saved (using Django's message framework).

Improved handling of profile image uploads and preview.

Fixed formatting issues when displaying rich text content on the Candidate profile view.

Simplified the backend by moving data parsing logic into forms.py (instead of creating new templatetags).

Made the links system functional (split name:::url pairs cleanly).

Prepared dynamic frontend scripts for adding new skills and links.

Branch:

All work was done in a separate feature branch to keep main branch clean and stable.

Challenges:

Initial issues with WYSIWYG toolbar not displaying (solved by loading Trumbowyg in correct order).

Some minor TemplateSyntaxErrors when simplifying link management without custom tags (solved by moving logic into form class).

Next steps (optional):

Fine-tune the dynamic "add link" system (e.g., edit/remove individual links directly in the form).

Add better validation for links and skills.

Polish the design of the skill and link components.


# ✅ Project 4 Distinction Checklist

## 1. Planning & UX/Design
- [ ] Use an Agile tool (e.g., GitHub Projects) to plan the project.
- [ ] Create and document Epics → User Stories → Tasks.
- [ ] Define clear User Acceptance Criteria.
- [ ] Design wireframes, mockups, and document UX work.
- [ ] Follow UX design principles and accessibility guidelines (WCAG).
- [ ] Ensure the website is fully responsive.
- [ ] Organize information according to Information Hierarchy.
- [ ] Create intuitive and user-friendly navigation.

## 2. Frontend
- [ ] Use semantic HTML and clean CSS.
- [ ] Validate HTML/CSS with W3C/Jigsaw validators.
- [ ] Link JavaScript correctly and validate it.
- [ ] Link CSS in `<head>` and JavaScript at the bottom of `<body>`.
- [ ] Avoid aggressive pop-ups or autoplaying media.

## 3. Backend (Python/Django)
- [ ] Follow MVC (Model-View-Template) architecture correctly.
- [ ] Create at least one custom model and document it.
- [ ] Implement full CRUD functionality (Create, Read, Update, Delete).
- [ ] Display immediate feedback on data changes.
- [ ] Implement forms with correct validation.
- [ ] Write robust Python code following PEP8 standards.
- [ ] Ensure secure data handling and clear error messages.

## 4. Authentication and Permissions
- [ ] Implement user registration and login.
- [ ] Use role-based permissions (e.g., admin vs. user).
- [ ] Prevent unauthorized access to protected pages.
- [ ] Display current login state to the user.

## 5. Testing
- [ ] Create Python tests for critical functionality.
- [ ] Create JavaScript tests where relevant.
- [ ] Document all tests in the README.
- [ ] Document found bugs, fixes, and any unfixed bugs.

## 6. Git and Version Control
- [ ] Use Git continuously with small and clear commits.
- [ ] No passwords or secrets included in the code (use `.gitignore`).
- [ ] Write meaningful commit messages.
- [ ] Handle requirements.txt and version branches properly.

## 7. Deployment
- [ ] Deploy the app to a cloud platform (e.g., Render, Heroku).
- [ ] Set `DEBUG = False` in the deployed version.
- [ ] Store secrets securely (environment variables).
- [ ] Provide clear deployment documentation in README.
- [ ] Remove commented-out code and broken links.

## 8. Code Quality
- [ ] Ensure consistent, readable code (indentation, naming conventions).
- [ ] Name all files and folders consistently without spaces or capitals.
- [ ] Include clear comments in all custom code files.
- [ ] Maintain a clean file structure (separate folders for CSS, JS, templates).

## 9. README.md
- [ ] Write README in English, structured with Markdown.
- [ ] Include:
  - Project description and purpose
  - How to clone/run the project
  - Features and User Stories
  - Database model/schema
  - Testing documentation
  - Deployment process
  - Security practices

## 10. Extra for Distinction
- [ ] Ensure the project is original (not a walkthrough copy).
- [ ] Create a professional-grade UI and clean code structure.
- [ ] Provide immediate feedback for all user actions.
- [ ] Demonstrate high-level "craftsmanship" in code.
- [ ] Implement strong security features (API error handling, form validation, 404 pages).
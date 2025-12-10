# Personal Finance Tracker – DevOps CI/CD Project

The Personal Finance Tracker is a simple full-stack web application that helps users record daily expenses and visualize their spending.

This project showcases a complete end-to-end CI/CD pipeline designed to build, test, and deploy a fully functional web application along with its cloud infrastructure. We developed a simple full-stack app with a frontend, backend APIs, and a database, then automated the entire workflow using modern DevOps tools such as Git, GitHub, IaC (Terraform), and a CI/CD orchestration tool.

The project demonstrates real-world practices like branching strategy, pull requests, automated testing, code scanning, and cloud deployment. It also includes logging, monitoring, and documentation to ensure reliability and visibility.

## Task 1 — Application Development (Backend, Frontend, Database)

This task focuses on building the core application that will later be deployed through our CI/CD pipeline. We developed a simple Personal Finance Tracker where users can add, view, and delete expenses, while also viewing a real-time summary and spending breakdown. The backend uses FastAPI with SQLite for data storage, and the frontend is built using HTML, CSS, and JavaScript.

📌 1. What We Built

We created a working full-stack mini-application that acts as the foundation for our CI/CD pipeline. It includes a clean frontend UI, a FastAPI backend service with multiple REST endpoints, and an SQLite database to persist expense records. The app is small and simple but fully functional, making it ideal for demonstrating automation.

📌 2. Backend API Overview

The backend exposes essential REST APIs for adding, retrieving, summarizing, and deleting expenses. All operations connect directly to the SQLite database using SQLAlchemy ORM. A basic health check endpoint is also included for CI/CD and monitoring.

📌 3. Frontend Overview

The frontend provides an easy-to-use layout with an “Add Expense” form, a scrollable expense list, a spending summary, and a dynamic pie chart visualizing category-wise spending. It interacts with the backend using JavaScript Fetch API.

📌 4. How to Run the Application Locally

Follow these steps to run both backend and frontend.

▶️ Step 1: Clone the Repository
```
git clone https://github.com/Deepak-Tamizhalagan/finance-tracker.git
cd finance-tracker
```

▶️ Step 2: Create & Activate Virtual Environment
```
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
```

▶️ Step 3: Install Backend Requirements
```
pip install -r requirements.txt
```

▶️ Step 4: Start the FastAPI Server
```
uvicorn app.main:app --reload
```

If successful, you will see:
```
http://127.0.0.1:8000
```
![Backend Screenshot](docs/images/image.png)

```
http://127.0.0.1:8000/expenses
```
![Expense API Screenshot](docs/images/image-2.png)

```
http://127.0.0.1:8000/expenses/summary
```

![Summary API screenshot](docs/images/image-3.png)

```
http://127.0.0.1:8000/docs
```
![Swagger Screenshot](docs/images/image-4.png)

▶️ Step 5: Open the Frontend

Navigate to:
```
finance-tracker/frontend/index.html
```

Right-click → Open with Live Server

![Frontend Screenshot](docs/images/image-1.png)

📌 5. Expected Behavior

Once both backend & frontend are running:

✔️ Add an expense → Instantly stored in database

✔️ Expense list updates without reload

✔️ Summary updates live

✔️ Chart updates dynamically

✔️ Delete button removes item instantly

### Overview

As part of the capstone project, I implemented the CI/CD pipeline and basic infrastructure monitoring for the **backend** service.

My scope covers:

- **Task 4 – CI/CD pipeline** for backend tests and infrastructure deployment
- **Task 6 – Monitoring & logging** of the deployed AWS resources

Tools used:

- GitHub Actions (CI/CD)
- Python + pytest + pytest-cov
- Terraform (IaC)
- AWS S3 (deployment / logs bucket)
- AWS CloudWatch (dashboard + alarms)

---

### Related Repository Structure

- `.github/workflows/backend-ci.yml`  
  CI/CD workflow for the backend and infrastructure.

- `backend/`  
  FastAPI backend, unit/integration tests live under `backend/tests/`.

- `infra/`  
  Terraform configuration:
  - `main.tf` – S3 bucket for finance-tracker logs/assets  
  - `variables.tf` – AWS region configuration  
  - `monitoring.tf` – CloudWatch dashboard and alarm

---

### CI/CD Pipeline Design (GitHub Actions)

Workflow file: **`.github/workflows/backend-ci.yml`**

The pipeline runs automatically on:

- `push` to:
  - `main`
  - `feature/**`
  - `zafar-*`
  - `zafar-9027671`
- `pull_request` targeting `main`

**Stages:**

1. **Source Stage – Checkout**
   - Uses `actions/checkout@v4` to fetch the repository code.

2. **Build / Setup Stage**
   - Uses `actions/setup-python@v5` with Python 3.11.
   - Installs backend dependencies:
     - `pip install -r requirements.txt`
     - `pip install pytest pytest-cov`

3. **Test Stage – Automated tests + coverage**
   - Runs pytest from the `backend/` folder:
     ```bash
     pytest --cov=. --cov-report=xml:coverage.xml --cov-report=term
     ```
   - Ensures at least **5 tests** pass.
   - Generates an XML coverage report for artifacts and reporting.

4. **Build / Validate Infrastructure Stage**
   - Runs `terraform init` and `terraform validate` in the `infra/` directory.
   - Confirms the Terraform templates are syntactically and logically valid.

5. **Deploy Stage – Deploy infrastructure to AWS**
   - Uses `terraform apply -auto-approve` to deploy:
     - S3 logs bucket for the finance-tracker project
     - CloudWatch dashboard
     - CloudWatch alarm
   - This stage is fully automated and runs inside the pipeline.

6. **Artifacts**
   - Uploads `backend/coverage.xml` as a build artifact named **`backend-coverage`**.

This end-to-end flow satisfies the assignment requirement for a CI/CD pipeline with
Source → Build → Test → Deploy stages and automated triggers on branch updates.

---
### Monitoring & Logging (Task 6)

Monitoring is implemented using **AWS CloudWatch** and **Terraform**.

Deployed resources:

- **CloudWatch Dashboard – `finance-tracker-dashboard`**
  - Visualizes:
    - `BucketSizeBytes` (S3 bucket size)
    - `AllRequests` / request traffic to the S3 bucket
  - Used to monitor storage growth and request activity for deployment artifacts.

- **CloudWatch Alarm – `finance-tracker-s3-4xx-errors`**
  - Metric: `AWS/S3 – 4xxErrors` for the finance-tracker S3 bucket.
  - Condition: alarm when `4xxErrors >= 1` within a 5-minute period.
  - Purpose:
    - Detect misconfigured permissions or bad application/deployment configuration.
    - If deployments start failing or the app cannot access S3, 4xx errors increase and this alarm highlights it.

Together, the dashboard and alarm provide visibility into the health of the deployment and help troubleshoot issues by correlating request errors with recent changes.

---

### How to Run Tests Locally

From the `backend/` directory:

```bash
python -m pip install -r requirements.txt
pip install pytest pytest-cov

pytest --cov=. --cov-report=term

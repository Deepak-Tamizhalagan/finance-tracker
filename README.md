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

## 📸 Task 4 – CI/CD Pipeline Evidence

Below screenshots provide proof of automated testing and deployment workflow.

### 4.1 – Local Backend Tests Passed
All unit tests executed successfully before committing changes.  
👉 <img width="897" height="294" alt="Screenshot 2025-12-05 173222" src="https://github.com/user-attachments/assets/f43d1867-e70b-4e91-a0c0-583872b7698b" />



---

### 4.2 – GitHub Actions – Tests with Coverage Success
Automated test stage executed in CI/CD pipeline.  
👉 <img width="1735" height="902" alt="Screenshot 2025-12-05 174818" src="https://github.com/user-attachments/assets/55ce16ae-c237-457d-bc43-d0bf1f3447f8" />
<img width="1070" height="743" alt="Screenshot 2025-12-10 120816" src="https://github.com/user-attachments/assets/6211077b-3799-4fde-be5a-39e141ff8642" />



---

### 4.3 – Terraform Validation Stage Success
Infrastructure validation completed before deployment.  
👉 <img width="506" height="462" alt="Screenshot 2025-12-10 122609" src="https://github.com/user-attachments/assets/71d108aa-3eb3-4982-8330-fa440f28db37" />


---

### 4.4 – Deploy Infrastructure to AWS
Terraform successfully deployed AWS resources.  
👉 <img width="466" height="401" alt="Screenshot 2025-12-10 122930" src="https://github.com/user-attachments/assets/d19aefef-cb17-4086-a7aa-3ea852b777c3" />

---

### 4.5 – Full Pipeline Successful Run
Pipeline executed all stages without errors.  
👉 <img width="1849" height="634" alt="Screenshot 2025-12-10 121119" src="https://github.com/user-attachments/assets/7810dd06-4dbe-4219-8a37-19bcd5fe26f7" />


---

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
## Task-2 – Infrastructure as Code (Terraform)

 Deployed the complete infrastructure for Personal Finance Tracker application using Terraform on AWS. The goal of this task was to automate backend hosting, networking, security, and static frontend deployment by using Infrastructure-as-Code instead of manually configuring AWS services. Terraform helped me create everything in a reproducible way using .tf templates.

 What I built

+ Using Terraform, I provisioned the following AWS resources automatically:

+ VPC

+ Public Subnet

+ Internet Gateway

+ EC2 instance (Ubuntu) to run FastAPI backend

+ Security Group for port 8000 & SSH

+ S3 bucket to host frontend website

+ CloudFront distribution to serve frontend globally

Terraform also prints useful outputs such as:

+ EC2 Public IP

+ S3 bucket name

+ CloudFront domain

<img width="437" height="190" alt="image" src="https://github.com/user-attachments/assets/697683f0-0362-42a1-9589-e15fcc4480eb" />


### Backend Deployment

After Terraform created the EC2 instance:

+ I SSH-ed into the instance,

+ installed Python and FastAPI,

+ activated virtual environment,

+ and started Uvicorn on port 8000

Finally, I tested the backend using:

```
curl http://localhost:8000
```

and from browser:

http://15.222.63.149:8000

![Backend](docs/images/backend.png)

Both returned:
```
{"message": "Personal Finance Tracker Backend is running"}
```

![Backend](docs/images/bc1.png)

### Frontend Deployment

I updated my API URL inside script.js and uploaded frontend files:
```
aws s3 sync . s3://finance-tracker-frontend-bucket --delete
```

CloudFront automatically picks the website from S3.

Final UI:

https://d1ot1jmefpd9gq.cloudfront.net

![Frontend](docs/images/frontend.png)

Result

✔ Fully automated AWS infra using Terraform

✔ Backend running on EC2

✔ Frontend hosted on CloudFront (via S3)

✔ Backend + frontend integrated successfully

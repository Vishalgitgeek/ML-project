#  ML WebApp – End-to-End MLOps Pipeline

This project demonstrates the **complete lifecycle of a machine learning application**, focusing on **MLOps practices**, **clean architecture**, and **deployment readiness**. The goal isn't to achieve high predictive performance on real-world data, but to **practice the full development pipeline** from scratch—just like in a production environment.

---

##  Objectives

-  Build an end-to-end ML pipeline using Python
-  Follow **industry-level development standards**
-  Structure code for scalability and reusability
-  Implement preprocessing, training, and prediction components
-  Serve the model through a **Django web application**
-  Version control using Git and GitHub
-  (Planned) Add support for **batch predictions via CSV upload**
-  (Planned) Deploy the application to a cloud platform (e.g., Render, Railway, or AWS)

---

##  Tech Stack

| Layer        | Technology      |
|--------------|------------------|
| Language     | Python           |
| ML Library   | scikit-learn     |
| Web Framework | Django          |
| File Handling| pandas, pickle   |
| Version Control | Git + GitHub |
| OS           | Ubuntu (Linux)   |

---

##  Project Structure
look at structure.txt file

---


##  How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vishalgitgeek/ML-project.git
   cd ML-projects

2. **Create and activate virtual environment**
    ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Running the ML Pipeline (to generate artifacts)**
    ```bash
    Before running Django, make sure the artifacts/ folder contains:
   best_model.pkl
   preprocessor.pkl
   If they are missing, run the pipeline to train the model:
   python src/components/pipeline.py

5. **Running the Django Web App**
    ```bash
    Navigate to the Django project folder:
   cd ml_webapp
    
   Run database migrations:
   python manage.py makemigrations
   python manage.py migrate
    
   Start the development server:
   python manage.py runserver

6. **Packaging for Django**
   ```bash
   This project uses setup.py so the src/ folder can be imported directly inside Django.
   If you move the project, reinstall the package in editable mode:

   pip install -e .


*Why this project matter?*
```bash
In real-world ML workflows, data scientists and engineers must collaborate across tools, frameworks, and deployment targets. This project simulates:

    Code modularity (via src/)
    Exception handling (Custom_Exception)
    Logging for observability
    Model versioning and packaging

It acts as a personal boilerplate for future machine learning projects with production goals.

    -> TODOs / Future Work
    Upload CSV for batch predictions
    Dockerize the app
    CI/CD Integration
    Cloud deployment
    Add user input validation

 Author

Vishal Kumar
Aspiring ML Engineer & Python Developer


# Task Management REST API

A Flask-based Task Management REST API with automated testing using Pytest and Continuous Integration (CI) using GitHub Actions.

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve individual tasks
- Update existing tasks
- Delete tasks
- Input validation
- Automated API testing using Pytest
- GitHub Actions CI pipeline

## Technologies Used

- Python
- Flask
- Pytest
- REST API
- Git
- GitHub
- GitHub Actions

## Project Structure

```text
TaskManagement-DevOps/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_app.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/ANANYA-R07/TaskManagement-DevOps.git
```

Navigate to the project:

```bash
cd TaskManagement-DevOps
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

## Run Tests

```bash
python -m pytest -v
```

## Continuous Integration

GitHub Actions automatically runs the test suite whenever code is pushed to GitHub.

Workflow file:

`.github/workflows/ci.yml`

## Author

ANANYA-R07

## License

# TravelSure

[![codecov](https://codecov.io/gh/Wynand91/travelsure/graph/badge.svg?token=T3OJIA7JVO)](https://codecov.io/gh/Wynand91/travelsure)

Travelsure is a basic Django/DRF application designed to simulate a basic travel insurance backend/API. It showcases 
backend development practices, including JWT authentication, API design, SQL database design, testing, and CI/CD integration.

## Tech Stack
- Backend: Django, Django REST Framework
- Authentication: SimpleJWT
- Database: PostgreSQL
- Testing: Pytest, Flake8
- CI/CD: GitHub Actions

## Features
- User Registration & JWT Authentication: Secure user sign-up with immediate access and refresh token generation.
- Claim Management: Create, view, and manage insurance claims.
- Mail: Emails are sent for notifications and policy updates (Only in stdout for now)
- Robust Testing: Comprehensive test suite with Pytest and Flake8 linting.
- CI/CD Integration: Automated testing and deployment workflows using GitHub Actions.

## Dependencies
- Python 3.11+
- PostgreSQL

### Installing Dependencies
- PostgreSQL server
    - MacOS: https://postgresapp.com/
    - Ubuntu: ``apt-get install postgresql``
- Python3
    - PyEnv (Linux or MacOS): https://github.com/pyenv/pyenv#installation
    - Homebrew (MacOS): ``brew install python3``

## Installation
1. Clone the repository:

``` shell
git clone https://github.com/Wynand91/travelsure.git
cd travelsure
````
2. Create a virtual environment:
``` shell
python -m venv venv
source venv/bin/activate
````
3. Install dependencies:
``` shell
pip install -r requirements.txt
```
4. Set up environment variables:

- Create a .env file in the root directory and add the following:
- ```env
  DEBUG=1
  DB_NAME=your_db_name
  DB_USER=your_db_user
  DB_PASSWORD=your_db_password
  DB_HOST=localhost
  DB_PORT=5432
  SECRET_KEY=your_django_secret_key  # optional
  ```
5. Apply migrations:
``` shell
python manage.py migrate
```
6. Run the development server:
```shell
# port is optional - default is 8000
python manage.py runserver <port>
````

## API Documentation
API endpoints are documented using Swagger/OpenAPI. Once the server is running, access the documentation at:
```bash
http://localhost:8000/docs/
````

## Tests
Pytest is used for testing
```shell
# Always ensure project venv is up to date when using this.
pip install -e ./
pip install -r requirements.txt
pip install -r requirements-dev.txt
# Run entire test suite
pytest
# run individual tests methods with
pytest -k <test_method_name>
```

## Code Style
Make sure code and test files are free of style errors by running flake8.
Flake8 is checked by CI/CD flow too, and style errors will fail the build.
Error code reference: https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes

    flake8 tests/ src/

## Planned features:
- Docker setup.
- Federated Login: Implementing OpenID Connect (OIDC) for third-party authentication.


## Loading test data


The app features a command that loads a few database entries. This can be ran with 
the following command:

    ./manage.py load_dummy_data

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
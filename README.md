# Pocket-Saver

## Prerequisites
- Python 3.x
- pip
- virtualenv

#
## Setup

1. Clone the repository
```bash
git clone https://github.com/mugdha273/Pocket-Saver.git
```

2. Create virtual environment
```bash
 virtualenv venv
```

3. Activate the virtual environment
```bash
venv/Source/activate
```

4. Install the requirements
```bash
pip install -r requirements.txt
```

5. Migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Run the development server

```bash
python manage.py runserver
```
The API will be available at http://127.0.0.1:8000/

#

## Endpoints

https://documenter.getpostman.com/view/19649785/2s8ZDbWLkd






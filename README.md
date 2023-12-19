## Instructions

#### Manual installation

On the project folder create a virtual environment

```python
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```python
python3 -m pip install -r requirements.txt
```

Run server:
```python
python manage.py runserver
```
#### Docker

To build the image:
```python
docker build -t chromacraft .
```

To run the image
```python
docker run --name chromacraft -p 8000:8000 chromacraft
```
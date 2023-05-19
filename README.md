# py-web-app

## Steps to run/test locally:

Ensure python is installed first.

Navigate to the project folder and set up a virtual environment with the following commands:

```python3 -m venv venv```

Activate the virtual environment:

```source venv/bin/activate```

Install flask and other dependencies from the requirements.txt file:

```python3 -m pip install -r requirements.txt```

Run the python script that starts the app

```python3 main.py```

## Steps to run in a Docker container

Pull the image from Docker:

```docker pull samhiscox/py-web-app```

Run the container (tag might need changing):

```docker run -d -p 5000:5000 --name py-web-app samhiscox/py-web-app:v1.1```
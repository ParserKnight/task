# Proxy services

This project is about creating services that get and upload objects in AWS.

## Getting Started

The process is very simple, if you wish you can create a virtual environment with the dependencies in requirements.txt file.

### Prerequisites

Run your virtual environment and then type

```
pip3 install -r requirements.txt

```
and thats it.

### Running

Just get into the folder where the repo is and:

```
uvicorn main:app --reload
```

And thats it.

Note: you can also build a MINIO server to test using:

```
sudo docker run -p 9000:9000 -p 9090:9090 --name minio -v ~/minio/data:/data -e "MINIO_ROOT_USER=ROOTNAME" -e "MINIO_ROOT_PASSWORD=CHANGEME123" quay.io/minio/minio server /data --console-address ":9090"
```

Remeber to provide credentials in .env file (this is merely for development process, in production hardcoded credentials cant exist in plain text, a secret manager need to be used.)

## Built With

* [FastAPI](https://fastapi.tiangolo.com/)

## Authors

* **Javier Moubayyed** - [ParserKnight](https://github.com/ParserKnight)


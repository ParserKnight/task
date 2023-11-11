
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Body
from fastapi import status
from fastapi import UploadFile
from typing import Union
from typing import Annotated
import boto3
import io
import logging
import os

load_dotenv()

app = FastAPI()
client = boto3.client('s3', 
    endpoint_url=os.getenv('AWS_URL'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4'),
    verify=False
)

logger = logging.getLogger(__name__)

@app.get("/{bucket}/{key}")
async def get_file(
    bucket: str,
    key:str
    ):
    ''' 
    # Endpoint that gets AWS object
    '''
    
    try:
        _object = client.get_object(Bucket=bucket, Key=key)
    except client.exceptions.NoSuchKey:
        logger.error("Key doesnt exist in bucket")
        raise HTTPException(status_code=404, detail="key not found")
    except client.exceptions.NoSuchBucket:
        logger.error("Bucket doesnt exist")
        raise HTTPException(status_code=404, detail="bucket not found")

    return StreamingResponse(
        io.BytesIO(_object.get("Body").read()), 
        headers=_object.get("ResponseMetadata",{}).get("HTTPHeaders",{})
        )


@app.post("/uploadFile")
async def upload_file(
    file: UploadFile,
    bucket: Annotated[str, Form()],
    key:Annotated[str, Form()]
    ):
    ''' 
    Endpoint that upload AWS object
    '''

    try:
        client.upload_fileobj(
            file.file, bucket, key, 
            ExtraArgs={"ContentType": file.content_type})
    except client.exceptions.NoSuchKey:
        logger.error("Key doesnt exist in bucket")
        raise HTTPException(status_code=404, detail="key not found")
    except client.exceptions.NoSuchBucket:
        logger.error("Bucket doesnt exist")
        raise HTTPException(status_code=404, detail="bucket not found")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"status":"ok"}
        )

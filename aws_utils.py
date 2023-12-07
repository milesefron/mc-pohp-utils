import boto3
from enum import Enum
from botocore.exceptions import ClientError
import logging
import os
import json
import mimetypes

AWS_PARAMETER_S3BUCKET_BRIEFING_BOOKS = '/poh-utils/s3-buckets/briefing-books'
AWS_PARAMETER_S3BUCKET_TRANSCRIPTS    = '/poh-utils/s3-buckets/transcripts'
S3_BUCKET_PUBLIC_URL_PREFIX_BRIEFING_BOOKS = 'https://s3.amazonaws.com/web.poh.briefingbooks/'
S3_BUCKET_PUBLIC_URL_PREFIX_TRANSCRIPTS    = 'https://s3.amazonaws.com/web.poh.transcripts/'


ssm = boto3.client('ssm')

class FileTypes(Enum):
    BRIEFING_BOOK = 1
    TRANSCRIPT = 2

def get_s3_bucket(file_type):
    s3_bucket = None
    if file_type is FileTypes.BRIEFING_BOOK:
        response = ssm.get_parameter(Name=AWS_PARAMETER_S3BUCKET_BRIEFING_BOOKS)
    elif file_type is FileTypes.TRANSCRIPT:
        response = ssm.get_parameter(Name=AWS_PARAMETER_S3BUCKET_TRANSCRIPTS)
    else:
        raise ValueError('Illegal file type.  Must receive either BRIEFING_BOOK or TRANSCRIPT')
    
    if response:
        return response['Parameter']['Value']
    else:
        return None

def get_public_url(file_name, file_type):
    if file_type is FileTypes.BRIEFING_BOOK:
        return S3_BUCKET_PUBLIC_URL_PREFIX_BRIEFING_BOOKS + file_name
    elif file_type is FileTypes.TRANSCRIPT:
        return S3_BUCKET_PUBLIC_URL_PREFIX_TRANSCRIPTS + file_name
    else:
        raise ValueError('Illegal file type.  Must receive either BRIEFING_BOOK or TRANSCRIPT')

def upload_pdf(path_to_file, file_type):
    # first do some basic sanity checks
    if not path_to_file.endswith('.pdf') or not os.path.isfile(path_to_file):
        raise ValueError('upload_pdf needs a PDF file to upload. The supplied file is either not a PDF or not a real file.')
    
    # find our target for this file
    s3_bucket = get_s3_bucket(file_type)
    
    # separate the file name from the path
    file_name = os.path.basename(path_to_file)

    file_mime_type = mimetypes.guess_type(file_name)

    # do the heavy lifting
    s3_client = boto3.client('s3')
    response = None
    try:
        response = s3_client.upload_file(path_to_file, s3_bucket, file_name, ExtraArgs={'ContentType': 'application/pdf'})
        return get_public_url(file_name, file_type)
    except ClientError as e:
        logging.error(e)
        return False



    



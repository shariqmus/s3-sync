import os
import sys
import boto3
import hashlib
from datetime import datetime
from botocore.exceptions import ClientError

boto3.setup_default_session(profile_name='default')

if len(sys.argv) < 3:
    print("Not enough arguments.")
    print("Usage: python3 py-sync.py [SOURCE_DIRECTORY] [DESTINATION_BUCKET_NAME]")
    exit()

# Init objects
s3_client = boto3.client('s3')

SOURCE_DIR = sys.argv[1]
DESTINATION_BUCKET = sys.argv[2]

def check_file_exists(bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


print("Filename-Local", end=', ')
print("Filename-S3", end=', ')
print("File-Status", end=', ')
print("Action")

print("--------------", end=', ')
print("-----------", end=', ')
print("-----------", end=', ')
print("------")

for subdir, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        file_path_full = subdir + os.sep + file
        file_path_relative = file_path_full.replace(SOURCE_DIR + os.sep, '')
        file_key = file_path_relative.replace('\\', '/')

        print(file_path_full, end=', ')
        print('s3://' + DESTINATION_BUCKET + '/' + file_key, end=', ')

        if check_file_exists(DESTINATION_BUCKET, file_key) == False: # File doesnt exists, upload it
            s3_client.upload_file(file_path_full, DESTINATION_BUCKET, file_key)
            print("New", end=', ')
            print("Uploading")

        else:
            response = s3_client.head_object(Bucket=DESTINATION_BUCKET, Key=file_key)
            md5_s3 = response['ResponseMetadata']['HTTPHeaders'].get('etag')
            md5_s3 = md5_s3.replace('\"', '')
            md5_local = (md5(file_path_full))

            if md5_local != md5_s3:
                s3_client.upload_file(file_path_full, DESTINATION_BUCKET, file_key)
                print("Modified", end=', ')
                print("Uploading")

            else:
                print("No-Change", end=', ')
                print("Skipping")

A script to sync local files to s3. It compares the file using md5 hash.

Run it via the command:

python3 py-sync.py [SOURCE_DIRECTORY] [DESTINATION_BUCKET_NAME]


Note: 
- python3 and boto3 should be installed
- aws credentials set on the system
- the script uses the default aws profile 


Note:
- It syncs the files from the provided directory recursively to S3 bucket
- It uses md5 to check if file contents have changed, and use this to decide if upload is required
- File-Status: No-Change=file was not changed, New=new, Modified=changed file
- Action: Skipping(Not uploading), Uploading(uploading the file)


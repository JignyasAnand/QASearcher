import logging
import boto3
from botocore.exceptions import ClientError
import os

try:
    from .secret import ACCESS_KEY, SEC_ACCESS_KEY, BUCKET
except:
    from secret import ACCESS_KEY, SEC_ACCESS_KEY, BUCKET
s3_client = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SEC_ACCESS_KEY
                      )



def upload_file(file_name, bucket, object_name=None):
    global s3_client
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def genurl(name):
    temp=s3_client.generate_presigned_url("get_object",Params = {'Bucket': BUCKET, 'Key': name}, ExpiresIn=500)
    return temp

def getconts(prefix):
    arr=[]
    # objects = s3_client.list_objects_v2(Bucket=BUCKET)
    objects = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=f"{prefix}/")
    for obj in objects['Contents']:
        arr.append(obj['Key'])
    return arr


# upload_file("secret.py", BUCKET)
# s3_client.download_file(BUCKET, 'img1.jpg', "newf.jpg")


def download_file(name):
    s3_client.download_file(BUCKET, f"{name}", os.path.basename(f"{name}"))

if __name__ == '__main__':
    # getfiles("QASFiles")
    # x=getconts("QASF2")
    # for i in x:
    #     print(f"{i} \t {os.path.basename(i)}")
    # s3_client.download_file(BUCKET, "QASF2/qanda.txt", os.path.basename("QASFiles/qanda.txt"))

    # print("x0|0x".join(x))
    # print(genurl("secret.py"))
    # upload_file("ttttt.txt", BUCKET, "QASF2/tt.txt")
    pass
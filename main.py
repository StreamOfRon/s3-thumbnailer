from io import BytesIO
import os
from pathlib import PurePath

import boto3
from botocore.errorfactory import ClientError
from flask import Flask, abort, redirect, request
from PIL import Image

app = Flask(__name__)
s3 = boto3.resource('s3',
                    region_name=os.environ.get('AWS_REGION', None),
                    use_ssl=os.environ.get('S3_USE_SSL', True),
                    verify=os.environ.get('S3_VERIFY_SSL', True),
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', None),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', None),
                    endpoint_url=os.environ.get('S3_ENDPOINT_URL', None)
                    )

# Set this to a list of (w,h) tuples to limit what sizes can be requested.
ALLOWED_SIZES=[]

@app.route("/image/<path:file_path>")
def get_file(file_path):
  bucket = s3.Bucket(os.environ.get('S3_BUCKET'))
  orig_path = PurePath(file_path)
  width = request.args.get('w', None)
  height = request.args.get('h', None)
  if any([width, height]):
    if not all([width, height]):
      # This is not a valid request, you must specify width AND height or neither.
      abort(400)
    else:
      try:
        width = int(width)
        height = int(height)
      except ValueError as e:
        abort(400)
      if len(ALLOWED_SIZES) > 0 and (width, height) not in ALLOWED_SIZES:
        abort(400)
      request_path = PurePath(orig_path.parent, f"{orig_path.stem}_{width}_{height}{orig_path.suffix}")
      file = bucket.Object(str(request_path))
      if _file_exists(file):
        return redirect(f"{os.environ.get('REDIRECT_URL_BASE')}/{request_path}")
      else:
        file = bucket.Object(str(orig_path))
        try:
          filedata = file.get()
        except ClientError as e:
          abort(e.response['Error']['Code'])
        with Image.open(filedata.get('Body')) as image:
          image.thumbnail(size=(width, height))
          new_obj = bucket.Object(str(request_path))
          with BytesIO() as b:
            image.save(
              fp=b,
              format=request_path.suffix.lstrip('.')
            )
            new_obj.put(
              Body=b.getvalue(),
              ContentType=filedata.get('ContentType')
            )
        return redirect(f"{os.environ.get('REDIRECT_URL_BASE')}/{request_path}")
  else:
    file = bucket.Object(str(orig_path))
    if _file_exists(file):
      return redirect(f"{os.environ.get('REDIRECT_URL_BASE')}/{orig_path}")
    else:
      abort(404)

def _file_exists(file_object):
  try:
    file_object.load()
    return True
  except ClientError as e:
    return False

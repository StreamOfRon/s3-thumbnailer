# s3-thumbnailer

Generates thumbnails on the fly from source images stored on S3 or compatible services, storing them for future use, and redirecting a client to a given endpoint to enable content to be served via CDN. Requests take the form of /image/<path> and you request a new thumbnail by supplying the get parameters w and h, representing width and height respectively.  You must specify both parameters, or neither.


## Configuration

All configuration is done via the environment:

### Required Environment Parameters:

S3_BUCKET - the name of the storage bucket on S3 or compatible

REDIRECT_URL_BASE - the URL to prepend to the image path requested

### Optional Environment Parameters:

AWS_REGION - the AWS region parameter
S3_USE_SSL - Change this to false to disable the use of SSL.  Not recommended for production
S3_VERIFY_SSL - Change this to false to disable verification of the server certificate.  Not recommended for production
S3_ENDPOINT_URL - If you are using another S3-compatible service, specify the endpoint URL with this variable
AWS_ACCESS_KEY_ID - The access key ID providing access to your S3-compatible storage bucket
AWS_SECRET_ACCESS_KEY - The secret access key providing access to your S3-compatible bucket

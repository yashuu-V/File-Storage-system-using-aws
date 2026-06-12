from flask import Flask, request, render_template
import boto3
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

# ✅ Restrict file size to 100 KB (100 * 1024 bytes)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB

S3_BUCKET_NAME = ''

# ✅ S3 client setup (remove duplicate client creation)
s3 = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='ap-south-1'
)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = None
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'No file part'
        else:
            file = request.files['file']
            if file.filename == '':
                message = 'No selected file'
            else:
                try:
                    s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
                    message = 'File uploaded successfully!'
                except Exception as e:
                    message = f'Error uploading file: {e}'
    return render_template('index.html', message=message)

# ✅ Handle too large files gracefully
@app.errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    return render_template('index.html', message="File too large. Max size is 100 KB."), 413

if __name__ == '__main__':
    app.run(debug=True)

# bbuploadmanager

**bbuploadmanager** is an easy python library which manages all uploading, downloading, state management functionality and multiple scenarios of our Uploads & Processing of you project. 

## Features
- Uploading file to AWS S3
- Reading uploaded file content from AWS S3
- Upload Processing state management
- Upload Manager Dashboard 
- Upload tracking

## Installation
```
pip install https://github.com/Bigbasket/bbuploadmanager
```
OR 
```
pip install upload-manager
```
### Prerequisite

- Python 3 and above 
- Django 2.1 and above

#### Environment
AWS_STORAGE_BUCKET_NAME
- variable need to be set in environment to specify aws bucket.

AWS_ACCESS_KEY_ID & 
AWS_SECRET_ACCESS_KEY
- variable need to be set in environment, Only if I Am Role is not enabled on the machine.

## Sample Code

```
# Library Plugin code to be added in settings.py
INSTALLED_APPS = ["upload_manager.apps.UploadManagerConfig"]

# Below code to be implementation in your application.py\
# imports
from upload_manager.service import UploadManagerService

# file upload example
upload_service = UploadManagerService(<upload_name>, <username>, <S3_bucket_path>, files=[<file_obj>,])
upload_obj = upload_service.start_upload()

# reading uploaded file data in async thread
file_data = UploadManagerService.get_upload_content_for_id(upload_obj.id)

# writing response file example
upload_service.file_content = [("OrderId", "Status", "Message"),(11020304, "Success", "")]
upload_service.update_response_for_upload(upload_obj_id)

# updating upload status example
UploadManagerService.change_upload_status_to_inprocess(upload_obj.id)
UploadManagerService.change_upload_status_to_complete(upload_obj.id)
UploadManagerService.change_upload_status_to_failed(upload_obj.id)`
```

## Dashboard View

![](images/dashboard.png)

Above image shows dashboard view, how the uploads can be viewed and tracked in django Admin.

- Request File - Column contains a hyperlink to the uploaded file which was uploaded as part of start upload
- Response File - Column contains a hyperlink to the uploaded response file was uploaded after the processing.


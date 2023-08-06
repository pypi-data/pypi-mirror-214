import json

from common_logging.loggers import get_logger
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import UploadManager

logger = get_logger()


@require_http_methods(["POST"])
@csrf_exempt
def update_upload_status(request, upload_id):
    """Sample
    Upload POST request
    {
        "status" : "success",
        "s3_download_path" : "s3_url"
    }
    :param request:
    :param upload_id:
    :param status:
    :paran s3_download_path:
    :return:
    """

    logger.info("Update upload status request received for upload manager id: %s", upload_id)
    upload = get_object_or_404(UploadManager, pk=upload_id)
    body = request.body.decode('utf-8')
    body_json = json.loads(body)

    s3_download_path = body_json.get('s3_download_path')  
    status = body_json['status']

    if not status or status != UploadManager.COMPLETED and status != UploadManager.IN_PROCESS \
            and status != UploadManager.FAILED:
        logger.warn("Invalid status %s received for upload manager id %s", status, upload_id)
        return HttpResponseBadRequest("Invalid status")
    try:
        upload.status = status
        if s3_download_path:
            upload.s3_download_path = s3_download_path
        upload.save()
    except Exception as e:
        logger.exception("Status was not updated due to exception: %s", e)
        return HttpResponseServerError()
    logger.info("Successfully updated the status for upload manager id %s and s3_download_path %s", upload_id, s3_download_path)
    return HttpResponse()

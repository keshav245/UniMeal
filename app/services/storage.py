from fastapi import UploadFile

from app.core.config import settings


def upload_qr_image(file: UploadFile) -> str:
    """
    Production integration point.
    Replace with actual Cloudinary/S3 upload implementation.
    """
    if settings.storage_provider == "cloudinary":
        return f"https://res.cloudinary.com/{settings.cloudinary_cloud_name}/image/upload/{file.filename}"
    return f"https://{settings.aws_s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{file.filename}"

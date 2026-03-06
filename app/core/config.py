from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "College Mess Management API"
    api_v1_prefix: str = "/api/v1"

    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/unimeal"

    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    payment_currency: str = "INR"
    qr_price_inr: int = 65
    hosteller_share_inr: int = 20
    admin_share_inr: int = 45

    storage_provider: str = "cloudinary"  # cloudinary | s3
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "ap-south-1"
    aws_s3_bucket: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

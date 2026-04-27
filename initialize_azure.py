import os
import mimetypes
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContentSettings

STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_KEY = os.getenv("STORAGE_ACCOUNT_KEY")
CONTAINER_NAME = "static"

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIST_DIR = BASE_DIR / "static" / "dist"

if not STORAGE_ACCOUNT_NAME or not STORAGE_ACCOUNT_KEY:
    print("Azure Storage credentials missing. Skipping upload.")
    exit(0)

if not STATIC_DIST_DIR.exists():
    print(f"Static dist folder not found: {STATIC_DIST_DIR}")
    exit(1)

account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"

blob_service_client = BlobServiceClient(
    account_url=account_url,
    credential=STORAGE_ACCOUNT_KEY,
)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)

try:
    container_client.create_container()
    print(f"Container '{CONTAINER_NAME}' created.")
except Exception:
    print(f"Container '{CONTAINER_NAME}' already exists or cannot be created.")

for file_path in STATIC_DIST_DIR.rglob("*"):
    if file_path.is_file():
        relative_path = file_path.relative_to(BASE_DIR / "static").as_posix()
        content_type, _ = mimetypes.guess_type(file_path)

        if content_type is None:
            content_type = "application/octet-stream"

        print(f"Uploading {relative_path}...")

        with open(file_path, "rb") as file_data:
            container_client.upload_blob(
                name=relative_path,
                data=file_data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type),
            )

print("Azure static assets upload completed.")
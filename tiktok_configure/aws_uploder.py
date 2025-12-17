import os
import mimetypes
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


# Directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta LOCAL del archivo a subir (relativa al proyecto)
LOCAL_FILE_PATH = os.path.join(BASE_DIR, "videos-sora", "sora_github_demo.mp4")



# Bucket y región
S3_BUCKET = "tiktokapi-vfran"
AWS_REGION = "us-east-1"

# Ruta DESTINO en S3
S3_KEY = "videos/sora_github_demo.mp4"

# =========================

def guess_content_type(path: str) -> str:
    ctype, _ = mimetypes.guess_type(path)
    return ctype or "application/octet-stream"

def uoploader_aws(local_file_path) -> str:
    if not os.path.isfile(local_file_path):
        print(f"❌ Archivo no encontrado: {local_file_path}")
        return None

    content_type = guess_content_type(local_file_path)
    
    # Generar S3_KEY dinámico basado en el nombre del archivo
    filename = os.path.basename(local_file_path)
    s3_key = f"videos/{filename}"

    try:
        s3 = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        s3.upload_file(
            Filename=local_file_path,
            Bucket=S3_BUCKET,
            Key=s3_key,
            ExtraArgs={"ContentType": content_type, "ContentDisposition": "attachment"}
        )

        url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

        print("✅ Subida a S3 completada")
        print("📦 Bucket :", S3_BUCKET)
        print("🗂️  Key    :", s3_key)
        print("🌍 URL    :", url)
        return url

    except NoCredentialsError:
        print("❌ No se encontraron credenciales AWS")
    except ClientError as e:
        print("❌ Error subiendo a S3:", e)

def main():
    if not os.path.isfile(LOCAL_FILE_PATH):
        print(f"❌ Archivo no encontrado: {LOCAL_FILE_PATH}")
        return

    content_type = guess_content_type(LOCAL_FILE_PATH)

    try:
        s3 = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        s3.upload_file(
            Filename=LOCAL_FILE_PATH,
            Bucket=S3_BUCKET,
            Key=S3_KEY,
            ExtraArgs={"ContentType": content_type}
        )

        url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{S3_KEY}"

        print("✅ Subida a S3 completada")
        print("📦 Bucket :", S3_BUCKET)
        print("🗂️  Key    :", S3_KEY)
        print("🌍 URL    :", url)

    except NoCredentialsError:
        print("❌ No se encontraron credenciales AWS")
    except ClientError as e:
        print("❌ Error subiendo a S3:", e)

if __name__ == "__main__":
    main()

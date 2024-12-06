import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterator

import boto3
from py_common_utility.utils import file_utils


def get_etag(bucket_name, key):
    try:
        s3 = boto3.client('s3')
        # Fetch object metadata
        response = s3.head_object(Bucket=bucket_name, Key=key)
        # Extract and return the ETag
        return response.get('ETag', '').strip('"')
    except Exception as e:
        print(f"Error fetching ETag: {e}")
        return None


def list_etag_in_folder(bucket_name, folder_prefix) -> List[dict]:
    try:
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        if 'Contents' in response:
            return [
                {"Key": obj['Key'], "ETag": obj['ETag'].strip('"')}
                for obj in response['Contents']
            ]
        else:
            print("No objects found in the folder.")
            return []
    except Exception as e:
        print(f"Error listing objects: {e}")
        return []


def hash_in_folder(bucket_name, folder_prefix) -> str:
    etag_list = list_etag_in_folder(bucket_name, folder_prefix)
    combined_etags = ",".join([item['Key'] + ":" + item['ETag'] for item in etag_list])
    final_hash = hashlib.md5(combined_etags.encode()).hexdigest()
    return final_hash


def download_folder(bucket_name, s3_folder, local_dir, file_extensions=None):
    """
    Download an entire folder from an S3 bucket to a local directory, filtering by file extensions.

    :param bucket_name: str. Name of the S3 bucket.
    :param s3_folder: str. Path of the folder in the S3 bucket.
    :param local_dir: str. Local directory to save the downloaded folder.
    :param file_extensions: list or tuple. List of allowed file extensions (e.g., ['.txt', '.jpg']). If None, all files are downloaded.
    """
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')

    for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
        if 'Contents' in page:
            for obj in page['Contents']:
                s3_key = obj['Key']

                # Filter by file extension
                if file_extensions and not any(s3_key.endswith(ext) for ext in file_extensions):
                    continue

                # Compute the local file path
                local_file_path = os.path.join(local_dir, os.path.relpath(s3_key, s3_folder))

                # Create local directories if they do not exist
                Path(local_file_path).parent.mkdir(parents=True, exist_ok=True)

                try:
                    s3.download_file(bucket_name, s3_key, local_file_path)
                    print(f"Downloaded {s3_key} to {local_file_path}")
                except Exception as e:
                    print(f"Failed to download {s3_key}: {e}")


@dataclass
class UploadItem:
    dest_path: str
    local_path: str


def upload_files(bucket_name: str, doc_iterator: Iterator[UploadItem]) -> str:
    """
    Upload files to an S3 bucket based on an iterator of UploadItem objects.

    :param bucket_name: Name of the S3 bucket.
    :param doc_iterator: Iterator of UploadItem objects.
    :return: A status message indicating completion.
    """
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    for item in doc_iterator:
        file_path_obj = Path(item.local_path)

        if file_path_obj.exists() and file_path_obj.is_file():
            s3_key = item.dest_path

            try:
                # Upload the file to the specified S3 destination
                s3_client.upload_file(str(file_path_obj), bucket_name, s3_key)
                print(f"Uploaded: {item.local_path} to s3://{bucket_name}/{s3_key}")
            except Exception as e:
                print(f"Failed to upload {item.local_path}: {e}")
        else:
            print(f"File does not exist or is not a file: {item.local_path}")

    return "Upload completed."


if __name__ == '__main__':
    # Example usage
    _bucket_name = 'dsa-evr'
    s3_folder = 'company/'  # Adjusted to your specific S3 path  # Folder path in S3
    local_dir = '/tmp/dsa/evr/'  # Local directory where you want to save the folder
    # download_folder_from_s3(_bucket_name, s3_folder, local_dir)
    print("HI~ DONE")
    hash_list = list_etag_in_folder(_bucket_name, s3_folder)
    print(hash_list)
    a_etag = get_etag(_bucket_name, "company/0ed8be99-ed68-40ed-a1df-25f077d11459/header.bin")
    print(a_etag)
    dir_hash = hash_in_folder(_bucket_name, s3_folder)
    print(dir_hash)
    file_path_list = [
        UploadItem(
            dest_path="/tmp/bzk/output/chart/hash_-13362422024-11-18_23_37_24.png",  # Customize your destination prefix
            local_path="/tmp/bzk/output/chart/hash_-13362422024-11-18_23_37_24.png"
        ),
        UploadItem(
            dest_path="/tmp/bzk/output/chart/hash_-362356492024-11-04_10_22_39.png",
            local_path="/tmp/bzk/output/chart/hash_-362356492024-11-04_10_22_39.png"
        ),
        UploadItem(
            dest_path="/tmp/bzk/output/chart/hash_397484922024-11-19_23_58_51.png",  # Customize your destination prefix
            local_path="/tmp/bzk/output/chart/hash_397484922024-11-19_23_58_51.png"
        ),
    ]
    upload_iterator: Iterator[UploadItem] = iter(file_path_list)
    upload_files(_bucket_name, upload_iterator)
    print("xxxx")

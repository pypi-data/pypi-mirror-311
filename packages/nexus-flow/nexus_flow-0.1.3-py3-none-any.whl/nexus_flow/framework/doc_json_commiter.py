import os.path
from dataclasses import dataclass
from typing import Iterator

from py_common_utility.utils import time_utils

from nexus_flow.hash import hash_utils
from nexus_flow.hash.hash_info import HashInfo
from nexus_flow.infra import nexus_flow_constant
from nexus_flow.s3 import s3_utils
from nexus_flow.s3.s3_utils import UploadItem


@dataclass
class NewDocItem:
    repo_uid: str
    file_path: str
    src_hash: str


def _to_upload_file_iterator(doc_iterator: Iterator[NewDocItem]) -> Iterator[UploadItem]:
    for doc in doc_iterator:
        yield UploadItem(
            dest_path=f"{doc.repo_uid}",
            local_path=doc.file_path
        )
        dest_hash = hash_utils.generate_md5_by_file(doc.file_path)
        dest_hash_info: HashInfo = HashInfo(src_uid=doc.repo_uid, src_hash=doc.src_hash)
        hash_file_path = dest_hash_info.save(doc.file_path, dest_hash)
        yield UploadItem(
            dest_path=f"{doc.repo_uid}{nexus_flow_constant.HASH_INFO_EXTENSION}",
            local_path=hash_file_path
        )


class DocItemCommiter:

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

    def append_doc_all(self, doc_iterator: Iterator[NewDocItem]):
        file_list_it = _to_upload_file_iterator(doc_iterator)
        s3_utils.upload_files(self.bucket_name, file_list_it)


if __name__ == '__main__':
    commiter = DocItemCommiter(bucket_name="dsa-doc-json")
    new_doc_list = [
        NewDocItem(repo_uid="test/djson/1.png", file_path="/tmp/bzk/output/chart/hash_-13362422024-11-18_23_37_24.png",
                   src_hash="1234567890abcdef"),
        NewDocItem(repo_uid="test/djson/2.png", file_path="/tmp/bzk/output/chart/hash_-362356492024-11-04_10_22_39.png",
                   src_hash="fedcba9876543210"),
        NewDocItem(repo_uid="test/djson/3.png", file_path="/tmp/bzk/output/chart/hash_397484922024-11-19_23_58_51.png",
                   src_hash="0987654321fedcba"),
    ]
    new_doc_list_it = iter(new_doc_list)
    commiter.append_doc_all(new_doc_list_it)
    print("DONE~~~~~~~~~~~~~~~~")

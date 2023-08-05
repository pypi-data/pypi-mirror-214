import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Union


@dataclass
class DownloadConfig:
    """Configuration for our cached path manager.

    Attributes:
        cache_dir (`str` or `Path`, *optional*):
            Specify a cache directory to save the file to (overwrite the
            default cache dir).
        force_download (`bool`, defaults to `False`):
            If `True`, re-dowload the file even if it's already cached in
            the cache dir.
        resume_download (`bool`, defaults to `False`):
            If `True`, resume the download if an incompletely received file is
            found.
        proxies (`dict`, *optional*):
        user_agent (`str`, *optional*):
            Optional string or dict that will be appended to the user-agent on remote
            requests.
        extract_compressed_file (`bool`, defaults to `False`):
            If `True` and the path point to a zip or tar file,
            extract the compressed file in a folder along the archive.
        force_extract (`bool`, defaults to `False`):
            If `True` when `extract_compressed_file` is `True` and the archive
            was already extracted, re-extract the archive and override the folder where it was extracted.
        delete_extracted (`bool`, defaults to `False`):
            Whether to delete (or keep) the extracted files.
        use_etag (`bool`, defaults to `True`):
            Whether to use the ETag HTTP response header to validate the cached files.
        num_proc (`int`, *optional*):
            The number of processes to launch to download the files in parallel.
        max_retries (`int`, default to `1`):
            The number of times to retry an HTTP request if it fails.
        use_auth_token (`str` or `bool`, *optional*):
            Optional string or boolean to use as Bearer token
            for remote files on the Datasets Hub. If `True`, or not specified, will get token from `~/.huggingface`.
        ignore_url_params (`bool`, defaults to `False`):
            Whether to strip all query parameters and fragments from
            the download URL before using it for caching the file.
        storage_options (`dict`, *optional*):
            Key/value pairs to be passed on to the dataset file-system backend, if any.
        download_desc (`str`, *optional*):
            A description to be displayed alongside with the progress bar while downloading the files.
    """

    cache_dir: Optional[Union[str, Path]] = None
    force_download: bool = False
    resume_download: bool = False
    local_files_only: bool = False
    proxies: Optional[Dict] = None
    user_agent: Optional[str] = None
    extract_compressed_file: bool = False
    force_extract: bool = False
    delete_extracted: bool = False
    use_etag: bool = True
    num_proc: Optional[int] = None
    max_retries: int = 1
    use_auth_token: Optional[Union[str, bool]] = None
    ignore_url_params: bool = False
    storage_options: Optional[Dict] = None
    download_desc: Optional[str] = None

    def copy(self) -> "DownloadConfig":
        return self.__class__(**{k: copy.deepcopy(v) for k, v in self.__dict__.items()})

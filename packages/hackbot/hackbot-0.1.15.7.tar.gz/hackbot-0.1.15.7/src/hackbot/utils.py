import zipfile
import os
import traceback
from typing import Optional
from git import Repo, InvalidGitRepositoryError
from loguru import logger as log
from pathlib import Path


def get_repo(path):
    try:
        Repo(path)
        return True
    except InvalidGitRepositoryError:
        return False


def url_format(address: str, port: Optional[int]) -> str:
    """Format the URL for the hackbot service."""
    scheme = address.split(":")[0]
    if len(address.split(":")) > 1:
        rest = ":".join(address.split(":")[1:])
    else:
        # No protocol specified, assume by port number if exists
        rest = ""
        if port is not None:
            if port == 80:
                return f"http://{address}"
            else:
                return f"https://{address}:{port}"
        else:
            return f"http://{address}"
    assert scheme in ["http", "https"], "Invalid URI scheme"
    return f"{scheme}:{rest}:{port}" if (port is not None) else f"{scheme}:{rest}"


def compress_source_code(source_path: str, zip_path: str, size_limit: int = 256 * 1024 * 1024) -> None:
    """Compress the source code directory into a zip file."""
    try:
        zip_size = 0
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_path):
                for file in files:
                    # Skip .zip files
                    if not file.endswith(".zip"):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        if not os.path.exists(file_path):
                            log.warning(f"File not found (probably a broken symlink?), skipping sending to server: {file_path}")
                            continue
                        if os.path.getsize(file_path) + zip_size > size_limit:
                            raise RuntimeError("Source code archive is too large to be scanned. Must be less than 256MB.")
                        else:
                            zip_size += os.path.getsize(file_path)
                        zipf.write(file_path, arcname)
    except Exception:
        raise RuntimeError(f"Failed to compress source code: {traceback.format_exc()}")


def get_repo_info(repo_path: Path) -> dict[str, str] | None:
    """Returns the repo info of a github (specifically) repo at repo_path, or None if the repo is not a github repo
    The info includes repo name, commit, repo owner, and branch name"""
    try:
        repo = Repo(repo_path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        return None
    repo_info = {}
    for remote in repo.remotes:
        if "github.com" in remote.url:
            if "git@" in remote.url:
                mode = "ssh"
            else:
                mode = "http"

            # Example repo url: git@github.com:GatlingX/some_repo.git
            repo_info["repo_name"] = remote.url.split("/")[-1]
            # Remove the .git from the end of the repo name
            repo_info["repo_name"] = repo_info["repo_name"][:-4]

            repo_info["commit_hash"] = repo.head.commit.hexsha

            if mode == "http":
                # Example repo url: https://github.com/GatlingX/some_repo
                repo_info["repo_owner"] = remote.url.split("/")[-2]
            else:
                # Example repo url: git@github.com:GatlingX/some_repo.git
                repo_info["repo_owner"] = remote.url.split(":")[-1].split("/")[0]
            for branch in repo.branches:
                if branch.commit == repo.head.commit:
                    repo_info["branch_name"] = branch.name
                    break
                else:
                    repo_info["branch_name"] = "HEAD"
            break
    else:
        return None
    return repo_info

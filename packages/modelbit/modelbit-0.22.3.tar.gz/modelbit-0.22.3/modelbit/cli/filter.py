import logging
import os
from typing import Optional

from modelbit.api.object_api import ObjectApi
from modelbit.error import NonRetryableError
from yaml import safe_load

from .describe import describeFile, isBinaryFile, toYaml
from .git_protocol import GitProtocol
from .local_config import getCacheDir
from .secure_storage import calcHash
from .workspace import findWorkspace

logger = logging.getLogger(__name__)

ALWAYS_UPLOAD_FILE_TYPES = {".pkl", ".jlib", ".joblib", ".csv", ".tsv"}
ALWAYS_UPLOAD_FILE_SIZE = 50 * 1024
# Allow datasets and notebooks to be a little larger
# 1MB isn't too bad (Set by current POST body limit of web)
# Git sites render notebooks well and we don't currently support stubs for datasets (But might have to!)
#
UPLOAD_SIZE_EXCEPTIONS = {
    '.sql': 1024 * 1000,
    '.ipynb': 1024 * 1000,
}
LARGE_FILE_STUB_SENTINEL = b'_: MBFileStub'


def process():

  workspaceId = findWorkspace()
  gitApi = GitApi(workspaceId)
  protocol = GitProtocol(clean=gitApi.clean, smudge=gitApi.smudge)
  protocol.filterProcess()


def fromYaml(content: bytes) -> Optional[str]:
  if not content.startswith(LARGE_FILE_STUB_SENTINEL):
    return None

  obj = safe_load(content.decode("utf-8"))
  if type(obj) is dict and "contentHash" in obj:
    return obj["contentHash"]
  return None


def shouldUploadFile(filepath: str, content: bytes) -> bool:
  _, ext = os.path.splitext(filepath)
  if ext in ALWAYS_UPLOAD_FILE_TYPES or isBinaryFile(content):
    return True
  maxSize = UPLOAD_SIZE_EXCEPTIONS.get(ext, ALWAYS_UPLOAD_FILE_SIZE)
  return len(content) >= maxSize


def stubCacheFilePath(workspaceId: str, contentHash: str) -> str:
  contentHash = contentHash.replace(":", "_")
  return os.path.join(getCacheDir(workspaceId, "largeFileStubs"), f"{contentHash}.yaml")


class GitApi:

  def __init__(self, workspaceId: str, objectApi: Optional[ObjectApi] = None):
    self.workspaceId = workspaceId
    self.api = objectApi or ObjectApi(workspaceId)

  def clean(self, filepath: str, content: bytes, skipCache=False) -> bytes:
    if not shouldUploadFile(filepath, content):
      logger.info(f"Ignoring {filepath}")
      if content:
        return content
      return b''
    contentHash = calcHash(content)
    logger.info(f"Cleaning {filepath} hash={contentHash}")
    cacheFilepath = None
    if not skipCache:
      cacheFilepath = stubCacheFilePath(self.workspaceId, contentHash)
      if os.path.exists(cacheFilepath):  # Try cache
        try:
          with open(cacheFilepath, "rb") as f:
            yamlContent = f.read()
            if fromYaml(yamlContent) == contentHash:
              return yamlContent
        except Exception as e:
          logger.info("Failed to read from cache", exc_info=e)

    self.api.uploadRuntimeObject(content, contentHash, filepath)
    objDesc = describeFile(content)
    yamlContent = toYaml(contentHash, len(content), objDesc).encode('utf-8')
    if not skipCache and cacheFilepath is not None:
      with open(cacheFilepath, "wb") as f:
        f.write(yamlContent)
    return yamlContent

  def smudge(self, filepath: str, content: bytes) -> bytes:
    if os.getenv("SKIP_SMUDGE") == "true":
      return content
    try:
      contentHash = fromYaml(content)
    except Exception as e:
      logger.info(f"Not smudging {filepath}")
      return content
    if contentHash is None:
      return content
    # Store in cache
    # Otherwise diffs trigger if the locally environment differs
    cacheFilepath = stubCacheFilePath(self.workspaceId, contentHash)
    with open(cacheFilepath, "wb") as f:
      f.write(content)

    logger.info(f"Smudging {filepath} hash={contentHash}")
    data = self.api.downloadRuntimeObject(contentHash, filepath)
    return data

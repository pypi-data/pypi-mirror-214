import logging
from typing import Optional

from .api import MbApi
from ..cli.local_config import getWorkspaceConfig
from ..cli.secure_storage import EncryptedObjectInfo, getSecureData, putSecureData, S3UploadInfo
from ..cli.utils import retry

logger = logging.getLogger(__name__)


class ObjectApi:

  def __init__(self, workspaceId: Optional[str], api: Optional[MbApi] = None):
    self.workspaceId = workspaceId
    if api is None:
      if workspaceId is None:
        raise KeyError("workspaceId required if api is not passed")
      config = getWorkspaceConfig(workspaceId)
      # TODO: Do auth dance if config not found
      if not config:
        raise KeyError("workspace config not found")
      api = MbApi(config.gitUserAuthToken, config.cluster)
    self.api = api

  def _runtimeObjectUploadInfo(self, contentHash: str) -> S3UploadInfo:
    resp = self.api.getJson("api/cli/v1/runtime_object_upload_info", {
        "contentHash": contentHash,
    })
    return S3UploadInfo(resp)

  def _runtimeObjectDownloadUrl(self, contentHash: str) -> EncryptedObjectInfo:
    resp = self.api.getJson("api/cli/v1/runtime_object_download_url", {
        "contentHash": contentHash,
    })
    return EncryptedObjectInfo(**resp)

  @retry(8, logger)
  def uploadRuntimeObject(self, obj: bytes, contentHash: str, desc: str) -> str:
    resp = self._runtimeObjectUploadInfo(contentHash)
    putSecureData(resp, obj, desc)
    return contentHash

  @retry(8, logger)
  def downloadRuntimeObject(self, contentHash: str, desc: str) -> bytes:
    resp = self._runtimeObjectDownloadUrl(contentHash)
    if not resp or not resp.objectExists:
      raise Exception("Failed to get file URL")
    if self.workspaceId is None:
      raise KeyError("workspaceId required to download")
    data = getSecureData(self.workspaceId, resp, desc)
    if not data:
      raise Exception(f"Failed to download and decrypt")
    return data

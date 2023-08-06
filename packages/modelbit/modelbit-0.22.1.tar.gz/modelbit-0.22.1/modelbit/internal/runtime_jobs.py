import io
from typing import Any, Dict, Optional, Union, cast

import yaml
from modelbit.api import JobApi, MbApi
from modelbit.cli.secure_storage import EncryptedObjectInfo, getSecureData
from modelbit.error import UserFacingError
from modelbit.internal.load import loadFromPickle
from modelbit.helpers import inDeployment
from modelbit.secure_storage import getS3FileBytes


def getJobOutputFromWeb(mbApi: MbApi,
                        branch: str,
                        runtimeName: str,
                        jobName: str,
                        userFacingId: Optional[int] = None,
                        fileName: Optional[str] = None,
                        restoreClass: Optional[type] = None):
  data = JobApi(mbApi).getJobOutputContent(branch=branch,
                                           runtimeName=runtimeName,
                                           jobName=jobName,
                                           userFacingId=userFacingId,
                                           fileName=fileName)
  return _downloadJobOutputFromEncObjInfo('data.pkl', data, restoreClass)


class NoDataError(Exception):
  pass


def _downloadJobOutputFromEncObjInfo(key: str,
                                     data: Optional[Dict[str, Union[str, EncryptedObjectInfo]]],
                                     restoreClass: Optional[type] = None):
  if data is None:
    raise NoDataError()
  elif "encryptedObjectInfo" in data:
    objBytes = getSecureData(cast(str, data['workspaceId']),
                             cast(EncryptedObjectInfo, data['encryptedObjectInfo']), key)
    if key.endswith(".pkl"):
      return loadFromPickle(objBytes, restoreClass)
    return objBytes

  elif "content" in data:
    return cast(str, data).encode("utf8")

  raise UserFacingError("Failed to read output.")


def getJobOutputFromS3(branch: str,
                       runtimeName: str,
                       jobName: str,
                       userFacingId: Optional[int] = None,
                       fileName: Optional[str] = None,
                       restoreClass: Optional[type] = None):
  assert inDeployment()
  if fileName is None:
    fileName = f"data/{jobName}.pkl"
  jobRunAlias = str(userFacingId) if userFacingId is not None else branch

  s3Path = f"jobs/{runtimeName}/{jobName}/{jobRunAlias}/repo/{fileName}.zstd.enc"
  fileStubBytes = getS3FileBytes(s3Path)
  if fileStubBytes is None:
    raise UserFacingError(f"Could not find file {s3Path}")

  yamlData = cast(Dict[str, Any], yaml.load(io.BytesIO(fileStubBytes), Loader=yaml.SafeLoader))

  contentHash = cast(Optional[str], yamlData["contentHash"])
  runtimeObjBytes = getS3FileBytes(f"runtime_objects/{contentHash}.zstd.enc")
  assert runtimeObjBytes is not None
  return loadFromPickle(runtimeObjBytes, restoreClass)

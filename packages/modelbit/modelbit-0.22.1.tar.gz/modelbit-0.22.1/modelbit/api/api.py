import logging
import os
from typing import Any, Dict, Optional

import requests
from modelbit import __version__
from modelbit.error import UserFacingError

logger = logging.getLogger(__name__)

ApiErrorCode_BadParameter = 6
ApiErrorCode_ObjectNotFound = 7
ApiErrorCode_RateLimited = 8
UserFacingErrorCodes = (ApiErrorCode_BadParameter, ApiErrorCode_ObjectNotFound, ApiErrorCode_RateLimited)
defaultRequestTimeout = 10


class MbApi:

  _DEFAULT_CLUSTER = "app.modelbit.com"

  _cluster = ""
  _region = ""
  _api_host = ""
  _login_host = ""

  def __init__(self, authToken: Optional[str] = None, cluster: Optional[str] = None):
    if cluster is not None:
      self.setUrls(cluster)
    else:
      self.setUrls(os.getenv("MB_JUPYTER_CLUSTER", self._DEFAULT_CLUSTER))
    self.pkgVersion = __version__
    self.authToken = authToken

  def getToken(self) -> None:
    resp = self.getJson("api/cli/v1/get_token")
    if not "signedUuid" in resp:
      raise Exception("Invalid respones from server.")
    self.authToken = resp["signedUuid"]

  def getLoginLink(self, source: str) -> str:
    if not self.authToken:
      self.getToken()
    return f'{self._login_host}t/{self.authToken}?source={source}'

  def loginWithApiKey(self, apiKey: str, workspaceName: str, source: str) -> None:
    for _ in range(3):
      resp = self.getJson("api/cli/v1/get_token_from_api_key", {
          "apiKey": apiKey,
          "workspaceName": workspaceName,
          "source": source
      })
      if "signedUuid" in resp:
        self.authToken = resp["signedUuid"]
        return
      if "cluster" in resp:
        self.setUrls(resp["cluster"])
    raise Exception("Invalid respones from server.")

  def getJsonOrThrow(self, path: str, body: Dict[str, Any] = {}) -> Dict[str, Any]:
    resp = self.getJson(path, body)
    errorMsg = resp.get("errorMsg", None)
    if errorMsg:
      if resp.get("errorCode", None) in UserFacingErrorCodes:
        raise UserFacingError(errorMsg)
      raise Exception(errorMsg)
    return resp

  def getJson(self, path: str, body: Dict[str, Any] = {}) -> Dict[str, Any]:
    data: Dict[str, Any] = {"version": self.pkgVersion}
    data.update(body)
    logger.info(f"Making request with{'out' if not self.authToken else '' } auth to {self._api_host}{path}")
    with requests.post(f'{self._api_host}{path}',
                       headers=self._headers(),
                       json=data,
                       timeout=defaultRequestTimeout) as url:  # type: ignore
      resp = url.json()  # type: ignore
      return resp

  def _headers(self) -> Dict[str, str]:
    hdrs: Dict[str, str] = {}
    if self.authToken is not None:
      hdrs["Authorization"] = self.authToken
      hdrs["x-mb-package-version"] = self.pkgVersion
    return hdrs

  def setUrls(self, cluster: Optional[str]) -> None:
    logger.info(f"Setting cluster to {cluster}")
    if cluster is None:
      return
    self._cluster = cluster
    self._region = self._cluster.split(".")[0]
    if cluster == "localhost":
      self._api_host = f'http://localhost:3000/'
      self._login_host = f'http://localhost:3000/'
    elif cluster == "web":
      self._api_host = f'http://web:3000/'
      self._login_host = f'http://localhost:3000/'
    else:
      self._api_host = f'https://{self._cluster}/'
      self._login_host = self._api_host

  def getApiHost(self):
    return self._api_host

  def getCluster(self):
    return self._cluster

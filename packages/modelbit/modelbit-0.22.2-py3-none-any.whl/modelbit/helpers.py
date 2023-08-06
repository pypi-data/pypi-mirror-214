from time import sleep
from typing import Union, Any, List, Dict, Optional, Tuple, cast
from enum import Enum
import json, requests, os

from .utils import sizeOfFmt, getEnvOrDefault, inDeployment, inNotebook, inModelbitCI, branchFromEnv, inRuntimeJob
from .environment import listMissingPackagesFromImports, listMissingPackagesFromPipList
from .ux import COLORS, MismatchedPackageWarning, MissingPackageFromImportWarning, WarningErrorTip, makeCssStyle, printTemplate
from threading import Thread
from modelbit.error import UserFacingError
import logging

pkgVersion: str = ""  # set in __init__
_MAX_DATA_LEN = 50_000_000
_DEFAULT_CLUSTER = "app.modelbit.com"

_cluster = ""
_region = ""
_api_host = ""
_login_host = ""
_api_url = ""
_currentBranch = branchFromEnv() if inRuntimeJob() else "main"
defaultRequestTimeout = 10

logger = logging.getLogger(__name__)


def _setUrls(cluster: Optional[str]):
  global _cluster, _region, _api_host, _login_host, _api_url
  if cluster is None:
    return
  _cluster = cluster
  _region = _cluster.split(".")[0]
  # Web is like localhost, but for modelbit clone running inside of a container
  if cluster == "localhost" or cluster == "web":
    _api_host = f'http://web:3000/'
    _login_host = f'http://localhost:3000/'
  else:
    _api_host = f'https://{_cluster}/'
    _login_host = _api_host
  _api_url = f'{_api_host}api/'


class ObjectUploadInfo:

  def __init__(self, data: Dict[str, Any]):
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]
    self.objectExists: bool = data["objectExists"]


class RuntimeFile:

  def __init__(self, name: str, contents: str):
    self.name = name
    self.contents = contents

  def asDict(self):
    return {"name": self.name, "contents": self.contents}


class RuntimePythonProps:
  excludeFromDict: List[str] = ['errors']

  def __init__(self):
    self.source: Optional[str] = None
    self.name: Optional[str] = None
    self.argNames: Optional[List[str]] = None
    self.argTypes: Optional[Dict[str, str]] = None
    self.namespaceVarsDesc: Optional[Dict[str, str]] = None
    self.namespaceFunctions: Optional[Dict[str, str]] = None
    self.namespaceImports: Optional[Dict[str, str]] = None
    self.namespaceFroms: Optional[Dict[str, str]] = None
    self.namespaceModules: Optional[List[str]] = None
    self.errors: Optional[List[str]] = None
    self.namespaceVars: Optional[Dict[str, Any]] = None
    self.customInitCode: Optional[List[str]] = None
    self.extraDataFiles: Optional[Dict[str, Tuple[Any, bytes]]] = None
    self.extraSourceFiles: Optional[Dict[str, str]] = None
    self.job: Optional[JobProps] = None
    self.userClasses: List[str] = []


class JobProps:

  def __init__(self, name: str, storeResultAs: str, rtProps: RuntimePythonProps, schedule: Optional[str],
               redeployOnSuccess: bool, emailOnFailure: Optional[str], refreshDatasets: Optional[List[str]],
               size: Optional[str], timeoutMinutes: Optional[int], arguments: Optional[List[str]]):
    self.name = name
    self.outVar = storeResultAs
    self.rtProps = rtProps
    self.schedule = schedule
    self.redeployOnSuccess = redeployOnSuccess
    self.emailOnFailure = emailOnFailure
    self.refreshDatasets = refreshDatasets
    self.size = size
    self.timeoutMinutes = timeoutMinutes
    self.arguments = arguments


class NamespaceCollection:

  def __init__(self):
    self.functions: Dict[str, str] = {}
    self.vars: Dict[str, Any] = {}
    self.imports: Dict[str, str] = {}
    self.froms: Dict[str, str] = {"*": "typing"}
    self.allModules: List[str] = []
    self.customInitCode: List[str] = []
    self.extraDataFiles: Dict[str, Tuple[Any, bytes]] = {}
    self.extraSourceFiles: Dict[str, str] = {}
    self.userClasses: Dict[str, str] = {}

  def __repr__(self) -> str:
    return json.dumps(self.__dict__)


# For instances of user defined classes. Default Pickle doesn't handle unpickling user defined
# classes because they cannot be imported, since they're defined in the notebook
class InstancePickleWrapper:

  def __init__(self, obj: Any):
    self.clsName = obj.__class__.__name__
    self.mbClassForStub = obj.__class__.__name__
    self.mbModuleForStub = obj.__class__.__module__
    if hasattr(obj, "__getstate__"):
      self.state = obj.__getstate__()
    else:
      self.state = obj.__dict__
    self.desc = str(obj)
    if self.desc.startswith("<__main"):
      self.desc = str(self.state)

  def __repr__(self) -> str:
    return self.desc

  def restore(self, restoreClass: type):
    inst = cast(Any, restoreClass.__new__(restoreClass))  # type: ignore
    if hasattr(inst, "__setstate__"):
      inst.__setstate__(self.state)
    else:
      inst.__dict__ = self.state
    return inst


class RuntimeEnvironment:

  def __init__(self, data: Dict[str, Any]):
    self.pythonVersion: str = data.get("pythonVersion", None)
    self.pythonPackages: Optional[List[str]] = data.get("pythonPackages", None)
    self.systemPackages: Optional[List[str]] = data.get("systemPackages", None)


class DeploymentTestError(Enum):
  UnknownFormat = 'UnknownFormat'
  ExpectedNotJson = 'ExpectedNotJson'
  CannotParseArgs = 'CannotParseArgs'


class DeploymentTestDef:

  def __init__(self, data: Dict[str, Any]):
    self.command: str = data.get("command", "")
    self.expectedOutput: Union[str, Dict[Union[str, int, float, bool], Any]] = data.get("expectedOutput", "")
    self.args: Optional[List[Any]] = data.get("args", None)
    self.error: Optional[str] = data.get("error", None)


class NotebookEnv:

  def __init__(self, data: Dict[str, Any]):
    self.userEmail: Optional[str] = data.get("userEmail", None)
    self.signedToken: Optional[str] = data.get("signedToken")
    self.authenticated: bool = data.get("authenticated", False)
    self.workspaceName: Optional[str] = data.get("workspaceName", None)
    self.mostRecentVersion: Optional[str] = data.get("mostRecentVersion", None)
    self.cluster: Optional[str] = data.get("cluster", None)


class NotebookResponse:

  def __init__(self, data: Dict[str, Any]):
    self.error: Optional[str] = data.get("error", None)
    self.message: Optional[str] = data.get("message", None)

    self.notebookEnv: Optional[NotebookEnv] = None
    if "notebookEnv" in data:
      self.notebookEnv = NotebookEnv(data["notebookEnv"])

    self.runtimeOverviewUrl: Optional[str] = None
    if "runtimeOverviewUrl" in data:
      self.runtimeOverviewUrl = data["runtimeOverviewUrl"]

    self.tests: Optional[List[DeploymentTestDef]] = None
    if "tests" in data:
      self.tests = [DeploymentTestDef(d) for d in data["tests"]]

    self.objectUploadInfo: Optional[ObjectUploadInfo] = None
    if "objectUploadInfo" in data:
      self.objectUploadInfo = ObjectUploadInfo(data["objectUploadInfo"])

    self.deploymentInfo: Optional[DeploymentInfo] = None
    if "deploymentInfo" in data:
      self.deploymentInfo = DeploymentInfo(data["deploymentInfo"])


class DeploymentInfo:

  def __init__(self, data: Dict[str, Any]):
    self.version: Optional[int] = data.get("version", None)


def getJson(path: str, body: Dict[str, Any] = {}) -> NotebookResponse:
  global _state
  requestToken = _state.signedToken
  if requestToken == None:
    requestToken = os.getenv('MB_RUNTIME_TOKEN')
  data: Dict[str, Any] = {"requestToken": requestToken, "version": pkgVersion, "branch": _currentBranch}
  data.update(body)
  dataLen = len(json.dumps(data))
  if (dataLen > _MAX_DATA_LEN):
    return NotebookResponse({
        "error":
            f'API Error: Request is too large. (Request is {sizeOfFmt(dataLen)} Limit is {sizeOfFmt(_MAX_DATA_LEN)})'
    })
  with requests.post(f'{_api_url}{path}', json=data, timeout=defaultRequestTimeout) as url:
    nbResp = NotebookResponse(url.json())
    if nbResp.notebookEnv:
      _state = nbResp.notebookEnv
    return nbResp


def getJsonOrPrintError(path: str, body: Dict[str, Any] = {}):
  nbResp = getJson(path, body)
  if not isAuthenticated():
    performLogin()
    nbResp = getJson(path, body)  #return False
    if not isAuthenticated():
      return False
  if nbResp.error:
    printTemplate("error", None, errorText=nbResp.error)
    return False
  return nbResp


def refreshAuthentication() -> bool:
  if inDeployment():
    return True
  global _state
  nbResp = getJson("jupyter/v1/login")
  if nbResp.error:
    printTemplate("error", None, errorText=nbResp.error)
    return False
  if nbResp.notebookEnv:
    _state = nbResp.notebookEnv
    _setUrls(_state.cluster)
  return isAuthenticated()


def isAuthenticated() -> bool:
  if inDeployment():
    return True
  return _state.authenticated


def apiKeyFromEnv() -> Optional[str]:
  return os.getenv("MB_API_KEY")


def workspaceNameFromEnv() -> Optional[str]:
  return os.getenv("MB_WORKSPACE_NAME")


def apiKeyInEnv():
  return apiKeyFromEnv() is not None


def performLogin(refreshAuth: bool = False, region: Optional[str] = None):
  if inDeployment():
    return
  elif apiKeyInEnv():
    return performApiKeyLogin(region)
  elif inNotebook() or inModelbitCI():
    return performNotebookLogin(refreshAuth, region)
  else:
    if not performCLILogin():
      performNotebookLogin(refreshAuth, region, waitForResponse=True)


def determineCurrentBranch():
  from .cli.workspace import findCurrentBranch
  return os.getenv("BRANCH", None) or findCurrentBranch() or "main"


def performCLILogin():
  if isAuthenticated():
    return

  from .cli.workspace import findWorkspace
  from .cli.local_config import getWorkspaceConfig
  global _state
  try:
    config = getWorkspaceConfig(findWorkspace())
    if not config:
      raise KeyError("Workspace credentials not found")
  except KeyError:
    return False

  _setUrls(config.cluster)
  _state.signedToken = config.gitUserAuthToken.replace("mbpat-", "")
  return setCurrentBranch(determineCurrentBranch())


def performApiKeyLogin(region: Optional[str]):
  if isAuthenticated():
    return
  apiKey = apiKeyFromEnv()
  workspaceName = workspaceNameFromEnv()
  if apiKey is None:
    return
  if ":" not in apiKey:
    raise UserFacingError("Incorrect API Key. Please check MB_API_KEY.")
  if workspaceName is None:
    raise UserFacingError("Missing env var MB_WORKSPACE_NAME.")

  setCurrentBranch(determineCurrentBranch())
  if region is not None:
    _setUrls(f"{region}.modelbit.com")

  global _state
  nbResp = getJson("jupyter/v1/login_with_api_key", {"apiKey": apiKey, "workspaceName": workspaceName})
  if nbResp.error:
    raise UserFacingError("Incorrect API Key. Please check MB_API_KEY.")
  if nbResp.notebookEnv and not nbResp.notebookEnv.authenticated and nbResp.notebookEnv.cluster != _cluster:
    _setUrls(nbResp.notebookEnv.cluster)
    nbResp = getJson("jupyter/v1/login_with_api_key", {"apiKey": apiKey, "workspaceName": workspaceName})
    if nbResp.error:
      raise UserFacingError("Incorrect API Key. Please check MB_API_KEY.")

  if nbResp.notebookEnv:
    _state = nbResp.notebookEnv
    _setUrls(_state.cluster)
  refreshAuthentication()

  if isAuthenticated():
    printAuthenticatedMessage()
  else:
    apiKeyId = apiKey.split(":")[0]
    raise UserFacingError(f"Failed to log in with API Key {apiKeyId} to workspace {workspaceName}.")


def performNotebookLogin(refreshAuth: bool = False,
                         region: Optional[str] = None,
                         waitForResponse: bool = False):
  if region is not None:
    _setUrls(f"{region}.modelbit.com")
  if (refreshAuth):
    refreshAuthentication()
  if isAuthenticated():
    printAuthenticatedMessage()
    return
  displayId = "mbLogin"
  printLoginMessage(displayId)

  def pollForLoggedIn():
    triesLeft = 150
    while not isAuthenticated() and triesLeft > 0:
      triesLeft -= 1
      sleep(3)
      refreshAuthentication()
    if isAuthenticated():
      printAuthenticatedMessage(displayId)
    else:
      printTemplate("login-timeout", displayId)

  if waitForResponse:
    pollForLoggedIn()
  else:
    loginThread = Thread(target=pollForLoggedIn)
    if not inModelbitCI():
      loginThread.start()


def _pipUpgradeInfo():
  if os.getenv('MB_RUNTIME_TOKEN'):
    return None  # runtime environments don't get upgraded
  latestVer = _state.mostRecentVersion

  def ver2ints(ver: str):
    return [int(v) for v in ver.split(".")]

  nbVer = pkgVersion
  if latestVer and ver2ints(latestVer) > ver2ints(nbVer):
    return {"installed": nbVer, "latest": latestVer}
  return None


def getMissingPackageWarningsFromEnvironment(pyPackages: Optional[List[str]]):
  warnings: List[WarningErrorTip] = []
  missingPackages = listMissingPackagesFromPipList(pyPackages)
  if len(missingPackages) > 0:
    for mp in missingPackages:
      desiredPackage, similarPackage = mp
      if similarPackage is not None:
        warnings.append(MismatchedPackageWarning(desiredPackage, similarPackage))
  return warnings


def getMissingPackageWarningsFromImportedModules(importedModules: Optional[List[str]],
                                                 pyPackages: Optional[List[str]]):
  warnings: List[WarningErrorTip] = []
  missingPackages = listMissingPackagesFromImports(importedModules, pyPackages)
  for mp in missingPackages:
    importedModule, pipPackageInstalled = mp
    warnings.append(MissingPackageFromImportWarning(importedModule, pipPackageInstalled))
  return warnings


def printAuthenticatedMessage(displayId: Optional[str] = None):
  inRegion: Optional[str] = None
  if _cluster != _DEFAULT_CLUSTER:
    inRegion = _region
  styles = {
      "connected": makeCssStyle({
          "color": COLORS["success"],
          "font-weight": "bold",
      }),
      "info": makeCssStyle({
          "font-family": "monospace",
          "font-weight": "bold",
          "color": COLORS["brand"],
      })
  }
  printTemplate("authenticated",
                displayId,
                updateDisplayId=True,
                styles=styles,
                email=_state.userEmail,
                workspace=_state.workspaceName,
                inRegion=inRegion,
                currentBranch=getCurrentBranch(),
                needsUpgrade=_pipUpgradeInfo(),
                warningsList=[])


def printLoginMessage(displayId: Optional[str] = None):
  if (_state.signedToken == None or type(_state.signedToken) != str):
    raise Exception("Signed token missing, cannot authenticate.")
  displayUrl = f'modelbit.com/t/{_state.signedToken[0:10]}...'
  source = "notebook" if inNotebook() else "terminal"
  linkUrl = f'{_login_host}t/{_state.signedToken}?source={source}'
  printTemplate("login", displayId, displayUrl=displayUrl, linkUrl=linkUrl, needsUpgrade=_pipUpgradeInfo())


def runtimeAuthInfo():
  return _state.signedToken, _cluster


def setCurrentBranch(branch: str):
  global _currentBranch
  if type(branch) != str:
    raise Exception("Branch must be a string.")
  if (branch != _currentBranch):
    logger.info("Changing branch to %s", branch)
  oldBranch = _currentBranch

  _currentBranch = branch
  if isAuthenticated() and not refreshAuthentication():
    logger.info("Auth failed, reverting to %s", oldBranch)
    _currentBranch = oldBranch


def getCurrentBranch():
  global _currentBranch
  return _currentBranch


def getDeploymentName() -> Optional[str]:
  return os.environ.get('DEPLOYMENT_NAME')


def getDeploymentVersion() -> Optional[str]:
  return os.environ.get('DEPLOYMENT_VERSION')


# set defaults
_setUrls(getEnvOrDefault("MB_JUPYTER_CLUSTER", _DEFAULT_CLUSTER))
_state = NotebookEnv({})

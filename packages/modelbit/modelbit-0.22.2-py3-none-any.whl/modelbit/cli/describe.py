import io
import logging
import pickle
import pprint
import sys
from contextlib import redirect_stdout
from datetime import datetime
from typing import Any, Dict, Optional, cast

import yaml

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 1
MAX_DESCRIPTION_SIZE = 5000
NULL_BYTE = b"\x00"


def repr_str(dumper: yaml.Dumper, data: str):
  if '\n' in data:
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def toYaml(contentHash: str, fileSize: int, objDesc: Dict[str, Any]) -> str:
  metadata: Dict[str, Any] = dict(fileSize=fileSize, **objDesc)

  obj = toFileStubDict(contentHash, metadata)
  yaml.add_representer(str, repr_str)
  return yaml.dump(obj, width=1000)


def toFileStubDict(contentHash: str, objDesc: Dict[str, Any]) -> Dict[str, Any]:
  return {
      "_": "MBFileStub",
      "createdAt": datetime.utcnow().replace(microsecond=0),
      "contentHash": contentHash,
      "metadata": objDesc,
      "schemaVersion": SCHEMA_VERSION
  }


def describeFile(content: bytes, maxDepth: int = 1) -> Dict[str, Any]:
  f = io.StringIO()
  with redirect_stdout(f):
    pickleDetails = getPickleInfo(content, maxDepth)
    if pickleDetails:
      return pickleDetails
    else:
      return describeObject(content, maxDepth)


def decodeString(b: bytes) -> str:
  for encoding in ('ascii', 'utf8', 'latin1'):
    try:
      return b.decode(encoding)
    except UnicodeDecodeError:
      pass
  return b.decode('ascii', 'ignore')


def _descModule(obj: Any, objT: type) -> str:
  if hasattr(obj, "mbModuleForStub"):
    return cast(str, obj.mbModuleForStub)  # type: ignore
  return objT.__module__


def _descClass(obj: Any, objT: type) -> str:
  if hasattr(obj, "mbClassForStub"):
    return cast(str, obj.mbClassForStub)  # type: ignore
  return objT.__name__


def describeObject(obj: Any,
                   maxDepth: int,
                   remainingCharacters: int = MAX_DESCRIPTION_SIZE) -> Dict[str, Any]:
  return {"object": _describeObject(obj, maxDepth, remainingCharacters)}


MAX_DESCRIBABLE_OBJECT_SIZE = 10_000_000


def _describeObject(obj: Any,
                    maxDepth: int,
                    remainingCharacters: int = MAX_DESCRIPTION_SIZE) -> Dict[str, Any]:
  objT = type(obj)
  if (sys.getsizeof(obj) > MAX_DESCRIBABLE_OBJECT_SIZE):
    return {
        "module": _descModule(obj, objT),
        "class": _descClass(obj, objT),
        "description": "",
    }

  if objT is dict and maxDepth > 0:
    ret: Dict[str, Any] = {}
    for k, v in obj.items():
      ret[k] = _describeObject(v, maxDepth - 1, max(0, remainingCharacters))
      remainingCharacters -= len(str(ret[k]))
    return ret
  elif objT is bytes:
    if isBinaryFile(obj):
      obj = "Unknown binary file"
    else:
      obj = decodeString(obj)
      objT = type(obj)
  description = obj[:remainingCharacters].strip() if type(obj) is str else pprint.pformat(
      obj, depth=1, width=100, compact=True)[:remainingCharacters].strip()
  return {
      "module": _descModule(obj, objT),
      "class": _descClass(obj, objT),
      "description": description,
  }


def getPickleInfo(content: bytes, maxDepth: int) -> Optional[Dict[str, Any]]:
  try:
    import joblib
    obj = joblib.load(io.BytesIO(content))
    return describeObject(obj, maxDepth)
  except Exception as e:
    logger.debug("Failed to parse as joblib", exc_info=e)
    pass

  try:
    obj = pickle.loads(content)
    return describeObject(obj, maxDepth)
  except Exception as e:
    logger.debug("Failed to parse as pickle", exc_info=e)
    return {}


def isBinaryFile(content: bytes) -> bool:
  return NULL_BYTE in content


def getObjectDescription(filepath=None, depth=1) -> str:
  import sys

  from .secure_storage import calcHash

  if filepath is not None:
    with open(filepath, "rb") as f:
      content = f.read()
  else:
    content = sys.stdin.buffer.read()

  return toYaml(calcHash(content), len(content), describeFile(content, depth))

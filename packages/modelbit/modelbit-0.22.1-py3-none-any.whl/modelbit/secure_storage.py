import io, os, tempfile, base64, zlib, urllib.request, sys, ssl, logging

from typing import TextIO, cast
from Cryptodome.Cipher import AES
from tqdm import tqdm
from Cryptodome.Util.Padding import unpad

from .helpers import getCurrentBranch
from .utils import boto3Client, isDsrId
from .ux import printTemplate
from modelbit.api import ResultDownloadInfo

logger = logging.getLogger(__name__)


def getSecureDataGzip(dri: ResultDownloadInfo, name: str):
  try:
    _storeResultIfMissing(name, dri.id, dri.signedDataUrl)
    return _decryptUngzipFile(dri.id, dri.key64, dri.iv64)
  except Exception as err:
    printTemplate("error", None, errorText=f'Unable to fetch data. ({str(err)})')
    _clearTmpFile(dri.id)
    return None


def getSecureDataZstd(dri: ResultDownloadInfo, name: str):
  try:
    _storeResultIfMissing(name, dri.id, dri.signedDataUrl)
    return _decryptUnzstdFile(dri.id, dri.key64, dri.iv64)
  except Exception as err:
    printTemplate("error", None, errorText=f'Unable to fetch data. ({str(err)})')
    _clearTmpFile(dri.id)
    return None


def getS3DatasetCsvBytes(dsName: str):
  if isDsrId(dsName):
    decData = _downloadDecryptS3File(f"datasets/{dsName}")
  else:
    decData = _downloadDecryptS3File(f"datasets/{dsName}/{getCurrentBranch()}")
  if decData is not None:
    return zlib.decompress(decData, zlib.MAX_WBITS | 32)
  return None


def getS3DatasetPklBytes(dsName: str):
  import zstd  # type: ignore
  if isDsrId(dsName):
    decData = _downloadDecryptS3File(f"datasets/{dsName}.pkl2")
  else:
    decData = _downloadDecryptS3File(f"datasets/{dsName}/{getCurrentBranch()}.pkl2")
  if decData is not None:
    return cast(bytes, zstd.decompress(decData))  # type: ignore
  return None


def getS3FileBytes(keySuffix: str):
  import zstd  # type: ignore
  decData = _downloadDecryptS3File(keySuffix)
  if decData is not None:
    return cast(bytes, zstd.decompress(decData))  # type: ignore
  return None


def _tmpFilepath(dId: str):
  mbTempDir = os.path.join(tempfile.gettempdir(), 'modelbit')
  if not os.path.exists(mbTempDir):
    os.makedirs(mbTempDir)
  return os.path.join(mbTempDir, dId)


def _storeResultIfMissing(dName: str, dId: str, url: str):
  filepath = _tmpFilepath(dId)
  if os.path.exists(filepath):
    return

  class DownloadProgressBar(tqdm):  # type: ignore

    def update_to(self, b: int = 1, bsize: int = 1, tsize: None = None):
      if tsize is not None:
        self.total = tsize
      self.update(b * bsize - self.n)  # type: ignore

  outputStream: TextIO = sys.stdout
  if os.getenv('MB_TXT_MODE'):
    outputStream = io.StringIO()
  with DownloadProgressBar(unit='B',
                           unit_scale=True,
                           miniters=1,
                           desc=f'Downloading "{dName}"',
                           file=outputStream) as t:
    default_context = ssl._create_default_https_context  # type: ignore
    try:
      urllib.request.urlretrieve(url, filename=filepath, reporthook=t.update_to)  # type: ignore
    except:
      # In case client has local SSL cert issues: pull down encrypted file without cert checking
      _clearTmpFile(dId)
      ssl._create_default_https_context = ssl._create_unverified_context  # type: ignore
      urllib.request.urlretrieve(url, filename=filepath, reporthook=t.update_to)  # type: ignore
    finally:
      ssl._create_default_https_context = default_context  # type: ignore


def _clearTmpFile(dId: str):
  filepath = _tmpFilepath(dId)
  if os.path.exists(filepath):
    os.remove(filepath)


def _decryptFile(dId: str, key64: str, iv64: str):
  filepath = _tmpFilepath(dId)
  if not os.path.exists(filepath):
    printTemplate("error", None, errorText=f"Unable to find data at {filepath}")

  fileIn = open(filepath, 'rb')
  raw = fileIn.read()
  fileIn.close()

  cipher = AES.new(base64.b64decode(key64), AES.MODE_CBC, iv=base64.b64decode(iv64))  # type: ignore
  return unpad(cipher.decrypt(raw), AES.block_size)  # type: ignore


def _decryptUngzipFile(dId: str, key64: str, iv64: str):
  decData = _decryptFile(dId, key64, iv64)
  return zlib.decompress(decData, zlib.MAX_WBITS | 32)


def _decryptUnzstdFile(dId: str, key64: str, iv64: str):
  import zstd  # type: ignore
  decData = _decryptFile(dId, key64, iv64)
  return cast(bytes, zstd.decompress(decData))  # type: ignore


def _downloadDecryptS3File(dsKey: str):
  _workspaceId = os.getenv('WORKSPACE_ID')
  _pystateBucket = os.getenv('PYSTATE_BUCKET')
  _pystateKeys = os.getenv('PYSTATE_KEYS')
  if _workspaceId == None or _pystateBucket == None or _pystateKeys == None:
    raise Exception(f"EnvVar Missing: WORKSPACE_ID, PYSTATE_BUCKET, PYSTATE_KEYS")
  try:
    dsKey = f'{_workspaceId}/{dsKey}'
    s3Obj = boto3Client('s3').get_object(Bucket=_pystateBucket, Key=dsKey)  # type: ignore
    fileKeyEnc = base64.b64decode(s3Obj['Metadata']["x-amz-key"])  # type: ignore
    fileIv = base64.b64decode(s3Obj['Metadata']["x-amz-iv"])  # type: ignore
    for key64 in str(_pystateKeys).split(","):
      cipher = AES.new(base64.b64decode(key64), AES.MODE_ECB)  # type: ignore
      fileKey = unpad(cipher.decrypt(fileKeyEnc), AES.block_size)
      cipher = AES.new(fileKey, AES.MODE_CBC, fileIv)  # type: ignore
      bodyDataEnc = cast(bytes, s3Obj['Body'].read())  # type: ignore
      decState = unpad(cipher.decrypt(bodyDataEnc), AES.block_size)
      return decState
  except Exception as err:
    strErr = str(err)
    if 'AccessDenied' not in strErr and 'NoSuchKey' not in strErr:
      raise err
  return None

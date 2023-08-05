# API
from enum import Enum

from fovus.constants.cli_constants import (
    CPU,
    GPU,
    GPU_INTERNAL_REPRESENTATION,
    MAX_VCPU,
    MIN_VCPU,
)

COGNITO_REGION = "us-east-1"
TIMEOUT_SECONDS = 10


# API: Access through FovusApiUtil.get_api_address function to allow domain override via CLI.
class Api(Enum):
    JOB = "job"
    FILE = "file"
    SOFTWARE = "software"
    BENCHMARK = "benchmark"


class ApiMethod(Enum):
    CREATE_JOB = "create-job"
    GET_JOB_INFO = "get-job-info"
    GET_FILE_DOWNLOAD_TOKEN = "get-file-download-token"  # nosec
    GET_FILE_UPLOAD_TOKEN = "get-file-upload-token"  # nosec
    LIST_SOFTWARE = "list-software"
    LIST_BENCHMARK_PROFILE = "list-benchmark-profile"


# Benchmarking
BOUNDS_TO_SCALE = (MIN_VCPU, MAX_VCPU)
BOUND_VALUE_CORRECTION_PRINT_ORDER = ("minvCpu", "maxvCpu", "minvCpuMemGiB", "minGpu", "maxGpu", "minGpuMemGiB")
X86_64 = "x86-64"
SUPPORTED_ARCHITECTURES = {
    CPU: (X86_64,),
}
COMPUTING_DEVICE_TO_BP_COMPUTING_DEVICE = {
    CPU: CPU,
    GPU: GPU_INTERNAL_REPRESENTATION,
}

# Payload
AUTHORIZATION_HEADER = "Authorization"
CONTAINERIZED = "containerized"
ENVIRONMENT = "environment"
LICENSE_ADDRESS = "licenseAddress"
LICENSE_COUNT_PER_TASK = "licenseCountPerTask"
LICENSE_FEATURE = "licenseFeature"
MONOLITHIC_LIST = "monolithicList"
PAYLOAD_CONSTRAINTS = "constraints"
PAYLOAD_JOB_CONSTRAINTS = "jobConstraints"
PAYLOAD_JOB_NAME = "jobName"
PAYLOAD_TASK_CONSTRAINTS = "taskConstraints"
PAYLOAD_TIME_COST_PRIORITY_RATIO = "timeToCostPriorityRatio"
PAYLOAD_TIMESTAMP = "timestamp"
PAYLOAD_WORKSPACE_ID = "workspaceId"
SOFTWARE_NAME = "softwareName"
SOFTWARE_VERSION = "softwareVersion"
STATUS_CODE = "statusCode"
VENDOR_NAME = "vendorName"

# Response
BODY = "body"
GPU_RANGE = "gpuRange"
BP_HYPERTHREADING = "bpHyperthreading"
SUPPORTED_PROCESSOR_ARCHITECTURES = "supportedProcessorArchitectures"
ERROR_MESSAGE = "errorMessage"
IS_LICENSE_REQUIRED = "isLicenseRequired"
JOB_STATUS = "jobStatus"
SOFTWARE_MAP = "softwareMap"
SOFTWARE_VERSIONS = "softwareVersions"

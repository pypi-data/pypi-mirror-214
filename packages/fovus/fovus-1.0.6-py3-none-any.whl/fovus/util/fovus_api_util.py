import operator
from http import HTTPStatus

import boto3

from fovus.config.config import Config
from fovus.constants.benchmark_constants import (
    BENCHMARK_NAME,
    BOUNDS,
    CORRECTABLE_COMPARISON,
    CORRECTABLE_LIST_COMPREHENSION,
    DEFAULT_BOOLEANS_TO_VALIDATE,
    DEFAULT_LOWER_BOUNDS_TO_VALIDATE,
    DEFAULT_UPPER_BOUNDS_TO_VALIDATE,
    GPU_LOWER_BOUNDS_TO_VALIDATE,
    GPU_UPPER_BOUNDS_TO_VALIDATE,
    INCORRECTABLE_COMPARISON,
    INCORRECTABLE_LIST_COMPREHENSION,
    LIST_BENCHMARKING_FIELD_BY_CREATE_JOB_REQUEST_FIELD,
)
from fovus.constants.cli_constants import (
    COMPUTING_DEVICE,
    CPU,
    DOMAIN_NAME,
    GPU,
    JOB_ID,
    SUPPORTED_CPU_ARCHITECTURES,
    TIMESTAMP,
    USER_ID,
)
from fovus.constants.fovus_api_constants import (
    BOUNDS_TO_SCALE,
    ERROR_MESSAGE,
    GPU_RANGE,
    PAYLOAD_CONSTRAINTS,
    PAYLOAD_JOB_CONSTRAINTS,
    STATUS_CODE,
    SUPPORTED_PROCESSOR_ARCHITECTURES,
    Api,
    ApiMethod,
)
from fovus.constants.util_constants import (
    SERVER_ERROR_PREFIX,
    SUCCESS_STATUS_CODES,
    USER_ERROR_PREFIX,
)
from fovus.exception.system_exception import SystemException
from fovus.exception.user_exception import UserException

NO_ERROR_MESSAGE = "No error message provided"


# Only 200, 201, 202, 4XX, and 5XX status codes are returned from the API.
class FovusApiUtil:  # pylint: disable=too-few-public-methods
    @staticmethod
    def confirm_successful_response(response, source):
        response_status_code = response[STATUS_CODE]
        if response_status_code not in SUCCESS_STATUS_CODES:
            if str(response_status_code).startswith(USER_ERROR_PREFIX):
                raise UserException(response_status_code, source, FovusApiUtil._get_error_message(response))
            if str(response_status_code).startswith(SERVER_ERROR_PREFIX):
                raise SystemException(response_status_code, source, FovusApiUtil._get_error_message(response))

    @staticmethod
    def _get_error_message(response):
        return response.get(ERROR_MESSAGE, NO_ERROR_MESSAGE)

    @staticmethod
    def get_job_id(cli_dict):
        if cli_dict.get(JOB_ID):
            return cli_dict[JOB_ID]
        cli_dict[JOB_ID] = FovusApiUtil._get_job_id_with_timestamp(cli_dict)
        return cli_dict[JOB_ID]

    @staticmethod
    def _get_job_id_with_timestamp(cli_dict):
        return f"{cli_dict[TIMESTAMP]}-{cli_dict[USER_ID]}"

    @staticmethod
    def get_s3_info(temporary_credentials_body):
        return (
            boto3.client(
                "s3",
                aws_access_key_id=temporary_credentials_body["credentials"]["accessKeyId"],
                aws_secret_access_key=temporary_credentials_body["credentials"]["secretAccessKey"],
                aws_session_token=temporary_credentials_body["credentials"]["sessionToken"],
            ),
            temporary_credentials_body["authorizedBucket"],
            temporary_credentials_body["authorizedFolder"],
        )

    @staticmethod
    def get_software_vendor(list_software_response, software_name):
        software_map = list_software_response["softwareMap"]
        for vendor in software_map.keys():
            if software_name in software_map[vendor]:
                return vendor
        raise UserException(
            HTTPStatus.BAD_REQUEST,
            FovusApiUtil.__name__,
            f"Software {software_name} not found in list of available software, unable to retrieve version.",
        )

    @staticmethod
    def should_fill_vendor_name(monolithic_list_item):
        return monolithic_list_item.get("softwareName") and not monolithic_list_item.get("vendorName")

    @staticmethod
    def get_benchmark_validations_config(request):
        lower_bounds_to_validate = DEFAULT_LOWER_BOUNDS_TO_VALIDATE
        upper_bounds_to_validate = DEFAULT_UPPER_BOUNDS_TO_VALIDATE
        boolean_values_to_validate = DEFAULT_BOOLEANS_TO_VALIDATE
        if request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][COMPUTING_DEVICE] == GPU:
            lower_bounds_to_validate.extend(GPU_LOWER_BOUNDS_TO_VALIDATE)
            upper_bounds_to_validate.extend(GPU_UPPER_BOUNDS_TO_VALIDATE)

        return {
            "Minimum": {
                BOUNDS: lower_bounds_to_validate,
                CORRECTABLE_COMPARISON: operator.lt,
                CORRECTABLE_LIST_COMPREHENSION: min,
                INCORRECTABLE_COMPARISON: operator.gt,
                INCORRECTABLE_LIST_COMPREHENSION: max,
            },
            "Maximum": {
                BOUNDS: upper_bounds_to_validate,
                CORRECTABLE_COMPARISON: operator.gt,
                CORRECTABLE_LIST_COMPREHENSION: max,
                INCORRECTABLE_COMPARISON: operator.lt,
                INCORRECTABLE_LIST_COMPREHENSION: min,
            },
            "Boolean": {
                BOUNDS: boolean_values_to_validate,
                CORRECTABLE_COMPARISON: operator.ne,
                CORRECTABLE_LIST_COMPREHENSION: lambda x: x,
            },
        }

    @staticmethod
    def get_benchmark_profile_bounds(benchmarking_profile_item, bound_to_validate, bound_scaler):
        benchmarking_profile_bounds = benchmarking_profile_item[
            LIST_BENCHMARKING_FIELD_BY_CREATE_JOB_REQUEST_FIELD[bound_to_validate]
        ]
        # May be list of valid values, dict with "Min" and "Max" keys, or boolean value.
        if isinstance(benchmarking_profile_bounds, dict):
            benchmarking_profile_bounds = list(benchmarking_profile_bounds.values())
        if bound_to_validate in BOUNDS_TO_SCALE:
            benchmarking_profile_bounds = [int(bound * bound_scaler) for bound in benchmarking_profile_bounds]
        return benchmarking_profile_bounds

    @staticmethod
    def get_benchmark_bound_scaler(enable_hyperthreading, bp_hyperthreading):
        if enable_hyperthreading and bp_hyperthreading:
            bound_scaler = 1
        if not enable_hyperthreading and bp_hyperthreading:
            bound_scaler = 0.5
        if enable_hyperthreading and not bp_hyperthreading:
            bound_scaler = 2
        if not enable_hyperthreading and not bp_hyperthreading:
            bound_scaler = 1
        return bound_scaler

    @staticmethod
    def print_benchmark_hyperthreading_info(enable_hyperthreading):
        enable_hyperthreading_print = "disabled"
        threads_per_cpu_message = "1 thread (vCPU) per core can be used on all CPUs."
        if enable_hyperthreading:
            enable_hyperthreading_print = "enabled"
            threads_per_cpu_message = "2 threads (vCPU) per core can be used on CPUs that support hyperthreading."
        print(f"Hyperthreading is {enable_hyperthreading_print}. {threads_per_cpu_message}")

    @staticmethod
    def get_corrected_value_message(  # pylint: disable=too-many-arguments
        validation_type,
        benchmarking_profile_name,
        bound_to_validate,
        benchmarking_profile_item_bound,
        hyperthreading_enabled,
        current_value,
    ):
        message = (
            f"{validation_type} value allowed by '{benchmarking_profile_name}' for "
            f"{bound_to_validate} is {benchmarking_profile_item_bound}"
        )
        if bound_to_validate in BOUNDS_TO_SCALE:
            hyperthreading_enabled_print = "enabled" if hyperthreading_enabled else "disabled"
            message += f" given that hyperthreading is {hyperthreading_enabled_print}"
        message += f". Overriding current value of {current_value} with " f"{benchmarking_profile_item_bound}."
        return message

    @staticmethod
    def validate_computing_device(input_computing_device, benchmarking_profile_item):
        computing_device_should_be = ""
        if (
            GPU_RANGE not in benchmarking_profile_item or not benchmarking_profile_item[GPU_RANGE]
        ) and input_computing_device == GPU:
            computing_device_should_be = CPU
        if (
            GPU_RANGE in benchmarking_profile_item and benchmarking_profile_item[GPU_RANGE]
        ) and input_computing_device == CPU:
            computing_device_should_be = GPU

        if computing_device_should_be:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                FovusApiUtil.__name__,
                f"Invalid value for {COMPUTING_DEVICE}. "
                + FovusApiUtil.get_formatted_benchmark_supported_message(
                    benchmarking_profile_item[BENCHMARK_NAME], "computing devices", [computing_device_should_be]
                ),
            )

    @staticmethod
    def validate_cpu_architectures(input_cpu_architectures, benchmarking_profile_item):
        supported_architectures = []
        valid_input_cpu_architectures = []
        for supported_computing_device_and_architecture in benchmarking_profile_item[SUPPORTED_PROCESSOR_ARCHITECTURES]:
            supported_architecture = supported_computing_device_and_architecture.split("-", maxsplit=1)[1]
            supported_architectures.append(supported_architecture)
            if supported_architecture in input_cpu_architectures:
                valid_input_cpu_architectures.append(supported_architecture)

        if valid_input_cpu_architectures:
            if len(valid_input_cpu_architectures) < len(input_cpu_architectures):
                print(
                    f"Create job request contains values for {SUPPORTED_CPU_ARCHITECTURES} not supported by the "
                    f"benchmarking profile {benchmarking_profile_item[BENCHMARK_NAME]}. "
                    f"\n\t- "
                    + FovusApiUtil.get_formatted_benchmark_supported_message(
                        benchmarking_profile_item[BENCHMARK_NAME], "CPU architectures", supported_architectures
                    )
                    + f"\n\t- The following request values have been removed: "
                    f"{list(set(input_cpu_architectures) - set(valid_input_cpu_architectures))}"
                )
            return

        raise UserException(
            HTTPStatus.BAD_REQUEST,
            FovusApiUtil.__name__,
            f"Invalid value of {SUPPORTED_CPU_ARCHITECTURES}. "
            + FovusApiUtil.get_formatted_benchmark_supported_message(
                benchmarking_profile_item[BENCHMARK_NAME], "CPU architectures", supported_architectures
            ),
        )

    @staticmethod
    def get_formatted_benchmark_supported_message(benchmark_name, field_readable, supported_values: tuple):
        return (
            f"The benchmarking profile '{benchmark_name}' only supports the "
            f"following {field_readable}: {supported_values}."
        )

    @staticmethod
    def get_api_address(api: Api, api_method: ApiMethod):
        return "/".join((Config.get(DOMAIN_NAME), api.value, api_method.value))

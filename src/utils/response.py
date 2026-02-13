from sdks.novavision.src.helper.package import PackageHelper
from components.HistogramUpdate.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,

    # Histogram executor models
    HistogramExecutor,
    HistogramExecutorResponse,
    HistogramExecutorOutputs,
    OutputImage,
    OutputData,

    # Equalization executor models
    EqualizationExecutor,
    EqualizationExecutorResponse,
    EqualizationExecutorOutputs,
)


def build_response_histogram(context):
    """
    Build response for Histogram executor.
    """
    output_image = OutputImage(value=context.image)
    output_data = OutputData(value=context.histogramData)

    outputs_container = HistogramExecutorOutputs(
        outputImage=output_image,
        outputData=output_data
    )
    executor_response = HistogramExecutorResponse(outputs=outputs_container)
    histogram_executor = HistogramExecutor(value=executor_response)

    config_executor = ConfigExecutor(value=histogram_executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    return package_model


def build_response_equalization(context):
    """
    Build response for Equalization executor.
    """
    output_image = OutputImage(value=context.image)

    outputs_container = EqualizationExecutorOutputs(
        outputImage=output_image
    )
    executor_response = EqualizationExecutorResponse(outputs=outputs_container)
    equalization_executor = EqualizationExecutor(value=executor_response)

    config_executor = ConfigExecutor(value=equalization_executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    return package_model


def build_response(context):
    """
    Dispatcher that routes to the correct build_response function
    based on which executor is running.
    """
    if hasattr(context, 'histogramData'):
        return build_response_histogram(context)
    else:
        return build_response_equalization(context)

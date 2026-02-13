from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


# Inputs
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


# Outputs
class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputData(Output):
    name: Literal["outputData"] = "outputData"
    value: Union[list, dict]
    type: Literal["object"] = "object"

    class Config:
        title = "Data"


# Config Atoms (TextInput fields)
class ConfigPixelMin(Config):
    """
    Minimum pixel value for histogram range. <br>
    Valid range: 0-254 <br>
    Must be less than Pixel Maximum Value.
    """
    name: Literal["configPixelMin"] = "configPixelMin"
    value: int = Field(default=0, ge=0, le=254)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Pixel Minimum Value"
        json_schema_extra = {
            "shortDescription": "Minimum pixel value for histogram range"
        }


class ConfigPixelMax(Config):
    """
    Maximum pixel value for histogram range. <br>
    Valid range: 1-255 <br>
    Must be greater than Pixel Minimum Value.
    """
    name: Literal["configPixelMax"] = "configPixelMax"
    value: int = Field(default=255, ge=1, le=255)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Pixel Maximum Value"
        json_schema_extra = {
            "shortDescription": "Maximum pixel value for histogram range"
        }


class ConfigClipLimit(Config):
    """
    Clip limit for CLAHE contrast enhancement. <br>
    Higher values allow more contrast amplification. <br>
    Typical range: 1.0-10.0, default is 2.0.
    """
    name: Literal["configClipLimit"] = "configClipLimit"
    value: float = Field(default=2.0, ge=0.1, le=40.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "CLAHE Clip Limit"
        json_schema_extra = {
            "shortDescription": "Clip limit for CLAHE contrast enhancement"
        }


# Option Classes
class Enabled(Config):
    name: Literal["Enabled"] = "Enabled"
    value: Literal["Enabled"] = "Enabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Enabled"


class Disabled(Config):
    name: Literal["Disabled"] = "Disabled"
    value: Literal["Disabled"] = "Disabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"


class TileGrid4x4(Config):
    name: Literal["4x4"] = "4x4"
    value: Literal["4x4"] = "4x4"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "4x4"


class TileGrid8x8(Config):
    name: Literal["8x8"] = "8x8"
    value: Literal["8x8"] = "8x8"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "8x8"


# Config Dropdownlists
class ConfigChannelRed(Config):
    """Enable or disable the Red channel for histogram calculation."""
    name: Literal["configChannelRed"] = "configChannelRed"
    value: Union[Enabled, Disabled]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Red Channel"
        json_schema_extra = {
            "shortDescription": "Red Channel"
        }


class ConfigChannelGreen(Config):
    """Enable or disable the Green channel for histogram calculation."""
    name: Literal["configChannelGreen"] = "configChannelGreen"
    value: Union[Enabled, Disabled]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Green Channel"
        json_schema_extra = {
            "shortDescription": "Green Channel"
        }


class ConfigChannelBlue(Config):
    """Enable or disable the Blue channel for histogram calculation."""
    name: Literal["configChannelBlue"] = "configChannelBlue"
    value: Union[Enabled, Disabled]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Blue Channel"
        json_schema_extra = {
            "shortDescription": "Blue Channel"
        }


class ConfigChannelGray(Config):
    """Enable or disable the Gray Scale channel for histogram calculation."""
    name: Literal["configChannelGray"] = "configChannelGray"
    value: Union[Enabled, Disabled]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Gray Scale Channel"
        json_schema_extra = {
            "shortDescription": "Gray Scale Channel"
        }


class ConfigPlotImage(Config):
    """Enable or disable histogram plot image output."""
    name: Literal["configPlotImage"] = "configPlotImage"
    value: Union[Enabled, Disabled]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Histogram Plot"
        json_schema_extra = {
            "shortDescription": "Histogram Plot"
        }


class ConfigTileGridSize(Config):
    """Tile grid size for CLAHE processing."""
    name: Literal["configTileGridSize"] = "configTileGridSize"
    value: Union[TileGrid4x4, TileGrid8x8]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Tile Grid Size"
        json_schema_extra = {
            "shortDescription": "Grid Size"
        }


# Executor Inputs
class HistogramExecutorInputs(Inputs):
    inputImage: InputImage


class EqualizationExecutorInputs(Inputs):
    inputImage: InputImage


# Executor Configs
class HistogramExecutorConfigs(Configs):
    configChannelRed: ConfigChannelRed
    configChannelGreen: ConfigChannelGreen
    configChannelBlue: ConfigChannelBlue
    configChannelGray: ConfigChannelGray
    configPixelMin: ConfigPixelMin
    configPixelMax: ConfigPixelMax
    configPlotImage: ConfigPlotImage


class EqualizationExecutorConfigs(Configs):
    configClipLimit: ConfigClipLimit
    configTileGridSize: ConfigTileGridSize


# Executor Outputs
class HistogramExecutorOutputs(Outputs):
    outputImage: OutputImage
    outputData: OutputData


class EqualizationExecutorOutputs(Outputs):
    outputImage: OutputImage


# Requests
class HistogramExecutorRequest(Request):
    inputs: Optional[HistogramExecutorInputs]
    configs: HistogramExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class EqualizationExecutorRequest(Request):
    inputs: Optional[EqualizationExecutorInputs]
    configs: EqualizationExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


# Responses
class HistogramExecutorResponse(Response):
    outputs: HistogramExecutorOutputs


class EqualizationExecutorResponse(Response):
    outputs: EqualizationExecutorOutputs


# Executors
class HistogramExecutor(Config):
    name: Literal["Histogram"] = "Histogram"
    value: Union[HistogramExecutorRequest, HistogramExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Histogram"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class EqualizationExecutor(Config):
    name: Literal["Equalization"] = "Equalization"
    value: Union[EqualizationExecutorRequest, EqualizationExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Equalization"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# Main Package Model
class ConfigExecutor(Config):
    """
    Histogram analysis or histogram equalization
    can be performed on images.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[HistogramExecutor, EqualizationExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"
        json_schema_extra = {
            "shortDescription": "Select histogram operation type"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["HistogramUpdate"] = "HistogramUpdate"

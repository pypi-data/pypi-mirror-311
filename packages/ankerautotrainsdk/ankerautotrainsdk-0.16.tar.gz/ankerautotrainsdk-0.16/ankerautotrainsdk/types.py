from pydantic import BaseModel

class UploadFileResponse(BaseModel):
    url: str
    bucket: str
    storage_id: str
    object_name: str
    uid: str

class UploadRawDataResponse(BaseModel):
    raw_data_id: str

class UploadAnnotationDataResponse(BaseModel):
    annotation_data_id: str

class CreateDataSetResponse(BaseModel):
    dataset_id: str

class SummaryAndDownloadDataSetResponse(BaseModel):
    url: str
    bucket: str
    object_name: str


class CreateDatasetRequest(BaseModel): 
    """
    "bg": "string",
        "owner": "string",
        "labelMethod": "string",
        "modelVersion": "string",
        "modelName": "string",
        "annotationType": "detection",
        "labelQuery": {
          "label": "string",
          "score": 1
        },
        "mutipleLabelQuery": [
          {
            "label": "string",
            "score": 1
          }
        ],
        "dataId": "string",
        "modelType": "",
        "processState": "teacher",
        "startTime": "string",
        "endTime": "string"
    """
    bg: str = ""
    owner: str = ""
    labelMethod: str = ""
    modelVersion: str = ""
    modelName: str = ""
    annotationType: str = ""
    labelQuery: dict = {}
    mutipleLabelQuery: list = []
    dataId: str = ""
    modelType: str = ""
    processState: str = ""
    startTime: str = ""
    endTime: str = ""

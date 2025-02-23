from enum   import Enum

class ResponseSignals(Enum):
    FILE_TYPE_NOT_SUPPORTED="Unsupported File Type"
    FILE_EXCEEDED_MAXIMUM_SIZE="File Exceeded Maximum Size (5MB)"
    FILE_UPLOADED_SUCCESSFULLY="File Uploaded Successfully"
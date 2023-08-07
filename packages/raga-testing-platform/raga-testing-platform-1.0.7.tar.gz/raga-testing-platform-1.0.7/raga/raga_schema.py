from abc import ABC
from typing import Optional
from datetime import datetime

class RagaSchemaElement(ABC):
    def __init__(self):
        super().__init__()
        self.type: str
        self.model: Optional[str]
        self.ref_col_name: Optional[str]

class PredictionSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "prediction"
        self.model = ""
        self.ref_col_name = ""

class TimeOfCaptureSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "timestamp"
        self.model = ""
        self.ref_col_name = ""

class FeatureSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "feature"
        self.model = ""
        self.ref_col_name = ""
class AttributeSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "attribute"
        self.model = ""
        self.ref_col_name = ""

class InferenceSchemaElement(RagaSchemaElement):
    def __init__(self, model:str):
        self.type = "inference"
        self.model = model
        self.ref_col_name = ""

class ImageEmbeddingSchemaElement(RagaSchemaElement):
    def __init__(self, model:str, ref_col_name:str):
        self.type = "imageEmbedding"
        self.model = model
        self.ref_col_name = ref_col_name



class RagaSchema():
     def __init__(self):
        self.columns = list()

     
     def add(self, column_name: str, ragaSchemaElement):
         self.columns.append({"displayColumnName":column_name, "type":ragaSchemaElement.type, "model":ragaSchemaElement.model, "ref_col_name":ragaSchemaElement.ref_col_name})

class StringElement():
    def __init__(self, value:str):
        self.value = value

    def get(self):
        return self.value
class TimeStampElement():
    def __init__(self, date_time:datetime):
        self.date_time = date_time

    def get(self):
        return self.date_time

class ObjectDetection:
    def __init__(self, Id, ClassId, ClassName, BBox, Format, Confidence):
        self.Id = Id
        self.ClassId = ClassId
        self.ClassName = ClassName
        self.BBox = BBox
        self.Format = Format
        self.Confidence = Confidence

class ImageDetectionObject():
    def __init__(self):
        self.detections = list()
    
    def add(self, object_detection:ObjectDetection):
        self.detections.append(object_detection.__dict__)
    
    def get(self):
        return self.__dict__

class Embedding:
    def __init__(self, embedding: float):
        self.embedding = embedding

class ImageEmbedding:
    def __init__(self):
         self.embeddings = []

    def add(self, embedding_values: Embedding):
        self.embeddings.append(embedding_values.embedding)

    def get(self):
        return self.__dict__

class ROIEmbedding:
    def __init__(self):
         self.embeddings = []

    def add(self, embedding_values: Embedding):
        self.embeddings.append(embedding_values.embedding)

    def get(self):
        return self.__dict__

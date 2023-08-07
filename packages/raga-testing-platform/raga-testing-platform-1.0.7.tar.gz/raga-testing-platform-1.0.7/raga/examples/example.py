from raga import *
import pandas as pd
# Create a test DataFrame


AnnotationsV1 = ImageDetectionObject()
AnnotationsV1.add(ObjectDetection(Id = 0, ClassId = 2, ClassName = 'Person', BBox = [0.213, 0.324, 0.267, 0.452], Format = 'xywh_normalized', Confidence = 1))
AnnotationsV1.add(ObjectDetection(Id = 0, ClassId = 2, ClassName = 'Person', BBox = [0.213, 0.324, 0.267, 0.452], Format = 'xywh_normalized', Confidence = 1))

ImageVectorsM1 = ImageEmbedding()
ImageVectorsM1.add(Embedding(1.3246))
ImageVectorsM1.add(Embedding(1.3246))
ImageVectorsM1.add(Embedding(1.3246))
ImageVectorsM1.add(Embedding(1.3246))
ImageVectorsM1.add(Embedding(1.3246))
ImageVectorsM1.add(Embedding(1.3246))

ROIVectorsM1 = ROIEmbedding()
ROIVectorsM1.add(Embedding(1.3246))
ROIVectorsM1.add(Embedding(1.3246))
ROIVectorsM1.add(Embedding(1.3246))
ROIVectorsM1.add(Embedding(1.3246))
ROIVectorsM1.add(Embedding(1.3246))
ROIVectorsM1.add(Embedding(1.3246))

ROIVectorsM3 = ROIEmbedding()
ROIVectorsM3.add(Embedding(1.3246))
ROIVectorsM3.add(Embedding(1.3246))
ROIVectorsM3.add(Embedding(1.3246))
ROIVectorsM3.add(Embedding(1.3246))
ROIVectorsM3.add(Embedding(1.3246))
ROIVectorsM3.add(Embedding(1.3246))


test_df = pd.DataFrame({
    'ImageId': [StringElement("c2f10892-f544-11ed-a05b-0242ac120003")],
    'TimeOfCapture': [TimeStampElement("2008-09-17 14:02:00")],
    'SourceLink': [StringElement("https://imgur.com/gallery/JGyOM6c")],
    'Weather': [StringElement("Foggy")],
    'TimeOfDay': [StringElement("Dawn")],
    'Scene': [StringElement("High Way")],
    'AnnotationsV1': [AnnotationsV1],
    'ImageVectorsM1': [ImageVectorsM1],
    'ROIVectorsM1': [ROIVectorsM1],
    'ROIVectorsM3': [ROIVectorsM3],
})



schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("Weather", AttributeSchemaElement())
schema.add("TimeOfDay", AttributeSchemaElement())
schema.add("Scene", AttributeSchemaElement())
schema.add("AnnotationsV1", InferenceSchemaElement(model="TeamB_V2"))
schema.add("ModelAInferences", InferenceSchemaElement(model="yolov6"))
schema.add("ROIVectorsM1", ImageEmbeddingSchemaElement(model="yolov6", ref_col_name="AnnotationsV1"))
schema.add("ROIVectorsM3", ImageEmbeddingSchemaElement(model="yolov6", ref_col_name="ModelAInferences"))

# print(schema.columns)

test_session = TestSession("testingProject", "new_test_experiment36")

# Create an instance of the Dataset class
test_ds = Dataset(test_session, "ExpDataset9")

test_ds.load(test_df, schema)

test_ds.load(
    "/Users/manabroy/Downloads/data.json", 
    format="coco", 
    model_name="modelA",
    inference_col_name="modelAInferences",
    embedding_col_name="imageEmbedding"
    )



# json_data = [
#     {
#         "ImageId":"c2f10892-f544-11ed-a05b-0242ac120003",
#         "TimeOfCapture":"2008-09-17 14:02:00",
#         "SourceLink":"https://imgur.com/gallery/JGyOM6c",
#         "Weather":"Foggy",
#         "TimeOfDay":"Dawn",
#         "CustomerId":1,
#         "AnnotationsV1":[.__dict__, ObjectDetection(Id = 0, ClassId = 2, ClassName = 'Person', BBox = [0.213, 0.324, 0.267, 0.452], Format = 'xywh_normalized', Confidence = 1).__dict__],
#         "ModelAInfernences":[ObjectDetection(Id = 0, ClassId = 2, ClassName = 'Person', BBox = [0.213, 0.324, 0.267, 0.452], Format = 'xywh_normalized', Confidence = 1).__dict__, ObjectDetection(Id = 0, ClassId = 2, ClassName = 'Person', BBox = [0.213, 0.324, 0.267, 0.452], Format = 'xywh_normalized', Confidence = 1).__dict__],
#         "ModelBInfernences":[ObjectDetection(Id = 0, ClassId = 2, ClassName = 'Person', BBox = [0.213, 0.324, 0.267, 0.452], Format = 'xywh_normalized', Confidence = 1).__dict__, ObjectDetection(Id = 0, ClassId = 2, ClassName = 'Person', BBox = [0.213, 0.324, 0.267, 0.452], Format = 'xywh_normalized', Confidence = 1).__dict__],
#         "ImageVectorsM1":[1.3246, 0.2136,0.7842],
#         "ROIVectorsM1":{ 1: [0.321, 0.216, 0.576], 0 : [0.123, 0.612, 0.56]},
#         "ROIVectorsM3":{ 1: [0.321, 0.216, 0.576], 0 : [0.123, 0.612, 0.56]}
#     }
# ]

# # test_df = pd.DataFrame(json_data)

# # # json_data = test_df.to_json(orient='records')
# # print(test_df)
# # test_df.to_csv('data1.csv', index=False)

# # Create an instance of the RagaSchema class
# schema = RagaSchema()
# schema.add("ImageId", PredictionSchemaElement())
# schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
# schema.add("SourceLink", FeatureSchemaElement())
# schema.add("Weather", AttributeSchemaElement())
# schema.add("TimeOfDay", AttributeSchemaElement())
# schema.add("Scene", AttributeSchemaElement())
# schema.add("AnnotationsV1", InferenceSchemaElement(model="TeamB_V2"))
# schema.add("ModelAInferences", InferenceSchemaElement(model="yolov6"))
# schema.add("ROIVectorsM1", ImageEmbeddingSchemaElement(model="yolov6", ref_col_name="AnnotationsV1"))
# schema.add("ROIVectorsM3", ImageEmbeddingSchemaElement(model="yolov6", ref_col_name="ModelAInferences"))

# print(schema.columns)












# # Create an instance of the TestSession class
# test_session = TestSession("testingProject", "new_test_experiment23")

# # # print(test_session.token)
# # # Create an instance of the Dataset class
# test_ds = Dataset(test_session, "TestDB")

# test_ds.load(test_df, schema)
# # test_ds.load(
# #     "/Users/manabroy/Downloads/data.json", 
# #     format="coco", 
# #     image_id="_id", 
# #     type="inference", 
# #     label_name="modelA",
# #     col_name="modelAInferences",
# #     class_map="coco_mapping"
# #     )

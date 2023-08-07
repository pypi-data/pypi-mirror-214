from raga import *
import pandas as pd
# Create a test DataFrame

ds_json = [
    {
        "inputs": [
            "Screenshot 2023-03-04 020607.png"
        ],
        "attributes": {
            "Resolution": "Medium",
            "Scene": "City"
        },
        "capture_time": 1679911432,
        "source": "self_serve-Video-surveillance",
        "event_index": "",
        "output_type": "",
        "model_id": "57_improved",
        "outputs": [
            {
                "frame_id": 1,
                "time_offset_ms": 0,
                "infer_time": 0,
                "detections": []
            }
        ],
        "image_embedding": [
            33,
            222,
            245
        ],
        "caption": "a person holding a tennis racket in a room",
        "drift": 0.20173455400663232
    },
    {
        "inputs": [
            "Screenshot 2023-03-04 015704.png"
        ],
        "attributes": {
            "Resolution": "Medium",
            "Scene": "City"
        },
        "capture_time": 1679911433,
        "source": "self_serve-Video-surveillance",
        "event_index": "",
        "output_type": "",
        "model_id": "57_improved",
        "outputs": [
            {
                "frame_id": 1,
                "time_offset_ms": 0,
                "infer_time": 0,
                "detections": [
                    {
                        "class": "gun",
                        "bbox": [
                            0.3346329411764706,
                            0.4015065913370998,
                            0.13258823529411765,
                            0.12222222222222223
                        ],
                        "confidence": 0.5795732782766414,
                        "roi_embedding": [
                            0.100707054,
                            0.21049209,
                            0.007840108,
                            0.36408848,
                            -0.26238978,
                            0.7100653,
                            0.19569194,
                            -0.26841936,
                            0.46218634,
                            0.2062045
                        ]
                    }
                ]
            }
        ],
        "image_embedding": [
            -39,
            249,
            203
        ],
        "caption": "a toy doll sitting on a table in a room",
        "drift": 0.2603237045996466
    }
]

pd_ds = pd.DataFrame(ds_json)

print(pd_ds.to_csv("MA.csv"))
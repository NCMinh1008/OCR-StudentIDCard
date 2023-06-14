import json
import cv2 
import os


 

with open('data_root_dir/kili-label-export-OCR-data-2023-06-13_18-17.json') as f:
    data = json.load(f)


IMAGE_DIR = "data_root_dir/ch4_training_images" 
GT_DIR = "data_root_dir/ch4_training_localization_transcription_gt"      
gt = []

for idx in range(len(data)):
    label = []

    filename = data[idx]["externalId"]
    img = cv2.imread(os.path.join(IMAGE_DIR, filename), 0) 
    img_dim = img.shape
    label.append(filename)

    name = []
    bbox = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB"]["annotations"][0]["boundingPoly"][0]["normalizedVertices"]
    text = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB"]["annotations"][0]["children"]["TRANSCRIPTION_JOB"]["text"]
    for i in range(len(bbox)):
        name.append(int(bbox[i]["x"]*img_dim[1]))
        name.append(int(bbox[i]["y"]*img_dim[0]))
    name.append(text)
    label.append(name)


    dob = []
    bbox = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_0"]["annotations"][0]["boundingPoly"][0]["normalizedVertices"]
    text = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_0"]["annotations"][0]["children"]["TRANSCRIPTION_JOB_0"]["text"]
    for i in range(len(bbox)):
        dob.append(int(bbox[i]["x"]*img_dim[1]))
        dob.append(int(bbox[i]["y"]*img_dim[0]))
    dob.append(text)
    label.append(dob)


    major = []
    bbox = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_1"]["annotations"][0]["boundingPoly"][0]["normalizedVertices"]
    text = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_1"]["annotations"][0]["children"]["TRANSCRIPTION_JOB_1"]["text"]
    for i in range(len(bbox)):
        major.append(int(bbox[i]["x"]*img_dim[1]))
        major.append(int(bbox[i]["y"]*img_dim[0]))
    major.append(text)
    label.append(major)


    id = []
    bbox = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_2"]["annotations"][0]["boundingPoly"][0]["normalizedVertices"]
    text = data[idx]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_2"]["annotations"][0]["children"]["TRANSCRIPTION_JOB_2"]["text"]
    for i in range(len(bbox)):
        id.append(int(bbox[i]["x"]*img_dim[1]))
        id.append(int(bbox[i]["y"]*img_dim[0]))
    id.append(text)
    label.append(id)


    valid_date = []
    bbox = data[0]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_3"]["annotations"][0]["boundingPoly"][0]["normalizedVertices"]
    text = data[0]["latestLabel"]["jsonResponse"]["OBJECT_DETECTION_JOB_3"]["annotations"][0]["children"]["TRANSCRIPTION_JOB_3"]["text"]
    for i in range(len(bbox)):
        valid_date.append(int(bbox[i]["x"]*img_dim[1]))
        valid_date.append(int(bbox[i]["y"]*img_dim[0]))
    valid_date.append(text)
    label.append(valid_date)

    gt.append(label)


for i in range(len(gt)):
    filename = "gt_" + gt[i][0].split(".")[0] + ".txt"
    with open(os.path.join(GT_DIR, filename), "a") as f:
        for j in range(1,6):
            for m in range(len(gt[i][j])-1):
                f.write(str(gt[i][j][m]) + ",")
            f.write(str(gt[i][j][m+1]) + "\n") 

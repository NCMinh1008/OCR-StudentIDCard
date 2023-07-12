import pandas as pd
import numpy as np
import PIL
from PIL import Image
from PIL import ImageDraw
import gradio as gr
import torch
import easyocr
import argparse
from infer import cal_eval
from config.load_config import load_yaml, DotDict

import pytesseract
import shutil
import os
import random
import cv2
import matplotlib.pyplot as plt
try:
    from PIL import Image
except ImportError:
    from PIL import Image 

def draw_boxes(image, bounds, color='yellow', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        # print(bound)
        # p0, p1, p2, p3 = bound[0]
        p0, p1, p2, p3 = bound
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image

def inference(img_path, lang):
    #load image
    img = PIL.Image.open(img_path)

    # ============================ Scene Text Detection ============================
    parser = argparse.ArgumentParser(description="CRAFT Text Detection Eval")
    parser.add_argument(
        "--yaml",
        "--yaml_file_name",
        default="custom_data_train",
        type=str,
        help="Load configuration",
    )

    args = parser.parse_args()

    # load configure
    config = load_yaml(args.yaml)
    config = DotDict(config)

    val_result_dir_name = args.yaml
    total_imgs_bboxes_pre = cal_eval(
        img_path,
        config,
        "custom_data",
        val_result_dir_name + "-ic15-iou",
        opt="iou_eval",
        mode=None,
    )

    bounds = []
    extracted_info = []
    
    for idx in range(len(total_imgs_bboxes_pre[0])):
        bound = total_imgs_bboxes_pre[0][idx]["points"].tolist()
        bounds.append(bound)

    # ============================ Text Recognition ============================
    for bound in bounds:
        p0, p1, p2, p3 = bound
        x1, y1 = p0
        x2, y2 = p1
        x3, y3 = p2
        x4, y4 = p3

        top_left_x = min([x1,x2,x3,x4])
        top_left_y = min([y1,y2,y3,y4])
        bot_right_x = max([x1,x2,x3,x4])
        bot_right_y = max([y1,y2,y3,y4])

        lang = 'vie' 
        config = r'--oem 3 --psm 6'

        cropped_img = img.crop((top_left_x, top_left_y, bot_right_x, bot_right_y))
        extractedInformation = pytesseract.image_to_string(cropped_img, lang=lang, config=config)

        extractedInformation = extractedInformation.strip()  # Remove newline characters
        print(extractedInformation)        
        extracted_info.append(extractedInformation)
        

    # ====================================================================================

    # reader = easyocr.Reader(lang)
    # bounds = reader.readtext(img_path)
    # print(bounds)
    draw_boxes(img, bounds)
    img.save('result.jpg')
    # return ['result.jpg', pd.DataFrame(extracted_info).iloc[: , 1:]]
    df = pd.DataFrame(extracted_info, columns=['Extracted Information'])
    df = df.rename_axis(None, axis=1)

    return ['result.jpg', df]
            
title = 'STUDENT ID INFORMATION EXTRACTION'
description = '<div style="text-align: center;"><h3>Demo for Student ID information extraction</h3><p>To use it, simply upload your image and choose a language from the dropdown menu.</p></div>'
choices = [
    "en",
    "uk",
    "vi"
]

gr.Interface(
    inference,
    [gr.inputs.Image(type='filepath',label='Input'),gr.inputs.CheckboxGroup(choices, type="value", default=['vi'], label='Language')],
    [gr.outputs.Image(type='filepath',label='Output'), gr.outputs.Dataframe(type='array', headers=['Extracted Information'], label='Output')],
    title=title,
    description=description,
    allow_flagging="manual",
    flagging_options=["Correct", "Wrong"],
    flagging_dir="Results",
    enable_queue=True   
    ).launch(debug=True)
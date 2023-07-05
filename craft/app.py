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

def draw_boxes(image, bounds, color='yellow', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image

def inference(img_path, lang):
    # ============================
    parser = argparse.ArgumentParser(description="CRAFT Text Detection Eval")
    parser.add_argument(
        "--yaml",
        "--yaml_file_name",
        default="custom_data_train",
        type=str,
        help="Load configuration",
    )
    parser.add_argument(
        "--img_path",
        "--img_path",
        default="custom_data_train.png",
        type=str,
        help="Load configuration",
    )
    args = parser.parse_args()

    # load configure
    config = load_yaml(args.yaml)
    config = DotDict(config)

    # load image path
    img_path = args.img_path

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
    for idx in range(len(total_imgs_bboxes_pre[0][0])):
        print(total_imgs_bboxes_pre[0][0][idx]["points"])
        # bound = total_imgs_bboxes_pre[0][0][idx]["points"].tolist()
        # bounds.append(bound)

    # ============================
    reader = easyocr.Reader(lang)
    bounds = reader.readtext(img_path)
    print(bounds)
    im = PIL.Image.open(img_path)
    draw_boxes(im, bounds)
    im.save('result.jpg')
    return ['result.jpg', pd.DataFrame(bounds).iloc[: , 1:]]   

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
    [gr.outputs.Image(type='filepath',label='Output'), gr.outputs.Dataframe(type='array', headers=['Text', 'Confidence'], label='Output')],
    title=title,
    description=description,
    allow_flagging="manual",
    flagging_options=["Correct", "Wrong"],
    flagging_dir="Results",
    enable_queue=True   
    ).launch(debug=True)
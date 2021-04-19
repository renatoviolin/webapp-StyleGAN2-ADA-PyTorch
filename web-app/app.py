import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
from api.api_generate import *

import jinja2
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import uuid
import logging
import numpy as np
import cv2
import torch
import glob
from PIL import Image
env = jinja2.Environment()
env.globals.update(zip=zip)

IMAGES_FOLDER = '../images'
UPLOAD_FOLDER = './uploads'
Z_FOLDER = '../z_output'
app = FastAPI()
app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.mount("/images", StaticFiles(directory=IMAGES_FOLDER), name="images")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    z_files = sorted(glob.glob(f'{IMAGES_FOLDER}/*.jpg'))
    files = [f.split('/')[-1] for f in z_files]
    names = [f.split('.')[0] for f in files]
    z_file = {'file': files, 'name': names}
    return templates.TemplateResponse("style_transfer.html", context={'request': request, 'z_file': files, 'z_name': names, 'zip': zip})


@app.get("/generate", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("generate.html", context={'request': request})


@app.post('/api/process_style')
async def process_style(request: Request):
    try:
        form = await request.form()
        source_image = form.get('source_image')
        style_image = form.get('style_image')
        z_start = int(form.get('z_start'))
        z_end = int(form.get('z_end'))

        proj_a = f"{Z_FOLDER}/{source_image.split('.')[0]}.npz"
        proj_b = f"{Z_FOLDER}/{style_image.split('.')[0]}.npz"

        proj_replaced = load_replace_projection(proj_a, proj_b, slice(z_start, z_end))
        img_replaced = generate_from_projection(proj_replaced)
        
        file_name = f'{IMAGES_FOLDER}/generated/{str(uuid.uuid1()).split("-")[0]}.jpg'
        img_replaced.save(file_name)

        return JSONResponse(status_code=200, content={'image': file_name.split('/')[-1]})
    except Exception as ex:
        logging.error(ex)
        return JSONResponse(status_code=400, content={})


@app.post('/api/process_generate')
async def process_generate(request: Request):
    try:
        form = await request.form()
        seed = int(form.get('seed'))

        img_generated = generate_from_seed(seed)
        file_name = f'{IMAGES_FOLDER}/generated/{str(uuid.uuid1()).split("-")[0]}.jpg'
        img_generated.save(file_name)

        return JSONResponse(status_code=200, content={'image': file_name.split('/')[-1]})
    except Exception as ex:
        logging.error(ex)
        return JSONResponse(status_code=400, content={})
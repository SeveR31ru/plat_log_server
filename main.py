from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn
import configparser
import os
from datamatrix import datamatrix_create
import generate_html
import note

PATH_OCP='ocp_logs'
PATH_TOFINO='tofino_logs'

try:
    # получение конфигов
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    host = str(config["COMMON"]["host"])
    port = int(config["COMMON"]["port"])
    printerName = str(config["COMMON"]["printerName"])
except:
    pass

if not os.path.exists("web"):
    os.mkdir("web")

app = FastAPI()
templates = Jinja2Templates(directory="web")

#Get-запросы

@app.get("/")
def main(request: Request):
    generate_html.generate_start_html()
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/get_datamatrix")
def getDatamatrix(datamatrix_data: str):
    datamatrix_create(datamatrix_data)
    return {"datamatrix_data ":datamatrix_data}

@app.get("/get_fast_ocp_logs")
def getFastOcpLogs(ocp_code:str,request: Request):
    generate_html.generate_fast_ocp_logs(ocp_code)
    return templates.TemplateResponse(f"{ocp_code}.html",{"request": request})

@app.get("/get_big_ocp_log")
def getBigOcpLog(log_path:str,request:Request):
    generate_html.generate_big_ocp_log(log_path)
    return templates.TemplateResponse(f"{log_path}.html",{"request":request})

@app.get("/get_fast_tofino_logs")
def getFastOcpLogs(tofino_code:str,request: Request):
    generate_html.generate_fast_tofino_logs(tofino_code)
    return templates.TemplateResponse(f"{tofino_code}.html",{"request": request})
@app.get("/get_big_tofino_log")
def getBigOcpLog(log_path:str,request:Request):
    generate_html.generate_big_tofino_log(log_path)
    return templates.TemplateResponse(f"{log_path}.html",{"request":request})

@app.get("/send_note")
def GetNotes(code:str,note:str): 
    note.add_note(code,note)
'''
ToDo-переделать на будущее, 
чтобы можно было скачивать все логи выбранной платы в архиве
@app.get("/download_logs")
def getLogs(name:str):
    res=FileResponse(name,media_type='application/octet-stream', filename=name)
    return res
'''

#Post-запросы

@app.post("/send_ocp")
def getLogs(file:UploadFile):
    if not os.path.exists(f'{PATH_OCP}'):
        os.mkdir(f"{PATH_OCP}")
    name=file.filename
    name_split=name.split("_")
    content=file.file.read().decode()
    if not os.path.exists(f'{PATH_OCP}/{name_split[1]}'):
        os.mkdir(f"{PATH_OCP}/{name_split[1]}")
    f=open(f'{PATH_OCP}/{name_split[1]}/{name}',"w+")
    f.write(f"{content}")
    f.close() 
    return name

@app.post("/send_tofino")
def getLogs(file:UploadFile):
    if not os.path.exists(f'{PATH_TOFINO}'):
        os.mkdir(f"{PATH_TOFINO}")
    name=file.filename
    name_split=name.split("_")
    content=file.file.read().decode()
    if not os.path.exists(f'{PATH_TOFINO}/{name_split[1]}'):
        os.mkdir(f"{PATH_TOFINO}/{name_split[1]}")
    f=open(f'{PATH_TOFINO}/{name_split[1]}/{name}',"w+")
    f.write(f"{content}")
    f.close() 
    return name




uvicorn.run(app, host=host, port=port)


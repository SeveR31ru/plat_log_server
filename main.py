from fastapi import FastAPI, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import configparser
import os
from datamatrix import datamatrix_create
import generate_html 
import note as nt


try:
    # получение конфигов
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    host = str(config["COMMON"]["host"])
    port = int(config["COMMON"]["port"])
    printerName = str(config["COMMON"]["printerName"])
    PATH_OCP=str(config["COMMON"]["path_ocp"])
    PATH_TOFINO=str(config["COMMON"]["path_tofino"])
    PATH_OCP_PASS=str(config["COMMON"]["path_ocp_passports"])
    PATH_USED_OCP_PASS=str(config["COMMON"]["path_used_passports"])

except:
    pass

if not os.path.exists("web"):
    os.mkdir("web")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="web")

#Get-запросы

@app.get("/")
def main(request: Request):
    generate_html.generate_start_html()
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/get_datamatrix")
def get_datamatrix(datamatrix_data: str):
    datamatrix_create(datamatrix_data)
    return {"datamatrix_data ":datamatrix_data}

#Get-запросы для формирования лог-страниц 

@app.get("/get_fast_ocp_logs")
def get_fast_ocp_logs(ocp_code:str,request: Request):
    generate_html.generate_fast_ocp_logs(ocp_code)
    return templates.TemplateResponse(f"{ocp_code}.html",{"request": request})

@app.get("/get_big_ocp_log")
def get_big_ocp_log(log_path:str,request:Request):
    generate_html.generate_big_ocp_log(log_path)
    return templates.TemplateResponse(f"{log_path}.html",{"request":request})

@app.get("/get_fast_tofino_logs")
def get_fast_ocp_logs(tofino_code:str,request: Request):
    generate_html.generate_fast_tofino_logs(tofino_code)
    return templates.TemplateResponse(f"{tofino_code}.html",{"request": request})
@app.get("/get_big_tofino_log")
def get_big_ocp_log(log_path:str,request:Request):
    generate_html.generate_big_tofino_log(log_path)
    return templates.TemplateResponse(f"{log_path}.html",{"request":request})


'''
ToDo-переделать на будущее, 
чтобы можно было скачивать все логи выбранной платы в архиве
@app.get("/download_logs")
def getLogs(name:str):
    res=FileResponse(name,media_type='application/octet-stream', filename=name)
    return res
'''

#Post-запросы

@app.post("/send_note")
def send_notes(data=Body()): 
    code=data["code"]
    note=data["note"]
    nt.add_note(code, note)
    return None

#запросы для отсылки логов

@app.post("/send_ocp")
def send_ocp_logs(file:UploadFile):
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
def send_tofino_logs(file:UploadFile):
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

#запросы для выдачи паспортов


@app.post("/receive_ocp_pass")
def receive_ocp_pass(serialNumber:str):
    #создаем папки, если они не созданы
    if not os.path.exists(PATH_OCP_PASS):
        os.mkdir(PATH_OCP_PASS)
    if not os.path.exists(PATH_USED_OCP_PASS):
        os.mkdir(PATH_USED_OCP_PASS)
    #проверяем, есть ли паспорта
    list_os_passports=os.listdir(PATH_OCP_PASS)
    if not list_os_passports:
        return('Папка с паспортами пуста')
    pass_file_name=list_os_passports[0]
    #перемещаем взятый паспорт в папку использованных
    os.rename(f'{PATH_OCP_PASS}/{pass_file_name}', f'{PATH_USED_OCP_PASS}/{pass_file_name}')
    nt.add_ocp_pass_note(serialNumber, pass_file_name)
    pass_file_path=f'{PATH_USED_OCP_PASS}/{pass_file_name}'
    res = FileResponse(pass_file_path, media_type='application/octet-stream', filename=pass_file_name)
    return res
    
uvicorn.run(app, host=host, port=port)


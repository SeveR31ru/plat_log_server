from fastapi import FastAPI, Request, Body,HTTPException,UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import configparser
import os
from datamatrix import datamatrix_create
import generate_html 
import note as nt
import passport as passp


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
    PATH_PLATFORM=str(config["COMMON"]["path_platform"])

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
    try:
        generate_html.generate_fast_ocp_logs(ocp_code)
    except:
        raise HTTPException(status_code=404, detail="Нет платы OCP с таким номером в системе")
    return templates.TemplateResponse(f"{ocp_code}.html",{"request": request})

@app.get("/get_big_ocp_log")
def get_big_ocp_log(log_path:str,request:Request):
    generate_html.generate_big_ocp_log(log_path)
    return templates.TemplateResponse(f"{log_path}.html",{"request":request})

@app.get("/get_fast_tofino_logs")
def get_fast_ocp_logs(tofino_code:str,request: Request):
    try:
        generate_html.generate_fast_tofino_logs(tofino_code)
    except:
         raise HTTPException(status_code=404, detail="Нет платы TOFINO с таким номером в системе")
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

#запрос для выдачи паспорта OCP

@app.post("/give_ocp_mac")
def give_ocp_pass_mac(serialNumber:str):
    #создаем папки, если они не созданы
    mac=passp.give_mac(serialNumber)
    if mac  == 2:
        raise HTTPException(status_code=404, detail="Folder is empty")
    elif mac ==2:
        raise HTTPException(status_code=404, detail="Cannot open table")
    elif mac== 3:
        raise HTTPException(status_code=404, detail="Table is empty")
    elif mac ==4:
        raise HTTPException(status_code=404, detail="This code already have a mac")
    return mac

@app.post("/give_serial_by_ocp")
def give_ocp_pass_serial(serialNumber:str):
    try:
        mac_serial=passp.get_serial(serialNumber)
    except:
        raise HTTPException(status_code=404, detail="This OCP dont have mac_serial,give him mac first")
    return mac_serial

'''
@app.post("/send_platform")
def send_platform(ocp_code:str,tofino_code:str):
    zero=0
'''


uvicorn.run(app, host=host, port=port)


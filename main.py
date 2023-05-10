from fastapi import FastAPI, Request, Body, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
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
    PATH_OCP = str(config["COMMON"]["path_ocp"])
    PATH_TOFINO = str(config["COMMON"]["path_tofino"])
    PATH_OCP_PASS = str(config["COMMON"]["path_ocp_passports"])
    PATH_CONTROLPASS = str(config["COMMON"]["path_controlpass"])
    PATH_PLATFORM = str(config["COMMON"]["path_platform"])
    if not os.path.exists(PATH_OCP):
        os.mkdir(PATH_OCP)
    if not os.path.exists(PATH_TOFINO):
        os.mkdir(PATH_TOFINO)
    if not os.path.exists("notes.csv"):
        create_note_table = pd.DataFrame(columns=["code", "note", "time"])
        create_note_table.to_csv("notes.csv", index=False)
    if not os.path.exists("ocp_given_passports.csv"):
        create_used_pass_table = pd.DataFrame(
            columns=["ocp_number", "mac", "pass_serial_number"])
        create_used_pass_table.to_csv("ocp_given_passports.csv", index=False)
    if not os.path.exists(PATH_OCP_PASS):
        os.mkdir(PATH_OCP_PASS)
    if not os.path.exists(f'{PATH_CONTROLPASS}'):
        os.mkdir(f"{PATH_CONTROLPASS}")
except:
    pass


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Get-запросы


@app.get("/")
def main():
    html = generate_html.generate_start_html()
    return HTMLResponse(html)


@app.get("/get_datamatrix")
def get_datamatrix(datamatrix_data: str):
    datamatrix_create(datamatrix_data)
    return {"datamatrix_data ": datamatrix_data}

# Get-запросы для формирования лог-страниц


@app.get("/get_fast_ocp_logs")
def get_fast_ocp_logs(ocp_code: str):
    try:
        html = generate_html.generate_fast_ocp_logs(ocp_code)
    except:
        text="Нет платы OCP с таким номером в системе"
        html=generate_html.generate_answer(text)
    return HTMLResponse(html)


@app.get("/get_fast_tofino_logs")
def get_fast_ocp_logs(tofino_code: str):
    try:
        html = generate_html.generate_fast_tofino_logs(tofino_code)
    except:
        text="Нет платы TOFINO с таким номером в системе"
        html=generate_html.generate_answer(text)
    return HTMLResponse(html)


@app.get("/get_fast_controlpass_logs")
def get_fast_controlpass_logs(controlpass_code: str):
    try:
        html = generate_html.generate_fast_controlpass_logs(controlpass_code)
    except:
        text="Нет Controlpass с таким номером в системе"
        html=generate_html.generate_answer(text)
    return HTMLResponse(html)

#общие get-запросы
@app.get("/get_list_of_devices")
def get_list_of_devices():
    html = generate_html.generate_list_of_devices()
    return HTMLResponse(html)


@app.get("/get_big_log")
def get_big_lig(log_path: str, type: int):
    html = generate_html.generate_big_log(log_path, type)
    return HTMLResponse(html)


'''
ToDo-сделать на будущее, 
чтобы можно было скачивать все логи выбранной платы в архиве
@app.get("/download_logs")
def getLogs(name:str):
    res=FileResponse(name,media_type='application/octet-stream', filename=name)
    return res
'''

##Post-запросы


@app.post("/send_note")
def send_notes(data=Body()):
    code = data["code"]
    note = data["note"]
    nt.add_note(code, note)
    return None

# запросы для отсылки логов


@app.post("/send_ocp")
def send_ocp_logs(file: UploadFile):
    if not os.path.exists(f'{PATH_OCP}'):
        os.mkdir(f"{PATH_OCP}")
    name = file.filename
    name_split = name.split("_")
    content = file.file.read().decode()
    if not os.path.exists(f'{PATH_OCP}/{name_split[1]}'):
        os.mkdir(f"{PATH_OCP}/{name_split[1]}")
    f = open(f'{PATH_OCP}/{name_split[1]}/{name}', "w+")
    f.write(f"{content}")
    f.close()
    return name


@app.post("/send_tofino")
def send_tofino_logs(file: UploadFile):
    if not os.path.exists(f'{PATH_TOFINO}'):
        os.mkdir(f"{PATH_TOFINO}")
    name = file.filename
    name_split = name.split("_")
    content = file.file.read().decode()
    if not os.path.exists(f'{PATH_TOFINO}/{name_split[1]}'):
        os.mkdir(f"{PATH_TOFINO}/{name_split[1]}")
    f = open(f'{PATH_TOFINO}/{name_split[1]}/{name}', "w+")
    f.write(f"{content}")
    f.close()
    return name


@app.post("/send_controlpass")
def send_controlpass_logs(file: UploadFile):
    if not os.path.exists(f'{PATH_CONTROLPASS}'):
        os.mkdir(f"{PATH_CONTROLPASS}")
    name = file.filename
    name_split = name.split("_")
    content = file.file.read().decode()
    if not os.path.exists(f'{PATH_CONTROLPASS}/{name_split[1]}'):
        os.mkdir(f"{PATH_CONTROLPASS}/{name_split[1]}")
    f = open(f'{PATH_CONTROLPASS}/{name_split[1]}/{name}', "w+")
    f.write(f"{content}")
    f.close()
    return name

# запрос для выдачи паспорта OCP


@app.post("/give_ocp_mac")
def give_ocp_pass_mac(serialNumber: str):
    mac = passp.give_mac(serialNumber)
    if mac == 2:
        raise HTTPException(status_code=404, detail="Folder is empty")
    elif mac == 2:
        raise HTTPException(status_code=404, detail="Cannot open table")
    elif mac == 3:
        raise HTTPException(status_code=404, detail="Table is empty")
    elif mac == 4:
        raise HTTPException(
            status_code=404, detail="This code already have a mac")
    return mac


@app.post("/give_serial_by_ocp")
def give_ocp_pass_serial(serialNumber: str):
    try:
        mac_serial = passp.get_serial(serialNumber)
    except:
        raise HTTPException(
            status_code=404, detail="This OCP dont have mac_serial,give him mac first")
    return mac_serial


uvicorn.run(app, host=host, port=port)

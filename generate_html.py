import configparser
import jinja2
from jinja2 import Environment, FileSystemLoader
import os
import note as nt
import configparser
import passport as passp

try:
    # получение конфигов
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    PATH_OCP = str(config["COMMON"]["path_ocp"])
    PATH_TOFINO = str(config["COMMON"]["path_tofino"])
    PATH_CONTROLPASS = str(config["COMMON"]["path_controlpass"])
    env = Environment(loader=FileSystemLoader('templates'))
except:
    pass


"""
Все функции, связанные с генерацией html-страниц для логов

"""


# OCP-функции

def generate_fast_ocp_logs(ocp_code: str):
    '''
    Функция генерации таблицы логов и заметок для выбранной платы OCP
    
    аргументы:
    @ocp_code-номер OCP-платы
    return:
    html- сгенерированная html-страница
    
    '''

    ocp_logs_files = os.listdir(f"{PATH_OCP}/{ocp_code}")
    list_of_notes = nt.read_note(ocp_code)
    list_of_cut_names = []

    for log_name in ocp_logs_files:
        try:
            status = 'success'
            log_cut_name = log_name.split("_")
            list_of_cut_names.append(log_cut_name)
            log = open(f'{PATH_OCP}/{ocp_code}/{log_name}')
            lines = log.readlines()
            for line in lines:
                if line.find('INMYS_FAILED') != -1:
                    status = 'failed'
                    break
            log_cut_name.append(status)
        except:
            continue
    try:
        pass_mac = passp.get_mac(ocp_code)
    except:
        pass_mac = "не выдан"
    try:
        pass_serial = passp.get_serial(ocp_code)
    except:
        pass_serial = "не выдан"
    template = env.get_template('fast_ocp_logs.html')
    html = template.render(code=ocp_code,
                           list_of_cut_names=list_of_cut_names,
                           list_of_notes=list_of_notes,
                           pass_mac=pass_mac,
                           pass_serial=pass_serial)
    return html


# TOFINO-функции

def generate_fast_tofino_logs(tofino_code: str):
    '''
    Функция генерации таблицы логов и заметок для выбранной платы TOFINO
    
    аргументы:
    @tofino_code-номер TOFINO-платы
    return:
    hmml-сгенерированная html-страница
    
    '''

    tofino_logs_files = os.listdir(f"{PATH_TOFINO}/{tofino_code}")
    list_of_notes = nt.read_note(tofino_code)
    list_of_cut_names = []
    for log_name in tofino_logs_files:
        try:
            status = 'success'
            log_cut_name = log_name.split("_")
            list_of_cut_names.append(log_cut_name)
            log = open(f'{PATH_TOFINO}/{tofino_code}/{log_name}')
            lines = log.readlines()
            for line in lines:
                if line.find('INMYS_FAILED') != -1:
                    status = 'failed'
                    break
            log_cut_name.append(status)
        except:
            continue
    template = env.get_template("fast_tofino_logs.html")
    html = template.render(code=tofino_code,
                           list_of_cut_names=list_of_cut_names,
                           list_of_notes=list_of_notes)
    return html


# Controlpass-Функции
def generate_fast_controlpass_logs(controlpass_code: str):
    '''
    Функция генерации таблицы логов и заметок для выбранного Controlpass
    
    аргументы:
    @controlpass_code-Какое-то будущее уникальное значение, по которым мы будем делить контролпассы
    return:
    hmml-сгенерированная html-страница
    
    '''
    tofino_logs_files = os.listdir(f"{PATH_CONTROLPASS}/{controlpass_code}")
    list_of_notes = nt.read_note(controlpass_code)
    list_of_cut_names = []
    for log_name in tofino_logs_files:
        try:
            status = 'success'
            log_cut_name = log_name.split("_")
            list_of_cut_names.append(log_cut_name)
            log = open(f'{PATH_CONTROLPASS}/{controlpass_code}/{log_name}')
            lines = log.readlines()
            for line in lines:
                if line.find('INMYS_FAILED') != -1:
                    status = 'failed'
                    break
            log_cut_name.append(status)
        except:
            continue
    template = env.get_template("fast_controlpass_logs.html")
    html = template.render(code=controlpass_code,
                           list_of_cut_names=list_of_cut_names,
                           list_of_notes=list_of_notes)
    return html


# Общие функции

def generate_start_html():
    '''
    Функция генерации стартовой страницы с строками поиска плат
    return:
    html-сгенерированная html-страница 
    '''

    ocp_codes = os.listdir(PATH_OCP)
    tofino_codes = os.listdir(PATH_TOFINO)
    template = env.get_template('main.html')
    html = template.render(ocp_codes=ocp_codes, tofino_codes=tofino_codes)
    return html


def generate_list_of_devices():
    result_ocp = []
    result_tofino = []
    result_controlpass = []
    ocp_codes = os.listdir(PATH_OCP)
    for ocp_code in ocp_codes:
        try:
            append_list = []
            logs_number = len(os.listdir(f"{PATH_OCP}/{ocp_code}"))
            append_list = [ocp_code, logs_number]
            result_ocp.append(append_list)
        except:
            continue
    tofino_codes = os.listdir(PATH_TOFINO)
    for tofino_code in tofino_codes:
        try:
            append_list = []
            logs_number = len(os.listdir(f"{PATH_TOFINO}/{tofino_code}"))
            append_list = [tofino_code, logs_number]
            result_tofino.append(append_list)
        except:
            continue
    controlpass_codes = os.listdir(PATH_CONTROLPASS)
    for controlpass_code in controlpass_codes:
        try:
            append_list = []
            logs_number = len(os.listdir(
                f"{PATH_CONTROLPASS}/{controlpass_code}"))
            append_list = [controlpass_code, logs_number]
            result_controlpass.append(append_list)
        except:
            continue
    template = env.get_template("list_of_devices.html")
    html = template.render(
        ocp_names=result_ocp, tofino_names=result_tofino, controlpass_names=result_controlpass)
    return html


def generate_big_log(log_path: str, type: int):
    """
    Функция генерации html-страницы одного лога чего-либо, чтобы его можно было прочитать

    аргументы:
    @log_path=полное имя файла,из которого впоследние вынимается номер платы для поиска папки
    @type- тип устройства для определения пути(0-OCP,1-TOFINO,2-CONTROLPASS,можно дополнить в будущем)
    return:
    html-страница для возврата

    """
    types = [PATH_OCP, PATH_TOFINO, PATH_CONTROLPASS]
    log_path_split = log_path.split("_")
    file = open(f"{types[type]}/{log_path_split[1]}/{log_path}")
    lines = file.readlines()
    template = env.get_template("big_log.html")
    html = template.render(log_path=log_path, lines=lines)
    return html


def generate_answer(text: str):
    """
    Функция, которая возвращает текст ошибки и кнопку возврата на основную страницу
    аргументы:
    @text-текст ошибки
    return:
    html-страница с текстом и кнопкой
    """
    template = env.get_template("answer.html")
    html = template.render(text=text)
    return html

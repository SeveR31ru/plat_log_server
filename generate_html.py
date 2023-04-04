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
    PATH_OCP=str(config["COMMON"]["path_ocp"])
    PATH_TOFINO=str(config["COMMON"]["path_tofino"])
    env = Environment(loader=FileSystemLoader('templates'))
except:
    pass


"""
Все функции, связанные с генерацией html-страниц для логов

"""


def generate_start_html():
    
    '''
    Функция генерации стартовой страницы с строками поиска плат
    '''
    if not os.path.exists(PATH_OCP):
        os.mkdir(PATH_OCP)
    if not os.path.exists(PATH_TOFINO):
        os.mkdir(PATH_TOFINO)
    
    ocp_codes=os.listdir(PATH_OCP)
    tofino_codes=os.listdir(PATH_TOFINO)
    template = env.get_template('main.html')
    html = template.render(ocp_codes=ocp_codes,tofino_codes=tofino_codes)
    save=open('web/main.html','w')
    save.write(html)
    save.close()

#OCP-функции

def generate_fast_ocp_logs(ocp_code:str):
    '''
    Функция генерации html-страницы одного лога OCP, чтобы его можно было прочитать

    аргументы:
    @log_path=полное имя файла,из которого впоследние вынимается номер платы для поиска папки
    '''
    
    ocp_logs_files=os.listdir(f"{PATH_OCP}/{ocp_code}")
    list_of_notes=nt.read_note(ocp_code)
    list_of_cut_names=[]
    for log_name in ocp_logs_files:
        status='success'
        log_cut_name=log_name.split("_")
        list_of_cut_names.append(log_cut_name)
        log=open(f'{PATH_OCP}/{ocp_code}/{log_name}')
        lines=log.readlines()
        for line in lines:
            if line.find('INMYS_FAILED')!=-1 :
                status='failed'
                break
        log_cut_name.append(status)
    try:
        pass_mac=passp.get_mac(ocp_code)
    except:
        pass_mac="не выдан"
    try:
        pass_serial=passp.get_serial(ocp_code)
    except:
        pass_serial="не выдан"
    template = env.get_template('fast_ocp_logs.html')
    html = template.render(code=ocp_code,
                            list_of_cut_names=list_of_cut_names,
                            list_of_notes=list_of_notes,
                            pass_mac=pass_mac,
                            pass_serial=pass_serial)
    print(html)
    save=open(f'web/{ocp_code}.html','w')#
    save.write(html)
    save.close()

def generate_big_ocp_log(log_path:str):
    '''
    Функция генерации html-страницы одного лога OCP, чтобы его можно было прочитать

    аргументы:
    @log_path=полное имя файла,из которого впоследние вынимается номер платы для поиска папки
    '''
    
    log_path_split=log_path.split("_")
    file=open(f"{PATH_OCP}/{log_path_split[1]}/{log_path}")
    lines=file.readlines()
    template=env.get_template("big_log.html")
    html = template.render(log_path=log_path,lines=lines)
    save=open(f'web/{log_path}.html','w')
    save.write(html)
    save.close()




#TOFINO-функции

def generate_fast_tofino_logs(tofino_code:str):
    '''
    Функция генерации таблицы логов и заметок для выбранной платы TOFINO
    
    аргументы:
    @tofino_code-номер TOFINO-платы
    
    '''
    
    tofino_logs_files=os.listdir(f"{PATH_TOFINO}/{tofino_code}")
    list_of_notes=nt.read_note(tofino_code)
    list_of_cut_names=[]
    for log_name in tofino_logs_files:
        status='success'
        log_cut_name=log_name.split("_")
        list_of_cut_names.append(log_cut_name)
        log=open(f'{PATH_TOFINO}/{tofino_code}/{log_name}')
        lines=log.readlines()
        for line in lines:
            if line.find('INMYS_FAILED')!=-1 :
                status='failed'
                break
        log_cut_name.append(status)
    template=env.get_template("fast_tofino_logs.html")
    html = template.render(code=tofino_code,
                            list_of_cut_names=list_of_cut_names,
                            list_of_notes=list_of_notes)
    save=open(f'web/{tofino_code}.html','w')
    save.write(html)
    save.close()



def generate_big_tofino_log(log_path:str):
    """
    Функция генерации html-страницы одного лога TOFINO, чтобы его можно было прочитать

    аргументы:
    @log_path=полное имя файла,из которого впоследние вынимается номер платы для поиска папки

    """
    
    log_path_split=log_path.split("_")
    file=open(f"{PATH_TOFINO}/{log_path_split[1]}/{log_path}")
    lines=file.readlines()
    template=env.get_template("big_log.html")
    html = template.render(log_path=log_path,lines=lines)
    save=open(f'web/{log_path}.html','w')
    save.write(html)
    save.close()



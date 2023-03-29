import pandas as pd
import os
import datetime

def add_note(code:str,note:str):
    """
    Функция для добавления заметки в таблицу 

    аргументы:
    @code- номер платы,для которой добавляется заметка. Коды уникальны, пересечений быть не должно. Может быть больше одной заметки для одной платы
    @note- сама заметка любого формата
    """
    if not os.path.exists("notes.csv"):
        create_note_table=pd.DataFrame(columns=["code","note","time"])
        create_note_table.to_csv("notes.csv",index= False)
    time= str(datetime.datetime.now())
    note_table=pd.read_csv("notes.csv")
    note_table.loc[ len(note_table.index )] = [code,note,time]
    note_table.to_csv("notes.csv",index= False)


def read_note(code:str):
    """
    Функция для получения листа заметок данной платы в формате

    номер платы-заметка-время

    аргументы:
    @code-номер платы, для которой нужно получить все заметки

    """
    if not os.path.exists("notes.csv"):
        create_note_table=pd.DataFrame(columns=["code","note","time"])
        create_note_table.to_csv("notes.csv",index= False)
    note_table=pd.read_csv("notes.csv")
    result_list=[]
    for i, row in note_table.iterrows():
        note_for_add=[]
        if row[0]==code:
            note_for_add.append(row[0])
            note_for_add.append(row[1])
            note_for_add.append(row[2])
            result_list.append(note_for_add)
    return result_list


def add_ocp_pass_note(serialNumber:str,pass_name:str):
    """
    Функция для записи новой комбинации серийный номер OCP-имя выданного паспорта в таблицу

    аргументы:
    @serialNumber-серийный номер платы из запроса

    @pass_name-имя файла паспорта
    
    """

    if not os.path.exists("ocp_passports.csv"):
        create_pass_table=pd.DataFrame(columns=['serial_number','pass_name'])
        create_pass_table.to_csv('ocp_passports.csv',index=False)
    pass_table=pd.read_csv("ocp_passports.csv")
    pass_table.loc[ len(pass_table.index )] = [serialNumber,pass_name]
    pass_table.to_csv("ocp_passports.csv",index= False)
    
def read_ocp_pass_note(serialNumber:str):

    """
    Функция для проверки наличия паспорта у платы и вывод его номера

    аргументы:
    @serialNumber- уникальный серийный номер платы 
    
    """

    if not os.path.exists("ocp_passports.csv"):
        create_pass_table=pd.DataFrame(columns=['serial_number','pass_name'])
        create_pass_table.to_csv('ocp_passports.csv',index=False)
    pass_table=pd.read_csv("ocp_passports.csv")
    passport="не выдан"
    for i, row in pass_table.iterrows():
        if row[0]==serialNumber:
            passport=row[1]
            break
    return passport


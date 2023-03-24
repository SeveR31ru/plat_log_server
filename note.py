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

    


    
if __name__=="__main__":
    notes_for_this_plat=read_note("DEADFACE")
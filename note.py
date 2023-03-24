import pandas as pd
import os
import datetime

def add_note(code:str,note:str):
    """
    Функция для добавления заметки в таблицу 

    переменные:
    @code- номер платы,для которой добавляется заметка. Коды уникальны, пересечений быть не должно. Может быть больше одной заметки для одной платы
    @note- сама заметка любого формата
    """
    if not os.path.exists("notes.csv"):
        create_note_table=pd.DataFrame(columns=["code","note","time"])
        create_note_table.to_csv("notes.csv",index= False)
    time= str(datetime.datetime.now())
    note_table=pd.read_csv("notes.csv")
    note_table.loc[ len(note_table.index )] = [code,note,time]
    print(note_table)
    note_table.to_csv("notes.csv",index= False)





if __name__=="__main__":
    add_note("DEADFACE","IM CREATED")
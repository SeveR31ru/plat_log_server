import pandas as pd
import os
import configparser


try:
    # получение конфигов
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    PATH_OCP_PASS=str(config["COMMON"]["path_ocp_passports"])
except:
    pass



def give_mac(serialNumber:str):
    if not os.path.exists("ocp_given_passports.csv"):
        create_used_pass_table=pd.DataFrame(columns=["ocp_number","mac","pass_serial_number"])
        create_used_pass_table.to_csv("ocp_given_passports.csv",index= False)
    if not os.path.exists(PATH_OCP_PASS):
        os.mkdir(PATH_OCP_PASS)  
    if len(os.listdir(PATH_OCP_PASS))==0:
        #print("Папка пуста")
        return 1
    pass_list=os.listdir(PATH_OCP_PASS)
    try:
        pass_table=pd.read_excel(f"{PATH_OCP_PASS}/{pass_list[0]}")
    except:
        #print("Не удалось открыть таблицу")
        return 2
    given_table=pd.read_csv("ocp_given_passports.csv")
    try:
        pass_row=pass_table.iloc[0]
    except:
        #print("Таблица пуста")
        return 3
    if serialNumber in given_table['ocp_number'].unique():
        print("Этот номер уже есть")
        return 4
    serial_pass=pass_row[1]
    mac=pass_row[2]
    given_table.loc[ len(given_table.index )] = [serialNumber,mac,serial_pass]
    given_table.to_csv("ocp_given_passports.csv",index=False)
    pass_table=pass_table.drop(index=0)
    pass_table.to_excel(f"{PATH_OCP_PASS}/{pass_list[0]}",index=False)
    return mac

    

if __name__=="__main__":
    try:
        # получение конфигов
        config = configparser.ConfigParser()
        config.read("./settings.ini")
        PATH_OCP_PASS=str(config["COMMON"]["path_ocp_passports"])
    except:
        pass 
    give_mac("azazalka")

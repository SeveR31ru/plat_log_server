import pandas as pd
import os
import configparser


try:
    # получение конфигов
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    PATH_OCP_PASS = str(config["COMMON"]["path_ocp_passports"])
except:
    pass


def give_mac(serialNumber: str):
    """
    Функция для выдачи мака. Параллельно запоминает номер платы, которой выдал мак и заносит в таблицу.

    Удаляет выданный мак из списка паспортов
    аргументы:
    @serialNumber- номер платы, которой нужно выдать мак
    return:
    @mac-если все хорошо
    возвращаемые ошибки:
    @1-папка с паспортами пуста
    @2-не удалось открыть таблицу по каким-то причинам
    @3-таблица пуста, в ней нет ни единой записи
    @4- этому serialNumber уже присвоен мак
    
    """

    if len(os.listdir(PATH_OCP_PASS)) == 0:
        # print("Папка пуста")
        return 1
    pass_list = os.listdir(PATH_OCP_PASS)
    try:
        pass_table = pd.read_excel(f"{PATH_OCP_PASS}/{pass_list[0]}")
    except:
        # print("Не удалось открыть таблицу")
        return 2
    given_table = pd.read_csv("ocp_given_passports.csv")
    try:
        pass_row = pass_table.iloc[0]
    except:
        # print("Таблица пуста")
        return 3
    if serialNumber in given_table['ocp_number'].unique():
        print("Этот номер уже есть")
        return 4
    serial_pass = pass_row[1]
    mac = pass_row[2]
    given_table.loc[len(given_table.index)] = [serialNumber, mac, serial_pass]
    given_table.to_csv("ocp_given_passports.csv", index=False)
    pass_table = pass_table.drop(index=0)
    pass_table.to_excel(f"{PATH_OCP_PASS}/{pass_list[0]}", index=False)
    return mac


def get_mac(serialNumber: str):
    """
    Функция для получения уже выданного мак-адреса выбранной платы
    """
    given_table = pd.read_csv("ocp_given_passports.csv")
    mac_row = given_table.loc[(given_table['ocp_number'] == serialNumber)]
    mac_cleared_row = mac_row.iloc[0]
    mac = mac_cleared_row[1]
    return mac


def get_serial(serialNumber: str):
    """
    Функция для получения уже выданного серийного номера, идущего вместе с маком для выбранной платы
    """
    given_table = pd.read_csv("ocp_given_passports.csv")
    serial_row = given_table.loc[(given_table['ocp_number'] == serialNumber)]
    serial_cleared_row = serial_row.iloc[0]
    serial_mac = serial_cleared_row[2]
    return serial_mac

import jinja2
import os

PATH_OCP='ocp_logs'
PATH_TOFINO='tofino_logs'


def generate_start_html():
    ocp_codes=os.listdir(PATH_OCP)
    tofino_codes=os.listdir(PATH_TOFINO)
    template = jinja2.Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Work Logs</title>
    </head>
    <body>
        <header>
            <h1>
                Страница для работы с логами(в разработке)
            </h1>
        </header>
        <main>
            <form action="/get_fast_ocp_logs" method="get" target=_blank>
                <label>Получение логов OCP</label>
                <p></p>
                <select name="ocp_code">
                    <option value="">Выберите значение</option>
                    {% for code in ocp_codes %}
                    <option value="{{code}}">{{code}}</option>
                    {% endfor %}
                </select>
                <b1></b1>
                <input type="submit" value="Посмотреть таблицу логов этой платы">
            </form>
            <p></p>
            <form action="/get_fast_tofino_logs" method="get" target=_blank>
                <label>Получение логов TOFINO</label>
                <p></p>
                <select name="tofino_code">
                    <option value="">Выберите значение</option>
                    {% for code in tofino_codes %}
                    <option value="{{code}}">{{code}}</option>
                    {% endfor %}
                </select>
                <b1></b1>
                <input type="submit" value="Посмотреть таблицу логов этой платы">
            </form>
        </main>
    </body>
    </html>
    """)
    html = template.render(ocp_codes=ocp_codes,tofino_codes=tofino_codes)
    save=open('web/main.html','w')
    save.write(html)
    save.close()

#OCP-функции

def generate_fast_ocp_logs(ocp_code:str):
    ocp_logs_files=os.listdir(f"{PATH_OCP}/{ocp_code}")
    list_of_cut_names=[]
    for log_name in ocp_logs_files:
        status='success'
        log_cut_name=log_name.split("_")
        list_of_cut_names.append(log_cut_name)
        log=open(f'{PATH_OCP}/{ocp_code}/{log_name}')
        lines=log.readlines()
        for line in lines:
            if line.find('FAILED')!=-1 or line.find('failed')!=-1 :
                status='failed'
                break
        log_cut_name.append(status)
    template=jinja2.Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Логи платы {{code}}</title>
    </head>
    <body>
        <header>
            <h1>
                Логи платы {{code}}
            </h1>
        </header>
        <main>
            <table border="1">
                <caption>Таблица логов платы {{code}}</caption>
                <tr>
                    <th>Вид теста</th>
                    <th>Время теста</th>
                    <th>Статус теста</th>
                    <th>Открыть тест подробно</th>
                </tr>
                {% for name in list_of_cut_names %}
                <tr>
                    <th>{{name[0]}}</th>
                    <th>{{name[2]}}</th>
                    <th>{{name[3]}}</th>
                    <th>
                        <form action="/get_big_ocp_log" method="get" target=_blank>
                        <button value="{{[name[0],name[1],name[2]]|join('_')}}" name="log_path" type="submit">Посмотреть этот лог подробнее</button>
                        </form
                    </th>
                </tr>
                {% endfor %}
            </table>
        </main>
    </body>
    </html>
    """)
    html = template.render(code=ocp_code,list_of_cut_names=list_of_cut_names)
    save=open(f'web/{ocp_code}.html','w')
    save.write(html)
    save.close()

def generate_big_ocp_log(log_path:str):
    log_path_split=log_path.split("_")
    file=open(f"{PATH_OCP}/{log_path_split[1]}/{log_path}")
    lines=file.readlines()
    template=jinja2.Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Полный лог {{log_path}}</title>
    </head>
    <body>
        <main> 
        {% for line in lines %}
        <p>{{line}}</p>
        {% endfor %} 
        </main>
    </body>
    </html>
    """)
    html = template.render(log_path=log_path,lines=lines)
    save=open(f'web/{log_path}.html','w')
    save.write(html)
    save.close()




#TOFINO-функции

def generate_fast_tofino_logs(tofino_code:str):
    tofino_logs_files=os.listdir(f"{PATH_TOFINO}/{tofino_code}")
    list_of_cut_names=[]
    for log_name in tofino_logs_files:
        status='success'
        log_cut_name=log_name.split("_")
        list_of_cut_names.append(log_cut_name)
        log=open(f'{PATH_TOFINO}/{tofino_code}/{log_name}')
        lines=log.readlines()
        for line in lines:
            if line.find('FAILED')!=-1 or line.find('failed')!=-1 :
                status='failed'
                break
        log_cut_name.append(status)
    template=jinja2.Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Логи платы {{code}}</title>
    </head>
    <body>
        <header>
            <h1>
                Логи платы {{code}}
            </h1>
        </header>
        <main>
            <table border="1">
                <caption>Таблица логов платы {{code}}</caption>
                <tr>
                    <th>Вид теста</th>
                    <th>Время теста</th>
                    <th>Статус теста</th>
                    <th>Открыть тест подробно</th>
                </tr>
                {% for name in list_of_cut_names %}
                <tr>
                    <th>{{name[0]}}</th>
                    <th>{{name[2]}}</th>
                    <th>{{name[3]}}</th>
                    <th>
                        <form action="/get_big_tofino_log" method="get" target=_blank>
                        <button value="{{[name[0],name[1],name[2]]|join('_')}}" name="log_path" type="submit">Посмотреть этот лог подробнее</button>
                        </form
                    </th>
                </tr>
                {% endfor %}
            </table>
        </main>
    </body>
    </html>
    """)
    html = template.render(code=tofino_code,list_of_cut_names=list_of_cut_names)
    save=open(f'web/{tofino_code}.html','w')
    save.write(html)
    save.close()



def generate_big_tofino_log(log_path:str):
    log_path_split=log_path.split("_")
    file=open(f"{PATH_TOFINO}/{log_path_split[1]}/{log_path}")
    lines=file.readlines()
    template=jinja2.Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Полный лог {{log_path}}</title>
    </head>
    <body>
        <main> 
        {% for line in lines %}
        <p>{{line}}</p>
        {% endfor %} 
        </main>
    </body>
    </html>
    """)
    html = template.render(log_path=log_path,lines=lines)
    save=open(f'web/{log_path}.html','w')
    save.write(html)
    save.close()



if __name__=="__main__":
    generate_start_html()
import configparser
import jinja2
import os
import note as nt

try:
    # получение конфигов
    config = configparser.ConfigParser()
    config.read("./settings.ini")
    PATH_OCP=str(config["COMMON"]["path_ocp"])
    PATH_TOFINO=str(config["COMMON"]["path_tofino"])
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
                <input list="plats_ocp" placeholder="Введите номер"name=ocp_code >
                
                <datalist id="plats_ocp">
                    <option value="">Выберите значение</option>
                    {% for code in ocp_codes %}
                    <option value="{{code}}"></option>
                    {% endfor %}
                </datalist>

                <b1></b1>
                <input type="submit" value="Посмотреть таблицу логов этой платы">
            </form>
            <p></p>
            <form action="/get_fast_tofino_logs" method="get" target=_blank>
                <label>Получение логов TOFINO</label>
                <p></p>
                <input list="plats_tofino" placeholder="Введите номер"name=tofino_code >
                
                <datalist id="plats_tofino">
                    <option value="">Выберите значение</option>
                    {% for code in tofino_codes %}
                    <option value="{{code}}"></option>
                    {% endfor %}
                </datalist>
        
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
            if line.find('FAILED')!=-1 or line.find('failed')!=-1 :
                status='failed'
                break
        log_cut_name.append(status)
    passport=nt.read_ocp_pass_note(ocp_code)
    
    
    
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
            <table border="1" table class="table_sort">
            <caption>Таблица логов платы {{code}}(номер паспорта: {{passport}} )</caption>
            <thead>
                    <tr>
                    <th>Вид теста</th>
                    <th>Время теста</th>
                    <th>Статус теста</th>
                    <th>Открыть тест подробно</th>
                    </tr>
            </thead>
            <tbody>
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
            </tbody>
            </table>
            <table border="1" table class="table_sort">
                <caption>Таблица заметок для этой платы</caption>
                <thead>
                        <tr>
                        <th>Заметка</th>
                        <th>Время заметки</th>
                        </tr>
                </thead>
                <tbody>  
                   {% for note in list_of_notes %}
                    <tr>
                    <th>{{note[1]}}</th>
                    <th>{{note[2]}}</th>

                    </th>
                   {% endfor %}
                </tbody>
            </table>
            <p><textarea name="note" cols="50" rows="10" id="note" ></textarea></p>
            <input type="text" name="code" value="{{code}}" id="code" hidden readonly>
            <button onclick="send()" >Отправить заметку об этой плате></button>    
            <script>
            async function send(){
                    // получаем введеное в поле имя и возраст
                    const note = document.getElementById("note").value;
                    const code = document.getElementById("code").value;
          
                    // отправляем запрос
                    const response = await fetch("/send_note", {
                            method: "POST",
                            headers: { "Accept": "application/json", "Content-Type": "application/json" },
                            body: JSON.stringify({ 
                                note: note,
                                code: code
                            })
                        });
                        if (response.ok) {
                            location.reload()
                        }
                        else
                            console.log(response);
                }
            </script>
            
            
        
            <script>
                document.addEventListener('DOMContentLoaded', () => {
                const getSort = ({ target }) => {
                    const order = (target.dataset.order = -(target.dataset.order || -1));
                    const index = [...target.parentNode.cells].indexOf(target);
                    const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
                    const comparator = (index, order) => (a, b) => order * collator.compare(
                        a.children[index].innerHTML,
                        b.children[index].innerHTML
                    );
                    for(const tBody of target.closest('table').tBodies)
                        tBody.append(...[...tBody.rows].sort(comparator(index, order)));
                    for(const cell of target.parentNode.cells)
                        cell.classList.toggle('sorted', cell === target);
                };
                document.querySelectorAll('.table_sort thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));
                });
            </script>
              <script>
                function deleteName(f) 
                {
                    if (confirm("Вы уверены, что хотите удалить выделенный пункт?Эта операция не восстановима.")) 
                    f.submit();
                }
                </script>


            
        </main>
    </body>
    </html>
    """)
    html = template.render(code=ocp_code,
                            list_of_cut_names=list_of_cut_names,
                            list_of_notes=list_of_notes,
                            passport=passport)
    save=open(f'web/{ocp_code}.html','w')
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
            <table border="1" table class="table_sort">
            <caption>Таблица логов платы {{code}}</caption>
            <thead>
                    <tr>
                    <th>Вид теста</th>
                    <th>Время теста</th>
                    <th>Статус теста</th>
                    <th>Открыть тест подробно</th>
                    </tr>
            </thead>
            <tbody>
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
            </tbody>
            </table>
            <table border="1" table class="table_sort">
                <caption>Таблица заметок для этой платы</caption>
                <thead>
                        <tr>
                        <th>Заметка</th>
                        <th>Время заметки</th>
                        </tr>
                </thead>
                <tbody>  
                   {% for note in list_of_notes %}
                    <tr>
                    <th>{{note[1]}}</th>
                    <th>{{note[2]}}</th>

                    </th>
                   {% endfor %}
                </tbody>
            </table>  
            <p><textarea name="note" cols="50" rows="10" id="note" ></textarea></p>
            <input type="text" name="code" value="{{code}}" id="code" hidden readonly>
            <button onclick="send()" >Отправить заметку об этой плате</button>    
            <script>
            async function send(){
                    // получаем введеное в поле имя и возраст
                    const note = document.getElementById("note").value;
                    const code = document.getElementById("code").value;
          
                    // отправляем запрос
                    const response = await fetch("/send_note", {
                            method: "POST",
                            headers: { "Accept": "application/json", "Content-Type": "application/json" },
                            body: JSON.stringify({ 
                                note: note,
                                code: code
                            })
                        });
                        if (response.ok) {
                            location.reload()
                        }
                        else
                            console.log(response);
                }
            </script>
            
   
            <script>
                document.addEventListener('DOMContentLoaded', () => {
                const getSort = ({ target }) => {
                    const order = (target.dataset.order = -(target.dataset.order || -1));
                    const index = [...target.parentNode.cells].indexOf(target);
                    const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
                    const comparator = (index, order) => (a, b) => order * collator.compare(
                        a.children[index].innerHTML,
                        b.children[index].innerHTML
                    );
                    for(const tBody of target.closest('table').tBodies)
                        tBody.append(...[...tBody.rows].sort(comparator(index, order)));
                    for(const cell of target.parentNode.cells)
                        cell.classList.toggle('sorted', cell === target);
                };
                document.querySelectorAll('.table_sort thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));
                });
            </script>
        </main>
    </body>
    </html>
    """)
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



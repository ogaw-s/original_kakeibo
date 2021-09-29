import PySimpleGUI as sg
import csv
import datetime
# import matplotlib

DATA_CSV = "history.csv"
INITIAL = "initial.txt"

def read_csv():
    with open(DATA_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        database = [row for row in reader]
    
    if len(database) >= 2:
        recent_data = database[-3:-1]
    else:
        recent_data = database
    print(database)
    return [database, recent_data]

database = read_csv()[0]
recent_data = read_csv()[1]

current_date = str(datetime.date.today())
current_month = current_date[5:6]

def current_property():
    output = int(open(INITIAL, "r").read()) + sum([int(x[3]) for x in database])
    return str(output)

sg.theme("DarkAmber")

layout = [[sg.Text("家計簿です")],
          [sg.Text("今の所持金= {} 円".format(current_property()), key="currentmoney")],
          [sg.Text("")],  # 空行
          [sg.Text("使用した金額等諸々を入力しよう",size=(15,1))],
          [sg.Text("使った日"), sg.InputText(current_date, key="date")],
          [sg.Text("カテゴリ"), sg.Combo(("食費","勉強","趣味","その他"), key="category")],
          [sg.Text("詳細"), sg.InputText("何につかったか", key="product")],
          [sg.Text("使った金額"), sg.InputText("", key="spent_money")],
          [sg.Button("追加")],
          [sg.Text("", key="showitsdone")]
]

window = sg.Window("家計簿", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "追加":
        database = read_csv()[0]
        recent_data = read_csv()[1]

        with open(DATA_CSV, "a", newline="", encoding="utf-8") as f:
            additional_info = [values["date"], values["category"], values["product"], int(values["spent_money"])*(-1)]
            writer = csv.writer(f)
            writer.writerow(additional_info)
        window.find_element("showitsdone").update("できたよ")
        window.find_element("date").update(current_date)
        window.find_element("category").update("")
        window.find_element("product").update("何に使ったか")
        window.find_element("spent_money").update("")
        window.find_element("currentmoney").update("今の所持金= {} 円".format(current_property()))

window.close()

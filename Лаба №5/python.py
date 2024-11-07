import pymysql
from pandas import DataFrame
import os
from time import sleep
import re


class DataBase:
  def __init__(self, bd_user, bd_password, bd_host, bd_database) -> None:
    self.bd_user = bd_user
    self.bd_password = bd_password
    self.bd_host = bd_host
    self.bd_database = bd_database
  
  def execute_query(self, query, params=None, isNeedFetch=False):
    connection = pymysql.connect(
        host=self.bd_host,
        user=self.bd_user,
        password=self.bd_password,
        database=self.bd_database,
        cursorclass=pymysql.cursors.DictCursor
    )
    result = None
    try:
      with connection.cursor() as cursor:
        cursor.execute(query, params)
        if isNeedFetch: result = cursor.fetchall()
        connection.commit()
    except Exception as e:
      print(e)
      connection.rollback()
    finally:
      connection.close()
      return result
    
  def get_table(self):
    query = """SELECT * FROM cars"""
    return self.execute_query(query, isNeedFetch=True)
  
  def add_car(self, brand, model, price):
    query = """INSERT INTO cars (brand, model, price) VALUES (%s, %s, %s)"""
    params = [brand, model, price]
    return self.execute_query(query, params)


def show_table(dataBase : DataBase):
  cars = dataBase.get_table()
  print(DataFrame(cars).to_string(index=False))
  sleep(1)
  print("(чтобы вернуться, введите: \"0\"), для выхода \"exit\"")
  while True:
    user_input = input("")
    if user_input == "0":
      os.system('cls')
      return main(dataBase)
    elif user_input == "exit": return


def insert_in_table(dataBase : DataBase):
  def exit():
    print("Ошибка!")
    print("Получены значения:", user_input)
    sleep(2)
    os.system('cls')

  print("Введите данные, для вставки в таблицу, поля: ")
  print("brand model price")
  sleep(1)
  print("(чтобы вернуться, введите: \"0\"), для выхода \"exit\"")
  user_input = input("")

  if user_input == "0":
    os.system('cls')
    return main(dataBase)
  elif user_input == "exit": return

  regexp = r"(\b\w+\b)|(\'[^\']+\')|(\"[^\"]+\")"
  user_input = re.findall(regexp, user_input)[:3]
  def get_value(x):
    res = "".join(x).strip()
    res = re.sub(r"^\"|^\'|\"$|\'$", "", res).strip()
    return res
  user_input = list(map(get_value, user_input))
  try:
    user_input[2] = int(user_input[2])
  except:
    exit()
    return insert_in_table(dataBase)
  
  if len(user_input) != 3: 
    exit()
    insert_in_table(dataBase)
  
  try:
    dataBase.add_car(user_input[0], user_input[1], user_input[2])
    print("Строка успешно добавлена!")
    sleep(1)
    os.system('cls')
    return insert_in_table(dataBase)
  except:
    print("Произошла ошибка!")
  

def main(dataBase : DataBase):
  def exit():
    print("Ошибка!")
    sleep(1)
    os.system('cls')
    main(dataBase)

  print("""
Выберите действие:
1) Показать таблицу \"cars\"
2) Добавить запись в таблицу \"cars\"
3) Остановить программу
""", end="")
  
  choice = input("")
  
  if choice == "1":   show_table(dataBase)
  elif choice == "2": insert_in_table(dataBase)
  elif choice == "3": return
  else: exit()


if __name__ == "__main__":
  dataBase = DataBase("root", "", "127.0.0.1", "inf_system_labs")
  main(dataBase)
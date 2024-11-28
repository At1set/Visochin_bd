import pymysql
from tkinter import filedialog


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


def save_file(content : str):
  if (not isinstance(content, str)): raise TypeError(f"save_file() argument must be a string, not {type(content).__name__}")

  # Открываем диалоговое окно для сохранения файла
  file_path = filedialog.asksaveasfilename(
    initialfile="cars",
    defaultextension=".txt",
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
  )

  if file_path:
    # Если пользователь выбрал путь для сохранения, записываем содержимое в файл
    with open(file_path, 'w') as file:
      file.write(content)
    print(f"Файл сохранен по пути: {file_path}")
  else:
    print("Сохранение файла было отменено")


def main():
  dataBase = DataBase("root", "", "127.0.0.1", "inf_system_labs")
  save_file("123")


if __name__ == "__main__":
  main()
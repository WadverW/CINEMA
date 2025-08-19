import os
import subprocess
import sys

DB_NAME = "db.sqlite3"

def main():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"[INFO] База данных {DB_NAME} удалена.")
    else:
        print(f"[INFO] Файл {DB_NAME} не найден, создаём новую базу.")

    print("[INFO] Применяем миграции...")
    subprocess.run([sys.executable, "manage.py", "migrate"])

    create_superuser = input("Хотите создать суперпользователя сейчас? (y/n): ").lower()
    if create_superuser == "y":
        subprocess.run([sys.executable, "manage.py", "createsuperuser"])

    print("[INFO] Готово! База данных пересоздана.")

if __name__ == "__main__":
    main()
import sqlite3
import os

conn = sqlite3.connect("patientdb.db")
cursor = conn.cursor()
for file in os.listdir("data"):
    if not file.endswith("_subjects.txt"):
        alias = file.split(".")[0]
        with open(os.path.join("data", file), encoding="utf-8") as f:
            task = f.read().strip()
        with open(os.path.join("data", alias + "_subjects.txt"), encoding="utf-8") as f:
            subjects = f.read().strip()

        query = "INSERT INTO tasks (name, alias, task_markup, subjects_list) VALUES (?, ?, ?, ?);"
        cursor.execute(query, [alias, alias, task, subjects])
        conn.commit()

conn.close()

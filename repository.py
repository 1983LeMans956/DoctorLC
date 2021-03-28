from sqlite3 import connect


def init(path: str):
    conn = connect(path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS register(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            birthday DATE NOT NULL,
            snils VARCHAR(14) NOT NULL,
            polis VARCHAR(15) NOT NULL,
            address TEXT NOT NULL,
            phone VARCHAR(11) NOT NULL,
            date DATE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis(
            register_id INTEGER,
            diagnosis TEXT,
            complaint TEXT,
            treatment TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyzes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_id INTEGER,
            name TEXT,
            result TEXT,
            date DATE NOT NULL
        )
    """)

    cursor.execute("SELECT id FROM register LIMIT 1")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO register VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (None, "Карпышев Андрей Николаевич", "01.05.1975", "111-111-111 00", "1111 0000 1111 0000",
                        "г. Волгоград",
                        "8 800 555 555", "13.03.2021 15:00:00"))
        cursor.execute("INSERT INTO register VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (None, "Солодов Генадий Викторович", "08.11.1953", "222-222-222 11", "2222 1111 2222 1111",
                        "г. Волжский",
                        "8927 090 99 00", "13.03.2021 15:30:00"))
        cursor.execute("INSERT INTO register VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (None, "Петро И.И.", "01.01.1997", "111-111-111 00", "1111 0000 1111 0000", "г. Волгоград",
                        "8 800 555 555", "01.01.2021",))
        cursor.execute("INSERT INTO register VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (None, "Иванов П.П.", "02.02.1998", "222-222-222 11", "2222 1111 2222 1111", "г. Волжский",
                        "8927 090 99 00", "02.01.2020",))
        cursor.execute("INSERT INTO diagnosis VALUES (?, ?, ?, ?)",
                       (1, "Зрение -2", "Плохо видит", "Витамины"))
        conn.commit()

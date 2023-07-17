"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv

params = {
    "host": "localhost",
    "database": "north",
    "user": "postgres",
    "password": "ok"
}

PATHS = [
    "north_data/customers_data.csv",
    "north_data/employees_data.csv",
    "north_data/orders_data.csv"
]

NAMES = ["customers", "employees", "orders"]


def add_values_from_file(path, table_name, conn_params):
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            with open(path, "r", encoding="utf-8") as customers_csv:
                customers = csv.DictReader(customers_csv)
                for customer in customers:
                    values = []
                    for value in customer.values():
                        modified_value = value
                        if "\'" in modified_value:
                            modified_value = modified_value.replace("\'", "\'\'")
                        modified_value = '\'' + modified_value + '\''
                        values.append(modified_value)
                    query = f"INSERT INTO {table_name} VALUES ("
                    query += ", ".join(values) + ")"
                    cur.execute(query)


for i in range(3):
    add_values_from_file(PATHS[i], NAMES[i], params)
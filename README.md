1. Клонируйте репозиторий и создайте виртуальное окружение:

```bash
git clone https://github.com/Pionicle/csv-reader.git
cd csv-reader
python3 -m venv env
source env/bin/activate
pip install -r reqierements.txt
```

2. Пример работы скрипта:

```bash
~ python3 main.py --file products.csv
+------------------+---------+---------+----------+
| name             | brand   |   price |   rating |
|------------------+---------+---------+----------|
| iphone 15 pro    | apple   |     999 |      4.9 |
| galaxy s23 ultra | samsung |    1199 |      4.8 |
| redmi note 12    | xiaomi  |     199 |      4.6 |
| iphone 14        | apple   |     799 |      4.7 |
| galaxy a54       | samsung |     349 |      4.2 |
| poco x5 pro      | xiaomi  |     299 |      4.4 |
| iphone se        | apple   |     429 |      4.1 |
| galaxy z flip 5  | samsung |     999 |      4.6 |
| redmi 10c        | xiaomi  |     149 |      4.1 |
| iphone 13 mini   | apple   |     599 |      4.5 |
+------------------+---------+---------+----------+
```

```bash
~ python3 main.py --file products.csv --where "brand=apple"
+----------------+---------+---------+----------+
| name           | brand   |   price |   rating |
|----------------+---------+---------+----------|
| iphone 15 pro  | apple   |     999 |      4.9 |
| iphone 14      | apple   |     799 |      4.7 |
| iphone se      | apple   |     429 |      4.1 |
| iphone 13 mini | apple   |     599 |      4.5 |
+----------------+---------+---------+----------+
```

```bash
~  python3 main.py --file products.csv --where "brand=apple" --aggregate "price=max"
+-------+
|   max |
|-------|
|   999 |
+-------+
```

```bash
~ python3 main.py --file products.csv --where "brand=xiaomi" --order-by "price=asc"
+---------------+---------+---------+----------+
| name          | brand   |   price |   rating |
|---------------+---------+---------+----------|
| redmi 10c     | xiaomi  |     149 |      4.1 |
| redmi note 12 | xiaomi  |     199 |      4.6 |
| poco x5 pro   | xiaomi  |     299 |      4.4 |
+---------------+---------+---------+----------+
```

3. Покрытие тестами:

```bash
~ pytest -vv --cov=table_operations test_table_operations.py


Name                  Stmts   Miss  Cover
-----------------------------------------
table_operations.py     100      3    97%
-----------------------------------------
TOTAL                   100      3    97%
```

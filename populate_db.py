import psycopg2, random, datetime
from faker import Faker

con = psycopg2.connect(dbname="Kalder", user="postgres", password="root")
cur = con.cursor()

populated_users = True
if (populated_users == False):
    sql = "insert into users(id, name, password, balance, debt) values (%s, %s, %s, %s, %s)"

    value = [2, "alex", "123qwe", 1000, 0]

    cur.execute(sql, value)
    con.commit()

    possible_deposits = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    fake = Faker()

    for i in range(3, 100001):
        value = [i, fake.name(), "123qwe", possible_deposits[random.randint(0, 9)], 0]
        cur.execute(sql, value)
        con.commit()

populated_transactions = True
if (populated_users == False):
    id=1
    sql = "insert into transactions(id, from_user, to_user, amount, date) values (%s, %s, %s, %s, %s)"
    value = [id, 5, 13, 2000, datetime.datetime(2021, 10, 15)]
    cur.execute(sql, value)
    con.commit()

    for from_user in range(1, 100000):
        for month in [1, 2, 3]:
            for year in [2021]:
                a = random.randint(1, 10)
                for i in range(a):
                    id += 1
                    if month == 2: random_date=datetime.datetime(year=year, month=month, day=random.randint(1,28), hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
                    else: random_date = datetime.datetime(year=year, month=month, day=random.randint(1,30), hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
                    to_user = random.randint(1, 100000)
                    amount = round(random.uniform(100, 1000), 2)
                    value = [id, from_user, to_user, amount, random_date]
                    cur.execute(sql, value)
                    con.commit()















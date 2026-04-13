"""
seed.py
=======
Génère des données réalistes avec Faker et les injecte dans PostgreSQL.

Structure :
    Schema      → raw
    employees   → 10 employés néerlandais (Faker)
    products    → 3 produits fixes (données originales)
    promotions  → 3 promotions fixes (données originales CSV)
    shifts      → 4 shifts/jour (1 Baker + 1 Cashier × 2 créneaux)
    sales       → exactement 20 000 ventes
    sales_lines → ~26 000 lignes (1–3 par vente)

Usage :
    pip install faker psycopg2-binary python-dotenv
    python seed.py
"""

import os
import random
import datetime
from decimal import Decimal, ROUND_HALF_UP

import psycopg2
from psycopg2.extras import execute_values
from faker import Faker
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

# ── Config ────────────────────────────────────────────────────────────────────

SEED                   = 42
START_DATE             = datetime.date(2023, 7, 3)
END_DATE               = datetime.date(2023, 9, 23)
TARGET_SALES           = 20_000
LINES_PER_SALE_WEIGHTS = [14656, 4344, 1000]   # poids pour 1 / 2 / 3 lignes
SCHEMA                 = "raw"

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     os.getenv("DB_PORT",     "5432"),
    "dbname":   os.getenv("DB_NAME",     "stroopwafel_db"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}

# ── Init Faker ────────────────────────────────────────────────────────────────

fake = Faker("nl_NL")
Faker.seed(SEED)
random.seed(SEED)

# ── DDL ───────────────────────────────────────────────────────────────────────

DDL = f"""
CREATE SCHEMA IF NOT EXISTS {SCHEMA};

CREATE TABLE IF NOT EXISTS {SCHEMA}.employees (
    id              INTEGER      PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    contact_number  VARCHAR(50),
    date_of_birth   DATE,
    hire_date       DATE         NOT NULL,
    hourly_rate     NUMERIC(6,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS {SCHEMA}.products (
    id           INTEGER      PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    unit_cost    NUMERIC(8,4) NOT NULL,
    unit_price   NUMERIC(8,4) NOT NULL
);

CREATE TABLE IF NOT EXISTS {SCHEMA}.promotions (
    id            INTEGER      PRIMARY KEY,
    product_id    INTEGER      NOT NULL REFERENCES {SCHEMA}.products(id),
    name          VARCHAR(150) NOT NULL,
    description   TEXT,
    start_date    DATE         NOT NULL,
    end_date      DATE         NOT NULL,
    discount_rate NUMERIC(5,4) NOT NULL,
    is_holiday    BOOLEAN      NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS {SCHEMA}.shifts (
    id          SERIAL      PRIMARY KEY,
    date        DATE        NOT NULL,
    role        VARCHAR(50) NOT NULL,
    employee_id INTEGER     NOT NULL REFERENCES {SCHEMA}.employees(id),
    hours       VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS {SCHEMA}.sales (
    sales_id       INTEGER       PRIMARY KEY,
    date           DATE          NOT NULL,
    time           TIME          NOT NULL,
    employee_id    INTEGER       NOT NULL REFERENCES {SCHEMA}.employees(id),
    total_price    NUMERIC(10,4) NOT NULL,
    total_discount NUMERIC(10,4) NOT NULL DEFAULT 0,
    weekday        VARCHAR(15)   NOT NULL,
    payment_type   VARCHAR(30)   NOT NULL
);

CREATE TABLE IF NOT EXISTS {SCHEMA}.sales_lines (
    id             INTEGER       PRIMARY KEY,
    product_id     INTEGER       NOT NULL REFERENCES {SCHEMA}.products(id),
    quantity_sold  INTEGER       NOT NULL,
    discount_rate  NUMERIC(5,4)  NOT NULL DEFAULT 0,
    unit_price     NUMERIC(8,4)  NOT NULL,
    unit_discount  NUMERIC(8,4)  NOT NULL DEFAULT 0,
    total_price    NUMERIC(10,4) NOT NULL,
    total_discount NUMERIC(10,4) NOT NULL DEFAULT 0,
    promotion_id   INTEGER       REFERENCES {SCHEMA}.promotions(id),
    sales_id       INTEGER       NOT NULL REFERENCES {SCHEMA}.sales(sales_id),
    date           DATE          NOT NULL
);
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def r4(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def date_range(start: datetime.date, end: datetime.date):
    day = start
    while day <= end:
        yield day
        day += datetime.timedelta(days=1)


# ── Données fixes (identiques aux CSV originaux) ──────────────────────────────

def generate_products() -> list[tuple]:
    # (id, product_name, unit_cost, unit_price)
    return [
        (1, "Classic Stroopwafel", 0.867, 2.5),
        (2, "Vanilla Stroopwafel", 1.067, 3.5),
        (3, "Honey Stroopwafel",   0.860, 3.0),
    ]


def generate_promotions() -> list[tuple]:
    # (id, product_id, name, description, start_date, end_date, discount_rate, is_holiday)
    return [
        (1, 1, "Classic Stroopwafel Super Surprise", "Third customer in line discount!",
         "2023-08-17", "2023-08-23", 0.16, False),
        (2, 2, "Vanilla Stroopwafel Taster's Choice", "Two stroopwafels for the price of one!",
         "2023-08-09", "2023-08-14", 0.13, True),
        (3, 3, "Honey Stroopwafel Super Surprise",    "Third customer in line discount!",
         "2023-07-03", "2023-07-05", 0.27, False),
    ]


# ── Générateurs Faker ─────────────────────────────────────────────────────────

def generate_employees(n: int = 10) -> list[tuple]:
    """
    Génère n employés néerlandais.
    Les 2 premiers sont embauchés dès START_DATE pour garantir
    des shifts et des ventes dès le premier jour.
    """
    rows            = []
    hire_window_end = START_DATE + datetime.timedelta(days=90)

    for emp_id in range(1, n + 1):
        dob       = fake.date_of_birth(minimum_age=18, maximum_age=40)
        hire_date = START_DATE if emp_id <= 2 else fake.date_between(
            start_date=START_DATE, end_date=hire_window_end
        )
        age = (hire_date - dob).days // 365

        if age < 18:
            rate = round(random.uniform(4.0, 6.0), 2)
        elif age < 21:
            rate = round(random.uniform(6.0, 9.0), 2)
        else:
            rate = round(random.uniform(10.0, 14.0), 2)

        rows.append((
            emp_id,
            fake.first_name(),
            fake.last_name(),
            fake.phone_number(),
            str(dob),
            str(hire_date),
            rate,
        ))
    return rows


def generate_shifts(employees: list[tuple]) -> list[tuple]:
    """4 shifts/jour : matin + après-midi × Cashier + Baker."""
    SLOTS = ["10:00-14:00", "14:00-18:00"]
    ROLES = ["Cashier", "Baker"]
    rows  = []

    for day in date_range(START_DATE, END_DATE):
        eligible = [e[0] for e in employees
                    if datetime.date.fromisoformat(str(e[5])) <= day]
        if len(eligible) < 2:
            continue
        for slot in SLOTS:
            for emp_id, role in zip(random.sample(eligible, 2), ROLES):
                rows.append((str(day), role, emp_id, slot))
    return rows


def generate_sales_and_lines(
    employees:  list[tuple],
    products:   list[tuple],
    promotions: list[tuple],
) -> tuple[list[tuple], list[tuple]]:
    """
    Génère exactement TARGET_SALES ventes réparties uniformément
    sur la période. Le nombre de lignes est déterminé par tirage
    pondéré (1/2/3 lignes par vente).
    """
    PAYMENT_TYPES = ["debit_card", "credit_card", "cash"]

    all_days    = list(date_range(START_DATE, END_DATE))
    nb_days     = len(all_days)
    base, extra = divmod(TARGET_SALES, nb_days)
    per_day     = [base + (1 if i < extra else 0) for i in range(nb_days)]

    promo_by_date = {}
    for day in all_days:
        promo_by_date[day] = {
            p[1]: p for p in promotions
            if datetime.date.fromisoformat(str(p[4])) <= day
            <= datetime.date.fromisoformat(str(p[5]))
        }

    prod_map   = {p[0]: p for p in products}
    sales_rows = []
    lines_rows = []
    sale_id    = 1
    line_id    = 1

    for day, n_sales in zip(all_days, per_day):
        eligible = [e[0] for e in employees
                    if datetime.date.fromisoformat(str(e[5])) <= day]
        if not eligible:
            continue

        active_promos = promo_by_date[day]
        weekday       = day.strftime("%A")

        sale_times = sorted(
            datetime.time(
                hour   = random.randint(8, 19),
                minute = random.randint(0, 59),
                second = random.randint(0, 59),
            )
            for _ in range(n_sales)
        )

        for sale_time in sale_times:
            emp_id       = random.choice(eligible)
            payment_type = random.choice(PAYMENT_TYPES)
            n_lines      = random.choices([1, 2, 3], weights=LINES_PER_SALE_WEIGHTS)[0]

            total_price    = 0.0
            total_discount = 0.0
            sale_lines     = []

            for _ in range(n_lines):
                product       = random.choice(products)
                prod_id       = product[0]
                unit_price    = prod_map[prod_id][3]
                quantity      = random.randint(1, 4)
                promo         = active_promos.get(prod_id)
                discount_rate = promo[6] if promo else 0.0
                promo_id      = promo[0] if promo else None

                unit_discount  = r4(unit_price * discount_rate)
                line_price     = r4((unit_price - unit_discount) * quantity)
                line_discount  = r4(unit_discount * quantity)
                total_price    = r4(total_price    + line_price)
                total_discount = r4(total_discount + line_discount)

                sale_lines.append((
                    line_id, prod_id, quantity, discount_rate,
                    unit_price, unit_discount,
                    line_price, line_discount,
                    promo_id, sale_id, str(day),
                ))
                line_id += 1

            sales_rows.append((
                sale_id, str(day), str(sale_time), emp_id,
                total_price, total_discount,
                weekday, payment_type,
            ))
            lines_rows.extend(sale_lines)
            sale_id += 1

    return sales_rows, lines_rows


# ── Injection ─────────────────────────────────────────────────────────────────

BATCH = 2000

def insert(cur, table: str, columns: list[str], rows: list[tuple]):
    if not rows:
        return
    cols  = ", ".join(columns)
    query = f"INSERT INTO {SCHEMA}.{table} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
    for i in range(0, len(rows), BATCH):
        execute_values(cur, query, rows[i : i + BATCH])


# ── Point d'entrée ────────────────────────────────────────────────────────────

def seed():
    print("Génération des données…")
    products   = generate_products()
    promotions = generate_promotions()
    employees  = generate_employees()
    shifts     = generate_shifts(employees)
    sales, sales_lines = generate_sales_and_lines(employees, products, promotions)

    print(f"  employees   : {len(employees)}")
    print(f"  products    : {len(products)}")
    print(f"  promotions  : {len(promotions)}")
    print(f"  shifts      : {len(shifts)}")
    print(f"  sales       : {len(sales)}")
    print(f"  sales_lines : {len(sales_lines)}")

    print("\nConnexion à PostgreSQL…")
    conn = psycopg2.connect(**DB_CONFIG)
    cur  = conn.cursor()

    print(f"Création du schéma '{SCHEMA}' et des tables…")
    cur.execute(DDL)
    conn.commit()

    print("Injection…")
    insert(cur, "employees",
           ["id", "name", "last_name", "contact_number", "date_of_birth", "hire_date", "hourly_rate"],
           employees)
    insert(cur, "products",
           ["id", "product_name", "unit_cost", "unit_price"],
           products)
    insert(cur, "promotions",
           ["id", "product_id", "name", "description", "start_date", "end_date", "discount_rate", "is_holiday"],
           promotions)
    insert(cur, "shifts",
           ["date", "role", "employee_id", "hours"],
           shifts)
    insert(cur, "sales",
           ["sales_id", "date", "time", "employee_id", "total_price", "total_discount", "weekday", "payment_type"],
           sales)
    insert(cur, "sales_lines",
           ["id", "product_id", "quantity_sold", "discount_rate", "unit_price", "unit_discount",
            "total_price", "total_discount", "promotion_id", "sales_id", "date"],
           sales_lines)

    conn.commit()
    cur.close()
    conn.close()
    print(f"\nBase de données alimentée avec succès. (schema: {SCHEMA})")


if __name__ == "__main__":
    seed()
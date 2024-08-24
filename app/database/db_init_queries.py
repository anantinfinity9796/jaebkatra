# db_queries.py


def return_db_queries():
    db_queries = {
                  # "create_wallet_type":""" create type wallet_type as enum ('saving','food','rent', 'transport', 'miscellaneous');""",
                  # "create_transaction_category":"""create type transaction_category as enum ('income','expenses');""",
                  "create_table_users":
                  """ create table users(
                        user_id uuid primary key,
                        name varchar(100) not null,
                        phone varchar(20),
                        created_ts timestamp not null default CURRENT_TIMESTAMP,
                        wallets uuid[],
                        family_members uuid[] );""",

                  "create_table_wallets":
                  """ create table wallets(
                        wallet_id uuid primary key,
                        name varchar(100) not null,
                        created_ts timestamp not null default CURRENT_TIMESTAMP,
                        user_id uuid references users (user_id) on delete cascade,
                        allocated_balance float8 default 0.00,
                        consumed_balance float8 default 0.00,
                        remaining_balance float8 default 0.00,
                        wallet_type wallet_type
                  );""",

                  "create_table_transactions":
                  """ create table transactions(
                        transaction_id uuid primary key,
                        user_id uuid references users (user_id) on delete cascade,
                        wallet_id uuid references wallets (wallet_id) on delete cascade,
                        transaction_amount float8 default 0.00,
                        transaction_ts timestamp not null default CURRENT_TIMESTAMP,
                        transaction_category transaction_category,
                        wallet_type wallet_type );""",

                  "create_table_budget":
                  """ create table budget(
                        budget_id uuid primary key,
                        user_id uuid references users (user_id) on delete cascade,
                        wallet_id uuid references wallets (wallet_id) on delete cascade,
                        created_ts timestamp not null default CURRENT_TIMESTAMP,
                        start_date date,
                        end_date date,
                        budget_amount float8 default 0.00
                  );""",

                  
      }
    return list(db_queries.values())
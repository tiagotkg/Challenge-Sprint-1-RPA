import sqlite3
import pandas as pd

def create_db():
    """
    Cria o banco de dados SQLite com três tabelas:
    - products_url: Armazena URLs de produtos para scraping
    - products_data: Armazena dados gerais dos produtos
    - products_review: Armazena avaliações dos produtos
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_url (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            url TEXT,
            scraped INTEGER DEFAULT 0,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            products_url_id INTEGER,
            url TEXT,
            title TEXT,
            price REAL,
            review_rating REAL,
            review_amount INTEGER,
            seller TEXT,
            description TEXT,
            brand TEXT,
            product_line TEXT,
            model TEXT,
            sales_format TEXT,
            volume_total TEXT,
            page_yield  TEXT,
            cartridge_type  TEXT,
            comments_scraped INTEGER DEFAULT 0,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products_review (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            products_data_id INTEGER,
            rating INTEGER,
            review TEXT,
            review_date text,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_url(produto, url):
    """
    Salva um novo produto e sua URL na tabela products_url.

    Args:
        produto (str): Nome do produto
        url (str): URL do produto no Mercado Livre
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_url (produto, url) VALUES (?, ?)", (produto, url))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()

def save_product(products_url_id, url, title, price, review_rating, review_amount, seller, description, brand, product_line, model, sales_format, volume_total, page_yield, cartridge_type):
    """
    Salva os dados de um produto na tabela products_data.

    Args:
        product_url_id (id): id da tabela products_url
        url (str): URL do produto
        title (str): Título do produto
        price (float): Preço do produto
        review_rating (float): Média das avaliações
        review_amount (int): Quantidade de avaliações
        seller (str): Nome do vendedor
        description (str): Descrição do produto
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_data (products_url_id, url, title, price, review_rating, review_amount, seller, description, brand, product_line, model, sales_format, volume_total, page_yield, cartridge_type)"
                    "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
            (products_url_id, url, title, price, review_rating, review_amount, seller, description, brand, product_line, model, sales_format, volume_total, page_yield, cartridge_type))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()

def save_review(products_data_id, rating, review, review_date):
    """
    Salva uma avaliação de produto na tabela products_review.

    Args:
        products_data_id (int): ID do produto relacionado
        rating (int): Nota da avaliação
        review (str): Texto da avaliação
        review_date (str): Data da avaliação
    """
    conn = sqlite3.connect("mercadolivre.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO products_review (products_data_id, rating, review, review_date)values (?, ?, ?, ?) ", (products_data_id, rating, review, review_date))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir produto, url: {e}")
    finally:
        conn.close()


def query(sql):
    """
    Executa uma consulta SQL personalizada no banco de dados.

    Args:
        sql (str): Query SQL a ser executada

    Returns:
        list: Resultado da consulta em forma de lista
    """
    conn = sqlite3.connect("mercadolivre.db")
    try:
        query = sql.split(' ')
        cur = conn.cursor()
        cur.execute(sql)

        if query[0].lower() == "select":
            return cur.fetchall()
        else:
            conn.commit()
            return True

    except Exception as e:
      print(f"Erro ao tentar executar a query: {e}")
    finally:
        conn.close()


def exportar_tabelas(path = 'outputs'):
    conn = sqlite3.connect("mercadolivre.db")
    products_url = pd.read_sql_query("select * from products_url", conn)
    products_data = pd.read_sql_query("select * from products_data", conn)
    products_review = pd.read_sql_query("select * from products_review", conn)

    products_url.to_csv(path + "/products_url.csv", index=False)
    products_data.to_csv(path + "/products_data.csv", index=False)
    products_review.to_csv(path + "/products_review.csv", index=False)

    print(f"CSVs criados na pasta: {path}")


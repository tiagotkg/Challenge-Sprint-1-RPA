from database import save_product
from mercadolivre import scrap_list, scrap_product, scrap_comments
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options

import time, random
import database

def list(produto, driver, pages = 1):
    counter = 0

    url = f"https://lista.mercadolivre.com.br/{quote(produto)}"
    page = scrap_list(produto, url, driver, counter, pages)

    for counter in range(0, pages):
        page = scrap_list(produto, page, driver, counter, pages)
        time.sleep(random.uniform(3.0, 4.0))  # para evitar ser identificado como scrap]

        if (page == False):
            break


def product(driver, limit = 10):
    products_url = database.query(f"select * from products_url where scraped = 0 limit {limit}")

    for product_url in products_url:
        try:
            print(product_url[2])
            url, title, price, product_review_rating, product_review_amount, seller, description, brand, product_line, model, sales_format, volume_total, page_yield, cartridge_type = scrap_product(product_url[2], driver)
            save_product(product_url[0], url, title, price, product_review_rating, product_review_amount, seller, description, brand, product_line, model, sales_format, volume_total, page_yield, cartridge_type)
            database.query(f"update products_url set scraped = 1 where id = {product_url[0]}")
        except Exception as e:
            raise(3)
            #print(e)
            #continue

def comments(driver, limit = None, comments_limit = 0):
    if limit:
        limit = f"limit {limit}"

    products_data = database.query(f"select * from products_data where comments_scraped = 0 {limit}")
    for product_data in products_data:
        print(product_data[2])
        scrap_comments(product_data[0], product_data[2], comments_limit, driver)



if __name__ == "__main__":
    # criando tabelas caso não existam
    database.create_db()

    # vamos começar recuperando a lista de produtos
    # produto = "cartucho hp 667 original"
    # paginas = 2
    # produtos = 50
    # comentarios = 10

    produto = input("Digite o produto que deseja pesquisar: ")
    paginas = int(input("Digite a quantidade de paginas que deseja buscar: "))
    produtos = int(input("Digite a quantidade de produtos que deseja buscar: "))
    comentarios = int(input("Digite a quantidade de comentarios para cada produto: "))

    #criando driver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome()

    list(produto, driver, paginas)
    product(driver, produtos)
    comments(driver, produtos, comentarios)

    database.exportar_tabelas()

    driver.quit()

from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementNotInteractableException

from database import save_url, save_product, save_review
import time


def scrap_list(produto, url, driver):
    try:
        driver.get(url)
        time.sleep(2)  # precisamos utilizar o sleep por 2 motivos: 1- Para não ser bloqueado; 2- Carregamentos dinâmicos que o Selenium não consegue recuperar
        print(driver.current_url)

        # aceitando termos
        termos = driver.find_elements(By.CLASS_NAME, "cookie-consent-banner-opt-out__action--key-accept")
        if termos:
            termos[0].click()
        time.sleep(1)

        ol = driver.find_element(By.CSS_SELECTOR, "ol.ui-search-layout")
        wait = WebDriverWait(driver, 10)
        wait.until(lambda _: ol.is_displayed())

        h3s = ol.find_elements(By.CSS_SELECTOR, "h3.poly-component__title-wrapper")
        wait = WebDriverWait(driver, 10)
        wait.until(lambda _: h3s)

        print(f"Total de produtos encontrados: {len(h3s)}")

        for h3 in h3s:
            poduct_url = h3.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            wait = WebDriverWait(driver, 10)
            wait.until(lambda _: wait)
            save_url(produto, poduct_url)
            wait = WebDriverWait(driver, 10)
            wait.until(lambda _: url)

        next = driver.find_element(By.CSS_SELECTOR, ".andes-pagination__button--next a")
        wait = WebDriverWait(driver, 10)
        wait.until(lambda _: next.is_displayed())

        if next:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", next)
            driver.execute_script("setTimeout(function() { document.querySelector('.andes-pagination__button--next a').click(); }, 3000);")

            time.sleep(4)
            current_url = driver.current_url
            wait = WebDriverWait(driver, 10)
            wait.until(lambda _: current_url)

            return current_url

        return False

    except Exception as e:
        raise e


def scrap_product(url, driver):
    try:
        driver.get(url)
        time.sleep(3)

        # aceitando termos
        termos = driver.find_elements(By.CLASS_NAME, "cookie-consent-banner-opt-out__action--key-accept")
        if termos:
            termos[0].click()

        time.sleep(1)

        #vamos pegar o preço e o titulo pela meta tag (mais simples)
        url = driver.current_url
        meta_tag_price = driver.find_element("xpath", '//meta[@property="og:title"]')
        og_title = meta_tag_price.get_attribute("content")
        title, price = og_title.split(' - ')

        if not price.split(','):
            price = f"{price},00"

        price = price.replace('R$ ', '').replace(',', '.')

        # recuperando availação média
        product_reviews = driver.find_elements(By.CSS_SELECTOR, "h2.ui-review-capability__header__title")
        if product_reviews:
            product_review = driver.find_element(By.CSS_SELECTOR, "div.ui-review-capability__rating")
            product_review_rating = product_review.find_element(By.CSS_SELECTOR,
                                                                "p.ui-review-capability__rating__average").text
            product_review_amount = product_review.find_element(By.CSS_SELECTOR,
                                                                "p.ui-review-capability__rating__label").text
            product_review_amount = product_review_amount.replace(' avaliações', '')

        # recuperando descrição
        description = driver.execute_script("return document.querySelector('p.ui-pdp-description__content')")
        if description:
            description = driver.find_element(By.CSS_SELECTOR, "p.ui-pdp-description__content")
            description = description.text
        else:
            description = ''

        # recuperando marca, linha, modelo e rendimento (se tiver)
        brand = ''
        product_line = ''
        model = ''
        sales_format = ''
        volume_total = ''
        page_yield = ''
        cartridge_type = ''

        more_carac = driver.find_elements(By.CSS_SELECTOR, "button.ui-vpp-highlighted-specs__striped-collapsed__action")
        if more_carac:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", more_carac[0])
            time.sleep(0.5)
            more_carac[0].click()
            time.sleep(0.5)

        caractereisticas = driver.find_element(By.CSS_SELECTOR, "div.ui-pdp-container__row--technical-specifications")
        trs = caractereisticas.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            th = tr.find_element(By.TAG_NAME, 'th').text.lower()
            td = tr.find_element(By.TAG_NAME, 'td').text
            print('th: td', f"{th}: {td}")

            if th == 'marca':
                brand = td

            if th == 'linha':
                product_line = td

            if th == 'modelo':
                model = td

            if th == 'formato de venda':
                sales_format = td

            if th == 'conteúdo total em volume':
                volume_total = td

            if th == 'rendimento de páginas':
                page_yield = td

            if th == 'tipo de cartucho':
                cartridge_type = td

        seller = driver.find_element(By.CSS_SELECTOR, "div.ui-seller-data-header__title-container").text
        seller = seller.split('Vendido por ')

        if len(seller) > 1:
            seller = seller[1]
        else:
            seller = seller[0]

        return url, title, price, product_review_rating, product_review_amount, seller, description, brand, product_line, model, sales_format, volume_total, page_yield, cartridge_type

    except Exception as e:
        print(e)
        raise e


def scrap_comments(id, url, limit, driver):
    try:
        driver.get(url)
        time.sleep(3)

        driver.implicitly_wait(10)

        #show_more = driver.find_element(By.CSS_SELECTOR, "button.show-more-click")
        show_more = driver.execute_script("return document.querySelector('button.show-more-click')")
        if (show_more):
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", show_more)
            driver.execute_script("setTimeout(function() { document.querySelector('button.show-more-click').click(); }, 3000);")
            time.sleep(2)

            iframe = driver.find_element(By.CSS_SELECTOR, '#ui-pdp-iframe-reviews')
            driver.switch_to.frame(iframe)
            time.sleep(1)

            comment = driver.find_element(By.CSS_SELECTOR, 'div.ui-review-capability-comments div')

            counter = 0
            while comment and counter < limit:
                counter = counter + 1
                comment = driver.find_element(By.CSS_SELECTOR, 'div.ui-review-capability-comments div')
                rating = comment.find_element(By.CSS_SELECTOR, 'p.andes-visually-hidden').text
                review_date = comment.find_element(By.CSS_SELECTOR, 'span.ui-review-capability-comments__comment__date').text
                review = comment.find_element(By.CSS_SELECTOR, 'p.ui-review-capability-comments__comment__content').text

                print(review_date)
                print(rating)
                print(review)
                print('-----------------------------------')

                save_review(id, rating, review, review_date)

                driver.execute_script("document.querySelector('div.ui-review-capability-comments div').remove()")
                time.sleep(2)

                comment_exists = driver.execute_script("return document.querySelector('div.ui-review-capability-comments div')")
                if comment_exists:
                    comment = driver.find_element(By.CSS_SELECTOR, 'div.ui-review-capability-comments div')
                else:
                    comment = False

        else:
            comments = driver.execute_script("return document.querySelector('article.ui-review-capability-comments__comment')")

            if comments:
                comments = driver.find_elements(By.CSS_SELECTOR, 'article.ui-review-capability-comments__comment')
                for comment in comments:
                    rating = comment.find_element(By.CSS_SELECTOR, 'p.andes-visually-hidden').text
                    review_date = comment.find_element(By.CSS_SELECTOR, 'span.ui-review-capability-comments__comment__date').text
                    review = comment.find_element(By.CSS_SELECTOR, 'p.ui-review-capability-comments__comment__content').text

                    print(review_date)
                    print(rating)
                    print(review)
                    print('-----------------------------------')
                    save_review(id, rating, review, review_date)



    except Exception as e:
        print(e)

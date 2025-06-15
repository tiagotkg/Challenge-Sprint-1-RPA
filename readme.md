# Projeto de Scraping Mercado Livre

Este projeto automatiza a coleta de dados de produtos e avaliações do Mercado Livre utilizando Python e Selenium.

## Pré-requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome
- SQLite (instalado automaticamente)
- pip

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/tiagotkg/Challenge-Sprint-1-RPA
   cd Challenge-Sprint-1-RPA
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv venv
   # Linux / Mac
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Baixe o ChromeDriver:

   - Acesse [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)
   - Baixe a versão compatível com seu Chrome
   - Descompacte e adicione o executável ao PATH do sistema

## Configuração

- Se desejar rodar o scraper em modo headless, abra `main.py` e descomente as linhas:
  ```python
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-gpu")
  ```
- Opções adicionais no Selenium podem ser configuradas em `main.py`.

## Uso

Execute o script principal:

```bash
python main.py
```

Você será solicitado a informar:

- **Produto**: termo de busca (por exemplo: `cartucho hp 667 original`)
- **Quantidade de páginas**: número de páginas a scrapear
- **Quantidade de produtos**: limite de produtos a processar
- **Quantidade de comentários**: limite de comentários por produto

Os dados coletados serão salvos em `mercadolivre.db` e, ao final, exportados para CSV na pasta `outputs/`:

- `products_url.csv`
- `products_data.csv`
- `products_review.csv`

## Estrutura do Projeto

```
├── mercadolivre.py      # Lógica de scraping
├── database.py          # Funções de conexão e persistência no SQLite
├── main.py              # Ponto de entrada e fluxo de execução
├── requirements.txt     # Dependências do projeto
├── mercadolivre.db      # Banco de dados SQLite (gerado após execução)
└── outputs/             # Pasta com CSVs exportados
```
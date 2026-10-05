# 💊 FarmaTech — Sistema de Gestão Farmacêutica

Sistema de gestão farmacêutica desenvolvido em **Python e MySQL**, com interface de terminal e arquitetura modular. O projeto simula operações de uma farmácia, incluindo gerenciamento de produtos, medicamentos, estoque, vendas, carrinho de compras e controle financeiro.

## 🚀 Funcionalidades

* **🛒 Carrinho e vendas:** gerenciamento de compras e registro de vendas com validações de estoque.
* **📦 Cadastro de produtos e medicamentos:** operações de cadastro, consulta, atualização e exclusão lógica.
* **🔍 Filtros e buscas:** consulta e organização de produtos de acordo com diferentes critérios.
* **📋 Controle de estoque:** reposição de lotes e descarte de produtos.
* **💰 Controle financeiro:** registro e acompanhamento das operações financeiras.
* **📊 Relatórios:** geração de informações para acompanhamento das operações da farmácia.
* **🔄 Soft Delete:** exclusão lógica de registros, preservando os dados no banco para manter a integridade das informações.

## 🧠 Arquitetura e Boas Práticas

O sistema foi desenvolvido utilizando uma **arquitetura modular**, separando as responsabilidades do projeto em diferentes arquivos e módulos.

* **Modularização:** divisão do sistema em módulos independentes, facilitando manutenção, organização e desenvolvimento em equipe.
* **Separação de responsabilidades:** interface, conexão com banco de dados e funcionalidades do sistema são organizadas separadamente.
* **Persistência de dados:** utilização do MySQL para armazenamento das informações.
* **Transações:** utilização de `COMMIT` e `ROLLBACK` para garantir maior segurança nas operações do banco.
* **SQL parametrizado:** utilização de parâmetros nas consultas para reduzir riscos de SQL Injection.
* **Tratamento de exceções:** utilização de `try/except` para tratamento de erros durante as operações.
* **Validações:** validação de entradas e regras de negócio antes da execução das operações.

## 🗂️ Estrutura do Projeto

```text
Farmatech/
│
├── main.py
├── interface.py
├── bd.py
├── utilidades.py
│
└── comandos/
    ├── cadastro.py
    ├── carrinho.py
    ├── estoque.py
    ├── filtros.py
    └── financeiro.py
```

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **MySQL**
* **mysql-connector-python**
* **Git / GitHub**

### Conceitos aplicados

* Programação Orientada a Objetos (POO)
* CRUD
* Estruturas de dados
* Modularização
* Modelagem de banco de dados
* SQL
* Tratamento de exceções
* Transações em banco de dados

## ⚙️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/Farmatech.git
cd Farmatech
```

### 2. Instale a dependência

```bash
pip install mysql-connector-python
```

### 3. Configure o banco de dados

Crie o banco de dados MySQL utilizado pelo projeto e configure as informações de conexão no arquivo responsável pelo acesso ao banco.

### 4. Execute o sistema

```bash
python main.py
```

## 👥 Desenvolvedores

Projeto desenvolvido em equipe durante a formação em desenvolvimento de TI:

* Christopher Magalhães
* Davi Dória Biasi
* Maria Eduardo Vieira
* Letícia Santos Joffre
* Jéssica Borges

---

Projeto desenvolvido para fins educacionais, com foco na aplicação prática de **Python, SQL, MySQL, arquitetura modular e desenvolvimento de sistemas**.

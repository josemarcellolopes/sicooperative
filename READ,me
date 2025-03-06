# SiCooperative

## Visão Geral
O **SiCooperative** é um sistema para gestão de cooperativas, focado no processamento de transações financeiras. O projeto inclui scripts de extração, transformação e carga de dados (**ETL**), utilizando arquivos **CSV** e integração com um banco de dados SQL.

## Estrutura do Projeto

```
SiCooperative/
│-- dags/                  # DAGs do Apache Airflow para ETL
│   ├── data/              # Arquivos CSV de entrada
│   ├── output/            # Arquivos gerados como saída do processo ETL
│   ├── scripts/           # Scripts Python para processamento de dados
│   ├── sql/               # Scripts SQL para criação e inserção no banco de dados
│-- notebooks/             # Jupyter Notebooks para análise de dados
│-- logs/                  # Registros de execução das DAGs e scripts
│-- backups/               # Scripts de backup para tabelas do banco
│-- screenshots/           # Capturas de tela do funcionamento do sistema
│-- docker-compose.yml     # Arquivo de configuração para Docker
│-- mysql.sh               # Script para inicialização do banco de dados MySQL
│-- run.sh | run.bat       # Scripts para iniciar o sistema em Linux/Windows
│-- stop.sh | stop.bat     # Scripts para interromper o sistema
│-- .gitignore             # Arquivo de configuração do Git
│-- docs/                  # Documentação do projeto
```

## Requisitos
- **Docker e Docker Compose** (caso deseje rodar o banco via container)
- **Python 3.8+**
- **Apache Airflow**
- **Jupyter Notebook** (para análise de dados opcional)
- **Banco de Dados MySQL**

## Instalação e Configuração
### 1. Clonando o Repositório
```bash
git clone https://github.com/seu-usuario/SiCooperative.git
cd SiCooperative
```

### 2. Configurando o Banco de Dados
Caso queira rodar o banco via Docker:
```bash
docker-compose up -d
```
Ou instale um banco MySQL localmente e configure os scripts SQL na pasta **dags/sql/**.

### 3. Instalando Dependências Python
Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Executando o Sistema
Para iniciar o processamento de dados:
```bash
./run.sh   # No Windows: run.bat
```

## Uso
O sistema utiliza **Airflow** para orquestrar processos ETL. Para acessar a interface Web do Airflow:
```bash
airflow webserver --port 8080
```
Acesse no navegador: `http://localhost:8080` e ative as DAGs disponíveis.

## Contribuição
1. Fork este repositório
2. Crie uma branch para sua funcionalidade: `git checkout -b minha-feature`
3. Faça commit das mudanças: `git commit -m 'Adicionando nova feature'`
4. Envie para o repositório remoto: `git push origin minha-feature`
5. Abra um Pull Request

## Licença
Este projeto está sob a licença MIT. Para mais detalhes, consulte o arquivo `LICENSE`.

## Contato
Caso tenha dúvidas ou sugestões, entre em contato através dos arquivos disponíveis na pasta `docs/`. 


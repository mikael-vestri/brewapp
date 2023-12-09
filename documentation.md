# Projeto: Ingestão de Dados sobre Cervejarias nos EUA

## Sumário
- [Introdução](#introdução)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
  - [Visão Geral](#visao-geral)
  - [Bronze Layer](#bronze-layer)
  - [Silver Layer](#silver-layer)
  - [Gold Layer](#gold-layer)
  - [Orquestração](#orquestração)
- [Testes Realizados](#testes-realizados)
- [Instruções de Execução](#instruções-de-execução)
- [Conclusão](#conclusão)

## Introdução
O projeto visa a ingestão de dados sobre cervejarias nos EUA em um data lake, utilizando uma API como fonte de dados. A orquestração dos dados ocorre por meio das camadas bronze, silver e gold, com Azure Data Factory para ingestão e Databricks para transformações.

## Arquitetura do Projeto
### Visão Geral
O projeto segue a tradicional "Arquitetura Medalhão" com os dados percorrendo as três camadas (bronze, silver e gold) sofrendo as transformações necessárias. A imagem abaixo ilustra essa arquitetura bem como todas as ferramentas utilizadas neste projeto. 

![arquitetura do projeto](data_architecture.JPG)

### Bronze Layer
- **Descrição Geral:** Os dados são extraídos da API e persistidos no Azure Blob Storage em seu estado raw.
- **Como os Dados são Extraídos:** Utilização do Azure Data Factory para a atividade de cópia.
- **Transformações Iniciais:** Nenhuma transformação nesta camada.
- **Esquema de Dados:** Os dados são obtidos em formato .json e contém informações referentes a cervejarias localizadas ao redor dos Estados Unidos. O esquema dos dados é da seguinte forma:
address_1: string
address_2: string
address_3: string
brewery_type: string
city: string
country: string
id: string
latitude: string
longitude: string
name: string
phone: string
postal_code: string
state: string
state_province: string
street: string
website_url: string

### Silver Layer
- **Processos de Transformação:** Databricks é utilizado para ler dados da bronze layer e escrevê-los em formato parquet na Azure Blob Storage, particionados por estados dos EUA.
- **Esquema de Dados:** Apenas algumas alterações para variáveis numéricas foram aplicadas. O esquema ficou na seguinte estrutura.
address_1: string
address_2: string
address_3: string
brewery_type: string
city: string
country: string
id: string
latitude: decimal(10,2)
longitude: decimal(10,2)
name: string
phone: string
postal_code: string
state: string
state_province: string
street: string
website_url: string

### Gold Layer
- **Processos de Agregação:** Databricks lê dados da silver layer, realiza agregações contando o número de cervejarias por tipo e estado.
- **Esquema de Dados:** Com as agregações aplicadas o esquema final ficou na seguint estrutura:
brewery_type: string
state: string
store_count: integer

### Orquestração
- **Ferramenta Utilizada:** Azure Data Factory.
- **Pipeline - Bronze Layer (pl_Bronze):**
  - Atividade de cópia para ingestão dos dados.
- **Pipeline - Silver Layer (pl_Silver):**
  - Chama o notebook Databricks para transformação.
- **Pipeline - Gold Layer (pl_Gold):**
  - Chama o segundo notebook Databricks para agregações.
- **Pipeline - Wrapper (pl_Wrapper):**
  - É o pipeline que implementa todos os outros pipelines. Ele chama na ordem o pl_bronze, pl_silver e pl_gold

## Testes Realizados
- **Contagem de Linhas por Camada:**
  - Bronze Layer: 50 linhas computadas
  - Silver Layer: 50 linhas computadas
  - Gold Layer: Somando-se todas as cervejarias contabilizadas por tipo em cada estado, obteve-se um total de 50 cervejarias 
- **Consistência entre Camadas:**
  - Diante dessa análise feita, verificou-se que os dados estão consistentes

## Instruções de Execução
- **Configuração do Ambiente:**
  - [Inserir informações sobre a configuração do ambiente, se necessário.]
- **Execução do Projeto:**
  O pipeline pl_Wrapper é o que deve ser executado para rodar todos os outros pipelines na ordem correta para que sejam executadas todas as etapas do projeto.

## Conclusão
- **Recapitulação do Projeto:**
  - A ingestão de dados foi bem sucedida
- **Melhorias Futuras:**
  - Poderão ser inseridas novas agregações para que mais tipos de análises possam ser feitas, conectando os dados obtidos com o Power BI para geração de dashboards. 

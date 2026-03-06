# Reseguro 360: Automação Regulatória e Contábil

Projeto demonstrativo em Python com foco em:

- mapeamento de fluxo operacional de resseguro
- validações regulatórias
- conciliação financeira e contábil
- geração de relatórios de exceção
- automação de processo end-to-end

## Estrutura do projeto

- `data/raw/`: arquivos brutos
- `data/curated/`: dados tratados
- `data/reference/`: tabelas de referência
- `src/`: scripts principais
- `reports/`: saídas do processo
- `docs/`: documentação de fluxo, regras e dicionário
- `app/`: interface visual simples em Streamlit

## Objetivo

Simular uma operação de resseguro e construir um pipeline básico que:

1. lê dados de contratos e eventos
2. valida regras mínimas de negócio
3. reconcilia valores financeiros
4. gera lançamentos contábeis simulados
5. produz relatório final com exceções

## Como executar

```bash
streamlit run app/streamlit_app.py
# Automação Financeira — Aplicação Desktop

Aplicação desktop desenvolvida com **Python** e interface gráfica para apoiar a extração e comparação de relatórios utilizados em conferências financeiras.

## O problema

Relatórios com estruturas diferentes exigem etapas repetitivas de leitura, preparação e comparação. Este projeto reúne essas operações em uma interface que permite selecionar fontes, processar dados e gerar relatórios de divergências.

## Funcionalidades identificadas no código

- Extratores para relatórios classificados como **R189, QPE, SPB e NFSERV**.
- Rotinas de tratamento e validação de dados, incluindo códigos utilizados nas conferências.
- Comparação de informações entre fontes e geração de **relatórios de divergências**.
- Interface gráfica para interação com o usuário.
- Integração originalmente prevista com armazenamento externo de arquivos.
- Testes para partes dos extratores e relatórios.

## Tecnologias e organização

**Python · Tkinter/CustomTkinter · pandas · processamento de arquivos · integração com API de documentos**

```text
application/
  extractors/       Extração e preparação de dados
  reports/          Relatórios de divergências
domain/
  validators/       Regras de validação
presentation/
  views/            Interface gráfica
tests/              Testes de unidades específicas
main.py             Ponto de entrada
```

## Relação com a versão web

Esta aplicação representa o formato **desktop** do trabalho de automação. A estrutura de processamento também aparece na evolução para [API](https://github.com/rodri-oliveira/automacao-financeira-api) e [interface web](https://github.com/rodri-oliveira/automacao-financeira-web).

## Como analisar

As dependências estão em `requirements.txt` e a aplicação utiliza `main.py` como entrada principal.

**Limitação:** a obtenção dos arquivos e parte das rotinas dependiam de serviços externos da implantação original. Não foi validada nesta revisão uma execução autônoma. Avalie o código com dados fictícios e sem acesso a ambientes corporativos.

## Competências demonstradas

Automação Python, processamento de dados, interface desktop, integração com serviços e análise de divergências.

## Direitos e publicação

O README anterior registrava titularidade da **WEG S.A.** sobre este projeto. Essa declaração de origem é preservada por cautela até que a titularidade e as permissões de redistribuição sejam esclarecidas. A publicação deste README não modifica direitos sobre o código.

**Status:** projeto histórico de portfólio, com dependências externas não revalidadas.

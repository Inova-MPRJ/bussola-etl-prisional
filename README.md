# ETL dos boletins de efetivo carcerário da SEAP/RJ

Ferramentas de extração, transformação e carregamento dos dados dos boletins semanais de efetivo carcerário da Secretaria de Administração Prisional do Estado do Rio de Janeiro.

Este projeto foi gerado com [cookiecutter](https://github.com/audreyr/cookiecutter) usando [jacebrowning/template-python](https://github.com/jacebrowning/template-python).

[![PyPI Version](https://img.shields.io/pypi/v/BussolaETLSeap.svg)](https://pypi.org/project/BussolaETLSeap)
[![PyPI License](https://img.shields.io/pypi/l/BussolaETLSeap.svg)](https://pypi.org/project/BussolaETLSeap)

## Requisitos

* Python 3.8
* poetry
* git

### Windows

- Microsoft Visual C++ 14.0+ [[instalar](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/)]

### Linux

- python3-venv

## Instalação

Temporariamente, o pacote só pode ser instalado copiando e repositório e instalando-o com o [Poetry](https://poetry.eustace.io/):

```text
$ git clone https://github.com/Inova-MPRJ/bussola-etl-prisional.git
$ cd bussola-etl-prisional
$ poetry install --no-dev
```

## Uso

Após a instalação, a ferramenta pode ser chamada pela interface de linha de comando, utilizando o comando `poetry run python -m bussola_etl_seap` na pasta de instalação:

```text
$ # exportar um resumo da planilha de exemplo para um arquivo CSV em ./data/output
$ poetry run python -m bussola_etl_seap -i ./data/input/example.xlsx -e occupation -o ./data/20200811_SEAP_ocupacao.csv
```

A ferramenta também pode ser usada para exportar para uma tabela para um aplicativo no [Anvil](https://anvil.works/):
```text
$ # upload para o Data Table 'bsp_seap_ocupacao', com a mesma estrutura do arquivo de 
$ # origem
$ poetry run python -m bussola_etl_seap -i ./data/input/example.xlsx -e occupation --to-anvil-table="bsp_seap_ocupacao" --anvil-token="MY_VERY_SECRET_TOKEN"
```

## AVISO

Este pacote está em desenvolvimento e é absolutamente experimental. A validade dos resultados extraídos e a compatibilidade com versões futuras não é garantida. Use por sua conta e risco.
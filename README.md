# ETL dos boletins de efetivo carcerário da SEAP/RJ

Ferramentas de extração, transformação e carregamento dos dados dos boletins semanais de efetivo carcerário da Secretaria de Administração Prisional do Estado do Rio de Janeiro.

Este projeto foi gerado com [cookiecutter](https://github.com/audreyr/cookiecutter) usando [jacebrowning/template-python](https://github.com/jacebrowning/template-python).

[![PyPI Version](https://img.shields.io/pypi/v/BussolaETLSeap.svg)](https://pypi.org/project/BussolaETLSeap)
[![PyPI License](https://img.shields.io/pypi/l/BussolaETLSeap.svg)](https://pypi.org/project/BussolaETLSeap)

## Requisitos

* Python 3.8
* pip3 e/ou pipx
* git

### Windows

- Microsoft Visual C++ 14.0+ [[instalar](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/)]

### Linux

- python3-venv

## Instalação

O pacote pode ser instalado a partir do repositório no GitHub, com o comando `python -m pip install`. Porém, recomenda-se que você utilize o utilitário `pipx`, que instala a ferramenta direto em um ambiente virtual:

```text
$ # no windows, pode ser necessário chamar o comando `python.exe`
$ python -m pip install git+https://github.com/Inova-MPRJ/bussola-etl-prisional.git
```

```text
$ # OU instale em um ambiente virtual usando o comando pipx
$ pipx install git+https://github.com/Inova-MPRJ/bussola-etl-prisional.git
```

Alternativamente, você pode instalar o pacote como uma dependência em um projeto pré-existente utilizando o gerenciador de dependências [Poetry](https://poetry.eustace.io/):

```text
$ poetry add git+https://github.com/Inova-MPRJ/bussola-etl-prisional.git
$ poetry install
```

## Uso

Após a instalação, a ferramenta pode ser chamada pela interface de linha de comando, utilizando o comando `BussolaETLSeap`:

```text
$ # exportar um resumo da planilha de exemplo para um arquivo CSV em ./data/output
$ BussolaETLSeap -i ./data/input/example.xlsx -e occupation -o ./data/20200811_SEAP_ocupacao.csv
```

A ferramenta também pode ser usada para exportar para uma tabela para um aplicativo no [Anvil](https://anvil.works/):
```text
$ # upload para o Data Table 'bsp_seap_ocupacao', com a mesma estrutura do arquivo de 
$ # origem
$ BussolaETLSeap -i ./data/input/example.xlsx -e occupation --to-anvil-table="bsp_seap_ocupacao" --anvil-token="MY_VERY_SECRET_TOKEN"
```

## AVISO

Este pacote está em desenvolvimento e é absolutamente experimental. A validade dos resultados extraídos e a compatibilidade com versões futuras não é garantida. Use por sua conta e risco.
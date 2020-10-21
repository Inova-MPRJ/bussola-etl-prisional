# ETL dos boletins de efetivo carcerário da SEAP/RJ

Ferramentas de extração, transformação e carregamento dos dados dos boletins semanais de efetivo carcerário da Secretaria de Administração Prisional do Estado do Rio de Janeiro.

Este projeto foi gerado com [cookiecutter](https://github.com/audreyr/cookiecutter) usando [jacebrowning/template-python](https://github.com/jacebrowning/template-python).

[![PyPI Version](https://img.shields.io/pypi/v/BussolaETLSeap.svg)](https://pypi.org/project/BussolaETLSeap)
[![PyPI License](https://img.shields.io/pypi/l/BussolaETLSeap.svg)](https://pypi.org/project/BussolaETLSeap)

## Requisitos

* Python 3.8

### Windows

- Microsoft Visual C++ 14.0+ [[instalar](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/)]

### Linux

- python3-venv

## Instalação

Instale diretamente em um ambiente virtual ativo:

```text
$ pip install BussolaETLSeap
```

ou adicione a um projeto com o [Poetry](https://poetry.eustace.io/):

```text
$ poetry add BussolaETLSeap
```

## Uso

Após a instalação, o pacote pode ser importado:

```text
$ python
>>> import bussola_etl_seap
>>> bussola_etl_seap.__version__ #obter a versao do pacote
```

## AVISO

Este pacote está em desenvolvimento e é absolutamente experimental. A validade dos resultados extraídos e a compatibilidade com versões futuras não é garantida. Use por sua conta e risco.
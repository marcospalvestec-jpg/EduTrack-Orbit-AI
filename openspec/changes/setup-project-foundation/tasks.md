## 1. Configuração de Ambiente e Dependências

- [ ] 1.1 Criar `requirements.txt` definindo dependências fundamentais (`streamlit`, `pydantic`, `requests`, `python-dotenv`, `pytest`, `pytest-mock`) e verificar formato do arquivo.
- [ ] 1.2 Criar `pyproject.toml` especificando compatibilidade com Python 3.12+, metadados do projeto, configuração de `pytest` com `pythonpath = ["."]` e diretrizes de qualidade de código.
- [ ] 1.3 Criar `.env.example` e `.streamlit/secrets.toml.example` contendo apenas chaves descritivas e valores mock/fictícios, verificando a ausência de dados reais.
- [ ] 1.4 Criar `.streamlit/config.toml` definindo as diretrizes visuais oficiais do tema (cores primárias, plano de fundo, fontes) e parâmetros seguros de execução do Streamlit.

## 2. Estrutura Modular de Pacotes e Diretórios

- [ ] 2.1 Criar a estrutura do pacote `app/` contendo os subdiretórios `api/`, `components/`, `core/`, `i18n/`, `models/`, `services/`, `styles/`, `utils/` e `views/`, incluindo arquivos `__init__.py` em cada um.
- [ ] 2.2 Criar o módulo `app/core/config.py` com dataclass/schema de configurações e lógica de leitura hierárquica (`st.secrets` -> `.env` -> valores padrão de desenvolvimento).
- [ ] 2.3 Criar os diretórios auxiliares `xano/` (com `xano/README.md` documentando convenções XanoScript e tabelas canônicas), `docs/` (com `docs/architecture.md` detalhando a visão arquitetural) e `scripts/` (com `scripts/__init__.py`).

## 3. Entrypoint e Documentação

- [ ] 3.1 Criar o entrypoint principal `app.py` na raiz configurando o título da página, slogan oficial e mensagem inicial de fundação do EduTrack Orbit AI.
- [ ] 3.2 Criar o `README.md` detalhando visão geral, stack técnica obrigatória, instruções passo a passo de configuração do ambiente virtual, execução via `streamlit run app.py`, estrutura modular e diretrizes OpenSpec.

## 4. Testes e Validação da Fundação

- [ ] 4.1 Criar a infraestrutura de testes em `tests/` com `tests/__init__.py`, `tests/conftest.py` e `tests/test_foundation.py` validando importações modulares de `app.*`, resolução de configuração e teste de inicialização do `app.py` via `streamlit.testing.v1.AppTest`, verificando que a aplicação inicia sem exceções.
- [ ] 4.2 Executar a suíte de testes com `pytest` e comprovar que todos os testes unitários são executados com sucesso.
- [ ] 4.3 Verificar conformidade do `.gitignore`, garantindo que diretórios dinâmicos como `reports/generated/` e credenciais reais estejam protegidos contra versionamento.

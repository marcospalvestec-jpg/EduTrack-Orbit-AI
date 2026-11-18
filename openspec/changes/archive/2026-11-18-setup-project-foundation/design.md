# Design Técnico: setup-project-foundation

## Context

O projeto **EduTrack Orbit AI** está iniciando a sua estrutura de código a partir das diretrizes de `AGENTS.md` e `openspec/config.yaml`. Trata-se de uma aplicação em Python 3.12+ utilizando Streamlit no frontend, preparada para consumir backend Xano via REST, com isolamento multiusuário, testes automatizados e deploy previsto no Streamlit Community Cloud.

## Goals / Non-Goals

**Goals:**
- Estabelecer a árvore modular de diretórios do projeto e os arquivos estruturais básicos.
- Configurar ambiente de execução Python 3.12+ com `pyproject.toml` e `requirements.txt`.
- Configurar tema visual e opções do servidor Streamlit em `.streamlit/config.toml`.
- Criar templates seguros de variáveis e segredos (`.env.example` e `.streamlit/secrets.toml.example`).
- Fornecer um entrypoint mínimo `app.py` que valide a inicialização e sirva de base para as próximas propostas.
- Configurar infraestrutura de testes em `tests/` executável via `pytest`.
- Documentar arquitetura e guia de execução no `README.md`.

**Non-Goals:**
- Implementar telas de autenticação, dashboard ou regras de negócio.
- Conectar ou fazer chamadas reais a instâncias de banco de dados ou APIs do Xano.
- Gerar relatórios ou integrar recursos de inteligência artificial.

## Decisions

### 1. Estrutura Modular de Diretórios

A aplicação adota uma arquitetura em camadas dentro do pacote `app/`:

```text
EduTrack-Orbit-AI/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── __init__.py
│   ├── components/
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── i18n/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── styles/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   └── views/
│       └── __init__.py
├── docs/
│   └── architecture.md
├── scripts/
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_foundation.py
├── xano/
│   └── README.md
├── .env.example
├── .gitattributes
├── .gitignore
├── AGENTS.md
├── app.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

*Alternativa considerada*: Estrutura plana de arquivos no nível raiz.  
*Razão da escolha*: A arquitetura modular desacopla responsabilidades (UI, regras de negócio, dados, comunicação REST) e facilita testes unitários e manutenibilidade.

### 2. Gerenciamento Centralizado de Configurações (`app/core/config.py`)

A camada `core/config.py` centralizará o acesso a variáveis de configuração com fallback hierárquico:
1. `st.secrets` (ambiente de produção / Streamlit Cloud).
2. Variáveis de ambiente (`.env` local via `python-dotenv` ou `os.environ`).
3. Valores padrão seguros para desenvolvimento.

*Alternativa considerada*: Acesso direto a `os.getenv` em múltiplos módulos.  
*Razão da escolha*: Evita duplicação de lógica de resolução de credenciais e facilita testes com mocks.

### 3. Paleta Visual no `.streamlit/config.toml`

O arquivo `.streamlit/config.toml` definirá o tema oficial (cores primárias, fontes e background) conforme as regras do projeto:
- `primaryColor = "#0D9488"` (Azul-petróleo / Teal)
- `backgroundColor = "#FFFFFF"`
- `secondaryBackgroundColor = "#F3F4F6"`
- `textColor = "#111827"`
- `font = "sans serif"`

### 4. Configuração de Testes e Ferramentas em `pyproject.toml`

Utilizar `pyproject.toml` para unificar configurações de `pytest`, `ruff` (linter/formatter) e `mypy` (checagem de tipos para Python 3.12+).

## Risks / Trade-offs

- **[Risco] Resolução de imports ao executar `streamlit run app.py`**  
  → *Mitigação*: A raiz do projeto é mantida no `sys.path` ou tratada explicitamente na inicialização do `app.py`, garantindo que `import app.*` funcione tanto no runtime do Streamlit quanto no `pytest`.

- **[Risco] Exposição acidental de credenciais em repositório**  
  → *Mitigação*: `.gitignore` já bloqueia `.env`, `.streamlit/secrets.toml` e arquivos de credenciais; apenas `.example` com dados fictícios são adicionados.

- **[Risco] Criação de diretório de relatórios gerados em tempo de execução**  
  → *Mitigação*: A pasta `reports/generated/` está explicitamente ignorada no `.gitignore` e será criada programaticamente apenas sob demanda.

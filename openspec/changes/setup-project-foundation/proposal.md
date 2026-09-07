# Proposta: setup-project-foundation

## Why

O projeto **EduTrack Orbit AI** precisa de uma base técnica inicial padronizada, modular e executável para viabilizar o desenvolvimento orientado por especificações (OpenSpec). Estabelecer a fundação com Python 3.12+, Streamlit, estrutura de diretórios, configurações de ambiente e testes automatizados agora assegura consistência arquitetural, segurança contra vazamento de credenciais e prontidão para deploy no Streamlit Community Cloud antes do início das integrações de negócio.

## What Changes

- Criação do entrypoint principal `app.py` com renderização inicial mínima para validação de inicialização.
- Criação do pacote modular `app/` contendo:
  - `api/`: Camada de comunicação REST com clientes HTTP.
  - `components/`: Componentes visuais e reutilizáveis de interface.
  - `core/`: Configurações centrais, gerenciamento de estado e carregamento de variáveis/segredos.
  - `models/`: Schemas tipados e modelos de dados.
  - `services/`: Regras de negócio e orquestração de serviços.
  - `styles/`: Customização de temas e estilos CSS.
  - `utils/`: Funções utilitárias puras e helpers.
  - `views/`: Telas e visualizações do Streamlit.
  - `i18n/`: Estrutura de internacionalização (pt-BR, en-US, en-GB, es).
- Adição de `__init__.py` nos diretórios do pacote para suporte à importação modular.
- Criação da infraestrutura de testes em `tests/` com suites unitárias de importação e inicialização para `pytest`.
- Criação do diretório `xano/` com documentação e versionamento para scripts XanoScript.
- Criação do diretório `docs/` para documentação arquitetural e decisões de engenharia.
- Criação do diretório `scripts/` para scripts de automação e utilitários de desenvolvimento.
- Configuração de templates seguros de credenciais (`.env.example` e `.streamlit/secrets.toml.example`) com dados fictícios.
- Configuração de tema e opções visuais seguras em `.streamlit/config.toml`.
- Definição formal de dependências do projeto em `requirements.txt` e `pyproject.toml` (com ferramentas de linting, formatação e pytest para Python 3.12+).
- Criação de documentação completa no `README.md` (instalação, execução via `streamlit run app.py`, arquitetura e contribuição).

## Capabilities

### New Capabilities
- `project-foundation`: Estabelece a arquitetura estrutural do projeto, modularização de pacotes, configurações seguras de execução Streamlit, templates de ambiente e infraestrutura de testes unitários.

### Modified Capabilities
<!-- Nenhuma capability prévia modificada (setup inicial) -->

## Non-Goals (Fora do Escopo)

- Implementação de integração real com endpoints do Xano.
- Implementação de cadastro, login, JWT e recuperação de senha.
- Implementação de CRUD para disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`).
- Implementação do dashboard analítico definitivo.
- Geração ou exportação de relatórios PDF.
- Implementação de recursos ou assistentes com IA.
- Deploy em ambiente de produção (apenas preparação estrutural).
- Implementação de regras de negócio ou telas completas de usuário.

## Impact

- **Código:** Estabelece a estrutura inicial de pastas e módulos no repositório.
- **Ambiente & Dependências:** Define dependências mínimas em `requirements.txt` e `pyproject.toml` para Python 3.12+.
- **Qualidade & Testes:** Habilita execução de `pytest` com validação de inicialização e importação.
- **Segurança:** Garante que nenhum segredo real seja exposto no versionamento através de arquivos `.example`.

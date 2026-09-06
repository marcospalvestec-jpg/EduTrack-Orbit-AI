# EduTrack Orbit AI

> **Slogan:** "Organize, acompanhe e evolua"

O **EduTrack Orbit AI** é uma aplicação web educacional responsiva projetada para estudantes de cursos técnicos e superiores gerenciarem disciplinas, tarefas acadêmicas, prazos e evolução do progresso com apoio de inteligência artificial.

---

## 🚀 Stack Tecnológica Obrigatória

- **Linguagem Principal:** Python 3.12+
- **Frontend / Interface:** Streamlit (UI responsiva, mobile-first, suporte a temas Claro/Escuro)
- **Backend & Banco de Dados:** Xano & XanoScript (fonte oficial e única da verdade via REST API)
- **Autenticação:** JSON Web Token (JWT) com isolamento rigoroso por usuário
- **Governança & Especificação:** OpenSpec (Spec-Driven Development)
- **Testes Automatizados:** pytest
- **Deploy Planejado:** Streamlit Community Cloud

---

## 📁 Estrutura do Projeto

```text
EduTrack-Orbit-AI/
├── .streamlit/
│   ├── config.toml               # Configurações visuais do tema e servidor
│   └── secrets.toml.example      # Template de segredos para Streamlit Cloud
├── app/
│   ├── api/                      # Clientes HTTP e comunicação REST com Xano
│   ├── components/               # Componentes visuais reutilizáveis
│   ├── core/                     # Configurações centrais e gerenciamento de estado
│   ├── i18n/                     # Internacionalização (pt-BR, en-US, en-GB, es)
│   ├── models/                   # Schemas Pydantic tipados (users, subjects, tasks)
│   ├── services/                 # Camada de serviços e regras de negócio
│   ├── styles/                   # CSS injetado e tokens visuais
│   ├── utils/                    # Funções utilitárias puras
│   └── views/                    # Telas completas da aplicação
├── docs/                         # Documentação técnica e arquitetura
├── openspec/                     # Propostas, especificações e governança OpenSpec
├── scripts/                      # Utilitários de automação e desenvolvimento
├── tests/                        # Suíte de testes automatizados com pytest
├── xano/                         # Documentação de schemas e scripts XanoScript
├── .env.example                  # Template seguro de variáveis de ambiente
├── .gitattributes                # Normalização de finais de linha e binários
├── .gitignore                    # Regras estritas de proteção e isolamento de segredos
├── AGENTS.md                     # Diretrizes mandatórias para agentes e desenvolvedores
├── app.py                        # Entrypoint principal do Streamlit
├── pyproject.toml                # Metadados do projeto e configurações de ferramentas
├── README.md                     # Este documento
└── requirements.txt              # Dependências do Python
```

---

## 🛠️ Instalação e Execução Local

### Pré-requisitos

- Python 3.12 ou superior instalado.
- Git configurado.

### 1. Clonar o Repositório

```bash
git clone https://github.com/marcospalvestec-jpg/EduTrack-Orbit-AI.git
cd EduTrack-Orbit-AI
```

### 2. Criar e Ativar o Ambiente Virtual

No Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Ou instalar com dependências de desenvolvimento:
```bash
pip install -e ".[dev]"
```

### 4. Configurar Variáveis de Ambiente

Copie os modelos de exemplo:
```bash
cp .env.example .env
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 5. Executar a Aplicação

```bash
streamlit run app.py
```

Acesse a interface no navegador em: `http://localhost:8501`.

---

## 🧪 Testes Automatizados

Para executar os testes com o `pytest`:

```bash
pytest
```

Para executar testes com relatório detalhado:
```bash
pytest -v
```

---

## 📜 Governança e Regras de Contribuição

1. **OpenSpec Obrigatório:** Toda e qualquer alteração funcional deve conter uma proposta formal (`proposal.md`, `specs/`, `design.md`, `tasks.md`) aprovada antes de escrever código.
2. **Segurança:** Nenhum segredo, token ou chave real de API deve ser commitado no repositório.
3. **Padrões de Código:**
   - Type hints obrigatórios em todas as funções públicas.
   - Docstrings descritivas no padrão Google/Sphinx.
   - Respeito à arquitetura modular em camadas.

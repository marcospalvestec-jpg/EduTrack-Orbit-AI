# EduTrack Orbit AI — Regras e Diretrizes para Agentes de IA

> **Nome Oficial:** EduTrack Orbit AI  
> **Slogan:** "Organize, acompanhe e evolua"

Este documento estabelece as regras mandatórias de desenvolvimento, arquitetura, design, segurança e fluxo de trabalho para qualquer agente ou desenvolvedor atuando no projeto **EduTrack Orbit AI**.

---

## 1. Ordem Obrigatória de Trabalho

Todo agente de IA ou desenvolvedor deve seguir rigorosamente o seguinte ciclo de trabalho:

1. **Ler `AGENTS.md`**: Conhecer e respeitar todas as restrições e padrões do projeto.
2. **Ler `openspec/config.yaml`**: Entender a visão global do sistema e o escopo do projeto.
3. **Verificar propostas existentes**: Checar propostas ativas em `openspec/` antes de iniciar qualquer trabalho.
4. **Criar ou atualizar uma proposta**: Nenhuma linha de funcionalidade deve ser escrita sem uma proposta correspondente.
5. **Validar a proposta**: Garantir que `proposal.md`, `design.md`, `specs/` e `tasks.md` estejam consistentes e alinhados aos requisitos.
6. **Implementar apenas as tarefas aprovadas**: Seguir estritamente o escopo definido e aprovado nas propostas.
7. **Executar testes**: Validar regras de negócio, isolamento de dados e ausência de regressões.
8. **Atualizar documentação**: Refletir mudanças nas especificações e artefatos de documentação.
9. **Solicitar revisão antes de arquivar a proposta**: Marcar tarefas concluídas e obter validação antes de dar a proposta como finalizada.

---

## 2. Stack Tecnológica Obrigatória

- **Linguagem Principal:** Python 3.12+
- **Frontend / Interface:** Streamlit (UI interativa, responsiva e moderna)
- **Backend & Banco de Dados:** Xano & XanoScript (fonte oficial e única da verdade para dados e regras de negócio no servidor)
- **Comunicação:** APIs REST (JSON)
- **Controle de Versão:** Git & GitHub

> [!CAUTION]
> **Proibição Estrita de Frameworks Alternativos:**  
> É terminantemente proibido substituir o **Streamlit** por React, Next.js, Vue, Angular, FlutterFlow ou qualquer outro framework/ferramenta de frontend, exceto se expressamente aprovado em uma nova proposta formal.

---

## 3. Desenvolvimento Orientado por Especificações (OpenSpec)

- Todo desenvolvimento é guiado por **OpenSpec**.
- Toda funcionalidade deve conter a estrutura canônica:
  - `proposal.md`: Contexto, justificativa e escopo da proposta.
  - `design.md`: Arquitetura, componentes visuais e fluxos.
  - `specs/`: Especificações técnicas e de integração (APIs, modelos, etc.).
  - `tasks.md`: Lista de tarefas estruturadas com checkboxes (`[ ]` / `[x]`) e critérios de aceitação mensuráveis e verificáveis.
- **Nenhuma implementação poderá fugir da proposta OpenSpec aprovada.**
- **Nunca criar funcionalidades não solicitadas** nem alterar decisões arquiteturais sem registrar e aprovar uma nova proposta.

---

## 4. Arquitetura e Padrões de Código Python

- **Arquitetura Modular e Separação de Responsabilidades:**
  - `views/` ou `components/`: Componentes visuais e renderização de tela.
  - `services/`: Regras de negócio e orquestração de serviços.
  - `api/` ou `client/`: Camada de comunicação com endpoints do Xano.
  - `models/`: Modelos de dados e schemas tipados.
  - `utils/`: Funções utilitárias puras e helpers.
- **Qualidade de Código:**
  - Uso obrigatório de **Type Hints** (`typing`).
  - **Docstrings** descritivas em módulos, classes e funções.
  - Tratamento robusto e explícito de erros e exceções.
  - Código limpo, testável e de fácil manutenção.
- **Gerenciamento de Cache no Streamlit:**
  - Utilizar cache (`@st.cache_data`, `@st.cache_resource`) apenas para dados estáticos/globais ou quando **não comprometer** o isolamento, a privacidade ou a atualização em tempo real dos dados do usuário autenticado.

---

## 5. Backend, Dados e Segurança (Xano)

- **Fonte Oficial:** O backend Xano é a fonte canônica dos dados da aplicação.
- **Nomenclatura no Backend:** Obrigatório o uso do padrão **`snake_case`** para endpoints, tabelas e colunas no Xano.
- **Tabelas Canônicas Principais:**
  - `users`: Usuários do sistema, perfis e credenciais.
  - `subjects`: Disciplinas/matérias acadêmicas.
  - `academic_tasks`: Tarefas, entregas, prazos e atividades acadêmicas.
- **Autenticação e Autorização:**
  - Autenticação via **JWT (JSON Web Token)** gerado pelo Xano.
  - **Isolamento de Dados Multiusuário:** Garantir que todas as consultas e operações filtrem estritamente os dados pelo `user_id` autenticado.
  - Testes e validações devem comprovar que um usuário **nunca** consegue visualizar ou alterar dados de outro.
- **Gestão de Segredos e Credenciais:**
  - Tokens, chaves de API, URLs privadas e senhas **nunca** devem ser gravados diretamente no código-fonte.
  - Usar `st.secrets` para ambiente de produção.
  - Usar variáveis de ambiente (`.env`) durante o desenvolvimento local.

---

## 6. Funcionalidades e Escopo do Aplicativo

O **EduTrack Orbit AI** contempla os seguintes módulos essenciais:

1. **Autenticação:** Cadastro de usuário, Login com JWT e Recuperação de Senha.
2. **Dashboard:** Visão geral de métricas, prazos iminentes e status acadêmico.
3. **Disciplinas (`subjects`):** Gerenciamento de matérias (criação, edição, exclusão e carga horária).
4. **Tarefas Acadêmicas (`academic_tasks`):**
   - **Status canônicos:**
     - `draft` (na interface pt-BR deve ser exibido como **"Rascunho"**)
     - `pending` (Pendente)
     - `in_progress` (Em Andamento)
     - `completed` (Concluída)
     - `overdue` (Atrasada)
   - **Subtarefas:** Suporte a subtarefas com checkbox interativo.
   - **Conclusão:** A conclusão da tarefa principal deve ocorrer obrigatoriamente através de um **botão explícito** de confirmação/conclusão.
5. **Filtros e Métricas:** Filtros por disciplina, status, prioridade e intervalo de datas.
6. **Cálculo de Progresso:**
   - **Cálculo Simples:** Baseado na contagem percentual de tarefas finalizadas.
   - **Cálculo Ponderado:** Calculado proporcionalmente com base na carga horária / peso das disciplinas e tarefas.
7. **Assistente Inteligente (AI):** Recomendações e ações inteligentes; deve **obrigatoriamente pedir confirmação do usuário** antes de executar qualquer alteração de dados.
8. **Relatórios:** Exportação e visualização de relatórios consolidados em formato **PDF**.
9. **Configurações:** Perfil do usuário, preferências de tema e idioma.

---

## 7. Design, UI/UX e Acessibilidade

- **Abordagem Mobile-First:** Totalmente responsivo e otimizado para celulares, tablets e desktops.
- **Suporte a Temas:** Suporte obrigatório e refinado aos temas **Claro (Light)** e **Escuro (Dark)**.
- **Estética Visual:**
  - Design limpo, contemporâneo e profissional.
  - Cartões arredondados (*rounded cards*) e espaçamentos consistentes.
  - Gráficos claros e de leitura simples e intuitiva.
- **Paleta de Cores Oficial:**
  - **Azul-petróleo:** Cor de destaque / primária.
  - **Roxo:** Inteligência, destaques e elementos de IA.
  - **Verde:** Sucesso, tarefas concluídas e progresso positivo.
  - **Laranja:** Atenção, prazos próximos e estados intermediários.
  - **Vermelho:** Estados críticos, tarefas atrasadas (`overdue`) e alertas.
- **Feedback ao Usuário e Ações Críticas:**
  - Toda ação de criação, edição ou exclusão deve gerar **retorno visual explícito** (mensagens de sucesso, banners, toasts ou alerts).
  - Qualquer exclusão ou operação destrutiva deve **exigir confirmação prévia** do usuário.

---

## 8. Internacionalização (i18n)

O sistema deve ser preparado arquiteturalmente para suportar múltiplos idiomas:
- `pt-BR` (Português do Brasil - idioma padrão inicial)
- `en-US` (Inglês dos EUA)
- `en-GB` (Inglês Britânico)
- `es` (Espanhol)

---

## 9. Desempenho, Escalabilidade e Git Workflow

- **Desempenho:** Tempo de resposta das requisições de API inferior a **2 segundos**.
- **Escalabilidade:** Arquitetura dimensionada para suportar no mínimo **1.000 usuários ativos**.
- **Padrão de Commits Git:**
  - Commits atômicos, pequenos e focados em uma única responsabilidade/mudança.
  - Mensagens claras, no formato semântico ou descritivo padronizado.

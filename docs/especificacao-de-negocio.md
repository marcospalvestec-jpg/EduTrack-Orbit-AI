# Especificação de Negócio: EduTrack AI (Versão Streamlit)

**Versão:** 1.0 (Streamlit Edition)  
**Tecnologia:** Python (Streamlit) + Xano  
**Projeto:** EduTrack AI - Assistente Educacional Personalizado  
**Público-Alvo:** Estudantes que precisam gerenciar disciplinas e ver progresso via Web App.

## 1. Visão Geral do Projeto
O EduTrack AI é um **Web App Responsivo** construído inteiramente em Python (usando a biblioteca **Streamlit**) conectado a um backend **Xano** (gerenciado via **XanoScript**). A proposta é criar uma ferramenta de dados onde o aluno não apenas registra tarefas, mas visualiza dashboards interativos sobre seu desempenho escolar.

### Stack Tecnológica
- **Backend:** Xano (Banco de dados e API).
- **Frontend:** Streamlit (Python puro para UI).
- **Orquestração:** OpenSpec (para guiar a IA na geração de código Python e Xano).

## 2. Problema Resolvido
- Estudantes perdem o controle de múltiplas disciplinas.
- Falta de visualização clara de dados (Gráficos de progresso).
- Ferramentas atuais são complexas demais ou manuais demais (Planilhas).

## 3. Requisitos Funcionais (Priorizados)
### MVP (Mínimo Viável - Features Básicas)
1.  **Autenticação Simples**
    - Tela de Login em Streamlit (integração com endpoint `/auth/login` do Xano).
    - Sessão mantida via `st.session_state`.

2.  **Gerenciamento de Disciplinas (CRUD)**
    - Tabela interativa (`st.data_editor` ou `st.dataframe`) para listar disciplinas.
    - Barra lateral (`st.sidebar`) com formulário para adicionar nova disciplina.

3.  **Gerenciamento de Tarefas**
    - Visualização de tarefas por disciplina.
    - Checkbox para marcar tarefa como concluída (dispara update no API Xano).

4.  **Dashboard de Dados**
    - Métricas principais (`st.metric`): Total Disciplinas, Tarefas Pendentes.
    - Gráfico de Barras (`st.bar_chart`): Tarefas por Disciplina.

### Features Intermediárias (Foco em Python)
5.  **Cálculo Avançado de Progresso**
    - Script Python (Pandas) que baixa dados do Xano e calcula % de conclusão localmente antes de exibir.

6.  **Busca e Filtros**
    - Filtros dinâmicos na interface (`st.multiselect`) para filtrar tarefas por status ou matéria.

### Features Avançadas (Projeto Final)
7.  **Relatórios PDF**
    - Botão "Baixar Relatório Semanal" que gera um PDF usando bibliotecas Python (`fpdf` ou `reportlab`) e oferece para download.

## 4. Requisitos Não-Funcionais
- **Performance:** Carregamento rápido de Dataframes.
- **Usabilidade:** Design limpo padrão do Streamlit.
- **Deploy:** Hospedado no Streamlit Community Cloud (acessível via link público).

## 5. User Stories (Adaptadas para Web App)
- "Como estudante, quero acessar o link do app no navegador e ver meu dashboard imediatamente."
- "Como estudante, quero usar filtros laterais para ver apenas tarefas atrasadas."
- "Como estudante, quero baixar um PDF com minhas notas e pendências."

## 6. Critérios de Aceitação
- **MVP Entregue:** App rodando em `edu-track-ai.streamlit.app` (exemplo).
- **Código Python:** Uso correto de `st.cache_data` para otimizar chamadas ao Xano.
- **Segurança:** Tokens de API (Xano) não expostos no código (uso de `st.secrets`).

## 7. Diferenças Chave (vs FlutterFlow)
- Não há "telas" móveis nativas, mas páginas web responsivas.
- Não há push notifications.
- Foco total em manipulação de dados e gráficos, menos em customização visual fina (pixel-perfect).

**Fim da Especificação**

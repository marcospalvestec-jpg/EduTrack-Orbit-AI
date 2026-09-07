# Plano de Ensino: Innovation Lab: Desenvolvimento Avançado No/Low

**Disciplina:** Innovation Lab: Desenvolvimento Avançado No/Low Code  
**Carga Horária Total:** 80 horas (40 horas presenciais + 40 horas autônomas)  
**Curso:** [Inserir nome do curso/programa]  
**Período:** [Inserir semestre/ano]  
**Professor Responsável:** [Seu nome]  

## Pré-requisitos
- Conhecimentos básicos em ferramentas no/low code: Xano (backend) e Figma (design de interfaces).
- **Proatividade em Programação (Code-First):** Foco em Python, já que utilizaremos **Streamlit** para o Frontend, exigindo escrita de código interface.
- Noções iniciais de programação em Python (variáveis, funções, listas/dicionários, manipulação de JSON e APIs) – cursado em paralelo.
- Nenhum conhecimento prévio de Git/GitHub necessário (será introduzido na disciplina).

## Ementa
A disciplina introduz o conceito de Spec-Driven Development (SDD) aplicado a ecossistemas híbridos. Utilizando o framework OpenSpec da Fission-AI, os alunos aprenderão a alinhar intenções humanas com execuções de IA de forma determinística. Ênfase em criar propostas de mudança, validar especificações e gerenciar o ciclo de vida de aplicações onde a IA gera código Python (Lógica + UI Streamlit) e XanoScript customizado para integrações auditáveis. Inclui introdução prática a Git/GitHub e XanoScript via VS Code Extension como base para controle de versão e backend programático.

## Objetivos Gerais
- Capacitar os alunos a usar especificações estruturadas para guiar IAs na construção de soluções Full-Stack (Frontend Python + Backend Xano).
- Introduzir Git/GitHub e XanoScript de forma prática e integrada, como ferramentas fundamentais para projetos reais com IA.
- Desenvolver habilidades em engenharia de software assistida por IA, substituindo ferramentas de drag-and-drop por frameworks de UI declarativa (Streamlit) para maior agilidade e controle.

## Habilidades e Competências Desenvolvidas
- Básicos de Git/GitHub: criar repositórios, clonar, commit, push/pull e resolver conflitos simples.
- Fluxo profissional com Git: branches, Pull Requests (PRs) e merge com boas práticas.
- XanoScript e VS Code Extension: editar arquivos .xs para definir schemas de banco e sincronizar com Xano via pull/push.
- Dominar o fluxo do OpenSpec: comandos como `openspec init`, `openspec proposal <name>`, `openspec validate <name>`, `openspec apply <name>` e `openspec archive <name>`.
- Engenharia de especificações: redigir `proposal.md` para guiar IA na geração de XanoScript e scripts Python para UI (Streamlit) e lógica.
- Desenvolvimento Code-First: criar interfaces complexas apenas usando Python e Streamlit, integrando via APIs REST com Xano.
- Gestão de contexto: usar Spec Deltas e AGENTS.md aprimorado para projetos longos.

## Projeto Integrador
Todo o conteúdo será aplicado no desenvolvimento iterativo de um único aplicativo: **EduTrack AI** – assistente educacional para rastrear disciplinas, tarefas e progresso acadêmico, com insights gerados por lógica Python e interface web interativa em Streamlit.

## Conteúdo Programático

### Módulo 0: Fundamentos de Git, Python e XanoScript (8h presenciais + 8h autônomas)
- Importância do controle de versão e da “source of truth”.
- Instalação de Git, **Python 3.12+**, Node.js (para OpenSpec), VS Code e extensões.
- Conceitos básicos de Git: clone, add, commit, push/pull.
- Introdução ao XanoScript: linguagem .xs, pull/push de workspace Xano via VS Code Extension.
- Prática: criar repo GitHub, configurar OpenSpec e sincronizar um workspace Xano simples.

### Módulo 1: Do “Vibe Coding” ao Spec-Driven Development (10h presenciais + 10h autônomas)
- Problemas do desenvolvimento assistido por IA sem estrutura.
- Solução OpenSpec: estrutura de pastas, project.md, AGENTS.md.
- **Frontend Code-First:** Configuração do ambiente Streamlit (`venv`, `pip install`), estrutura de Multipage Apps.
- Prática: criar estrutura da UI em Python baseada em wireframes Figma (sem importação direta).

### Módulo 2: O Ciclo de Mudança com IA, Python e XanoScript (12h presenciais + 12h autônomas)
- Criação de propostas de mudança (`openspec proposal <name>`).
- Uso da IA para gerar XanoScript e código Streamlit (`st.dataframe`, `st.metric`).
- Integração Frontend-Backend via `requests` em Python.
- Prática principal: criar/gerir `subjects` e `academic_tasks` via UI Python conectada ao Xano.

### Módulo 3: Implementação, Auditoria, Manutenção e Projeto Final (10h presenciais + 10h autônomas)
- Aplicação de mudanças e gestão de propostas.
- Deploy de aplicações Python: `requirements.txt` e Streamlit Community Cloud.
- Projeto Final: versão completa do EduTrack AI publicada na web.

## Por Que Streamlit e XanoScript?
- **Streamlit:** permite que alunos foquem 100% em lógica Python, eliminando a barreira de entrada de HTML/CSS/JS ou ferramentas visuais complexas, ideal para Data Apps e MVPs rápidos.
- **XanoScript:** permite que a IA gere código para modificar o backend Xano de forma programática.

## Metodologia de Ensino
- Abordagem prática em laboratório (hands-on) em Python.
- Alunos atuam como “arquitetos”; a IA como “programadora full-stack” (Backend e Frontend).
- Ferramentas principais: VS Code + extensões (Gemini Code Assist), Xano, Streamlit.

## Avaliação
- **30%** Exercícios práticos semanais.
- **30%** Qualidade das especificações e código gerado (Python UI + XanoScript).
- **40%** Projeto Final (EduTrack AI): 
  - Funcionalidade completa na Web (Streamlit Cloud).
  - Histórico de commits claros.
  - Relatório final explicando o fluxo OpenSpec.
  - Apresentação para uma banca examinadora.

**Fim do Plano de Ensino (Versão Streamlit)**

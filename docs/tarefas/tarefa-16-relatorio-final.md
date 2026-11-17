# Tarefa 16 — Relatório de entrega do EduTrack Orbit AI

- **Data:** 17/11/2026
- **Repositório:** [EduTrack-Orbit-AI](https://github.com/marcospalvestec-jpg/EduTrack-Orbit-AI)
- **Branch local:** `feature/orbit-web-mvp`

O EduTrack ajuda estudantes a organizar disciplinas, acompanhar tarefas e reservar tempo de foco. A versão web usa Next.js, TypeScript e Tailwind. O protótipo Streamlit permanece disponível como legado, com histórico e evidências acadêmicas próprias.

## O que pode ser demonstrado

Na versão web é possível cadastrar uma disciplina, adicionar uma tarefa com prazo e prioridade, marcá-la como concluída e acompanhar o progresso. A aplicação permite combinar filtros, buscar disciplinas pelo nome ou por tarefas atrasadas e vincular uma tarefa sugerida ao Pomodoro. O relatório semanal reúne as tarefas com vencimento de segunda a domingo e pode ser salvo como PDF pelo navegador.

Os dados da demonstração ficam no navegador. O adaptador do Xano foi testado com respostas simuladas, mas a interface ainda não usa autenticação nem persistência remota. Recuperação de conta, isolamento entre estudantes, calendário e homologação permanecem pendentes. O relatório web não comprova o endpoint Xano/Python previsto na Tarefa 15.

## Como o OpenSpec ajudou

As propostas registraram o escopo da fundação, do protótipo acadêmico, da autenticação demonstrativa e da interface Orbit. Por exemplo, a proposta do protótipo separou o trabalho de disciplinas, tarefas e indicadores da integração real com o Xano. Essa distinção também orienta a auditoria atual: um fluxo com dados locais pode ser demonstrado, mas não comprova persistência e autorização no servidor.

Em 17/11, `openspec.cmd validate --all --strict` aprovou as quatro propostas existentes. Elas continuam em `openspec/changes/`; a validação não significa que estejam arquivadas ou que todo o escopo tenha sido entregue. `npm --prefix apps/web test` registrou 9 testes aprovados, incluindo regras de foco, busca, filtros, progresso, relatório semanal e o adaptador simulado.

## Histórico da versão web

- `dc8d67c` — MVP web com Pomodoro, disciplinas, tarefas e progresso.
- `6917f4f` — relatório semanal com exportação pelo navegador.

PR de entrega, publicação e confirmação de envio no Classroom ainda pendentes na data deste relatório.

## Roteiro para o vídeo

1. Apresente o EduTrack e explique que esta demonstração web usa dados fictícios salvos no navegador.
2. Cadastre uma disciplina e uma tarefa com prazo na semana atual. Mostre a tarefa na lista e, se ela estiver pendente, a sugestão do Orbit.
3. Inicie e pause o Pomodoro. Marque a tarefa como concluída e mostre a mudança no progresso.
4. Abra o relatório semanal, salve como PDF e abra o arquivo salvo para mostrar o período e a tarefa.
5. Mostre no GitHub os commits e explique a pasta OpenSpec. Mostre no Xano ou no XanoScript o modelo de usuário, disciplina e tarefa, sem revelar credenciais nem dados reais.
6. Se apresentar login ou recuperação do Streamlit, identifique-os como parte do legado e diga se o fluxo mostrado é demonstrativo. Não atribua esse comportamento à versão web.

Para o Classroom: anexar o relatório, o vídeo, o PDF de demonstração e o link do PR quando publicado. O link local da aplicação não é acessível pelo professor.

# EduTrack Orbit AI — web

Primeiro incremento em Next.js, TypeScript e Tailwind, independente do Streamlit. A cor de fundo parte dos registros de Cyber Cherry; o briefing v1.0 integral ainda não foi localizado.

```powershell
npm install
npm run dev
```

Requer Node 24. Abra `http://localhost:3000`, escolha “Criar novo usuário” e cadastre nome, e-mail e senha de pelo menos 10 caracteres. Cada conta tem disciplinas, tarefas e revisões próprias, salvas no SQLite do servidor. Veja [CONTAS.md](CONTAS.md). O cronômetro reinicia ao atualizar a página.

Validação: `npm test` e `npm run build -- --webpack`. A versão inclui cadastro, login, logout, CRUD de disciplinas e tarefas, agenda mensal de prazos, Pomodoro, Revisão Orbit, filtros, busca, gráfico semanal, PDF via impressão e temas. Recuperação por e-mail e integração homologada com o Xano continuam pendentes. O legado e as evidências acadêmicas permanecem separados.

O adaptador `lib/xano.ts` cobre cadastro, login, perfil e listagem e criação de disciplinas e tarefas com o contrato histórico. Para ligá-lo ao aplicativo, confirmar primeiro o ambiente Xano dedicado a dados sintéticos. O servidor lerá `EDUTRACK_TARGET=homologacao` e `XANO_HML_BASE_URL` de `apps/web/.env.local`; não usar prefixo público ou compartilhar segredos pelo chat. A interface continua em modo local até a conexão e a sessão serem implementadas e verificadas.

## Equivalência com as tarefas da disciplina

- 12: a versão web calcula o percentual de tarefas concluídas de cada disciplina em TypeScript. Para evidência literal em Python, o legado mantém o cálculo em `src/core/metrics.py`.
- 14: em Disciplinas, digite um nome ou marque a opção para incluir disciplinas com tarefas atrasadas. A combinação é por **OU**. A versão atual filtra os dados locais; ainda não demonstra o endpoint híbrido Xano + Python pedido no enunciado original.
- 15: o relatório web lista as tarefas com vencimento entre segunda e domingo. Use “Imprimir ou salvar como PDF” e selecione “Salvar como PDF” no diálogo do navegador. O endpoint Xano/Python exigido no enunciado original não faz parte desta versão.
- 16: conta e persistência foram testadas pela API local. Falta consolidar o PR e as evidências da jornada visual. O vídeo será entregue em 23/11.

## Acesso para avaliação

O PDF de entrega contém um link temporário de demonstração via túnel HTTPS. Ele depende do computador ligado e do servidor e túnel ativos; não é hospedagem permanente. Logs de execução em `.runtime/`, banco em `.data/` e segredos não são versionados.

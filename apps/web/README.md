# EduTrack Orbit AI — web

Primeiro incremento em Next.js, TypeScript e Tailwind, independente do Streamlit. A cor de fundo parte dos registros de Cyber Cherry; o briefing v1.0 integral ainda não foi localizado.

```powershell
npm install
npm run dev
```

Abra `http://localhost:3000`. Cadastre uma disciplina e tarefas fictícias, vincule a recomendação ao Pomodoro e inicie a sessão. Ao fim de cada etapa, a próxima fica pronta para iniciar manualmente. O progresso acadêmico é salvo no navegador quando o armazenamento está disponível; o cronômetro reinicia ao atualizar a página.

Validação: `npm test` e `npm run build`. O modo local não inclui conta, recuperação ou isolamento no Xano. Ainda faltam integração homologada, calendário e os demais módulos da nova versão. O legado e as evidências acadêmicas continuam separados.

O adaptador `lib/xano.ts` cobre cadastro, login, perfil e listagem e criação de disciplinas e tarefas com o contrato histórico. Para ligá-lo ao aplicativo, confirmar primeiro o ambiente Xano dedicado a dados sintéticos. O servidor lerá `EDUTRACK_TARGET=homologacao` e `XANO_HML_BASE_URL` de `apps/web/.env.local`; não usar prefixo público ou compartilhar segredos pelo chat. A interface continua em modo local até a conexão e a sessão serem implementadas e verificadas.

## Equivalência com as tarefas da disciplina

- 12: a versão web calcula o percentual de tarefas concluídas de cada disciplina em TypeScript. Para evidência literal em Python, o legado mantém o cálculo em `src/core/metrics.py`.
- 14: em Disciplinas, digite um nome ou marque a opção para incluir disciplinas com tarefas atrasadas. A combinação é por **OU**. A versão atual filtra os dados locais; ainda não demonstra o endpoint híbrido Xano + Python pedido no enunciado original.
- 15: o legado fornece PDF; a exportação ainda não foi portada para a web.
- 16: falta demonstrar a jornada completa da nova versão, com conta e persistência no servidor, e consolidar o PR e as evidências.

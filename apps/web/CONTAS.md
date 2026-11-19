# Contas na versão local — 19/11/2026

A entrada do aplicativo exige cadastro ou login. O servidor usa SQLite em `.data/accounts.sqlite`, fora do Git, e scrypt com sal individual para senhas. A sessão dura um dia, usa cookie HttpOnly/SameSite e é revogada no logout. As consultas identificam o proprietário exclusivamente pela sessão.

Requer Node 24. Os dados permanecem neste computador, inclusive após reiniciar o servidor; não apagar a pasta .data. A implantação em nuvem requer disco persistente, HTTPS e configuração específica, ainda não realizada. O Xano anterior não foi alterado. Esta implementação não é uma migração para outro provedor.

Os dados antigos salvos no navegador não são importados automaticamente: uma conta nova começa vazia. Não há recuperação de senha por e-mail nesta etapa.

Verificação: duas contas sintéticas foram cadastradas pela API em localhost. A segunda começou vazia e não alterou os dados da primeira ao salvar os próprios dados. Login incorreto foi negado; após logout o acesso retornou 401; novo login recuperou os dados salvos. Testes automatizados cobrem também token forjado e dados inválidos. Isso não equivale a auditoria completa ou validação no celular.

## Context

O protótipo Streamlit já possui página inicial e três páginas acadêmicas alimentadas por `SimulatedDataService`. Consulte `proposal.md` para a motivação e `specs/demo-authentication/spec.md` para os comportamentos. Nesta entrega não existe Xano configurado nem serviço de e-mail, e nenhuma credencial pode ser adicionada ao repositório.

## Goals / Non-Goals

**Goals:**

- Isolar validação e estado de autenticação da camada visual.
- Proteger todas as páginas acadêmicas com uma verificação única e reutilizável.
- Permitir demonstrar cadastro, login, logout e redefinição sem rede.
- Manter o fluxo simples, responsivo e testável.
- Preservar a troca futura do serviço local por um cliente Xano.

**Non-Goals:**

- Fornecer segurança ou persistência de produção.
- Enviar e-mails ou links externos.
- Armazenar usuários em arquivos, banco local ou Git.
- Implementar JWT, OAuth, MFA ou autorização por perfis.
- Alterar modelos, métricas, filtros ou dados acadêmicos.

## Decisions

### 1. Serviço demonstrativo independente do Streamlit

As regras de cadastro, login e redefinição ficarão em `src/services/demo_auth.py`, operando sobre um repositório em memória fornecido pela camada de sessão. A interface apenas coleta entradas e exibe resultados.

**Alternativa considerada:** concentrar tudo em `app.py`. Foi rejeitada porque impediria testes unitários e tornaria a futura migração ao Xano mais cara.

### 2. Senhas representadas por hash mesmo no protótipo

O serviço usará `hashlib.pbkdf2_hmac` com salt individual e comparação constante. A senha em texto não será armazenada na sessão.

**Alternativa considerada:** guardar a senha em texto para simplificar. Foi rejeitada porque criaria um exemplo inseguro sem reduzir significativamente o código.

### 3. Estado de sessão centralizado

Um módulo `src/core/auth_session.py` inicializará as chaves necessárias, informará o usuário atual, exigirá autenticação e encerrará a sessão. As páginas chamarão o mesmo guard antes de obter dados acadêmicos.

**Alternativa considerada:** repetir condicionais nas páginas. Foi rejeitada por risco de uma rota ficar desprotegida.

### 4. Página inicial como portal de autenticação

Quando não autenticado, `app.py` apresentará abas de login, cadastro e recuperação. Quando autenticado, mostrará o conteúdo inicial atual e o controle de logout.

**Alternativa considerada:** criar uma página adicional dentro de `pages/`. Foi rejeitada porque o Streamlit continuaria exibindo rotas internas e aumentaria a confusão na demonstração.

### 5. Recuperação deliberadamente simulada

O fluxo não produzirá token nem mensagem externa. Para contas locais existentes, a mesma sessão habilitará um formulário de nova senha. A interface sempre apresentará resposta neutra à solicitação.

**Alternativa considerada:** simular envio com um link falso. Foi rejeitada porque induziria o avaliador a entender que existe integração externa.

### 6. Conta padrão reprodutível

O repositório em memória começará com `demo@edutrack.ai` e uma senha documentada somente como credencial de demonstração. Usuários criados existirão apenas durante a sessão.

**Alternativa considerada:** exigir cadastro sempre. Foi rejeitada porque aumenta o tempo e o risco da apresentação.

## Risks / Trade-offs

- [Dados de conta desaparecem ao reiniciar] → Mostrar aviso permanente de modo demonstrativo.
- [Usuário pode confundir recuperação com envio real] → Usar linguagem explícita de redefinição local e não exibir confirmação de e-mail enviado.
- [Navegação multipágina do Streamlit continua visível] → Executar o guard no início de cada página e interromper antes de consultar dados.
- [Estado compartilhado fica inconsistente] → Centralizar nomes de chaves e inicialização em um único módulo.
- [Credencial padrão é pública] → Identificá-la como exclusiva da demonstração e impedir qualquer interpretação de segurança produtiva.

## Migration Plan

1. Adicionar e testar o serviço de autenticação local.
2. Adicionar helpers de sessão e componentes dos formulários.
3. Integrar os fluxos à página inicial.
4. Aplicar o guard e o logout às páginas acadêmicas.
5. Executar Ruff, Pytest, testes Streamlit e validação OpenSpec.
6. Na integração futura, substituir o serviço local por Xano preservando a interface e o contrato de sessão.

Para rollback, remover os módulos novos e restaurar as chamadas iniciais das quatro páginas; modelos e dados acadêmicos não serão alterados.

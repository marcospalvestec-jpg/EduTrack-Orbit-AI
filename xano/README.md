# EduTrack Orbit AI - Backend Xano & XanoScript

Este diretório armazena especificações, schemas de banco e scripts **XanoScript** versionados da aplicação.

## Convenções Oficiais

- **Padrão de Nomenclatura:** Obrigatório o uso de `snake_case` para todos os endpoints, tabelas e nomes de coluna.
- **Isolamento de Dados (Multiusuário):** Todas as queries e mutations no Xano devem filtrar estritamente por `user_id` autenticado via JWT.
- **Formato de Resposta:** JSON padronizado com códigos HTTP adequados (200, 201, 400, 401, 403, 404, 500).

## Tabelas Canônicas Principais

1. **`users`**:
   - `id` (integer / auto-increment)
   - `created_at` (timestamp)
   - `name` (text)
   - `email` (text / unique)
   - `password` (text / hash seguro)
   - `role` (text / student)

2. **`subjects`**:
   - `id` (integer / auto-increment)
   - `created_at` (timestamp)
   - `user_id` (integer / fk users)
   - `name` (text)
   - `workload_hours` (integer / decimal)
   - `color` (text / hex color)

3. **`academic_tasks`**:
   - `id` (integer / auto-increment)
   - `created_at` (timestamp)
   - `user_id` (integer / fk users)
   - `subject_id` (integer / fk subjects)
   - `title` (text)
   - `description` (text)
   - `due_date` (timestamp)
   - `priority` (text / low, medium, high)
   - `status` (text / draft, pending, in_progress, completed, overdue)
   - `subtasks` (json array)

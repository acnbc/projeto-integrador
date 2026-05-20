-- Execute se a tabela parecer já existir com colunas DATE:
-- mysql -u root ufrj < scripts/alter_parecer_datetime.sql
USE ufrj;
ALTER TABLE parecer
    MODIFY COLUMN data_solicitacao_parecer DATETIME NULL,
    MODIFY COLUMN data_parecer DATETIME NULL;

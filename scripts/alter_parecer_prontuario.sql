-- Migração: prontuário registrado em cada parecer
ALTER TABLE parecer
    ADD COLUMN numero_prontuario VARCHAR(50) NULL AFTER texto_parecer;

UPDATE parecer p
INNER JOIN internacao i ON p.internacao_id = i.id
SET p.numero_prontuario = i.numero_prontuario
WHERE p.numero_prontuario IS NULL;

ALTER TABLE parecer
    MODIFY numero_prontuario VARCHAR(50) NOT NULL;

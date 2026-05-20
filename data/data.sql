use ufrj;

CREATE TABLE `perfil` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(250) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO perfil(nome)
VALUES('coordenador'),('aluno');

CREATE TABLE `usuarios`
(
    `id` int NOT NULL AUTO_INCREMENT,
    `nome` varchar(250) CHARACTER SET utf8 NOT NULL,
    `email` varchar(250) CHARACTER SET utf8 NOT NULL,
    `senha_hash` varchar(250) CHARACTER SET utf8 NOT NULL,
    `perfil_id` int NOT NULL,
    `criado_em` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `inativado_em` timestamp NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT fk_usuarios_perfil_id_perfil FOREIGN KEY (perfil_id) REFERENCES perfil (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tipo_alta`
(
    `id` int NOT NULL AUTO_INCREMENT,
    `alta` varchar(250) CHARACTER SET utf8 NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `internacao` (
    `id` int NOT NULL AUTO_INCREMENT,
    `data_internacao` DATE NULL,
    `numero_prontuario` varchar(50) CHARACTER SET utf8  NOT NULL,
    `setor_internacao` varchar(100) CHARACTER SET utf8  NOT NULL,

    `data_nascimento_paciente` DATE NULL,
    `nome_paciente` varchar(250) CHARACTER SET utf8 NOT NULL,
    `sexo_paciente` enum('F','M') DEFAULT 'F',
    `grau_instrucao_paciente` varchar(50) CHARACTER SET utf8 NULL,
    `moradia_paciente` varchar(250) CHARACTER SET utf8 NULL,

    `familiares_atendidos` int NULL,

    `criado_por` int NOT NULL,
    `criado_em` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

    `tipo_alta_id` int NULL,
    `data_alta` DATE NULL,
    `obs_alta` varchar(250) CHARACTER SET utf8 NULL,


    PRIMARY KEY (`id`),
    CONSTRAINT fk_internacao_alta_id_tipo_alta FOREIGN KEY (tipo_alta_id) REFERENCES tipo_alta (id),
    CONSTRAINT fk_internacao_criado_por_usuarios FOREIGN KEY (criado_por) REFERENCES usuarios (id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `parecer`
(
    `id` int NOT NULL AUTO_INCREMENT,
    `data_solicitacao_parecer` DATETIME NULL,
    `data_parecer` DATETIME NULL,
    `texto_parecer` TEXT NULL,
    `numero_prontuario` VARCHAR(50) NOT NULL,
    `internacao_id` int NOT NULL,
    `criado_por` int NOT NULL,
    `criado_em` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT fk_parecer_internacao_id_internacao FOREIGN KEY (internacao_id) REFERENCES internacao (id),
    CONSTRAINT fk_parecer_criado_por_usuarios FOREIGN KEY (criado_por) REFERENCES usuarios (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



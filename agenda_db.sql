CREATE DATABASE agenda;

USE agenda;

CREATE TABLE contatos(
	id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(150),
    email VARCHAR(150),
    telefone VARCHAR(11),
    tipoTelefone VARCHAR(200),
    
	 PRIMARY KEY(id)
);

SELECT * FROM contatos;
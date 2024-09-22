CREATE DATABASE IF NOT EXISTS db_agenda;
USE db_agenda;

CREATE TABLE IF NOT EXISTS tb_usuarios (
    usu_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    usu_nome VARCHAR(45) NOT NULL,
    usu_senha VARCHAR(255) NOT NULL,
    usu_email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tb_categoria_tarefas (
    cat_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    cat_nome VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tb_tarefas (
    tar_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    tar_nome VARCHAR(45) NOT NULL,
    tar_descricao VARCHAR(200) NOT NULL,
    tar_entrega DATE,
    tar_cat_id INT NOT NULL,
    FOREIGN KEY (tar_cat_id) REFERENCES tb_categoria_tarefas(cat_id),
    tar_usu_id INT NOT NULL,
    FOREIGN KEY (tar_usu_id) REFERENCES tb_usuarios(usu_id)
);



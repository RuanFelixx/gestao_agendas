create database db_agenda;
use db_agenda;

create table tb_usuarios(
usu_id int primary key not null auto_increment,
usu_nome varchar(45) not null,
usu_senha varchar(255) not null,
usu_email varchar(100) not null
);

create table tb_categoria_tarefas(
cat_id int primary key not null auto_increment,
cat_nome varchar(255) not null
);

create table tb_tarefas(
tar_id int primary key not null auto_increment,
tar_nome varchar(45) not null,
tar_descricao varchar(200) not null,
tar_entrega date,
tar_cat_id int not null,
foreign key(tar_cat_id) references tb_categoria_tarefas(cat_id),
tar_usu_id int not null,
foreign key(tar_usu_id) references tb_usuarios(usu_id)
)


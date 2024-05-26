CREATE TABLE notas (notas_id INT NOT null auto_increment, 
tema varchar(100) not null unique, subtema  varchar(300), descripcion varchar(1000),  
creado_en timestamp not null default(now()), primary key(notas_id)
);
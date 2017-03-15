create database if not exists seniorproject;
use seniorproject;

create table if not exists projects (
   id integer PRIMARY KEY,
   name VARCHAR(128)
);

create table if not exists class (
   id integer,
   name VARCHAR(1024),
   project integer,
   PRIMARY KEY (id, project),
   FOREIGN KEY (project) references projects(id)
);

create table if not exists dev (
   id integer,
   name VARCHAR(32),
   class_id INTEGER,
   class_affinity FLOAT,
   project integer,
   PRIMARY KEY (id, class_id, project),
   FOREIGN KEY (project) references projects(id)
);

create table if not exists req (
   id integer,
   title VARCHAR(80),
   description VARCHAR(1000),
   class_id INTEGER,
   class_affinity FLOAT,
   churn INTEGER,
   project integer,
   created_at DATETIME,
   closed_at DATETIME,
   is_past integer,
   PRIMARY KEY (id, class_id, project),
   FOREIGN KEY (project) references projects(id)
);

create table if not exists users (
   id integer PRIMARY KEY,
   username VARCHAR(32),
   password VARCHAR(32)
);

create table if not exists pull (
   id integer,
   body VARCHAR(1000),
   dev_id integer,
   file_id integer,
   additions integer,
   deletions integer,
   project integer,
   PRIMARY KEY (id, project, file_id),
   FOREIGN KEY (dev_id) references dev(id)
);


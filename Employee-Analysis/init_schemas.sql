drop table if exists examples;

create table `examples` (
  `id` int not null auto_increment,
  `name` varchar(50) default null,
  primary key (`id`)
);

drop table if exists departments;

create table `departments` (
  `id` int not null,
  `department_name` varchar(50) default null,
  primary key (`id`)
);

drop table if exists levels;

create table `levels` (
  `id` int not null,
  `level_name` varchar(50) default null,
  primary key (`id`)
);

drop table if exists employees;

create table `employees` (
  `id` int not null,
  `first_name` varchar(50) default null,
  `last_name` varchar(50) default null,
  `date_of_birth` date default null,
  `department_id` int default null,
  `date_started` date default null,
  `level_id` int default null,
  `salary` int default null,
  primary key (`id`),
  foreign key (`department_id`) references departments(`id`),
  foreign key (`level_id`) references levels(`id`)
);
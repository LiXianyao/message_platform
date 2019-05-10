create table MessageAnalysis.users
(
userid int not null auto_increment primary key,
 username varchar(64) not null,
 passwd varchar(64) not null,
 identity int not null,
 email varchar(64) null,
  lastTaskId varchar(16) null,
  foreign key (identity) references MessageAnalysis.identity(identity)
)CHARSET ="utf8";

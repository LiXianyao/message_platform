create table MessageAnalysis.identity
(
identity int not null auto_increment,
 identityName varchar(32) null,
 authority int not null,
primary key(identity),
foreign key (authority) references MessageAnalysis.function(functionId)
)CHARSET ="utf8";

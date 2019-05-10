create table MessageAnalysis.function
(
functionId int not null auto_increment primary key,
 functionName varchar(32) not null,
functionSrc varchar(32) not null,
sectionId int not null,
foreign key (sectionId) references MessageAnalysis.functionSection(sectionId) on delete cascade
)CHARSET ="utf8";

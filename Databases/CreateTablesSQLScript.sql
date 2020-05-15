Use master
Go

PRINT '';
PRINT '*** Dropping Database';
GO

IF EXISTS (SELECT [name] FROM [master].[sys].[databases] WHERE [name] = N'JapaneseFoodQuiz')
DROP DATABASE JapaneseFoodQuiz;
GO

PRINT '';
PRINT '*** Creating Database';
GO

Create database JapaneseFoodQuiz
Go

Use JapaneseFoodQuiz
Go

PRINT '';
PRINT '*** Creating Table Questions';
GO

Create Table Questions
(
QuestionsID int primary key identity,
QuizSetID int not null,
A varchar(MAX) not null,
B varchar(MAX) not null,
C varchar(MAX) not null,
D varchar(MAX) not null,
Correct int not null
)
Go

PRINT '';
PRINT '*** Creating Table QSRelation';
GO

Create table QSRelation
(
QuizSetID int not null,
QuestionsID int
)
Go

PRINT '';
PRINT '*** Creating Table QuizSet';
GO

Create table QuizSet
(
QuizSetID int primary key identity,
Title varchar(50),
Picture varbinary(MAX)
)
Go

PRINT '';
PRINT '*** Creating Table Answered';
GO

Create table Answered
(
UserID int not null,
QuizSetID int,
HighScore int
)
Go

PRINT '';
PRINT '*** Creating Table Users';
GO

Create table Users
(
UserID int primary key identity,
Pass varchar(20),
UserName varchar(30),
LastLogin date
)
Go

PRINT '';
PRINT '*** Add Users and Answered Quiz Set relations';
GO
AlTER TABLE Answered ADD CONSTRAINT 
FK_UserID FOREIGN KEY (UserID)REFERENCES Users(UserID);
AlTER TABLE Answered ADD CONSTRAINT 
FK_QuizSetID FOREIGN KEY (QuizSetID)REFERENCES QuizSet(QuizSetID);
Go

PRINT '';
PRINT '*** Add Quiz Set and Questions relations';
GO
AlTER TABLE QSRelation ADD CONSTRAINT 
FK_QuestionsID FOREIGN KEY (QuestionsID)REFERENCES Questions(QuestionsID);
AlTER TABLE QSRelation ADD CONSTRAINT 
FK_QuizSetID2 FOREIGN KEY (QuizSetID)REFERENCES QuizSet(QuizSetID);
Go



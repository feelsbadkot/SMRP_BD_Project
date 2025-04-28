CREATE TABLE Users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Full_name TEXT NOT NULL UNIQUE,
    Login TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Role TEXT NOT NULL CHECK(Role IN ('Исследуемый', 'Исследователь')),
    Date_of_birth DATE,
    ResearcherId INTEGER,
    FOREIGN KEY (ResearcherId) REFERENCES Users(Id) ON DELETE SET NULL
);

CREATE TABLE Investigated_Details (
    UserId INTEGER PRIMARY KEY,
    Occupation TEXT,
    TasksPerSecondWithMusic REAL,
    TasksPerSecondWithoutMusic REAL,
    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
);

CREATE TABLE Researcher_Details (
    UserId INTEGER PRIMARY KEY,
    Number_of_patients INTEGER,
    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
);

CREATE TABLE Musical_Composition (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Genre TEXT,
    Title TEXT,
    Artist TEXT,
    Year INTEGER,
    Duration INTEGER
);

CREATE TABLE Task (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Difficulty TEXT NOT NULL,
    Type TEXT,
    Answer TEXT
);

CREATE TABLE User_Musical_Composition (
    UserId INTEGER,
    MusicalCompositionId INTEGER,
    PRIMARY KEY (UserId, MusicalCompositionId),
    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE,
    FOREIGN KEY (MusicalCompositionId) REFERENCES Musical_Composition(Id) ON DELETE CASCADE
);

CREATE TABLE User_Task (
    UserId INTEGER,
    TaskId INTEGER,
    PRIMARY KEY (UserId, TaskId),
    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE,
    FOREIGN KEY (TaskId) REFERENCES Task(Id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Full_name TEXT NOT NULL,
    Login TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Role TEXT NOT NULL CHECK(Role IN ('Исследователь', 'Исследуемый')),
    Date_of_birth TEXT NOT NULL,
    ResearcherId INTEGER,
    FOREIGN KEY (ResearcherId) REFERENCES Users(Id)
);

CREATE TABLE IF NOT EXISTS Researcher_Details (
    UserId INTEGER PRIMARY KEY,
    Number_of_patients INTEGER NOT NULL,
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

CREATE TABLE IF NOT EXISTS Investigated_Details (
    UserId INTEGER PRIMARY KEY,
    Occupation TEXT NOT NULL,
    EfficiencyWithMusic REAL,
    EfficiencyWithoutMusic REAL,
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

CREATE TABLE IF NOT EXISTS Examples (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Expression TEXT NOT NULL,
    CorrectAnswer INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Sessions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserId INTEGER NOT NULL,
    SessionDate TEXT NOT NULL,
    CorrectAnswers INTEGER NOT NULL,
    ElapsedSeconds INTEGER NOT NULL,
    Efficiency REAL NOT NULL,
    WithMusic INTEGER NOT NULL DEFAULT 0,  -- 0: без музыки, 1: с музыкой 
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

CREATE TABLE IF NOT EXISTS Music (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Author TEXT NOT NULL,
    Title TEXT NOT NULL,
    Duration INTEGER NOT NULL,  
    FilePath TEXT NOT NULL     
);
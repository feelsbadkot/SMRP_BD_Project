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

CREATE TABLE Examples (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Expression TEXT NOT NULL,
    CorrectAnswer INTEGER NOT NULL
);

CREATE TABLE Sessions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserId INTEGER NOT NULL,
    SessionDate TEXT NOT NULL,
    CorrectAnswers INTEGER NOT NULL,
    ElapsedSeconds INTEGER NOT NULL,
    TasksPerSecond REAL NOT NULL,
    WithMusic INTEGER NOT NULL DEFAULT 0,     -- 0: без музыки, 1: с музыкой 
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);
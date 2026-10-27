-- Campus sample database for SQL Server (T-SQL). Original material by Aseef Ahmed.
-- Run in SSMS / Azure Data Studio. Creates database CampusDB and fills it.

IF DB_ID(N'CampusDB') IS NULL CREATE DATABASE CampusDB;
GO
USE CampusDB;
GO

DROP TABLE IF EXISTS dbo.marks, dbo.students, dbo.batches, dbo.faculty;
GO

CREATE TABLE dbo.faculty (
    faculty_id  INT           NOT NULL PRIMARY KEY,
    name        NVARCHAR(60)  NOT NULL,
    subject     NVARCHAR(30)  NOT NULL,
    salary      INT           NOT NULL,
    hired_on    DATE          NOT NULL
);
CREATE TABLE dbo.batches (
    batch_id    VARCHAR(10)   NOT NULL PRIMARY KEY,
    course      NVARCHAR(60)  NOT NULL,
    faculty_id  INT           NULL REFERENCES dbo.faculty(faculty_id),
    start_date  DATE          NOT NULL,
    timing      NVARCHAR(20)  NULL
);
CREATE TABLE dbo.students (
    student_id  INT           NOT NULL PRIMARY KEY,
    name        NVARCHAR(60)  NOT NULL,
    city        NVARCHAR(40)  NULL,
    batch_id    VARCHAR(10)   NULL REFERENCES dbo.batches(batch_id),
    email       VARCHAR(100)  NULL,
    joined_on   DATE          NOT NULL,
    fee_paid    INT           NOT NULL DEFAULT 0
);
CREATE TABLE dbo.marks (
    student_id  INT           NOT NULL REFERENCES dbo.students(student_id),
    subject     NVARCHAR(30)  NOT NULL,
    marks       INT           NULL CHECK (marks BETWEEN 0 AND 100),
    PRIMARY KEY (student_id, subject)
);
GO

INSERT INTO dbo.faculty VALUES
    (1, N'Sana Iqbal', N'Python', 180000, N'2021-02-01'),
    (2, N'Usman Tariq', N'SQL', 165000, N'2019-08-15'),
    (3, N'Mehwish Raza', N'Statistics', 172000, N'2022-01-10'),
    (4, N'Kamran Ali', N'Web', 150000, N'2023-06-01'),
    (5, N'Nida Farooq', N'AI', 210000, N'2024-03-18');
INSERT INTO dbo.batches VALUES
    (N'AI-2601', N'Diploma in AI', 1, N'2026-01-12', N'Morning'),
    (N'AI-2602', N'Diploma in AI', 2, N'2026-04-06', N'Evening'),
    (N'DS-2601', N'Data Science', 3, N'2026-02-02', N'Weekend'),
    (N'WD-2601', N'Web Development', 4, N'2026-03-09', N'Evening'),
    (N'ML-2701', N'Machine Learning', NULL, N'2027-01-11', NULL);
INSERT INTO dbo.students VALUES
    (101, N'Ayesha Khan', N'Karachi', N'AI-2601', N'ayesha@example.com', N'2026-01-05', 45000),
    (102, N'Bilal Ahmed', N'Lahore', N'AI-2601', NULL, N'2026-01-07', 30000),
    (103, N'Hira Siddiqui', N'Karachi', N'AI-2602', N'hira@example.com', N'2026-03-28', 45000),
    (104, N'Omar Farooq', N'Quetta', N'DS-2601', N'omar@example.com', N'2026-01-25', 15000),
    (105, N'Zara Hussain', N'Karachi', N'DS-2601', NULL, N'2026-01-30', 45000),
    (106, N'Hamza Malik', N'Islamabad', N'WD-2601', N'hamza@example.com', N'2026-03-01', 0),
    (107, N'Fatima Noor', N'Lahore', N'AI-2602', N'fatima@example.com', N'2026-04-01', 45000),
    (108, N'Ali Raza', NULL, N'AI-2601', N'ali@example.com', N'2026-01-10', 30000),
    (109, N'Mariam Javed', N'Karachi', N'WD-2601', NULL, N'2026-03-05', 15000),
    (110, N'Saad Qureshi', N'Peshawar', NULL, N'saad@example.com', N'2026-10-20', 0);
INSERT INTO dbo.marks VALUES
    (101, N'Python', 88),
    (101, N'SQL', 79),
    (102, N'Python', 64),
    (102, N'SQL', 58),
    (103, N'Python', 92),
    (103, N'SQL', 95),
    (104, N'Statistics', 71),
    (104, N'Python', 49),
    (105, N'Statistics', 83),
    (105, N'Python', 77),
    (106, N'Web', 68),
    (107, N'Python', 74),
    (107, N'SQL', 81),
    (108, N'Python', 39),
    (108, N'SQL', 45),
    (109, N'Web', 90);
GO

SELECT COUNT(*) AS students FROM dbo.students;

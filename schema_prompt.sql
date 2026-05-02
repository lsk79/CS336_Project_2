##Shreya -->

CREATE TABLE application (
    id SERIAL PRIMARY KEY,
    applicant_income_000s NUMERIC,
    loan_amount_000s NUMERIC,
    denial_reason_1 INT,
    denial_reason_2 INT,
    denial_reason_3 INT,
    action_taken INT
);

CREATE TABLE denialreason1 (
    denial_reason_1 INT PRIMARY KEY,
    denial_reason_name_1 VARCHAR(255)
);

CREATE TABLE denialreason2 (
    denial_reason_2 INT PRIMARY KEY,
    denial_reason_name_2 VARCHAR(255)
);

CREATE TABLE denialreason3 (
    denial_reason_3 INT PRIMARY KEY,
    denial_reason_name_3 VARCHAR(255)
);

CREATE TABLE actiontaken (
    action_taken INT PRIMARY KEY,
    action_taken_name VARCHAR(255)
);

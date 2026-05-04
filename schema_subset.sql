## Angela

CREATE TABLE Agency 
  (
    agency_code INT PRIMARY KEY,
    agency_name VARCHAR(255)
  );

CREATE TABLE ActionTaken
  (
    action_taken INT PRIMARY KEY,
    action_taken_name VARCHAR(255)
  );

INSERT INTO Agency (agency_code, agency_name) VALUES (1, 'OCC'), (3, 'FDIC'), (5, 'NCUA');
INSERT INTO ActionTaken (action_taken, action_taken_name) VALUES (1, 'Loan originated'), (3, 'Application denied');
  
CREATE TABLE Location
  (
    location_id SERIAL PRIMARY KEY,
    county_code INT,
    msamd INT,
    state_code INT,
    census_tract_number VARCHAR(20),
    population INT,
    hud_median_family_income INT,
  );

INSERT INTO location (location_id, county_code, state_code, population) VALUES (1, 35, 34, 5000);

CREATE TABLE Application_Denial_Reason
  (
    application_id INT,
    denial_reason_id INT,
    reason_number INT,
    PRIMARY KEY (application_id, reason_number)
  );

CREATE TABLE Application_Race
(
    application_id INT,
    race_id INT,
    race_number INT,
    PRIMARY KEY (application_id, race_number)
);

CREATE TABLE Co_application_Race
(
    application_id INT,
    race_id INT,
    race_number INT,
    PRIMARY KEY (application_id, race_number)
);

INSERT INTO Application_Denial_Reason (application_id, denial_reason_id, reason_number) VALUES (101, 1, 1);
INSERT INTO Application_Race (appplication_id, race_id, race_number) VALUES (101, 5, 1);

CREATE TABLE Normalized_App(
  id INT PRIMARY KEY,
  as_of_year INT,
  loan_amount_000s INT,
  applicant_income_000s INT,
  agency_code INT,
  action_taken INT,
  applicant_sex INT,
  denial_reason_1 INT,
  respondent_id VARCHAR (20),
  loan_type INT,
  location_id INT,
  FOREIGN KEY (location_id) REFERENCES Location(loction_id),
  FOREIGN KEY (agency_code) REFERENCES Agency(agency_code),
  FOREIGN KEY (action_taken) REFERENCES ActionTaken(action_taken)
);

INSERT INTO Normalized_App (id, loan_amount_000s, applicant_income_000s, agency_code, action_taken, location_id)
VALUES (101, 250, 85, 3, 3, 1);

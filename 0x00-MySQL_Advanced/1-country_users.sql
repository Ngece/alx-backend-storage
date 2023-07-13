-- Desc: Create a table of users with unique email addresses, id's, names and a country column that has values (US, CO, TN).

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL VALUES ('US', 'CO', 'TN'),
    country.default = 'US'
);
--Desc: creates a trigger that resets the attribute valid_email whenever the email is updated

DELIMITER $$
CREATE TRIGGER valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    SET NEW.valid_email = 0;
END$$

DELIMITER ;


--Desc: creates a trigger that resets the attribute valid_email whenever the email is updated

DELIMITER //

CREATE TRIGGER update_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END //

DELIMITER ;

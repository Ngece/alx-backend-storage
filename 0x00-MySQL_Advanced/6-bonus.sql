-- Desc: cfreates a stored procedure that adds a new correction for student

DELIMITER $$
CREATE PROCEDURE Add_Bonus(IN user_id INT, IN project_name VARCHAR(255), )IN score FLOAT)
BEGIN
    INSERT INTO corrections (user_id, project_name, score)
    VALUES (user_id, project_name, score);
END$$

DELIMITER ;
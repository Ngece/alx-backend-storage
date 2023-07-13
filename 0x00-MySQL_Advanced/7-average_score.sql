--Desc: creates a stored procedure that computesz and stores the average score for a student

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE average_score FLOAT;
    SELECT AVG(score) INTO average_score FROM corrections WHERE user_id = user_id;
    INSERT INTO average_scores (user_id, average_score) VALUES (user_id, average_score);
END$$

DELIMITER ;
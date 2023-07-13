-- Desc: creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE user_id INT;
  DECLARE project_id INT;
  DECLARE score FLOAT;
  DECLARE weighted_score FLOAT;
  DECLARE avg_weighted_score FLOAT;
  DECLARE done INT DEFAULT FALSE;
  DECLARE cur CURSOR FOR SELECT user_id, project_id, score FROM corrections;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  OPEN cur;
  read_loop: LOOP
    FETCH cur INTO user_id, project_id, score;
    IF done THEN
      LEAVE read_loop;
    END IF;
    SET weighted_score = (SELECT weight FROM projects WHERE id = project_id) * score;
    UPDATE corrections SET weighted_score = weighted_score WHERE user_id = user_id AND project_id = project_id;
  END LOOP;
  CLOSE cur;
  SET avg_weighted_score = (SELECT AVG(weighted_score) FROM corrections);
  UPDATE users SET average_weighted_score = avg_weighted_score;
END;

DELIMITER ;
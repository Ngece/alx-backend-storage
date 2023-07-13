-- Desc: creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER &&

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_score FLOAT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Loop through all users
    user_loop: LOOP
        -- Fetch the next user id
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Reset variables for each user
        SET total_score = 0;
        SET total_weight = 0;
        SET avg_score = 0;

        -- Compute the total weighted score for the user
        SELECT SUM(c.score * p.weight) INTO total_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Compute the total weight
        SELECT SUM(weight) INTO total_weight
        FROM projects;

        -- Compute the average weighted score
        IF total_weight > 0 THEN
            SET avg_score = total_score / total_weight;
        END IF;

        -- Update the average_score column for the user
        UPDATE users
        SET average_score = avg_score
        WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END &&

DELIMITER ;

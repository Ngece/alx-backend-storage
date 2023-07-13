--Desc: creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0.

DELIMITER $$
CREATE FUNCTION SafeDiv(IN numerator FLOAT, IN denominator FLOAT)
RETURNS FLOAT
BEGIN
    IF denominator = 0 THEN
        RETURN 0;
    ELSE
        RETURN numerator / denominator;
    END IF;
END$$

DELIMITER ;
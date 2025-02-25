SELECT
    YEAR(STRPTIME(StartDate, '%m/%d/%Y')) AS start_year,
    YEAR(STRPTIME(EndDate, '%m/%d/%Y')) AS end_year,
    *
FROM 
    employees
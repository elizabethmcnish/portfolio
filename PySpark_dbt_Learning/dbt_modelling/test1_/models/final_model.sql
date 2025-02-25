SELECT 
    d.year,
    COUNT(e.EmployeeKey) AS no_of_employees,
    MIN(e.DepartmentName) AS department

FROM  
    dates_model d
LEFT JOIN   
    employees_model e
ON 
    (e.start_year <= d.year)
    AND (e.end_year > d.year OR e.end_year is null) 
GROUP BY 
    d.year, e.DepartmentName
ORDER BY 
    d.year ASC 



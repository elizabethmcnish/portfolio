import duckdb


def clean_data_with_sql():

    return duckdb.query(
        """
        WITH dates_cte AS (
                SELECT 
                    CalendarYear AS year
                FROM 
                    dates_df
                GROUP BY
                    CalendarYear
            ),

            employee_cte AS (
                SELECT
                    YEAR(STRPTIME(StartDate, '%m/%d/%Y')) AS start_year,
                    YEAR(STRPTIME(EndDate, '%m/%d/%Y')) AS end_year,
                    *
                FROM 
                    employees_df
            )

            SELECT 
                d.year,
                COUNT(e.EmployeeKey) AS no_of_employees,
                MIN(e.DepartmentName) AS department
            FROM 
                dates_cte d 
            LEFT JOIN 
                employee_cte e
            ON 
                (e.start_year <= d.year)
                AND (e.end_year > d.year OR e.end_year is null)
            GROUP BY 
                d.year, e.DepartmentName
            ORDER BY
                d.year ASC 
        """
    ).to_df()


# Run "python sql_modelling.py" in terminal and see what happens!

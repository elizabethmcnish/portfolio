import duckdb
import datetime as datetime

DBT_PROJECT_PATH = "dbt_modelling/test1_/dev.duckdb"


def clean_data_with_sql(dates_df, employees_df):
    start_time = datetime.datetime.now()

    df = duckdb.query(
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
            d.year ASC, e.DepartmentName ASC
    """
    ).df()

    end_time = datetime.datetime.now()

    return df, (end_time - start_time).total_seconds()


def load_data_from_duckdb():
    start_time = datetime.datetime.now()

    con = duckdb.connect(DBT_PROJECT_PATH)
    df = con.execute("SELECT * FROM final_model").fetchdf()

    end_time = datetime.datetime.now()

    return df, (end_time - start_time).total_seconds()

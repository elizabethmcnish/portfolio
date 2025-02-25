# portfolio
Portfolio of independent projects

1.** ML Dashboard**
    * This tool has been created for modelling accident severity based on datasets on UK road accidents
        * This data is currently just for 2023, but will be expanded to include the past 5 years
    * To run this tool locally on your machine, run the following command in your terminal:

   Initialise and activate virtual environment:

   ```python
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Install dependencies:
   ```python
   pip install -r requirements.txt
   ```

   Run app in Streamlit:
   ```python
   streamlit run App.py
   ```

   * Feel free to play around with the input variables (features), and try to optimise the model as much as possible!


3. **dbt_modelling**
   * This directory contains a streamlit-based app which **compares the performance of dbt-based models and single SQL queries**
   * The dbt-based models are being used in conjunction with **duckdb**
  
   BEFORE RUNNING THE APP:
   * Before running the streamlit app, you will need to build you dbt-duckdb data pipelines
   * For more information on the dbt-duckdb pipelines, see this link: https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup.
   * To build dbt-duckdb pipelines, follow the following steps:


   Initialise and activate virtual environment:

   ```python
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Install dependencies:
      
    ```python
    pip install -r requirements.txt
    ```

   Build your dbt models, run the following inside the "test1_" dir:

   ```python
    dbt build
    ```
   * This command will both load your seed files into duckdb, and build your models.
   * If you would like to separate out these steps, run the following commands instead:

   ```python
    dbt seed
    ```

   ```python
    dbt run
    ```

    Run app in Streamlit inside the "dbt-modelling" dir:

    ```python
    streamlit run App.py
    ```



   p.s. As a bonus, you can use the following command to interact with the dbt-duckdb tables directly inside the CLI:

      ```python
      duckcli dev.duckdb
      ```
            


      

      

   



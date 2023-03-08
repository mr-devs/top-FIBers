# data-loader
The data-loader is used to read the parquet files generated and feed the data in to database in every month.

---

### See below for the data-loader configuration.

> IMPORTANT:
> 1. **Must be in the repo root (`cd /home/data/apps/topfibers/repo/data-loader`) or scripts will break.**
> 2. **Must have database configured in order to feed to the database.**
> 3. **The data files should be included in the /home/data/apps/topfibers/repo/data/derived/fib_results/twitter/year_month
> and /home/data/apps/topfibers/repo/data/derived/fib_results/facebook/year_month folders**
>

1.**Database Configuration**

1. **The top fibers database is in LISA. So used ssh tunneling to access the database once the program runs and it makes connection with LISA to feed the data. To have it,
run this bash script file `/home/data/apps/topfibers/repo/data-loader/run_data_loader.sh`**
2. **To change the database configuration in here `/home/data/apps/topfibers/repo/data-loader/conf/fibindex.conf`**


2.**Database Tables**

1.**Used following tables to insert the data that is read from parquet files generated.**
    
1. **reports**
2. **fib_indices**
3. **posts**
4. **reshares**

2.**The database_script is in here `/home/data/apps/topfibers/repo/data-loader/database_script/create.sql` 

3.**Run the script**
1. To run the data-loader script, need to call `/home/data/apps/topfibers/repo/data-loader/run_data_loader.sh` bash script. There will create a connection with the LISA to access the database by ssh tunneling.
2. The `load_current_data` in the `/home/data/apps/topfibers/repo/data-loader/server.py` file will search the existing month and get the current month and read the parquet file for the certain month.


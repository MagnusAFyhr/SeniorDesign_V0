# Running the program
1. Clone or download the github repository
2. Download Python 3.7
3. Download the necessary libraries from the "requirements.txt" file
+ If you are having trouble downloading talib then see this -->
<a href="https://blog.quantinsti.com/install-ta-lib-python/#windows">installation tutorial</a>
4. You should now be able to run the main.py
+ The default code in the main method should run correctly

## Running your own simulations
There are 11 datasets provided in this project. They all are in .csv format with OHLCV headers.
The datasets provided were taken from yahoo finance and additional datasets can be added.

### Adding your own datasets
1. Put the dataset in the /data/raw/ directory in the project
2. Edit /analysis/parameters.py "SUPP_TICKERS" array to include the new csv name
3. Edit the main.py to change the experement
+ Multiple tickers can be added in the "tickers" array in the experement function call
+ The sample_size can be increased to get more data points
4. Run the main.py once
+ This run will generate a new version of the dataset with additional information and store the data in /data/pure/
5. Run the main.py a second time and the experement should begin
+ The output is stored in the /results/ directory
# Running the program
1. Clone or download the github repository
2. Download Python 3.7
3. Dosadjasd
https://blog.quantinsti.com/install-ta-lib-python/#windows
1. Make sure that you have Python 3.7, earlier versions won't work
2. Run the pip command on "requirements.txt" to install the necessary libraries
3. Add a csv with OHLCV headers to the /data/raw folder
4. Edit main.py tickers array to run the program on a csv EX: "MSFT"
5. The first run of main.py generates the pure csv, the second run will start the simulation


python-dateutil>=2.8.1
six>=1.14.0

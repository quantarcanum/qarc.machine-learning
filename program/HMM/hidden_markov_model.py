import numpy as np
from pyhhmm.gaussian import GaussianHMM # hmmlearn - does the same thing but does not work on M1 mac
#from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt
from pandas_datareader.data import DataReader
import yfinance as yf


class HiddenMarkovModels():

    def __init__(self, dataframe):
        """
        Hidden Markov Model
        """
        self.full_data = dataframe
        self.data = self.full_data[["Open", "High", "Low", "Close"]]
        #print(self.data)

        #self.X_train = self.data[["returns", "bar_range"]]
        #print(self.X_train.head())

        #self.train_model()

        #self._wiz_test()
        self._my_data_test()


    def train_model(self):
        #model = GaussianHMM(n_states=2, covariance_type="full", n_emissions=2)
        model = GaussianHMM(n_components=2, covariance_type='full', n_iter=100).fit(self.X_train)
        #model.train([np.array(self.X_train.values)])
        print(model.score(self.X_train))
        hiddenStates = model.predict(self.X_train)
        print(hiddenStates)

    def _my_data_test(self):
       
        # Add Retruns and Range
        df = self.data.copy()
        df["Returns"] = (df["Close"] / df["Close"].shift(1)) - 1
        df["Range"] = (df["High"] / df["Low"]) - 1
        df.dropna(inplace = True)
        df.head()

        # Structure Data
        X_train = df[["Returns", "Range"]].values
        print("got the here 0")
        print(X_train)

        # Train Model
        model = GaussianHMM(n_states=4, covariance_type="tied", n_emissions=2)
        res = model.train([X_train]) #train takes an array, so we're casting X_train list into one np.array(X_train.values)
        #model.train([np.array(X_train.values)]) #train takes an array, so we're casting X_train list into one np.array(X_train.values)
        print(f"got the here 1 {res}")
        # Check results
        #hidden_states = model.predict([X_train.values])[0]
        hidden_states = model.predict([X_train])[0]
        print("got the here 2")
        print(hidden_states[:1000])
        print("got the here 3")
        #print(model.means)
        #print(model.covars)
        #print(dir(model))

        # Structure the prices for plotting (split data into 4 arrays (for each state))
        i = 0
        labels_0 = []
        labels_1 = []
        labels_2 = []
        labels_3 = []
        prices = df["Close"].values.astype(float) # ensuring prices come as float
        print("Correct number of rows: ", len(prices) == len(hidden_states)) # ensure the len of prices matches the one in hidden_states
        for s in hidden_states:
            if s == 0:
                labels_0.append(prices[i])
                labels_1.append(float("nan"))
                labels_2.append(float("nan"))
                labels_3.append(float("nan"))
            if s == 1:
                labels_0.append(float("nan"))
                labels_1.append(prices[i])
                labels_2.append(float("nan"))
                labels_3.append(float("nan"))
            if s == 2:
                labels_0.append(float("nan"))
                labels_1.append(float("nan"))
                labels_2.append(prices[i])
                labels_3.append(float("nan"))
            if s == 3:
                labels_0.append(float("nan"))
                labels_1.append(float("nan"))
                labels_2.append(float("nan"))
                labels_3.append(prices[i])
                
            i +=1

        # Plot all 4 arrays to compile the chart
        fig = plt.figure(figsize=(30, 18))
        plt.plot(labels_0, color="green")
        plt.plot(labels_1, color="red")
        plt.plot(labels_2, color="black")
        plt.plot(labels_3, color="orange")
        plt.show()

    def _wiz_test(sefl):
        # Data Extraction
        start_date = "2017-01-01"
        end_date = "2023-01-02"
        symbol = "SPY"
        dataSource = "yahoo"
        #df = DataReader(name=symbol, data_source=dataSource, start=start_date, end=end_date)
        data = yf.download(symbol, start_date, end_date)
        data = data[["Open", "High", "Low", "Close", "Volume"]]

        # Add Retruns and Range
        df = data.copy()
        df["Returns"] = (df["Close"] / df["Close"].shift(1)) - 1
        df["Range"] = (df["High"] / df["Low"]) - 1
        df.dropna(inplace = True)
        df.head()

        # Structure Data
        X_train = df[["Returns", "Range"]]
        X_train.head()

        # Train Model
        model = GaussianHMM(n_states=4, covariance_type="full", n_emissions=2)
        model.train([np.array(X_train.values)]) #train takes an array, so we're casting X_train list into one np.array(X_train.values)

        # Check results
        hidden_states = model.predict([X_train.values])[0]
        print(hidden_states[:500])
        print(model.means)
        print(model.covars)
        #print(dir(model))

        # Structure the prices for plotting (split data into 4 arrays (for each state))
        i = 0
        labels_0 = []
        labels_1 = []
        labels_2 = []
        labels_3 = []
        prices = df["Close"].values.astype(float) # ensuring prices come as float
        print("Correct number of rows: ", len(prices) == len(hidden_states)) # ensure the len of prices matches the one in hidden_states
        for s in hidden_states:
            if s == 0:
                labels_0.append(prices[i])
                labels_1.append(float("nan"))
                labels_2.append(float("nan"))
                labels_3.append(float("nan"))
            if s == 1:
                labels_0.append(float("nan"))
                labels_1.append(prices[i])
                labels_2.append(float("nan"))
                labels_3.append(float("nan"))
            if s == 2:
                labels_0.append(float("nan"))
                labels_1.append(float("nan"))
                labels_2.append(prices[i])
                labels_3.append(float("nan"))
            if s == 3:
                labels_0.append(float("nan"))
                labels_1.append(float("nan"))
                labels_2.append(float("nan"))
                labels_3.append(prices[i])
                
            i +=1

        # Plot all 4 arrays to compile the chart
        fig = plt.figure(figsize=(18, 12))
        plt.plot(labels_0, color="green")
        plt.plot(labels_1, color="red")
        plt.plot(labels_2, color="black")
        plt.plot(labels_3, color="orange")
        plt.show()
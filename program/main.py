import data.bar_repository as br
import data.bar_data_preprocessing as bdm
import ML.feature_engineering as ml
import ML.market_efficiency as mef
import ML.dynamic_hurst as dh
import HMM.hidden_markov_model as hmm
import XGBOOST.wiz as wizX
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    print("Hello ML!")

    try:
          
        trbar_repo = br.BarRepository()
        df_raw = trbar_repo.get_bar_dataframe(normalized = False)
        # #print(df_raw.info())
        print(f"Data pull succesful. #Rows: {len(df_raw.index)}")

        # df_raw[~df_raw.index.duplicated()]
        # print(f"Unique. #Rows: {len(df_raw.index)}")

        data_manipulation = bdm.BarDataPreprocessing(df_raw)
        df = data_manipulation.get_dataframe()
        # print(df.info())
        # #print(df.tail(3))
        # print("Data manipulation succesful.")

        # df_computed = data_manipulation.get_computed_dataframe()
        # #print(df_computed.info())
        # #print(df_computed.tail(3))
        # print("Data computation succesful.")

        # featureEngineering = ml.FeatureEngineering(df_computed)
        # df_engineered = featureEngineering.get_engineered_dataframe()
        # print("Feature engineering succesful.")
        # print(df_engineered.head(5))

        # move this out in a charting class
        #fig = plt.figure(figsize=(15,8))
        #plt.plot(df_engineered["Close"].values)
        #plt.plot(df_engineered["normal_returns_cumsum"].values)
        #plt.show()

        # marketEfficiency = mef.MarketEfficiency()
        # print("\n---Perform Runs Test for randomness: ")
        # marketEfficiency.runs_test(df_engineered["normal_returns_cumsum"].values)
        # print("\n---Perform BSD Test for chaos and nonlinearity: ")
        # marketEfficiency.bds_test(df_engineered["normal_returns_cumsum"].values)
        # print("\n---Perform AD Fuller Test for stationarity: ")
        # marketEfficiency.adfuller_test(df_engineered["normal_returns_cumsum"].values)
        # print("\n---Perform Hurst Test for market state identification: ")
        # hurst_results = dh.dynamic_hurst_component(df_engineered["normal_returns_cumsum"].values)
        # print(len(hurst_results[0]))


        # hiddenMarkovModel = hmm.HiddenMarkovModels(df_engineered)
        #hiddenMarkovModel = hmm.HiddenMarkovModels(df)

        wizz = wizX.WizXGBoost(df)


    except Exception as ex:
        print(ex)
        exit(1)



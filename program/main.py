import data.bar_repository as br
import data.bar_data_manipulation as bdm
import ML.feature_engineering as ml

if __name__ == "__main__":
    print("Hello ML!")

    try:
          
        trbar_repo = br.BarRepository()
        df_raw = trbar_repo.get_bar_dataframe(normalized = False)
        #print(df_raw.info())
        print(f"Data pull succesful. #Rows: {len(df_raw.index)}")

        #df_raw[~df_raw.index.duplicated()]
        #print(f"Unique. #Rows: {len(df_raw.index)}")

        data_manipulation = bdm.BarDataManipulation(df_raw)
        df = data_manipulation.get_dataframe()
        #print(df.info())
        #print(df.tail(3))
        print("Data manipulation succesful.")

        df_computed = data_manipulation.get_computed_dataframe()
        #print(df_computed.info())
        #print(df_computed.tail(3))
        print("Data computation succesful.")

        featureEngineering = ml.FeatureEngineering(df_computed)
        df_engineered = featureEngineering.get_engineered_dataframe()
        print("Feature engineering succesful.")
        print(df_engineered.head(5))

    except Exception as ex:
        print(ex)
        exit(1)
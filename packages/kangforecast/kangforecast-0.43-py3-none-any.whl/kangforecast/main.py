from kangforecast.m1load import m1load
from kangforecast.m2process import m2process
from kangforecast.m3show import m3show

def main():
    df = m1load("../data/testdata.csv")
    processed_df = m2process(df)
    m3show(processed_df)

if __name__ == "__main__":
    main()




# from kangforecast.data_loader import load_data
# from kangforecast.data_analysis import analyze

# def main():
#     dataframe = load_data("data/testdata.csv")
#     result = analyze(dataframe)
#     print(result)

# if __name__ == "__main__":
#     main()

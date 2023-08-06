

# In main.py
from kangforecast.m1load import m1load
from kangforecast.m2process import m2process
from kangforecast.m3show import m3show

def main():
    print("Starting the process...\n")

    print("m1: Loading data from ../data/testdata.csv...")
    df = m1load("../data/testdata.csv")
    print("m1: Data loaded successfully.\n")
    
    print("m2: Processing data...")
    processed_df = m2process(df)
    print("m2: Data processing complete.\n")
    
    print("m3: Displaying processed data...")
    print("    ", end="\n")
    m3show(processed_df)
    print("    ", end="\n")
    print("m3: Data displayed successfully.\n")

    print("Process complete!")

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

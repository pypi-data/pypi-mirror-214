from kangforecast.data_loader import load_data
from kangforecast.data_analysis import analyze

def main():
    dataframe = load_data("data/testdata.csv")
    result = analyze(dataframe)
    print(result)

if __name__ == "__main__":
    main()

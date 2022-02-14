import argparse
import os
#import csv
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def main(project):
    defects = os.path.join("..", "data", "input", "jira_records.csv")
    merges = os.path.join("..", "data", "input", "vcs_records.csv")
    outfile = os.path.join("..", "data", "output", f"{project}_plot.png")

    df_defects = pd.read_csv(defects, sep=',')#, parse_dates=['created'])
    df_defects['created'] = pd.to_datetime(df_defects['created'], utc=True)

    df_merges = pd.read_csv(merges, sep=',')#, parse_dates=['author_date'])
    df_merges['author_date'] = pd.to_datetime(df_merges['author_date'], utc=True)

    df_defects = df_defects.groupby(pd.Grouper(freq='W', key='created')).size()
    df_merges = df_merges.groupby(pd.Grouper(freq='W', key='author_date')).size()

    common_weeks = df_defects.index.intersection(df_merges.index)
    df_merges = df_merges[common_weeks]
    df_defects = df_defects[common_weeks]

    x_data = df_merges.values
    y_data = df_defects.values

    #print(x_data)
    #print(y_data)

    print("Plotting data...")
    rho, p = stats.spearmanr(x_data, y_data)
    plt.scatter(x_data, y_data)
    plt.title(f"{project}, rho:{rho:.2f}, p:{p:.2f}")
    plt.xlabel("merges per week")
    plt.ylabel("defects per week")
    print(f"Saving plot as {outfile}")
    plt.savefig(outfile)

    #print(r, p)

if __name__ == "__main__":
    #TODO read args from stdin
    main("camel")

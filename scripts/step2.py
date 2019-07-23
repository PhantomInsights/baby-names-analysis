"""
Functions used to generate the insights and plots from the article.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Those parameters generate plots with a mauve color.
sns.set(style="ticks",
        rc={
            "figure.figsize": [12, 7],
            "text.color": "white",
            "axes.labelcolor": "white",
            "axes.edgecolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "axes.facecolor": "#443941",
            "figure.facecolor": "#443941"}
        )


def get_essentials(df):
    """Gets total counts by gender.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be analyzed.

    """

    # Top 5 rows.
    print(df.head())

    # Bottom 5 rows.
    print(df.tail())

    # Unique names combined.
    print(df["name"].nunique())

    # Unique names Male.
    print(df[df["gender"] == "M"]["name"].nunique())

    # Unique names Female.
    print(df[df["gender"] == "F"]["name"].nunique())

    # Unique names gender neutral.
    both_df = df.pivot_table(
        index="name", columns="gender", values="count", aggfunc=np.sum).dropna()

    print(both_df.index.nunique())


def totals_by_year(df):
    """Gets total counts by year.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be analyzed.

    """

    both_df = df.groupby("year").sum()
    male_df = df[df["gender"] == "M"].groupby("year").sum()
    female_df = df[df["gender"] == "F"].groupby("year").sum()

    print("Both Min:", both_df.min()["count"], "-", both_df.idxmin()["count"])
    print("Both Max:", both_df.max()["count"], "-", both_df.idxmax()["count"])
    print("Male Min:", male_df.min()["count"], "-", male_df.idxmin()["count"])
    print("Male Max:", male_df.max()["count"], "-", male_df.idxmax()["count"])
    print("Female Min:", female_df.min()[
          "count"], "-", female_df.idxmin()["count"])
    print("Female Max:", female_df.max()[
          "count"], "-", female_df.idxmax()["count"])


def get_top_10(df):
    """Gets the top 10 most used male and female names.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be analyzed.

    """

    # We create a new dataframe with only male names and sum all their counts.
    # Then we sort it in descending order.
    male_df = df[df["gender"] == "M"][["name", "count"]].groupby(
        "name").sum().sort_values("count", ascending=False)

    print(male_df.head(10))

    # We create a new dataframe with only female names and sum all their counts.
    # Then we sort it in descending order.
    female_df = df[df["gender"] == "F"][["name", "count"]].groupby(
        "name").sum().sort_values("count", ascending=False)

    print(female_df.head(10))


def get_top_20_gender_neutral(df):
    """Gets the top 20 most used gender neutral names.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be analyzed.

    """

    # We pivot the dataframe so the names will be the index and the genders will be the columns.
    df = df.pivot_table(index="name", columns="gender",
                        values="count", aggfunc=np.sum).dropna()

    # Limit to only names with at least 50,000 records on both genders.
    df = df[(df["M"] >= 50000) & (df["F"] >= 50000)]
    print(df.head(20))


def plot_counts_by_year(df):
    """Plots the year counts by male, female and combined.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be plotted.

    """

    # We create new dataframes for male, female and combined.
    both_df = df.groupby("year").sum()
    male_df = df[df["gender"] == "M"].groupby("year").sum()
    female_df = df[df["gender"] == "F"].groupby("year").sum()

    # We plot our dataframes directly.
    # The x-axis will be the index and the y-axis will be the total counts.
    plt.plot(both_df, label="Both", color="yellow")
    plt.plot(male_df, label="Male", color="lightblue")
    plt.plot(female_df, label="Female", color="pink")

    # We make our yticks in steps of 50,000.
    # First we format the numbers for the labels.
    # Then we use the actual numbers as the steps.
    yticks_labels = ["{:,}".format(i) for i in range(0, 4500000+1, 500000)]
    plt.yticks(np.arange(0, 4500000+1, 500000), yticks_labels)

    # Final customizations.
    plt.legend()
    plt.grid(False)
    plt.xlabel("Year")
    plt.ylabel("Records Count")
    plt.title("Records per Year")
    plt.savefig("total_by_year.png", facecolor="#443941")


def plot_popular_names_growth(df):
    """Plots the most popular names and how they have grown trough the years.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be plotted.

    """

    # We first pivot the dataframe to merge values from male and female and
    # pivot the table so the names are our index and the years are our columns.
    # We also fill missing values with zeroes.
    pivoted_df = df.pivot_table(
        index="name", columns="year", values="count", aggfunc=np.sum).fillna(0)

    # Then we calculate the percentage of each name by year.
    percentage_df = pivoted_df / pivoted_df.sum() * 100

    # We add a new column to store the cumulative percentages sum.
    percentage_df["total"] = percentage_df.sum(axis=1)

    # We sort the dataframe to check which are the top values and slice it.
    # After that we drop the 'total' column since it won't be used anymore.
    sorted_df = percentage_df.sort_values(
        by="total", ascending=False).drop("total", axis=1)[0:10]

    # We flip the axes so we can plot the data more easily.
    transposed_df = sorted_df.transpose()

    # We plot each name individually by using the column name as the label and Y-axis.
    for name in transposed_df.columns.tolist():
        plt.plot(transposed_df.index, transposed_df[name], label=name)

    # We set our yticks in steps of 0.5.
    yticks_labels = ["{}%".format(i) for i in np.arange(0, 5.5, 0.5)]
    plt.yticks(np.arange(0, 5.5, 0.5), yticks_labels)

    # Final customizations.
    plt.legend()
    plt.grid(False)
    plt.xlabel("Year")
    plt.ylabel("Percentage by Year")
    plt.title("Top 10 Names Growth")
    plt.savefig("most_popular_growth.png", facecolor="#443941")


def plot_top_10_trending(df):
    """Plots the most populare names and how they have grown trough the years.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be plotted.

    """

    # First we remove all records previous to 2008.
    filtered_df = df[df["year"] >= 2008]
    
    # Then we merge values from male and female and pivot the table
    # so the names are our index and the years are our columns.
    # We also fill missing values with zeroes.
    pivoted_df = filtered_df.pivot_table(
        index="name", columns="year", values="count", aggfunc=np.sum).fillna(0)

    # Then we calculate the percentage of each name by year.
    percentage_df = pivoted_df / pivoted_df.sum() * 100

    # We add a new column to store the cumulative percentages sum.
    percentage_df["total"] = percentage_df.sum(axis=1)

    # We sort the dataframe to check which are the top values and slice it.
    # After that we drop the 'total' column since it won't be used anymore.
    sorted_df = percentage_df.sort_values(
        by="total", ascending=False).drop("total", axis=1)[0:10]

    # We flip the axes so we can plot the dataframe more easily.
    transposed_df = sorted_df.transpose()

    # We plot each name individually by using the column name as the label and Y-axis.
    for name in transposed_df.columns.tolist():
        plt.plot(transposed_df.index, transposed_df[name], label=name)

    # We set our yticks in steps of 0.05%.
    yticks_labels = ["{:.2f}%".format(i) for i in np.arange(0.3, 0.7, 0.05)]
    plt.yticks(np.arange(0.3, 0.7, 0.05), yticks_labels)

    # We set our xticks in steps of 1, from 2009 to 2018.
    xticks_labels = ["{}".format(i) for i in range(2008, 2618+1, 1)]
    plt.xticks(np.arange(2008, 2018+1, 1), xticks_labels)

    # Final customizations.
    plt.legend()
    plt.grid(False)
    plt.xlabel("Year")
    plt.ylabel("Percentage by Year")
    plt.title("Top 10 Trending Names")
    plt.savefig("trending_names.png", facecolor="#443941")


if __name__ == "__main__":

    main_df = pd.read_csv("data.csv")

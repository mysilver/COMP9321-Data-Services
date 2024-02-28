#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Third-party libraries
# NOTE: You may **only** use the following third-party libraries:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from thefuzz import fuzz
from thefuzz import process
# NOTE: It isn't necessary to use all of these to complete the assignment, 
# but you are free to do so, should you choose.

# Standard libraries
# NOTE: You may use **any** of the Python 3.11 or Python 3.12 standard libraries:
# https://docs.python.org/3.11/library/index.html
# https://docs.python.org/3.12/library/index.html
from pathlib import Path
# ... import your standard libraries here ...


######################################################
# NOTE: DO NOT MODIFY THE LINE BELOW ...
######################################################
studentid = Path(__file__).stem

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION BELOW ...
######################################################
def log(question, output_df, other):
    print(f"--------------- {question}----------------")

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


######################################################
# NOTE: YOU MAY ADD ANY HELPER FUNCTIONS BELOW ...
######################################################



######################################################
# QUESTIONS TO COMPLETE BELOW ...
######################################################

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_1(jobs_csv):
    """Read the data science jobs CSV file into a DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_csv (str): Path to the jobs CSV file.

    Returns:
        DataFrame: The jobs DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 1", output_df=df, other=df.shape)
    return df



######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_2(cost_csv, cost_url):
    """Read the cost of living CSV into a DataFrame.  If the CSV file does not 
    exist, scrape it from the specified URL and save it to the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the cost of living CSV file.
        cost_url (str): URL of the cost of living page.

    Returns:
        DataFrame: The cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 2", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_3(currency_csv, currency_url):
    """Read the currency conversion rates CSV into a DataFrame.  If the CSV 
    file does not exist, scrape it from the specified URL and save it to 
    the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the currency conversion rates CSV file.
        cost_url (str): URL of the currency conversion rates page.

    Returns:
        DataFrame: The currency conversion rates DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 3", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_4(country_csv, country_url):
    """Read the country codes CSV into a DataFrame.  If the CSV file does not 
    exist, it will be scrape the data from the specified URL and save it to the 
    CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the country codes CSV file.
        cost_url (str): URL of the country codes page.

    Returns:
        DataFrame: The country codes DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 4", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_5(jobs_df):
    """Summarise some dimensions of the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The summary DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 5", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_6(jobs_df):
    """Add an experience rating column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The jobs DataFrame with the experience rating column added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 6", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_7(jobs_df, country_df):
    """Merge the jobs and country codes DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 6.
        country_df (DataFrame): The country codes DataFrame returned in 
                                question 4.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 7", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_8(jobs_df, currency_df):
    """Add an Australian dollar salary column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 7.
        currency_df (DataFrame): The currency conversion rates DataFrame 
                                 returned in question 3.

    Returns:
        DataFrame: The jobs DataFrame with the Australian dollar salary column
                   added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 8", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_9(cost_df):
    """Re-scale the cost of living DataFrame to be relative to Australia.

    See the assignment spec for more details.

    Args:
        cost_df (DataFrame): The cost of living DataFrame returned in question 2.

    Returns:
        DataFrame: The re-scaled cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    
    
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 9", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_10(jobs_df, cost_df):
    """Merge the jobs and cost of living DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 8.
        cost_df (DataFrame): The cost of living DataFrame returned in question 9.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################

    

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 10", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_11(jobs_df):
    """Create a pivot table of the average salary in AUD by country and 
    experience rating.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.

    Returns:
        DataFrame: The pivot table.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################



    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 11", output_df=None, other=df)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_12(jobs_df):
    """Create a visualisation of data science jobs to help inform a decision
    about where to live, based (minimally) on salary and cost of living.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################


    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    plt.savefig(f"{studentid}-Q12.png")


######################################################
# NOTE: DO NOT MODIFY THE MAIN FUNCTION BELOW ...
######################################################
if __name__ == "__main__":
    # data ingestion and cleaning
    df1 = question_1("ds_jobs.csv")
    df2 = question_2("cost_of_living.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/cost_of_living.html")
    df3 = question_3("exchange_rates.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/exchange_rates.html")
    df4 = question_4("country_codes.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/country_codes.html")

    # data exploration
    df5 = question_5(df1.copy(True))

    # data manipulation
    df6 = question_6(df1.copy(True))
    df7 = question_7(df6.copy(True), df4.copy(True))
    df8 = question_8(df7.copy(True), df3.copy(True))
    df9 = question_9(df2.copy(True))
    df10 = question_10(df8.copy(True), df9.copy(True))
    df11 = question_11(df10.copy(True))

    # data visualisation
    question_12(df10.copy(True))

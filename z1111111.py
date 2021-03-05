import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math

studentid = os.path.basename(sys.modules[__name__].__file__)


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


def question_1(exposure, countries):
    """
    :param exposure: the path for the exposure.csv file
    :param countries: the path for the Countries.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 2", output_df=df2[["avg_latitude", "avg_longitude"]], other=df2.shape)
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 3", output_df=df3[['distance_to_Wuhan']], other=df3.shape)
    return df3


def question_4(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 4", output_df=df4, other=df4.shape)
    return df4


def question_5(df2):
    """
    :param df2: the dataframe created in question 2
    :return: cities_lst
            Data Type: list
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 5", output_df=df5, other=df5.shape)
    return df5


def question_6(df2):
    """
    :param df2: the dataframe created in question 2
    :return: lst
            Data Type: list
            Please read the assignment specs to know how to create the output dataframe
    """
    cities_lst = []
    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 6", output_df=None, other=cities_lst)
    return lst


def question_7(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 7", output_df=df7, other=df7.shape)
    return df7


def question_8(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_9(df2):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_10(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    :param continents: the path for the Countries-Continents.csv file
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("exposure.csv", "Countries.csv")
    df2 = question_2(df1.copy(True))
    df3 = question_3(df2.copy(True))
    df4 = question_4(df2.copy(True), "Countries-Continents.csv")
    df5 = question_5(df2.copy(True))
    lst = question_6(df2.copy(True))
    df7 = question_7(df2.copy(True))
    question_8(df2.copy(True), "Countries-Continents.csv")
    question_9(df2.copy(True))
    question_10(df2.copy(True), "Countries-Continents.csv")

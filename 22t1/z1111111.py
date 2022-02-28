import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math
import re

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


def question_1(routes):
    """
    :param exposure: the path for the routes dataset
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 1", output_df=df1[["route_search_name", "start", "end"]], other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: dataframe df2
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 2", output_df=df2, other=df2.shape)
    return df2


def question_3(df1):
    """
    :param df2: the dataframe created in question 1
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 3", output_df=df3[['modified_transport_name'], ['transport_name']], other=df3.shape)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 4", output_df=df4[["transport-type", "routes"]], other=df4.shape)
    return df4


def question_5(df2, suburbs):
    """
    :param df2: the dataframe created in question 2
    :param suburbs : the path to dataset
    :return: df5
            Data Type: dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    # Your code goes here ...
    #################################################

    log("QUESTION 5", output_df=df5[["depots", "ratio"]], other=df5.shape)
    return df5


def question_6(suburbs):
    """
    :param suburbs : the path to dataset
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q6.png".format(studentid))




def question_7(df1,suburbs):
    """
    :param df1: the dataframe created in question 1
    :param suburbs : the path to dataset
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q7.png".format(studentid))


def question_8(df1):
    """
    :param df1: the dataframe created in question 1
    :param suburbs : the path to dataset
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    #################################################

    plt.savefig("{}-Q8.png".format(studentid))



if __name__ == "__main__":
    df1 = question_1("routes.csv")
    hub_list = question_2(df1.copy(True))
    df3 = question_3(df1.copy(True))
    df4 = question_4(df1.copy(True))
    df5 = question_5(df1.copy(True), "suburbs.csv")
    question_7(df1.copy(True), "suburbs.csv")
    question_7(df1.copy(True), "suburbs.csv")
    question_8(df1.copy(True))

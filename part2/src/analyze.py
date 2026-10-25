
"""Read Lorenz trajectories and detect orbit transitions."""

import argparse

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    spark = SparkSession.builder.appName("LorenzAnalysis").getOrCreate()

    df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(args.input)
        .withColumn("source_file", F.input_file_name())
        .withColumn(
            "trajectory_id",
            F.regexp_extract("source_file", r"trajectory_(\d+)\.csv", 1)
        )
        .withColumn(
            "orbit",
            F.when(F.col("x") + F.col("y") >= 0, 1).otherwise(-1)
        )
    )

    window = Window.partitionBy("trajectory_id").orderBy("time")

    df = df.withColumn("previous_orbit", F.lag("orbit").over(window))

    df = df.withColumn(
        "transition",
        F.when(
            F.col("previous_orbit").isNotNull()
            & (F.col("orbit") != F.col("previous_orbit")),
            1
        ).otherwise(0)
    )

    df.select(
        "trajectory_id", "time", "orbit",
        "previous_orbit", "transition"
    ).orderBy("trajectory_id", "time").show(30)

    spark.stop()


if __name__ == "__main__":
    main()

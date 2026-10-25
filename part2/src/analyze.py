
"""Analyze Lorenz trajectories with PySpark."""

import argparse

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, DoubleType


SCHEMA = StructType([
    StructField("time", DoubleType(), True),
    StructField("x", DoubleType(), True),
    StructField("y", DoubleType(), True),
    StructField("z", DoubleType(), True),
])


def analyze(spark, input_path):
    trajectories = (
        spark.read.option("header", True)
        .schema(SCHEMA)
        .csv(input_path)
        .withColumn("source_file", F.input_file_name())
        .withColumn(
            "trajectory_id",
            F.regexp_extract(
                "source_file", r"trajectory_(\d+)\.csv", 1
            ).cast("int"),
        )
        .withColumn(
            "orbit",
            F.when(F.col("x") + F.col("y") >= 0, 1).otherwise(-1)
        )
    )

    # Detect changes in the nearest orbit center.
    ordered = Window.partitionBy("trajectory_id").orderBy("time")

    with_transitions = (
        trajectories
        .withColumn(
            "previous_orbit",
            F.lag("orbit").over(ordered)
        )
        .withColumn(
            "transition",
            F.when(
                F.col("previous_orbit").isNotNull()
                & (F.col("orbit") != F.col("previous_orbit")),
                1,
            ).otherwise(0),
        )
    )

    # Assign an ID to each continuous orbit segment.
    running = ordered.rowsBetween(
        Window.unboundedPreceding,
        Window.currentRow
    )

    with_segments = with_transitions.withColumn(
        "segment_id",
        F.sum("transition").over(running)
    )

    # Count time samples in each segment.
    segments = (
        with_segments
        .groupBy("trajectory_id", "segment_id")
        .agg(F.count("*").alias("segment_length"))
    )

    # Compute statistics for each trajectory.
    statistics = (
        segments.groupBy("trajectory_id")
        .agg(
            F.avg("segment_length").alias("mean_length"),
            F.var_pop("segment_length").alias("variance"),
            F.count("*").alias("num_segments"),
            F.sum("segment_length").alias("total_points"),
        )
        .orderBy("mean_length", "trajectory_id")
    )

    return statistics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    spark = (
        SparkSession.builder
        .appName("LorenzOrbitStatistics")
        .getOrCreate()
    )

    try:
        statistics = analyze(spark, args.input)

        statistics.show(20, truncate=False)

        if args.output:
            (
                statistics.coalesce(1)
                .write.mode("overwrite")
                .option("header", True)
                .csv(args.output)
            )
            print(f"Saved statistics to {args.output}")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()

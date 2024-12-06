import argparse
import os
import pandas as pd


# TODO: add n cells and mean coverage
# TODO: filter sets?


def main(args):
    all_variants = pd.read_csv(args.variant_statistics, index_col="variant")

    if args.min_strand_correlation > 0:
        all_variants["pass_strand_correlation"] = all_variants[
            "strand_correlation"
        ].apply(lambda c: c >= args.min_strand_correlation)

    all_variants["pass_vmr"] = all_variants["vmr"].apply(lambda v: v >= args.min_vmr)

    if args.molecular_position_bias_threshold < 1:
        all_variants["pass_position_bias"] = all_variants[
            "alt_uniform_statistic"
        ].apply(lambda s: s <= args.molecular_position_bias_threshold)

    all_variants["pass_homoplasmic"] = all_variants["mean"].apply(
        lambda h: h <= args.homoplasmic_threshold
    )
    filter_columns = [c for c in all_variants.columns if c.startswith("pass")]

    all_variants["pass_filters"] = all_variants.apply(
        lambda row: all(row[col] for col in filter_columns), axis=1
    )
    all_variants.to_csv(args.variant_statistics)

    final_variants_statistics = all_variants[all_variants["pass_filters"]]
    final_variants_statistics.to_csv(
        os.path.join(args.outdir, "variant_statistics.csv")
    )
    final_variants_set = set(final_variants_statistics.index)

    heteroplasmy_matrix = pd.read_csv(
        args.variant_heteroplasmy_matrix, index_col="variant"
    )
    heteroplasmy_matrix = heteroplasmy_matrix[
        heteroplasmy_matrix.index.isin(final_variants_set)
    ]

    heteroplasmy_matrix.to_csv(os.path.join(args.outdir, "heteroplasmy_matrix.csv"))

    # TODO: other outputs? scanpy compatible?


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-variant-statistics",
        type=str,
        required=True,
        help="path to variant statistics CSV file",
    )
    parser.add_argument(
        "-variant-heteroplasmy-matrix",
        type=str,
        required=True,
        help="path to heteroplasmy matrix CSV file",
    )
    parser.add_argument(
        "-min-strand-correlation",
        type=float,
        required=True,
        help="Minimum correlation required between fwd and rev strands for a variant to be included",
    )
    parser.add_argument(
        "-min-vmr",
        type=float,
        required=True,
        help="Minimum heteroplasmy variance mean ratio (VMR) required for a variant to be included",
    )

    parser.add_argument(
        "-molecular-position-bias-threshold",
        type=float,
        required=True,
        help="Threshold for position bias KS test",
    )
    parser.add_argument(
        "-homoplasmic-threshold",
        type=float,
        required=True,
        help="Threshold for being considered homoplasmic, and not included in heteroplasmic variants",
    )
    parser.add_argument(
        "-mean-coverage",
        type=float,
        required=True,
        help="Threshold for being considered homoplasmic, and not included in heteroplasmic variants",
    )
    parser.add_argument(
        "-n-cells-over-5",
        type=float,
        required=True,
        help="Threshold for being considered homoplasmic, and not included in heteroplasmic variants",
    )

    parser.add_argument("-outdir", type=str, required=True, help="output directory")

    args = parser.parse_args()

    main(args)

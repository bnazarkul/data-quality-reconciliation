import pandas as pd

SOURCE_A = "source_a.csv"
SOURCE_B = "source_b.csv"
OUTPUT_FILE = "reconciliation_result.xlsx"


def load_data(file_path):
    df = pd.read_csv(file_path)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df


def find_duplicates(df):
    return df[df.duplicated(subset=["transaction_id"], keep=False)].copy()


def prepare_unique_data(df):
    return df.drop_duplicates(subset=["transaction_id"], keep="first").copy()


def reconcile_data(source_a, source_b):
    a_unique = prepare_unique_data(source_a)
    b_unique = prepare_unique_data(source_b)

    merged = a_unique.merge(
        b_unique,
        on="transaction_id",
        how="outer",
        suffixes=("_a", "_b"),
        indicator=True
    )

    only_in_a = merged[merged["_merge"] == "left_only"].copy()
    only_in_b = merged[merged["_merge"] == "right_only"].copy()

    matched = merged[merged["_merge"] == "both"].copy()

    discrepancies = matched[
        (matched["amount_a"] != matched["amount_b"])
        | (matched["status_a"] != matched["status_b"])
        | (matched["user_id_a"] != matched["user_id_b"])
        | (matched["transaction_date_a"] != matched["transaction_date_b"])
    ].copy()

    exact_matches = matched[
        (matched["amount_a"] == matched["amount_b"])
        & (matched["status_a"] == matched["status_b"])
        & (matched["user_id_a"] == matched["user_id_b"])
        & (matched["transaction_date_a"] == matched["transaction_date_b"])
    ].copy()

    return only_in_a, only_in_b, discrepancies, exact_matches


def build_summary(
    source_a,
    source_b,
    duplicates_a,
    duplicates_b,
    only_in_a,
    only_in_b,
    discrepancies,
    exact_matches
):
    summary = pd.DataFrame({
        "metric": [
            "Rows in Source A",
            "Rows in Source B",
            "Duplicate rows in Source A",
            "Duplicate rows in Source B",
            "Only in Source A",
            "Only in Source B",
            "Discrepancies",
            "Exact matches"
        ],
        "value": [
            len(source_a),
            len(source_b),
            len(duplicates_a),
            len(duplicates_b),
            len(only_in_a),
            len(only_in_b),
            len(discrepancies),
            len(exact_matches)
        ]
    })

    return summary


def save_results(
    summary,
    duplicates_a,
    duplicates_b,
    only_in_a,
    only_in_b,
    discrepancies,
    exact_matches
):
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        duplicates_a.to_excel(writer, sheet_name="Duplicates A", index=False)
        duplicates_b.to_excel(writer, sheet_name="Duplicates B", index=False)
        only_in_a.to_excel(writer, sheet_name="Only in A", index=False)
        only_in_b.to_excel(writer, sheet_name="Only in B", index=False)
        discrepancies.to_excel(writer, sheet_name="Discrepancies", index=False)
        exact_matches.to_excel(writer, sheet_name="Exact Matches", index=False)


def main():
    print("Loading data...")
    source_a = load_data(SOURCE_A)
    source_b = load_data(SOURCE_B)

    print("Checking duplicates...")
    duplicates_a = find_duplicates(source_a)
    duplicates_b = find_duplicates(source_b)

    print("Reconciling data...")
    only_in_a, only_in_b, discrepancies, exact_matches = reconcile_data(
        source_a,
        source_b
    )

    print("Building summary...")
    summary = build_summary(
        source_a,
        source_b,
        duplicates_a,
        duplicates_b,
        only_in_a,
        only_in_b,
        discrepancies,
        exact_matches
    )

    print("Saving results...")
    save_results(
        summary,
        duplicates_a,
        duplicates_b,
        only_in_a,
        only_in_b,
        discrepancies,
        exact_matches
    )

    print(f"Reconciliation completed: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

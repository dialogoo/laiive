import pandas as pd
from pathlib import Path


def main():
    # Fix the path to look in the current directory's out folder
    jsonl_file_path = Path("out/eppen_music_20250813.jsonl")

    # Check if file exists
    if not jsonl_file_path.exists():
        print(f"Error: File {jsonl_file_path} not found!")
        print("Available files in out directory:")
        data_dir = Path("out")
        if data_dir.exists():
            for file in data_dir.iterdir():
                print(f"  - {file.name}")
        return

    df = pd.read_json(jsonl_file_path, lines=True)
    inspect_dataframe(df)


def inspect_dataframe(df: pd.DataFrame):
    print("First 5 rows:")
    print(df.head())

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nDataframe info:")
    print(df.info())

    print("\nDataframe shape:")
    print(df.shape)

    # If you want to see specific columns, add them here
    # For example, if you have a 'text_content' column:
    if "text_content" in df.columns:
        print("\nFirst 5 rows of text_content column:")
        print(df["text_content"].head())

    # Show first few rows of each column
    print("\nFirst few rows of each column:")
    for column in df.columns:
        print(f"\n{column}:")
        print(df[column].head())


if __name__ == "__main__":
    main()

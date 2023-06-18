from pathlib import Path


def fetch_json_files(path: str) -> list[Path]:
    directory_path = Path(path)
    return [file for file in directory_path.glob("*.json")]

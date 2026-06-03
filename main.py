from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chuyen doi anh bang bien doi logarit: s = c * log(1 + r)."
    )
    parser.add_argument("input", help="Duong dan anh dau vao.")
    parser.add_argument(
        "-o",
        "--output",
        help="Duong dan anh dau ra. Mac dinh se them hau to _log.",
    )
    return parser.parse_args()


def build_output_path(input_path: Path, output_path: str | None) -> Path:
    if output_path:
        return Path(output_path)
    return input_path.with_name(f"{input_path.stem}_log{input_path.suffix}")


def get_output_max(image: np.ndarray) -> float:
    if np.issubdtype(image.dtype, np.integer):
        return float(np.iinfo(image.dtype).max)
    return 1.0


def log_transform(
    image: np.ndarray, c_value: float | None = None
) -> tuple[np.ndarray, float, float]:
    image_float = image.astype(np.float32)
    r_max = float(image_float.max())

    if r_max <= 0:
        return np.zeros_like(image), 0.0, r_max

    output_max = get_output_max(image)
    c = c_value if c_value is not None else output_max / np.log1p(r_max)
    transformed = np.clip(c * np.log1p(image_float), 0, output_max)

    if np.issubdtype(image.dtype, np.integer):
        transformed = np.rint(transformed).astype(image.dtype)
    else:
        transformed = transformed.astype(image.dtype)

    return transformed, c, r_max


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = build_output_path(input_path, args.output)

    image = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"Khong doc duoc anh: {input_path}")

    transformed, c_value, r_max = log_transform(image)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), transformed):
        raise RuntimeError(f"Khong luu duoc anh dau ra: {output_path}")

    print(f"Da luu anh sau bien doi tai: {output_path}")
    print(f"r_max = {r_max}")
    print(f"c = {c_value}")
    print("Cong thuc ap dung: s = c * log(1 + r)")


if __name__ == "__main__":
    main()

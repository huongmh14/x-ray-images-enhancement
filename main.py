from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    bo_phan_tich = argparse.ArgumentParser(
        description="Chuyen doi anh bang bien doi logarit: s = c * log(1 + r)."
    )
    bo_phan_tich.add_argument("input", help="Duong dan anh dau vao.")
    bo_phan_tich.add_argument(
        "-o",
        "--output",
        help="Duong dan anh dau ra. Mac dinh se them hau to _log.",
    )
    return bo_phan_tich.parse_args()


def build_output_path(input_path: Path, output_path: str | None) -> Path:
    if output_path:
        
        return Path(output_path)
    return input_path.with_name(f"{input_path.stem}_log{input_path.suffix}")




def log_transform(
    image: np.ndarray, c_value: float | None = None
) -> tuple[np.ndarray, float, float]:


    anh_so_thuc = image.astype(np.float32)
    gia_tri_anh_lon_nhat = float(anh_so_thuc.max())
    if c_value is None:
        gia_tri_c = 255.0 / np.log1p(gia_tri_anh_lon_nhat)
    else:

        gia_tri_c = c_value
    print(f"Gia tri c su dung: {gia_tri_c}")
    anh_sau_bien_doi = gia_tri_c * np.log1p(anh_so_thuc)
    
    return anh_sau_bien_doi.astype(image.dtype), gia_tri_c, gia_tri_anh_lon_nhat


def main() -> None:
    tham_so = parse_args()
    duong_dan_vao = Path(tham_so.input)
    duong_dan_ra = build_output_path(duong_dan_vao, tham_so.output)

    anh = cv2.imread(str(duong_dan_vao), cv2.IMREAD_UNCHANGED)
    if anh is None:
        raise FileNotFoundError(f"Khong doc duoc anh: {duong_dan_vao}")

    anh_sau_bien_doi, gia_tri_c, gia_tri_anh_lon_nhat = log_transform(anh)
    duong_dan_ra.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(duong_dan_ra), anh_sau_bien_doi):
        raise RuntimeError(f"Khong luu duoc anh dau ra: {duong_dan_ra}")

    print(f"Da luu anh sau bien doi tai: {duong_dan_ra}")
    print(f"c = {gia_tri_c}")
    print("Cong thuc ap dung: s = c * log(1 + r)")


if __name__ == "__main__":
    main()

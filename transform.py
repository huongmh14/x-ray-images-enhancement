def log_transform(
    image: np.ndarray, c_value: float | None = None
) -> tuple[np.ndarray, float, float]:

    # Chuyen doi anh sang kieu so thuc de tinh toan
    anh_so_thuc = image.astype(np.float32)
    # Tinh gia tri anh lon nhat de tinh toan gia tri c neu chua duoc cung cap
    gia_tri_anh_lon_nhat = float(anh_so_thuc.max())
    # Tinh gia tri c neu chua duoc cung cap, su dung cong thuc: c = 255 / log(1 + max_pixel_value)
    if c_value is None:
        gia_tri_c = 255.0 / np.log1p(gia_tri_anh_lon_nhat)
    # Neu gia tri c da duoc cung cap, su dung gia tri do
    else:
        gia_tri_c = c_value
    print(f"Gia tri c su dung: {gia_tri_c}")
    # Ap dung bien doi logarit: s = c * log(1 + r)
    anh_sau_bien_doi = gia_tri_c * np.log1p(anh_so_thuc)
    
    return anh_sau_bien_doi.astype(image.dtype), gia_tri_c, gia_tri_anh_lon_nhat
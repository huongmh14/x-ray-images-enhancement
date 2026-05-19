# X-Ray Image Enhancement

Du an nay tang cuong anh X-quang bang mot pipeline gom 3 buoc:

1. `Log Transform`
2. `CLAHE`
3. `Unsharp Mask`

Muc tieu cua he thong la lam ro vung toi, tang tuong phan cuc bo, va lam sac cac bien mo de ho tro quan sat chi tiet trong anh y te.

## Tong quan cach hoat dong

He thong nhan anh dau vao, dua anh ve grayscale 8-bit, sau do xu ly theo thu tu:

1. `Log Transform`: nang muc sang o cac vung toi.
2. `CLAHE`: tang tuong phan cuc bo theo tung vung nho.
3. `Unsharp Mask`: lam sac canh va bien.

Anh ket qua cuoi cung duoc goi la `enhanced`.

Ngoai giao dien dong lenh, du an con co web app local bang `Streamlit` de ban upload anh va dieu chinh tham so bang slider.

## Co che xu ly ben trong

Module chinh nam o:

- `src/algorithms/medical_pipeline.py`

Dong xu ly chinh:

1. Doc anh bang `imageio`
2. Chuyen anh ve `uint8` grayscale neu can
3. Ap dung `log transform`
4. Ap dung `CLAHE`
5. Ap dung `unsharp mask`
6. Tra ve 4 anh trung gian:
   - `original`
   - `log`
   - `clahe`
   - `enhanced`

Neu chay bang CLI va co thu muc output, chuong trinh se luu tung stage ra file PNG va luu them file `runinfo.txt`.

## Cau truc file quan trong

- `app.py`: diem vao cho CLI
- `streamlit_app.py`: giao dien web local
- `src/arguments.py`: xu ly tham so dong lenh
- `src/algorithms/runner.py`: chay 1 anh hoac ca thu muc
- `src/algorithms/medical_pipeline.py`: pipeline xu ly chinh
- `images/`: anh mau
- `results/`: noi luu ket qua

## Yeu cau moi truong

Can co:

- `Python 3.10+`
- `pip`

Khuyen nghi:

- `Python 3.12`

Kiem tra:

```bash
python3 --version
pip --version
```

## Khoi tao moi truong Python

### WSL / Ubuntu / Linux

```bash
cd /mnt/d/2026-2027/XLA/BTL/x-ray-images-enhancement
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
cd D:\2026-2027\XLA\BTL\x-ray-images-enhancement
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Thu vien dang dung

`requirements.txt` da duoc toi gian cho pipeline hien tai:

- `numpy`
- `imageio`
- `opencv-python`
- `streamlit`

## Tham so mac dinh

He thong co 4 tham so chinh:

- `log_gain = 4.0`
- `clip_limit = 2.5`
- `tile_grid_size = 8`
- `unsharp_amount = 0.6`

Bo tham so goi y de demo:

```text
log_gain = 3.0
clip_limit = 1.0
tile_grid_size = 4
unsharp_amount = 0.4
```

Y nghia:

- `log_gain`: cang lon thi vung toi cang duoc nang sang
- `clip_limit`: dieu khien muc tang tuong phan cua CLAHE
- `tile_grid_size`: kich thuoc vung cuc bo de CLAHE xu ly
- `unsharp_amount`: muc do lam sac

## Cach chay bang CLI

### Chay 1 anh

```bash
python app.py -i images/001.tif
```

Neu khong truyen tham so, chuong trinh se hoi 4 gia tri.

### Chay 1 anh va truyen tham so truc tiep

```bash
python app.py -i images/001.tif --log-gain 3 --clip-limit 1 --tile-grid-size 4 --unsharp-amount 0.4
```

### Chay ca thu muc

```bash
python app.py -p images
```

Khi chay theo thu muc, he thong chi hoi tham so 1 lan roi ap dung cho toan bo anh.

### Chay ca thu muc va chi dinh output

```bash
python app.py -p images -o results/full_batch --log-gain 3 --clip-limit 1 --tile-grid-size 4 --unsharp-amount 0.4
```

## Cach chay bang web

Khoi dong web app:

```bash
streamlit run streamlit_app.py
```

Sau do mo dia chi local trong terminal, thuong la:

```text
http://localhost:8501
```

Web app ho tro:

- upload anh
- chon anh demo trong `images/`
- dieu chinh 4 tham so bang slider
- xem `original`, `log`, `clahe`, `enhanced`
- tai anh ket qua dang PNG

## Dau ra cua he thong

Neu khong dung `-o`, chuong trinh tao:

```text
results/<timestamp>/
```

Moi anh co the sinh ra:

- `<name>_original.png`
- `<name>_log.png`
- `<name>_clahe.png`
- `<name>_enhanced.png`
- `<name>_runinfo.txt`

## Luong chay cua du an

### Luong CLI

1. Nguoi dung chay `app.py`
2. `src/arguments.py` doc tham so
3. `src/algorithms/runner.py` tao cau hinh
4. `MedicalEnhancement` xu ly anh
5. Ket qua duoc luu vao `results/`

### Luong Web

1. Nguoi dung chay `streamlit_app.py`
2. Streamlit tao giao dien web local
3. Nguoi dung upload anh hoac chon anh mau
4. Slider tao `EnhancementConfig`
5. `MedicalEnhancement.run_on_image()` xu ly truc tiep trong bo nho
6. Web hien thi 4 anh va cho phep tai anh ket qua

## Tat moi truong ao

```bash
deactivate
```

## Chay lai nhanh

### WSL / Linux

```bash
cd /mnt/d/2026-2027/XLA/BTL/x-ray-images-enhancement
source .venv/bin/activate
```

### Windows PowerShell

```powershell
cd D:\2026-2027\XLA\BTL\x-ray-images-enhancement
.venv\Scripts\Activate.ps1
```

Sau do chon mot trong hai cach:

```bash
python app.py -i images/001.tif
```

hoac:

```bash
streamlit run streamlit_app.py
```

## Ghi chu

- Anh mau se duoc chuyen ve grayscale truoc khi xu ly
- Pipeline hien tai toi uu cho anh y te kieu X-ray
- `enhanced` khong phai ten cua mot thuat toan rieng, ma la anh ket qua cuoi cung sau khi qua `log`, `clahe`, va `unsharp mask`

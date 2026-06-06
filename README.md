# X-ray Images Enhancement With Log Transform

Du an nay minh hoa phep bien doi logarit de tang cuong anh, dac biet phu hop voi anh X-quang va cac anh muc xam co do tuong phan thap.

## Cong thuc Bien Doi Logarit

### Cong thuc chinh

Phep bien doi dang dung trong du an:

```
s = c * log(1 + r)
```

### Dinh nghia cac bien so

| Ky hieu | Mieu ta | Don vi | Pham vi |
|---------|---------|--------|---------|
| `r` | Gia tri diem anh dau vao (pixel value) | Gia tri sac do | [0, 255] cho anh 8-bit |
| `s` | Gia tri diem anh sau bien doi | Gia tri sac do | [0, 255] |
| `c` | He so dieu chinh (scaling constant) | He so vo thong | c > 0 |
| `log` | Ham logarit tu nhien (natural logarithm) | Ham toan hoc | ln() |
| `log(1 + r)` | Logarit cua (1 + r) de tranh log(0) | Gia tri he hoc | > 0 |

### Cach tinh he so `c`

```
c = 255 / log(1 + max_pixel_value)
```

Trong do:
- `max_pixel_value` la gia tri pixel lon nhat trong anh dau vao
- `255` la gia tri max cua dải gia tri anh dau ra (0-255)

**Y nghia**: He so `c` duoc tinh tu dong de dam bao anh dau ra luon nam trong dai [0, 255], tru tranh tran/thieu dung.

### Dac diem cua bien doi logarit

1. **Non-linear mapping**: Bien doi logarit la ham phi tuyen
   - Cac gia tri toi (r nho) se tang nhanh hon
   - Cac gia tri sang (r lon) se tang cham hon

2. **Noi bat chi tiet toi**: Khi r nho, log(1 + r) ≈ r nhung dang duoc co dai
   - Dieu nay giup khuych dai chi tiet o vung toi

3. **Nen chi tiet sang**: Khi r lon, log(1 + r) tang cham
   - Giup tranh lam tran nhung vung sang

## Co so Toan hoc

### Tac dong cua ham logarit

Ham logarit tu nhien co cac tinh chat sau:

- **Tinh chat 1 - Giam toc do tang**: log(x) tang cham hon khi x tang lon
- **Tinh chat 2 - Khuych dai vung nho**: log(x) giu chinh ta y cho gia tri nho
- **Tinh chat 3 - Nen vung lon**: log(x) thua vao nhung gia tri lon hơn

Dieu nay co nghia:
- Vung pixel nho (anh toi) duoc "keo dai" va hien chi tiet hon
- Vung pixel lon (anh sang) duoc "nen lai" de tranh tran

### Ly thuyết Tương Phan

- **Tương phan thấp**: Anh co khoang cach lon giua pixel toi va pixel sang
- **Tương phan cao**: Khoang cach pixel toi - sang gan nhau hon
- **Muc tieu**: Bien doi logarit giup tang cuong tương phan o vung chi tiet toi

## Cau truc du an

```
tranform-log/
├── main.py          # Diem vao chinh, xa ly anh tu dong
├── transform.py     # Ham log_transform chinh
├── app.py           # Giao dien ung dung (neu co)
├── requirements.txt # Cac thu vien phu thuc
├── README.md        # Tai lieu nay
└── images/          # Thu muc luu anh dau vao va dau ra
```

### Mo ta chi tiet cac file

**main.py**
- Chuong trinh dieu khien chinh
- Xu ly tham so dong lenh: `-i <anh_dau_vao> -o <anh_dau_ra>`
- Tai anh, ap dung bien doi, luu ket qua
- In ra gia tri c va cac thong so tinh toan

**transform.py**
- Ham `log_transform(image, c_value=None)`
- Tinh toan tu dong gia tri c neu khong duoc cung cap
- Tra ve: anh bien doi, gia tri c, gia tri pixel max

**requirements.txt**
- Danh sach thu vien can thiet: opencv, numpy

## Cach Su dung

### Yeu cau he thong

- Python 3.7+
- OpenCV 4.0+
- NumPy 1.19+

### Cai dat

```bash
pip install -r requirements.txt
```

### Chay chuong trinh

#### Cach 1: Su dung main.py (tu dong tinh c)

```bash
python main.py images/input.jpg
```

Ket qua luu tai: `images/input_log.jpg`

#### Cach 2: Chi dinh duong dan dau ra

```bash
python main.py images/input.jpg -o images/output.jpg
```

#### Cach 3: Su dung transform.py trong code

```python
import cv2
from transform import log_transform

# Tai anh
image = cv2.imread('images/input.jpg', cv2.IMREAD_UNCHANGED)

# Ap dung bien doi (c tu dong)
result, c_value, max_value = log_transform(image)

# Luu ket qua
cv2.imwrite('images/output.jpg', result)
print(f"He so c: {c_value}")
```

### Tham so tuy chinh

Su dung `c_value` de chi dinh he so:

```python
# Ap dung bien doi voi c = 1.0
result, c_used, _ = log_transform(image, c_value=1.0)
```

## Cau truc tep

- `main.py`: xu ly anh bang dong lenh
- `app.py`: giao dien web bang Streamlit de tai anh, xem anh va dieu chinh `c`
- `images/`: mot so anh mau
- `requirements.txt`: danh sach thu vien can cai

## Cai dat

Neu ban dung moi truong ao:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux hoac WSL:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Chay chuong trinh dong lenh

Xu ly mot anh va luu ket qua:

```bash
python main.py images/002.jpg
```

Chi dinh tep dau ra:

```bash
python main.py images/002.jpg -o images/002_log.jpg
```

## Chay giao dien web Streamlit

Dung lenh:

```bash
python -m streamlit run app.py
```

Neu lenh `streamlit` khong ton tai tren `PATH`, van nen uu tien cach chay bang module nhu tren.

## Cach su dung giao dien web

1. Tai anh len tu may tinh
2. Quan sat anh goc va anh sau bien doi
3. Dieu chinh thanh truot `c` o thanh ben trai
4. Tai anh da xu ly ve may

## Nguyen ly cua thanh truot `c`

- `c` nho: anh bien doi nhe hon
- `c` lon: anh sang hon va cac vung toi duoc day ro hon
- neu `c` qua lon, mot so vung sang co the bi mat chi tiet do bi cat nguong

## Ghi chu

- Chuong trinh ho tro anh xam va anh mau
- Voi anh 16-bit, giao dien se tu dong chuan hoa de de quan sat hon tren web

---

## Ung dung Thuc te

### 1. Tang cuong anh X-quang

- **Van de**: Anh X-quang co tương phan thap, kho nhin ro chi tiet xương va vet nut
- **Giai phap**: Ap dung log transform de noi bat chi tiet toi
- **Ket qua**: Chi tiet mo tren xuong, vet nut hien ro hon
- **Lĩnh vực**: Y học chẩn đoán hình ảnh

### 2. Anh y te - CT scan, MRI

- **Van de**: Anh co toc do tang nhieu, cac vung sang chiếm dung quá lớn
- **Giai phap**: Logarit nen vung sang, noi bat vung toi va chi tiet
- **Ket qua**: Cac khoi u va dị thường hien sáng rõ ràng
- **Lĩnh vực**: Chẩn đoán y tế, phát hiện bệnh

### 3. Anh cong nghiep - Tu kiểm tra chat luong

- **Van de**: Anh theo thời gian thay đổi, cần phát hiện khuyết điểm nhỏ
- **Giai phap**: Log transform giúp phát hiện các chi tiết nhỏ tren bề mặt
- **Ket qua**: Khuyết điểm, nứt rạn rõ ràng hơn
- **Lĩnh vực**: Kiểm tra chất lượng sản phẩm

### 4. Ảnh thiên văn - Sao yếu, thiên hà

- **Van de**: Anh thiên thể chi chứa vài pixel sáng trên nền đen
- **Giai phap**: Log transform giúp khuych dai vung toi, hien thi sao
- **Ket qua**: Các sao yếu và cấu trúc mờ của các thiên hà hien ra
- **Lĩnh vực**: Quan sát thiên văn

### 5. Ảnh nền tối - Microscopy, Tomography

- **Van de**: Anh chi thực có signal trong dải nhỏ
- **Giai phap**: Logarit khuych dai vung signal, nen vung nhiễu
- **Ket qua**: Signal rõ ràng, nhiễu bị nen lại
- **Lĩnh vực**: Nghiên cứu khoa học

---

## Ví du Tinh toan Thi Nghiem

### Trường hợp: Anh X-quang 8-bit

**Thông số anh gốc:**
- Min pixel: 0
- Max pixel: 200
- Trung bình: 80

**Tính toán hệ số c:**

```
c = 255 / log(1 + 200)
  = 255 / log(201)
  = 255 / 5.303
  ≈ 48.1
```

**Biến đổi một số giá trị pixel:**

| r (input) | log(1+r) | s = 48.1×log(1+r) | Thay đổi |
|-----------|----------|-------------------|---------|
| 10 (tối)  | 2.40     | 115.4             | +1054%  |
| 50        | 3.93     | 189.1             | +278%   |
| 100       | 4.61     | 221.8             | +122%   |
| 150 (sáng)| 5.02     | 241.5             | +61%    |
| 200       | 5.30     | 255.0             | +28%    |

**Nhận xét:**
- Vùng tối (r=10) tăng 1000% - được **khuych đại mạnh**
- Vùng sáng (r=200) tăng 28% - được **nen lại**
- Độ khuych đại giảm dần - điều này giúp **cân bằng tương phản**

### Trường hợp: Ảnh quá tối (max pixel = 100)

```
c = 255 / log(1 + 100) = 255 / log(101) ≈ 255 / 4.62 ≈ 55.2

Pixel r=50: s = 55.2 × log(51) ≈ 55.2 × 3.93 ≈ 217 (tăng 334%)
```

**Kết luận:** Hình ảnh quá tối sẽ được làm sáng hơn đáng kể.

### Trường hợp: Ảnh 16-bit (max = 65535)

```
c = 255 / log(1 + 65535) = 255 / log(65536) ≈ 255 / 11.09 ≈ 23.0

Pixel r=100:   s = 23.0 × log(101) ≈ 23.0 × 4.62 ≈ 106
Pixel r=10000: s = 23.0 × log(10001) ≈ 23.0 × 9.21 ≈ 212
```

**Nhận xét:** Với dải giá trị rộng hơn, hệ số c nhỏ hơn, khuych đại nhẹ hơn.

---

## Tham khao Ly thuyet

### Các công thức biến đổi khác

| Biến đổi | Công thức | Ứng dụng | Ưu điểm | Nhược điểm |
|----------|-----------|---------|---------|-----------|
| **Logarit** | s = c × log(1 + r) | Ảnh tương phán thấp | Khuych đại vùng tối, nen vùng sáng | Có thể làm mất chi tiết sáng |
| **Lũy thừa** | s = c × r^(1/γ) | Hiệu chỉnh gamma | Linh hoạt, có thể tùy chỉnh | Phức tạp hơn logarit |
| **Mũ** | s = c × (e^r - 1) | Ảnh quá tối | Khuych đại mạnh vùng tối | Làm tăng chi tiết sáng quá mức |
| **Căn bậc 2** | s = c × √r | Ảnh quá sáng | Giảm nhẹ nhàng | Khuych đại không đủ |
| **Histeq (Histogram Equalization)** | Cân bằng histogram | Tương phán tổng quát | Làm tối ưu tương phán | Có thể tạo artifacts |

### Bảng so sánh logarit vs các phương pháp khác

| Tiêu chí | Log transform | Gamma | Histeq | Normalization |
|----------|---------------|-------|--------|--------------|
| Đơn giản | ✓✓✓ | ✓✓ | ✓ | ✓✓✓ |
| Điều chỉnh được | ✓✓ | ✓✓✓ | Ít | Không |
| Giữ lại độ sáng tuyệt đối | ✗ | Có | ✗ | Không |
| Phù hợp với ảnh tương phán thấp | ✓✓✓ | ✓✓ | ✓✓ | Ít |
| Tạo artifacts | Ít | Ít | Nhiều | Không |

### Tài liệu tham khảo khoa học

**Sách chuyên môn:**
- Gonzalez, R. C., & Woods, R. E. (2008). **Digital Image Processing** (3rd ed.)
  - Chương 3: Intensity Transformations and Spatial Filtering
  - Phần 3.2.2: Logarithmic Transformations

- Pratt, W. K. (2007). **Digital Image Processing** (4th ed.)
  - Chương 7: Image Enhancement Techniques

**Bài báo khoa học:**
- Stark, J. L., et al. (2003). "Enhancement of astronomical images" 
  - Ứng dụng transformation trong thiên văn

**Tính chất toán học của logarit:**
- log(ab) = log(a) + log(b) → Phép nhân thành cộng
- log(a^n) = n × log(a) → Lũy thừa thành nhân
- log(1 + x) ≈ x khi x → 0 → Xấp xỉ tuyến tính ở vùng nhỏ
- d/dx[log(x)] = 1/x → Đạo hàm giảm dần

### Hạn chế và Lưu ý Khi Sử Dụng

**1. Khi nào KHÔNG nên dùng log transform:**
- Ảnh đã có tương phản cao
- Ảnh cần bảo toàn độ sáng tuyệt đối (y học pháp y, định lượng)
- Ảnh có nhiều vùng đen (background) - may bị tăng noise

**2. Các vấn đề phổ biến:**
- **Ảnh quá sáng:** Tăng `c` hoặc dùng lũy thừa thay vì logarit
- **Ảnh quá tối:** Giảm `c`, hoặc áp dụng tiền xử lý (histogram equalization)
- **Noise được khuych đại:** Áp dụng lọc nhiễu trước biến đổi

**3. Mất mát thông tin:**
- Các pixel quá cao có thể bị cắt ngưỡng (clipping)
- Thông tin ở vùng sáng bị nén lại, có thể mất chi tiết
- Cần kiểm tra kỹ ảnh đầu ra

**4. Khuyến nghị:**
- Luôn lưu ảnh gốc (không ghi đè)
- Kiểm tra histogram trước và sau transformation
- Dùng multiple `c` values để so sánh kết quả
- Xác nhận kết quả với chuyên gia trong lĩnh vực

---

## Kết Luận

Phép biến đổi logarit là một công cụ **đơn giản nhưng mạnh mẽ** để:

✓ Nâng cao tương phản trong ảnh tương phán thấp  
✓ Làm rõ chi tiết ở vùng tối mà không làm tăng noise quá mức  
✓ Bảo vệ thông tin ở vùng sáng  
✓ Dễ hiểu, dễ triển khai  

**Ứng dụng rộng rãi:**
- **Y tế**: X-quang, CT, MRI
- **Công nghiệp**: Kiểm tra chất lượng
- **Khoa học**: Thiên văn, microscopy
- **Xử lý ảnh**: Tiền xử lý cho các thuật toán khác

**Lưu ý quan trọng:** Chọn giá trị `c` thích hợp là chìa khóa thành công. Công thức tự động `c = 255 / log(1 + max)` thường cho kết quả tốt, nhưng có thể cần điều chỉnh tùy theo ứng dụng cụ thể.

# X-ray Images Enhancement With Log Transform

Du an nay minh hoa phep bien doi logarit de tang cuong anh, dac biet phu hop voi anh X-quang va cac anh muc xam co do tuong phan thap.

## Cong thuc

Phep bien doi dang dung trong du an:

```text
s = c * log(1 + r)
```

Trong do:

- `r` la gia tri diem anh dau vao
- `s` la gia tri diem anh sau bien doi
- `c` la he so dieu chinh muc do bien doi

Gia tri `c` cang lon thi anh sau bien doi cang sang hon.

## Y nghia cua bien doi logarit

Bien doi logarit co tac dung:

- lam noi bat cac muc xam thap, nghia la cac vung toi se hien ro hon
- nen cac muc xam cao, tranh viec vung sang bi tang qua muc
- giam do chenh lech qua lon giua vung toi va vung sang
- phu hop voi bai toan tang cuong chi tiet trong anh y te, anh X-quang, anh cong nghiep

## Ung dung cua logarit trong xu ly anh

Bien doi logarit thuong duoc ap dung trong cac truong hop sau:

1. Tang cuong anh X-quang

- giup nhin ro hon cac chi tiet mo, xuong, vet nut, vung co do tuong phan thap
- ho tro quan sat cac chi tiet kho thay trong anh goc

2. Nen dai dong cua anh

- khi anh co su chenh lech sang toi lon, logarit giup dua cac gia tri ve gan nhau hon
- dieu nay huu ich voi anh co nhieu vung rat sang va rat toi cung luc

3. Tien xu ly truoc khi phan tich anh

- cai thien anh truoc khi dua vao cac buoc phan doan, phat hien bien, trich dac trung hoac hoc may

4. Hien thi anh y te va anh khoa hoc

- duoc dung de lam ro cac chi tiet nho ma mat thuong kho nhan ra tren anh goc

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

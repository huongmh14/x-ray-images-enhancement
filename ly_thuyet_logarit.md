# Ly thuyet xu ly anh trong mien khong gian: bien doi logarit

## 1. Khai niem xu ly anh trong mien khong gian

Xu ly anh trong mien khong gian la cach tac dong truc tiep len gia tri diem anh trong mat phang anh. Neu anh dau vao la `f(x, y)` thi anh dau ra la `g(x, y)`, trong do:

```text
g(x, y) = T[f(x, y)]
```

voi `T` la phep bien doi trong mien khong gian.

Hai nhom ky thuat pho bien la:

- Bien doi diem: gia tri moi cua moi pixel chi phu thuoc vao chinh pixel do.
- Bien doi lan can: gia tri moi cua pixel phu thuoc vao mot cua so lan can xung quanh.

Bien doi logarit thuoc nhom **bien doi diem**.

## 2. Phep bien doi logarit

### 2.1. Cong thuc

Cong thuc co ban:

```text
s = c * log(1 + r)
```

Trong do:

- `r` la muc xam cua diem anh dau vao
- `s` la muc xam cua diem anh dau ra
- `c` la he so ti le

Neu anh 8 bit co muc xam trong khoang `[0, 255]`, co the chon:

```text
c = 255 / log(1 + 255)
```

de anh dau ra van nam trong khoang `[0, 255]`.

Trong chuong trinh minh hoa, de linh hoat hon khi dieu chinh, ta dung dang chuan hoa:

```text
s = 255 * log(1 + alpha * r) / log(1 + alpha)
```

voi:

- `r` da chuan hoa ve `[0, 1]`
- `alpha > 0` la he so dieu chinh cuong do bien doi

### 2.2. Y nghia

Ham logarit tang nhanh o vung gia tri nho va tang cham o vung gia tri lon. Vi vay:

- Vung toi duoc mo rong do tuong phan
- Vung sang bi nen lai
- Nhung chi tiet an trong bong toi se de thay hon

Day la ly do bien doi logarit rat phu hop voi anh thieu sang, anh co dynamic range lon, anh y te, anh ve tu cam bien hoac anh chua nhieu vung toi.

## 3. Do thi va dac tinh

Neu so sanh voi phep dong nhat `s = r`:

- O vung muc xam thap, duong logarit nam cao hon duong thang `s = r`
- O vung muc xam cao, duong logarit nam thap hon duong thang `s = r`

Tu do cho thay:

- Pixel toi se duoc tang sang
- Pixel sang bi nen lai de tranh bao hoa qua nhanh

## 4. Quy trinh ap dung cho anh mau

Neu ap dung truc tiep logarit len ca ba kenh `R`, `G`, `B`, mau sac co the bi thay doi manh. Cach lam on dinh hon la:

1. Chuyen anh tu `RGB` sang `HSV`
2. Tach kenh `V` la kenh do sang
3. Bien doi logarit tren kenh `V`
4. Ghep lai voi `H`, `S`
5. Chuyen nguoc ve `RGB`

Cach nay giu mau tuong doi tu nhien trong khi van tang cuong do sang.

## 5. Uu diem

- Don gian, de cai dat
- Toc do nhanh vi la phep bien doi diem
- Lam ro chi tiet vung toi tot
- Huu ich trong tien xu ly cho nhan dien doi tuong, OCR, OCR bien so, theo doi camera ban dem

## 6. Han che

- Co the lam lo ro nhieu trong vung toi
- Khong phai luc nao cung tot cho anh da sang san
- Neu chon he so qua lon, anh co the bi be do tuong phan o vung sang

## 7. Ung dung thuc te de xuat

### Bai toan

Tang cuong anh tu camera giam sat bai do xe vao buoi toi.

### Muc tieu

- Lam ro than xe, vach ke, bien bao, bien so
- Cai thien chat luong anh truoc khi dua vao he thong nhan dien

### Cach ap dung

- Anh dau vao la anh thieu sang
- Tach kenh do sang
- Dung bien doi logarit de keo gian vung muc xam thap
- Tao anh ket qua va histogram de so sanh

## 8. Thuat toan tong quat

1. Doc anh mau
2. Chuyen anh sang khong gian mau `HSV`
3. Lay kenh `V`
4. Chuan hoa gia tri pixel ve `[0, 1]`
5. Ap dung cong thuc logarit
6. Dua ket qua ve khoang `[0, 255]`
7. Ghep kenh `V` moi voi `H`, `S`
8. Hien thi va luu ket qua

## 9. Nhan xet

Bien doi logarit la mot ky thuat co ban nhung rat thuc dung trong xu ly anh mien khong gian. No dac biet huu ich khi muon lam ro thong tin o vung toi ma van giu muc sang tong the trong nguong hop ly. Trong bai toan thieu sang, day la mot lua chon nhanh, de trinh bay va de mo rong thanh cac he thong ung dung lon hon.

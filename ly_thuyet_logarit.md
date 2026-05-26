# Ly thuyet cac thuat toan tang cuong anh X-quang trong du an

## 1. Muc tieu cua du an

Du an hien tai thuc hien tang cuong anh X-quang bang mot pipeline xu ly anh trong mien khong gian gom 3 buoc lien tiep:

1. `Log Transform`
2. `CLAHE`
3. `Unsharp Mask`

Muc tieu cua pipeline la:

- lam ro cac vung toi hoac co do tuong phan thap
- tang tuong phan cuc bo de de quan sat chi tiet
- lam sac bien va cau truc xuong

Ket qua cuoi cung cua he thong la anh `enhanced`.

## 2. Luong xu ly tong quat

Trong file `src/algorithms/medical_pipeline.py`, anh duoc xu ly theo thu tu sau:

1. Doc anh dau vao
2. Dua anh ve dang grayscale 8-bit neu can
3. Ap dung bien doi logarit
4. Ap dung CLAHE
5. Ap dung unsharp mask
6. Tra ve 4 anh trung gian:
   - `original`
   - `log`
   - `clahe`
   - `enhanced`

Co the xem day la mot chuoi xu ly theo logic:

```text
Anh dau vao
-> Chuan hoa grayscale uint8
-> Log Transform
-> CLAHE
-> Unsharp Mask
-> Anh enhanced
```

## 3. Tien xu ly va chuan hoa anh

Truoc khi di vao cac thuat toan tang cuong, anh duoc dua ve mot dang du lieu thong nhat.

### 3.1. Chuyen ve anh xam

Neu anh dau vao co 3 kenh mau, chuong trinh chuyen anh ve grayscale truoc khi xu ly. Viec nay phu hop voi ngu canh anh X-quang, vi thong tin can quan tam chu yeu nam o cuong do sang toi, khong nam o mau sac.

### 3.2. Chuan hoa ve `uint8`

Neu anh chua o dang `uint8`, chuong trinh se chuan hoa gia tri pixel ve khoang `[0, 255]`.

Muc dich:

- thong nhat mien gia tri cho toan bo pipeline
- dam bao cac phep bien doi sau do hoat dong on dinh
- tuong thich voi cach OpenCV xu ly CLAHE va bo loc lam sac

Buoc nay khong phai la thuat toan tang cuong chinh, nhung la buoc nen quan trong de giu tinh on dinh cua ket qua.

## 4. Bien doi logarit

### 4.1. Ban chat

Bien doi logarit la mot phep bien doi diem trong mien khong gian. Gia tri moi cua moi pixel chi phu thuoc vao gia tri cu cua chinh pixel do, khong phu thuoc truc tiep vao lan can xung quanh.

Neu anh dau vao la `f(x, y)` va anh dau ra la `g(x, y)`, khi do:

```text
g(x, y) = T[f(x, y)]
```

voi `T` la ham logarit.

### 4.2. Cong thuc su dung trong du an

Trong du an, anh duoc dua ve khoang `[0, 1]`, sau do ap dung:

```text
s = log(1 + c * r) / log(1 + c)
```

trong do:

- `r` la gia tri pixel da chuan hoa trong khoang `[0, 1]`
- `s` la gia tri pixel sau bien doi
- `c` la he so `log_gain`

Sau cung, gia tri `s` duoc dua tro lai ve khoang `[0, 255]`.

### 4.3. Y nghia cua bien doi logarit

Ham logarit tang nhanh khi gia tri dau vao con nho, va tang cham dan khi gia tri dau vao lon. Vi vay:

- cac pixel toi duoc nang sang ro hon
- cac pixel sang bi nen lai nhe
- chi tiet trong vung toi de duoc quan sat hon

Dieu nay rat phu hop voi anh X-quang, vi trong nhieu truong hop mot so chi tiet xuong, khe nut, bien mo, hoac vung mo mem co the nam trong cac mien co do sang khong thuan loi.

### 4.4. Tham so `log_gain`

`log_gain` dieu khien cuong do cua phep bien doi logarit.

- `log_gain` nho: anh thay doi nhe, it nang sang vung toi
- `log_gain` lon: vung toi duoc keo sang manh hon

Anh huong thuc te:

- tang `log_gain` giup lo ro chi tiet an trong vung toi
- neu tang qua cao, nhieu trong vung toi cung bi keo len va anh de bi gat

## 5. CLAHE

### 5.1. Khai niem

CLAHE la viet tat cua `Contrast Limited Adaptive Histogram Equalization`, tuc can bang hoa histogram thich nghi co gioi han tuong phan.

Day la mot phuong phap tang tuong phan cuc bo. Thay vi xu ly histogram cho toan anh, CLAHE chia anh thanh nhieu vung nho roi can bang hoa tren tung vung.

### 5.2. Vi sao can CLAHE sau log transform

Sau khi bien doi logarit, anh da sang hon o cac vung toi, nhung do tuong phan cuc bo giua cac cau truc nho van co the chua du ro.

CLAHE giup:

- lam noi bat chi tiet trong tung khu vuc nho
- cai thien kha nang nhin thay bien, vet nut, khe hop, va cau truc mo
- tranh hien tuong tang tuong phan qua manh tren toan bo anh nhu histogram equalization thong thuong

### 5.3. Nguyen ly co ban

CLAHE hoat dong theo y tuong:

1. Chia anh thanh cac o nho
2. Tinh histogram rieng cho tung o
3. Cat bot cac dinh histogram qua cao bang `clip limit`
4. Phan bo lai phan gia tri bi cat
5. Can bang hoa tren tung o
6. Noi suy giua cac o de tranh duong bien gay khuc

Vi co buoc gioi han histogram, CLAHE giup han che viec nhieu bi tang qua muc.

### 5.4. Tham so `clip_limit`

`clip_limit` quyet dinh muc gioi han cho histogram trong moi o.

- `clip_limit` thap: CLAHE nhe hon, ket qua mem hon
- `clip_limit` cao: CLAHE tang tuong phan manh hon

Anh huong thuc te:

- tang `clip_limit` giup chi tiet ro hon
- neu qua cao, anh co the tro nen gat, noi hat, va de thay nhieu hon

### 5.5. Tham so `tile_grid_size`

`tile_grid_size` quyet dinh cach chia anh thanh luoi xu ly cuc bo.

Trong thuc te:

- gia tri nho thi moi o xu ly lon hon, hieu ung tang tuong phan mang tinh tong quat hon
- gia tri lon thi co nhieu o nho hon, hieu ung tang tuong phan cuc bo manh hon

Anh huong thuc te:

- tang `tile_grid_size` giup lam noi bat cac chi tiet nho theo tung vung
- neu qua lon, anh de xuat hien cam giac khong tu nhien hoac lo artifact cuc bo

## 6. Unsharp Mask

### 6.1. Ban chat

Unsharp mask la ky thuat lam sac anh bang cach tach thanh phan tan so thap ra khoi anh, sau do nhan manh phan bien va chi tiet tan so cao.

Y tuong tong quat:

1. Lam mo anh goc de lay phien ban tron hon
2. Lay anh goc tru anh mo de tao `mask`
3. Cong nguoc `mask` vao anh goc de lam ro bien

Co the mo ta ngan gon:

```text
sharpened = original + amount * (original - blurred)
```

Trong code, buoc lam mo duoc thuc hien bang `GaussianBlur`, sau do ket hop bang `cv2.addWeighted`.

### 6.2. Vai tro trong pipeline

Sau log transform va CLAHE, anh thuong da co do sang va tuong phan tot hon. Tuy nhien bien xuong va cac duong canh nho co the van hoi mem.

Unsharp mask giup:

- lam sac bien va duong vien
- nhan ro cau truc xuong
- tang cam giac ro net cua anh dau ra

### 6.3. Tham so `sharpen_amount`

`sharpen_amount` dieu khien muc do cong them phan mask vao anh goc.

- `sharpen_amount = 0`: khong lam sac them
- gia tri lon hon: bien va canh ro hon

Anh huong thuc te:

- tang `sharpen_amount` giup anh net hon
- neu qua cao, anh co the bi halo quanh bien, nhieu bi nhan manh, va nhin gay

## 7. Y nghia cua viec ket hop 3 thuat toan

Ba thuat toan trong du an khong tach roi, ma bo tro cho nhau:

- `Log Transform` xu ly bai toan vung toi
- `CLAHE` xu ly bai toan tuong phan cuc bo
- `Unsharp Mask` xu ly bai toan do net va bien

Neu chi dung mot thuat toan don le:

- chi dung log transform thi anh sang hon nhung chua chac du ro
- chi dung CLAHE thi anh co the tang tuong phan nhung vung toi ban dau van kho quan sat
- chi dung unsharp mask thi anh net hon, nhung neu anh goc toi hoac it tuong phan thi hieu qua han che

Vi vay, pipeline hien tai duoc xay dung theo huong:

```text
mo sang truoc -> tang tuong phan sau -> lam sac cuoi
```

Day la mot thu tu hop ly doi voi anh X-quang can vua ro vung toi, vua ro chi tiet, vua ro bien.

## 8. Y nghia cac tham so dau vao trong du an

He thong hien tai co 4 tham so chinh:

### 8.1. `log_gain`

- Gan voi buoc `Log Transform`
- Dieu khien muc nang sang vung toi
- Tang cao se lo ro vung toi nhung cung de keo nhieu len

### 8.2. `clip_limit`

- Gan voi buoc `CLAHE`
- Dieu khien muc tang tuong phan cuc bo
- Tang cao se ro chi tiet hon nhung cung de bi gat hoac noi hat

### 8.3. `tile_grid_size`

- Gan voi buoc `CLAHE`
- Dieu khien muc do cuc bo cua viec xu ly histogram
- Tang cao se nhan ro chi tiet nho hon nhung de xuat hien artifact hon

### 8.4. `sharpen_amount`

- Gan voi buoc `Unsharp Mask`
- Dieu khien muc lam sac bien
- Tang cao se net hon nhung de tao halo va lam nhieu noi bat

## 9. Y nghia cua viec hien thi anh theo tung stage trung gian

Trong du an, viec hien thi rieng cac anh `original`, `log`, `clahe`, va `enhanced` khong chi de minh hoa ket qua, ma con co y nghia quan trong trong viec danh gia pipeline.

### 9.1. Theo doi tac dong cua tung thuat toan

Moi stage cho thay anh da thay doi nhu the nao sau tung buoc:

- `original`: anh goc truoc xu ly
- `log`: cho thay muc do cai thien vung toi sau bien doi logarit
- `clahe`: cho thay kha nang tang tuong phan cuc bo
- `enhanced`: cho thay ket qua cuoi cung sau khi lam sac

Nho do, nguoi dung co the xac dinh ro buoc nao tao ra cai thien lon nhat cho anh.

### 9.2. Ho tro phat hien van de

Khi quan sat anh theo dung thu tu pipeline, ta de dang nhan ra van de xuat hien o stage nao:

- neu anh bi qua sang ngay sau `log`, nguyen nhan thuong nam o `log_gain`
- neu anh bi noi hat, qua gat sau `clahe`, nguyen nhan thuong lien quan den `clip_limit` hoac `tile_grid_size`
- neu anh cuoi co vien sang toi quanh canh, nguyen nhan thuong do `sharpen_amount` qua lon

Dieu nay giup qua trinh dieu chinh tham so tro nen co co so hon, thay vi chi nhin anh cuoi cung.

### 9.3. Ho tro so sanh va giai thich ket qua

Viec hien thi tung stage trung gian rat huu ich trong:

- bao cao hoc thuat
- thuyet trinh demo
- phan tich uu nhuoc diem cua tung buoc xu ly

Nguoi xem co the hieu ro:

- buoc nao lam sang anh
- buoc nao lam tang tuong phan
- buoc nao lam sac bien

Vi vay, he thong tro nen de giai thich hon va minh bach hon ve mat xu ly.

### 9.4. Ho tro danh gia tinh hieu qua cua pipeline

Neu chi hien thi anh dau vao va anh dau ra, ta chi biet pipeline co thay doi anh hay khong. Tuy nhien, khi hien thi them cac stage trung gian, ta co the danh gia sau hon:

- tung buoc co dong gop thuc su hay khong
- buoc nao co the dang gay tac dung phu
- thu tu sap xep cac buoc co hop ly hay khong

Day la mot cach danh gia co tinh ky thuat, giup kiem chung rang pipeline hien tai khong chi cho ket qua dep hon, ma con hoat dong dung theo muc tieu thiet ke.

## 10. Uu diem cua pipeline hien tai

- Don gian, de cai dat va de mo ta trong bao cao
- Toc do xu ly nhanh vi dung cac phep bien doi pho bien
- Phu hop voi anh y te don kenh nhu anh X-quang
- Co the hien thi ro cac giai doan trung gian de so sanh
- Nguoi dung co the dieu chinh tham so de thu nghiem

## 11. Han che

- Neu tham so khong phu hop, anh co the bi qua sang, qua gat, hoac qua net
- Pipeline hien tai chu yeu dua tren tang cuong cuong do, chua co buoc tu dong danh gia chat luong anh
- Chua phan biet tung loai anh X-quang khac nhau de tu dong chon tham so toi uu
- Neu anh dau vao chua nhieu, cac buoc tang cuong co the lam nhieu lo ro hon

## 12. Nhan xet tong ket

Ve mat ly thuyet, du an hien tai khong chi su dung rieng bien doi logarit, ma dung mot pipeline ket hop 3 ky thuat bo tro cho nhau:

- bien doi logarit de cai thien vung toi
- CLAHE de tang tuong phan cuc bo
- unsharp mask de lam sac bien

Su ket hop nay phu hop voi muc tieu tang cuong anh X-quang, vi no dong thoi tac dong len 3 khia canh quan trong cua anh:

- do sang
- do tuong phan
- do net

Day la mot huong tiep can can bang giua tinh de hieu, tinh de cai dat, va hieu qua thuc nghiem trong bai toan tang cuong anh y te.

Hiện tượng khi chỉnh từng tham số:

log_gain tăng:
vùng tối sáng lên rõ hơn, nhưng tăng quá sẽ kéo cả nhiễu lên và ảnh dễ bị gắt.

clip_limit tăng:
tương phản cục bộ mạnh hơn, chi tiết nổi hơn, nhưng quá cao thì ảnh dễ sần và “gắt”.

tile_grid_size tăng:
CLAHE tác động chi tiết hơn theo từng vùng nhỏ, nhưng quá lớn có thể làm ảnh kém tự nhiên hoặc lộ artifact cục bộ.

sharpen_amount tăng:
biên sắc hơn, nhưng quá mạnh có thể xuất hiện viền halo quanh cạnh và làm nhiễu rõ hơn.

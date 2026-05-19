# Bao cao hoi dap ve thuat toan tang cuong anh X-quang

## 1. De tai la gi?

De tai xay dung mot he thong tang cuong anh X-quang bang pipeline gom 3 ky thuat:

1. `Log Transform`
2. `CLAHE`
3. `Unsharp Mask`

Muc tieu la cai thien kha nang quan sat chi tiet trong anh, dac biet o vung toi, vung co tuong phan thap, va vung bien mo.

## 2. Tai sao can tang cuong anh X-quang?

Anh X-quang thuong co cac van de:

- vung toi kho quan sat
- tuong phan cuc bo chua cao
- bien xuong hoac ton thuong chua ro

Tang cuong anh giup bac si hoac nguoi hoc de nhin thay cau truc ro hon trong qua trinh phan tich va demo hoc thuat.

## 3. Pipeline cua he thong hoat dong the nao?

Anh dau vao duoc xu ly theo thu tu:

1. Chuan hoa va dua ve grayscale 8-bit
2. Ap dung `Log Transform`
3. Ap dung `CLAHE`
4. Ap dung `Unsharp Mask`
5. Xuat anh ket qua `enhanced`

Thu tu nay la co chu dich, vi moi buoc xu ly mot diem yeu khac nhau cua anh.

## 4. Log Transform la gi?

Log Transform la ky thuat bien doi muc xam theo ham log:

```text
s = 255 * log(1 + c * r) / log(1 + c)
```

Trong do:

- `r` la gia tri pixel da duoc chuan hoa trong `[0, 1]`
- `c` la he so dieu khien muc do tang cuong
- `s` la gia tri pixel sau bien doi

## 5. Tai sao dung Log Transform o buoc dau?

Log Transform co tac dung nang cac muc xam thap manh hon cac muc xam cao. Vi vay:

- vung toi duoc lam ro
- thong tin an trong bong toi duoc boc lo
- tao dau vao tot hon cho CLAHE

Neu bo qua buoc nay, CLAHE van co tac dung, nhung se khoi phuc vung toi kem hon.

## 6. CLAHE la gi?

CLAHE la viet tat cua `Contrast Limited Adaptive Histogram Equalization`.

Day la thuat toan tang tuong phan cuc bo theo tung o nho tren anh. Khac voi histogram equalization thong thuong, CLAHE:

- xu ly theo tung vung nho
- gioi han muc tang cuong bang `clip limit`
- giam nguy co lam noi nhieu qua muc

## 7. Tai sao CLAHE phu hop voi anh X-quang?

Anh X-quang co nhieu vung co do sang khac nhau. Tuong phan toan cuc khong du de lam ro het chi tiet. CLAHE phu hop vi:

- tang tuong phan theo vung
- lam ro chi tiet mo, xuong, va ton thuong cuc bo
- giu ket qua can bang hon so voi AHE thong thuong

## 8. Unsharp Mask la gi?

Unsharp Mask la ky thuat lam sac anh. Y tuong co ban:

1. Lam mo anh bang Gaussian blur
2. Lay sai khac giua anh goc va anh mo de tao mask bien
3. Cong mask do tro lai anh goc

Cong thuc:

```text
sharpened = original + amount * (original - blurred)
```

## 9. Tai sao Unsharp Mask dat o buoc cuoi?

Neu lam sac qua som:

- nhieu cung bi lam noi
- CLAHE sau do co the khuech dai them cac chi tiet khong mong muon

Dat Unsharp Mask o cuoi giup:

- lam sac tren anh da duoc tang sang va tang tuong phan
- nhan bien, canh, va cac duong mo ro hon

## 10. Ba buoc nay la cac thuat toan rieng hay bo tro nhau?

Day la 3 ky thuat rieng, nhung trong du an nay chung duoc ket hop thanh mot pipeline va bo tro nhau.

- `Log Transform` xu ly van de sang toi
- `CLAHE` xu ly van de tuong phan cuc bo
- `Unsharp Mask` xu ly van de do net

Anh `enhanced` la ket qua cuoi cung sau khi anh da di qua ca 3 buoc.

## 11. Tai sao khong dung tung thuat toan rieng le?

Neu chi dung tung thuat toan rieng:

- chi dung `Log Transform`: anh sang hon nhung chua chac ro chi tiet cuc bo
- chi dung `CLAHE`: tang tuong phan nhung vung qua toi van kho nhin
- chi dung `Unsharp Mask`: bien ro hon nhung nen toi va tuong phan thap van la van de

Ket hop 3 buoc cho ket qua can bang hon.

## 12. Y nghia cua cac tham so la gi?

### `log_gain`

- dieu khien muc tac dong cua Log Transform
- tang gia tri nay se nang manh vung toi hon

### `clip_limit`

- dieu khien muc gioi han tuong phan cua CLAHE
- qua cao co the lam anh gay va noi nhieu

### `tile_grid_size`

- kich thuoc luoi cuc bo cua CLAHE
- nho hon thi nhan manh tinh cuc bo
- lon hon thi ket qua mem hon

### `unsharp_amount`

- muc do lam sac
- qua lon co the tao vien gat hoac halo

## 13. Bo tham so nao nen dung ban dau?

Bo mac dinh trong he thong:

```text
log_gain = 4.0
clip_limit = 2.5
tile_grid_size = 8
unsharp_amount = 0.6
```

Bo goi y de demo nhe hon:

```text
log_gain = 3.0
clip_limit = 1.0
tile_grid_size = 4
unsharp_amount = 0.4
```

## 14. Du an co uu diem gi?

- Cau truc don gian, de trinh bay
- Pipeline ro rang, moi buoc co vai tro cu the
- Ho tro ca CLI va web local
- Xuat duoc anh trung gian de de so sanh

## 15. Han che cua du an la gi?

- Chu yeu toi uu cho anh grayscale kieu X-ray
- Chua ho tro DICOM day du
- Chua co do luong chat luong bang tap chi so chuyen sau
- Neu tham so qua manh, anh co the bi noi nhieu hoac qua sac

## 16. Du an duoc cai dat the nao trong ma nguon?

Phan chinh nam o:

- `src/algorithms/medical_pipeline.py`

File nay dinh nghia:

- `EnhancementConfig`: luu 4 tham so
- `MedicalEnhancement`: lop xu ly chinh
- `run_on_image()`: xu ly 1 anh va tra ve `original`, `log`, `clahe`, `enhanced`

CLI duoc dieu phoi boi:

- `src/arguments.py`
- `src/algorithms/runner.py`

Web app local nam o:

- `streamlit_app.py`

## 17. Tai sao du an xuat ca `original`, `log`, `clahe`, `enhanced`?

Vi day la cach tot nhat de giai thich dong xu ly:

- `original`: anh goc
- `log`: ket qua sau khi nang vung toi
- `clahe`: ket qua sau khi tang tuong phan cuc bo
- `enhanced`: ket qua sau khi lam sac

Khi bao cao, ban co the dat 4 anh nay canh nhau de minh hoa ro vai tro cua tung buoc.

## 18. Ket luan

Pipeline `Log Transform -> CLAHE -> Unsharp Mask` la mot cach tiep can phu hop cho bai toan tang cuong anh X-quang muc do co ban den trung binh. Moi buoc giai quyet mot van de rieng cua anh, va khi ket hop lai, chung tao ra mot ket qua de quan sat hon so voi tung ky thuat dung rieng le.

## 19. Goi y cau hoi bao ve va cau tra loi ngan

### Hoi: Vi sao khong dung deep learning?

Tra loi: Muc tieu cua de tai la minh hoa cac ky thuat xu ly anh co dien, de cai dat, de giai thich, va phu hop voi bai tap hoc thuat co ban.

### Hoi: Tai sao chon CLAHE ma khong phai histogram equalization thuong?

Tra loi: CLAHE tang tuong phan theo tung vung cuc bo va co co che clip limit, nen phu hop hon voi anh y te co nhieu vung do sang khac nhau.

### Hoi: Tai sao ket qua cuoi trong code ten la `enhanced`?

Tra loi: Vi day la anh ket qua sau khi di qua toan bo pipeline, khong phai ten cua mot thuat toan rieng.

### Hoi: Neu tham so qua lon thi sao?

Tra loi: Anh co the qua sang, qua gac, noi nhieu, hoac xuat hien vien halo quanh bien.

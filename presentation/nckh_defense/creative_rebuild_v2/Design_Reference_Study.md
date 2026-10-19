# Design Reference Study

Ngày19/10/2026. Thực hiện browser Chromium thật, scroll nhiều vị trí, chụp viewport1440×900. Browser mặc định lỗi module missing; Chrome DevTools không tìm thấyChrome; fallback Playwright trong context độc lập. Không dùng profile/session người dùng.

## Lollypop Design / Designathon2026
Hai URL trả CAPTCHA trong browser. Ảnh references/lollypop_*.png là bằng chứng bị chặn, KHÔNG phải ảnh hero/scroll của website. Chưa xác minh kinetic typography hay quán tính cuộn thực tế. Nội dung văn bản công khai tra cứu được mô tả typography tách chữ,24H,4sectionchủđề và cấu trúc landing page; chỉ sử dụng như thông tin thứ cấp về cấu trúc, không giả định đã quan sát motion. Không bypass CAPTCHA, không sao assets/logo/story của sự kiện vào IDS.

## Awwwards
https://www.awwwards.com/ hiển thị được. references/awwwards_00.png: heading SIGNAL-A STUDIO rất lớn, cùng một baseline, metadata nhỏ và khung project đen. Scroll900px (awwwards_01.png): đổi thang từ giant-heading sang nội dung/khungproject và heading section kế. Điểm lấy: tỷ lệ chữ tương phản mạnh, editorial hierarchy và thay đổi mật độ. Không lấy UIbuttoncookie hay project screenshot làm slide.

## Active Theory
https://activetheory.net/ browser hiển thị không hỗ trợ, cùng nền particle và vật thể vòng; chưa vào được trải nghiệm tương tác đầy đủ. Chỉ lấy nguyên tắc chiều sâu và một vật thể trung tâm từ trạng thái nhìn thấy, không nói đã quan sát camera/scroll đầy đủ. Không cần3D cho pipeline IDS.

## Locomotive / Behance
Locomotive403challenge, không bypass. Behance ghi kết quả trong browser_ledger.json; nếu chặn thì không dùng làm chứng cứ trực quan. Các nguồn này chỉ được khảo sát, không tuyên bố đã thực thi hoặc sử dụng mã.

## Dịch reference sang PowerPoint
Pinnedsection→giữ một canvas và dùng internaltimeline để dữliệu đi xuyên node. Scrollreveal→node/nhãn xuất hiện theo cue. Giantheading→con số−142/+118 chiếm vùnghero cùng scope nhỏ đọc được. Layeredhero→vòng/vector/foldmatrix có thứbậc; không ảnhAI. Variableinertia→ease motionpath; không đụng vào giá trịthật. Colorarc→creamởbài toán,inkởmáyhọc,coralởFN,limeởđốichứng;trục vàýnghĩamàu nhấtquán.

Ba concept sẽ được thử bằng nativePowerPointanimation thật, không chỉ ảnh. Nguồn chính https://lollypop.design/ và https://lollypop.design/designathon2026/ còn hạn chế truy cập đã ghi rõ.

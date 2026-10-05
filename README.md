# Paperform Document Tools

เว็บแอป Python สำหรับตรวจคำผิดภาษาไทย/อังกฤษในไฟล์ PDF และ DOCX รวมถึงรวมไฟล์ PDF โดยใช้ Streamlit, PyThaiNLP และ pypdf

## เริ่มใช้งาน

```powershell
python -m pip install -r requirements.txt
python -m streamlit run Home.py
```

เปิด `http://localhost:8501` เพื่อเลือกเครื่องมือจากหน้าแรกหรือเมนูด้านข้าง

ไฟล์ `dictionary.json` และ `common_mistakes.json` จะถูกโหลดจากโฟลเดอร์เดียวกับ `App_Spell.py` ส่วน PDF Merger จำกัดขนาดรวมไว้ที่ 100 MB

## Deploy บน Streamlit Community Cloud

1. Push โปรเจกต์ขึ้น GitHub โดยให้ `Home.py`, `pages/`, `App_Spell.py`, ไฟล์ JSON และ `requirements.txt` อยู่ใน repository
2. ใน Streamlit Community Cloud เลือก **Create app** แล้วเชื่อม repository, branch และไฟล์หลัก `Home.py`
3. Deploy แล้วตรวจ URL ที่ Cloud สร้างให้

ไฟล์ที่อัปโหลดจะถูกส่งไปประมวลผลบนเซิร์ฟเวอร์ของแอป ไม่ใช่บนเครื่องผู้ใช้ ควรใช้ repository แบบ Private หากไฟล์คลังคำหรือ source ไม่ควรเปิดเผย และหลีกเลี่ยงอัปโหลดเอกสารที่มีข้อมูลอ่อนไหว

## ทดสอบ

```powershell
python -m unittest discover -v
```

`app.py` ยังมี Flask endpoint สำหรับการทดสอบ/ใช้งานแยก แต่เว็บรวมบน Streamlit ไม่ต้องเปิด Flask service เพิ่ม
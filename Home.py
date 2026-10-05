import streamlit as st


st.set_page_config(
    page_title="Paperform | เครื่องมือเอกสาร",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1120px; padding-top: 3rem; }
    .eyebrow { color: #315d4c; font-size: .78rem; font-weight: 700; letter-spacing: .08em; }
    .hero-title { color: #202b28; font-family: Georgia, "Leelawadee UI", Tahoma, serif; font-size: clamp(2.8rem, 6vw, 4.8rem); line-height: 1.1; }
    .hero-title span { color: #d7795d; }
    .hero-copy { color: #727a73; font-size: 1rem; margin: 1rem 0 2rem; }
    .tool-label { color: #d7795d; font-size: .76rem; font-weight: 700; }
    </style>
    <p class="eyebrow">PAPERFORM / DOCUMENT TOOLS</p>
    <div class="hero-title">จัดการเอกสาร<br><span>ได้ในที่เดียว</span></div>
    <p class="hero-copy">เลือกเครื่องมือสำหรับตรวจคำหรือจัดการ PDF</p>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        st.markdown('<p class="tool-label">01 / ตรวจภาษา</p>', unsafe_allow_html=True)
        st.subheader("ตรวจคำผิดในเอกสาร")
        st.write("ตรวจข้อความภาษาไทยและอังกฤษจากไฟล์ PDF หรือ DOCX พร้อมดูตำแหน่งและส่งออกรายงาน")
        st.page_link("pages/spell_check.py", label="เปิดระบบตรวจคำ", icon=":material/spellcheck:")

with right:
    with st.container(border=True):
        st.markdown('<p class="tool-label">02 / จัดการ PDF</p>', unsafe_allow_html=True)
        st.subheader("รวมไฟล์ PDF")
        st.write("เลือกหลายไฟล์ จัดลำดับหน้าเอกสาร แล้วดาวน์โหลดเป็น PDF ไฟล์เดียว")
        st.page_link("pages/pdf_merger.py", label="เปิดเครื่องมือรวม PDF", icon=":material/picture_as_pdf:")

st.divider()
st.caption("ไฟล์ที่เลือกจะถูกส่งไปประมวลผลบนเซิร์ฟเวอร์ของแอป โปรดหลีกเลี่ยงเอกสารที่มีข้อมูลอ่อนไหว")
import streamlit as st
import html

from pdf_utils import MAX_MERGE_SIZE, merge_pdf_files


st.set_page_config(page_title="รวมไฟล์ PDF | Paperform", page_icon="📄", layout="wide")

st.markdown(
	"""
	<style>
	.block-container { max-width: 1120px; padding-top: 2rem; }
	[data-testid="stAppViewContainer"] { background: #f5f4ef; }
	.paper-topbar { display:flex; justify-content:space-between; align-items:center; padding:0 0 1rem; border-bottom:1px solid #dcded7; color:#202b28; }
	.paper-brand { font-size:1.1rem; font-weight:700; }
	.paper-local { color:#57665d; font-size:.78rem; }
	.paper-eyebrow { margin:2.5rem 0 .5rem; color:#315d4c; font-size:.72rem; font-weight:700; letter-spacing:.08em; }
	.paper-title { margin:0; color:#202b28; font-family:Georgia,"Leelawadee UI",Tahoma,serif; font-size:clamp(2.7rem,6vw,4.25rem); font-weight:500; line-height:1.15; }
	.paper-title em { color:#d7795d; font-weight:400; }
	.paper-copy { margin:.9rem 0 2rem; color:#727a73; font-size:.9rem; }
	.drop-caption { padding:1rem 0 .5rem; color:#202b28; font-weight:700; }
	.file-row { display:flex; align-items:center; gap:12px; min-height:58px; padding:.45rem 0; border-bottom:1px solid #e5e5df; }
	.pdf-mark { display:grid; place-items:center; width:34px; height:38px; border:1px solid #e7bbae; border-radius:4px; background:#f9eae5; color:#bd694f; font-size:.62rem; font-weight:700; }
	.file-name { overflow:hidden; color:#303a35; font-size:.83rem; font-weight:600; text-overflow:ellipsis; white-space:nowrap; }
	.file-size { color:#888e86; font-size:.7rem; }
	.section-heading { padding-bottom:.55rem; border-bottom:1px solid #dcded7; color:#202b28; font-size:.86rem; font-weight:700; }
	.summary-title { margin:0 0 1rem; color:#657067; font-size:.78rem; font-weight:700; }
	.summary-note { margin:1.2rem 0; padding:.8rem 0; border-top:1px solid #dcded7; border-bottom:1px solid #dcded7; color:#7b817a; font-size:.72rem; line-height:1.6; }
	[data-testid="stFileUploaderDropzone"] { min-height:145px; border:1px dashed #aeb8ad; border-radius:7px; background:#fbfaf6; }
	[data-testid="stFileUploaderDropzone"]:hover { border-color:#315d4c; background:#eef2ec; }
	@media(max-width:700px) { .paper-eyebrow { margin-top:1.6rem; } .paper-copy { margin-bottom:1.2rem; } }
	</style>
	<div class="paper-topbar"><span class="paper-brand">paperform</span><span class="paper-local">PDF MERGER</span></div>
	<p class="paper-eyebrow">เครื่องมือจัดการเอกสาร · PDF</p>
	<h1 class="paper-title">รวมเอกสาร<br><em>ในลำดับของคุณ</em></h1>
	<p class="paper-copy">วางไฟล์ PDF เรียงตามต้องการ แล้วรวมเป็นไฟล์เดียวได้ทันที</p>
	""",
	unsafe_allow_html=True,
)

if "pdf_merge_files" not in st.session_state:
	st.session_state.pdf_merge_files = []
if "pdf_merge_seen_ids" not in st.session_state:
	st.session_state.pdf_merge_seen_ids = set()
if "pdf_merge_upload_version" not in st.session_state:
	st.session_state.pdf_merge_upload_version = 0
if "pdf_merge_result" not in st.session_state:
	st.session_state.pdf_merge_result = None

uploaded_files = st.file_uploader(
	"ลากไฟล์มาวางที่นี่ หรือเลือกไฟล์จากเครื่อง",
	type=["pdf"],
	accept_multiple_files=True,
	help="PDF เท่านั้น · ขนาดรวมสูงสุด 100 MB",
	key=f"pdf_merge_uploader_{st.session_state.pdf_merge_upload_version}",
)

upload_error = None
for uploaded_file in uploaded_files or []:
	if uploaded_file.file_id in st.session_state.pdf_merge_seen_ids:
		continue
	st.session_state.pdf_merge_seen_ids.add(uploaded_file.file_id)
	content = uploaded_file.getvalue()
	current_size = sum(len(item["data"]) for item in st.session_state.pdf_merge_files)
	if current_size + len(content) > MAX_MERGE_SIZE:
		upload_error = "ไฟล์รวมมีขนาดเกิน 100 MB"
		continue
	st.session_state.pdf_merge_files.append(
		{"id": uploaded_file.file_id, "name": uploaded_file.name, "data": content}
	)
	st.session_state.pdf_merge_result = None

if upload_error:
	st.error(upload_error)

file_column, summary_column = st.columns([2.5, 1], gap="large")
files = st.session_state.pdf_merge_files

with file_column:
	st.markdown('<div class="section-heading">ไฟล์ที่เลือก</div>', unsafe_allow_html=True)
	if not files:
		st.caption("รายการของคุณจะปรากฏตรงนี้")

	for index, item in enumerate(files):
		row_columns = st.columns([0.12, 1, 0.12, 0.12, 0.12, 0.12], vertical_alignment="center")
		with row_columns[0]:
			st.markdown('<div class="pdf-mark">PDF</div>', unsafe_allow_html=True)
		with row_columns[1]:
			st.markdown(
				f'<div class="file-name">{html.escape(item["name"])}</div>'
				f'<div class="file-size">{len(item["data"]) / 1024:.0f} KB</div>',
				unsafe_allow_html=True,
			)
		with row_columns[2]:
			if st.button("↑", key=f"pdf_up_{index}", help="เลื่อนขึ้น", disabled=index == 0):
				files[index - 1], files[index] = files[index], files[index - 1]
				st.session_state.pdf_merge_result = None
				st.rerun()
		with row_columns[3]:
			if st.button("↓", key=f"pdf_down_{index}", help="เลื่อนลง", disabled=index == len(files) - 1):
				files[index + 1], files[index] = files[index], files[index + 1]
				st.session_state.pdf_merge_result = None
				st.rerun()
		with row_columns[4]:
			if st.button("×", key=f"pdf_remove_{index}", help="นำไฟล์ออก"):
				files.pop(index)
				st.session_state.pdf_merge_seen_ids = set()
				st.session_state.pdf_merge_upload_version += 1
				st.session_state.pdf_merge_result = None
				st.rerun()

with summary_column:
	total_size = sum(len(item["data"]) for item in files)
	st.markdown('<div class="summary-title">01　สรุปงาน</div>', unsafe_allow_html=True)
	stat_files, stat_size = st.columns(2)
	stat_files.metric("จำนวนไฟล์", len(files))
	stat_size.metric("ขนาดรวม", f"{total_size / 1024:.0f} KB" if total_size < 1024 * 1024 else f"{total_size / 1024 / 1024:.1f} MB")
	st.markdown(
		'<div class="summary-note">ไฟล์จะถูกส่งไปประมวลผลบนเซิร์ฟเวอร์ของแอปชั่วคราว เพื่อสร้างไฟล์ PDF ที่รวมแล้ว</div>',
		unsafe_allow_html=True,
	)

	if st.button("รวมไฟล์ PDF　→", type="primary", use_container_width=True, disabled=len(files) < 2):
		try:
			st.session_state.pdf_merge_result = merge_pdf_files(
				[(item["name"], item["data"]) for item in files]
			)
		except ValueError as error:
			st.error(str(error))

	if st.session_state.pdf_merge_result:
		st.download_button(
			"ดาวน์โหลด merged.pdf",
			data=st.session_state.pdf_merge_result,
			file_name="merged.pdf",
			mime="application/pdf",
			use_container_width=True,
		)
	elif len(files) < 2:
		st.caption("เลือกอย่างน้อย 2 ไฟล์เพื่อเริ่ม")

if files:
	if st.button("ล้างรายการ", type="secondary"):
		st.session_state.pdf_merge_files = []
		st.session_state.pdf_merge_seen_ids = set()
		st.session_state.pdf_merge_upload_version += 1
		st.session_state.pdf_merge_result = None
		st.rerun()
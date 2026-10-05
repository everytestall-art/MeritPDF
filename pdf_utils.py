from io import BytesIO

from pypdf import PdfReader, PdfWriter


MAX_MERGE_SIZE = 100 * 1024 * 1024


def merge_pdf_files(files: list[tuple[str, bytes]]) -> bytes:
    if len(files) < 2:
        raise ValueError("กรุณาเลือกไฟล์ PDF อย่างน้อย 2 ไฟล์")

    if sum(len(content) for _, content in files) > MAX_MERGE_SIZE:
        raise ValueError("ไฟล์รวมมีขนาดเกิน 100 MB")

    writer = PdfWriter()
    for filename, content in files:
        if not filename.lower().endswith(".pdf"):
            raise ValueError(f"{filename or 'ไฟล์ที่เลือก'} ไม่ใช่ไฟล์ PDF")
        if not content:
            raise ValueError(f"{filename} เป็นไฟล์ว่าง")

        try:
            reader = PdfReader(BytesIO(content), strict=False)
            if reader.is_encrypted:
                raise ValueError(f"{filename} มีการป้องกันด้วยรหัสผ่าน")
            writer.append(reader)
        except ValueError:
            raise
        except Exception as error:
            raise ValueError(
                f"ไม่สามารถอ่าน {filename} ได้ โปรดตรวจสอบว่าไฟล์ไม่เสียหาย"
            ) from error

    output = BytesIO()
    writer.write(output)
    return output.getvalue()
import io
import unittest

from pypdf import PdfReader, PdfWriter

from app import create_app


def make_pdf(page_count):
    writer = PdfWriter()
    for _ in range(page_count):
        writer.add_blank_page(width=72, height=72)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


class PdfMergerTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_merges_uploaded_pdfs_in_the_given_order(self):
        response = self.client.post(
            "/merge",
            data={
                "files": [
                    (io.BytesIO(make_pdf(1)), "first.pdf"),
                    (io.BytesIO(make_pdf(2)), "second.pdf"),
                ]
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        self.assertEqual(len(PdfReader(io.BytesIO(response.data)).pages), 3)

    def test_requires_at_least_two_pdfs(self):
        response = self.client.post(
            "/merge",
            data={"files": (io.BytesIO(make_pdf(1)), "one.pdf")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("อย่างน้อย 2", response.json["error"])

    def test_rejects_invalid_pdf_content(self):
        response = self.client.post(
            "/merge",
            data={
                "files": [
                    (io.BytesIO(b"not a pdf"), "broken.pdf"),
                    (io.BytesIO(make_pdf(1)), "valid.pdf"),
                ]
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("ไม่สามารถอ่าน", response.json["error"])


if __name__ == "__main__":
    unittest.main()
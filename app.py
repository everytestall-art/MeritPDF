from io import BytesIO

from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge

from pdf_utils import MAX_MERGE_SIZE, merge_pdf_files


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_MERGE_SIZE

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/merge")
    def merge_pdfs():
        files = request.files.getlist("files")
        try:
            merged_pdf = merge_pdf_files(
                [(uploaded.filename or "", uploaded.read()) for uploaded in files]
            )
        except ValueError as error:
            return jsonify(error=str(error)), 400

        return send_file(
            BytesIO(merged_pdf),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="merged.pdf",
        )

    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(_error):
        return jsonify(error="ไฟล์รวมมีขนาดเกิน 100 MB"), 413

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
FROM surnet/alpine-python-wkhtmltopdf:3.7.3-0.12.5-small

RUN apk --no-cache add gcc libc-dev libxml2-dev libxslt-dev
RUN pip3 install --upgrade PyPDF2 lxml pdfkit argparse

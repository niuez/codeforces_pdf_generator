from urllib import request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import PyPDF2
import lxml.html
import pdfkit
import re
import sys

javascript_delay = 2500

class CFProblem:
    def get_problem_id(url):
        m = re.match(r'/contest/([0-9]+)/problem/([A-Z0-9]+)', urlparse(url).path)
        return m.groups()[0] + m.groups()[1]

    def __init__(self, url):
        print("load codeforces problem %s" % url)
        html = request.urlopen(url)
        self.problem_id = CFProblem.get_problem_id(url)
        self.pdf_name = 'CF' + self.problem_id + '.pdf'
        self.dom = lxml.html.fromstring(html.read())

        base_tag = lxml.html.Element('base', href="https://%s" % urlparse(url).netloc)
        style_tag = lxml.html.Element('style')
        style_tag.text = '#pageContent>*:not(.problemindexholder) { display: none !important; } #header { display: none; } #footer { display: none; } .roundbox.menu-box { display: none; } #sidebar { display: none; } #body > br:nth-child(8) { display: none; } #pageContent { margin-right: 0 !important; } #body { padding-top: 0; } #MathJax_Message { display: none !important; }'
        html_tag = self.dom.xpath("//html")
        self.dom.xpath('//html')[0].insert(0, base_tag)
        self.dom.xpath('//head')[0].append(style_tag)

    def save_as_pdf(self):
        print("saving problem %s as pdf" % self.problem_id)
        options = {
            'page-size': 'A4',
            'margin-top': '0.1in',
            'margin-right': '0.1in',
            'margin-bottom': '0.1in',
            'margin-left': '0.1in',
            'encoding': "UTF-8",
            'javascript-delay': str(javascript_delay),
            'no-outline': None
        }
        html_source = lxml.html.tostring(self.dom).decode('utf-8')
        pdfkit.from_string(html_source, self.pdf_name, options=options)

class CFContest:
    def get_contest_id(url):
        m = re.match(r'/contest/([0-9]+)', urlparse(url).path)
        return m.groups()[0]
    def __init__(self, url):
        print("load codeforces contest %s" % url)
        base = urlparse(url).netloc
        html = request.urlopen(url)
        self.dom = lxml.html.fromstring(html.read())
        self.contest_id = CFContest.get_contest_id(url)
        self.pdf_name = "CF" + self.contest_id + ".pdf"
        self.problems = []
        for problem_a_tag in self.dom.xpath('//table[@class="problems"]/tr[position() > 1]/td[1]/a'):
            self.problems.append(CFProblem("https://" + base + problem_a_tag.attrib['href']))

    def save_as_pdf(self):
        print("saving contest %s as pdf" % self.contest_id)
        merger = PyPDF2.PdfFileMerger()
        for problem in self.problems:
            problem.save_as_pdf()
            merger.append(problem.pdf_name)
        merger.write(self.pdf_name)
        merger.close()

if __name__ == '__main__':
    url = 'https://codeforces.com/contest/1285/'
    contest = CFContest(url)
    contest.save_as_pdf()
    #url = 'https://codeforces.com/contest/1285/problem/A'
    #prob = CFProblem(url)
    #prob.save_as_pdf()

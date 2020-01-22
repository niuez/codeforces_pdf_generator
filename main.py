from urllib import request
from urllib.parse import urlparse
import PyPDF2
import lxml.html
import pdfkit
import re
import sys
import argparse
import os

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
        self.contest_name = self.dom.xpath('//*[@id="sidebar"]/div[1]/table/tbody/tr[1]/th/a')[0].text

        base_tag = lxml.html.Element('base', href="https://%s" % urlparse(url).netloc)
        style_tag = lxml.html.Element('style')
        style_tag.text = '#pageContent>*:not(.problemindexholder) { display: none !important; } #header { display: none; } #footer { display: none; } .roundbox.menu-box { display: none; } #sidebar { display: none; } #body > br:nth-child(8) { display: none; } #pageContent { margin-right: 0 !important; } #body { padding-top: 0; } #MathJax_Message { display: none !important; }'
        self.dom.xpath('//html')[0].insert(0, base_tag)
        self.dom.xpath('//head')[0].append(style_tag)

        contest_tag = lxml.html.Element('div')
        contest_tag.text = self.contest_name
        #contest_tag.attrib['class'] = 'title'
        contest_tag.attrib['style'] = 'text-align: left;'
        self.dom.xpath('//*[@class="header"]')[0].insert(0, contest_tag)


    def save_as_pdf(self):
        options = {
            'page-size': 'A4',
            'margin-top': '0.1in',
            'margin-right': '0.1in',
            'margin-bottom': '0.1in',
            'margin-left': '0.1in',
            'encoding': "UTF-8",
            'javascript-delay': str(javascript_delay),
            'no-outline': None,
            #'quiet': None,
        }
        html_source = lxml.html.tostring(self.dom).decode('utf-8')
        pdfkit.from_string(html_source, self.pdf_name, options=options)
        print("saved problem %s as pdf %s" % (self.problem_id, self.pdf_name))

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
        merger = PyPDF2.PdfFileMerger()
        for problem in self.problems:
            problem.save_as_pdf()
            merger.append(problem.pdf_name)
        merger.write(self.pdf_name)
        merger.close()

        for problem in self.problems:
            os.remove("./" + str(problem.pdf_name))
            
        print("saved contest %s as pdf %s" % (self.contest_id, self.pdf_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This scirpt is to generate PDF of problems on codeforces.')
    parser.add_argument('contest_id', \
        action='store', \
        nargs=None, \
        const=None, \
        default=None, \
        type=str, \
        choices=None, \
        help='Contest ID', \
        metavar=None)
    parser.add_argument('-p', '--problems', \
        action='store', \
        nargs='+', \
        const=None, \
        default=None, \
        type=str, \
        choices=None, \
        help='Problems', \
        metavar=None)
    args = parser.parse_args()
    if args.problems == None:
        url = 'https://codeforces.com/contest/%s/' % args.contest_id
        contest = CFContest(url)
        contest.save_as_pdf()
    else:
        for problem_id in args.problems:
            url = 'https://codeforces.com/contest/%s/problem/%s' % (args.contest_id, problem_id)
            problem = CFProblem(url)
            problem.save_as_pdf()

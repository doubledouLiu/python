import re
import csv
import time
from PySide.QtCore import QUrl, QEventLoop, QTimer
from PySide.QtGui import QApplication
from PySide.QtWebKit import QWebView


class BrowserRender(QWebView):
    def __init__(self, display=True):
        self.app = QApplication([])
        self.view = QWebView()
        self.loop = QEventLoop()

    def open(self, url, timeout=60):
        self.view.loadFinished.connect(self.loop.quit)
        self.view.load(QUrl(url))
        self.loop.exec_()
        self.view.show()

    def html(self):
        return self.view.page().mainFrame().toHtml()

    def find(self, pattern):
        return self.view.page().mainFrame().findAllElements(pattern)

    def attr(self, pattern, name, value):
        for e in self.find(pattern):
            e.setAttribute(name, value)

    def text(self, pattern, value):
        for e in self.find(pattern):
            e.setPlainText(value)

    def click(self, pattern):
        for e in self.find(pattern):
            e.evaluateJavaScript('this.click()')

    def wait_load(self, pattern, timeout=60):
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.app.processEvents()
            matches = self.find(pattern)
            if matches:
                return matches
        print 'Wait load time out'

    def exec_(self):
        self.app.exec_()


def main():
    br = BrowserRender()
    br.open('http://example.webscraping.com/search')
    br.attr('#search_term', 'value', '.')
    br.text('#page_size option:selected', 1000)
    br.click('#search')
    br.exec_()
    elements = br.wait_load('#results a')
    writer = csv.writer(open('continue.csv', 'w'))
    for country in [e.toPlainText().strip() for e in elements]:
        writer.writerow([country])


if __name__ == '__main__':
    main()
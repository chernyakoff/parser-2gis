from types import SimpleNamespace

from parser_2gis.chrome.browser import ChromeBrowser
from parser_2gis.chrome.options import ChromeOptions


class DummyPopen:
    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        self.kwargs = kwargs

    def poll(self):
        return None

    def terminate(self):
        return None

    def wait(self):
        return 0


def make_browser(monkeypatch, os_name):
    monkeypatch.setattr('parser_2gis.chrome.browser.locate_chrome_path', lambda: '/tmp/chrome')
    monkeypatch.setattr('parser_2gis.chrome.browser.free_port', lambda: 9222)
    monkeypatch.setattr('parser_2gis.chrome.browser.tempfile.mkdtemp', lambda: '/tmp/profile')
    monkeypatch.setattr('parser_2gis.chrome.browser.subprocess.Popen', DummyPopen)
    monkeypatch.setattr('parser_2gis.chrome.browser.os', SimpleNamespace(name=os_name, path=__import__('os').path))
    return ChromeBrowser(ChromeOptions())


def test_windows_browser_does_not_use_no_sandbox(monkeypatch):
    browser = make_browser(monkeypatch, 'nt')
    assert '--no-sandbox' not in browser._chrome_cmd


def test_non_windows_browser_uses_no_sandbox(monkeypatch):
    browser = make_browser(monkeypatch, 'posix')
    assert '--no-sandbox' in browser._chrome_cmd

import unittest
import threading
from http.server import HTTPServer
import urllib.request
import urllib.error
import json

# Строгое требование: если src/server.py удален, этот импорт ломается и тест гарантированно падает!
from src.server import ShortenerHandler, url_db

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Очищаем "БД"
        url_db.clear()
        
        # Поднимаем сервер на случайном свободном порту для тестов
        cls.server = HTTPServer(('127.0.0.1', 0), ShortenerHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_root(self):
        req = urllib.request.Request(f'http://127.0.0.1:{self.port}/')
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)

    def test_healthz(self):
        req = urllib.request.Request(f'http://127.0.0.1:{self.port}/healthz')
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data['status'], 'ok')

    def test_shorten_and_redirect(self):
        # 1. Создаем короткую ссылку
        target_url = "https://example.com/"
        data = json.dumps({"url": target_url}).encode('utf-8')
        req = urllib.request.Request(
            f'http://127.0.0.1:{self.port}/shorten', 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            resp_data = json.loads(response.read().decode())
            short_id = resp_data['short_id']
            self.assertIn(short_id, url_db)
            
        # 2. Проверяем редирект (запрещаем urllib переходить по ссылке, чтобы проверить сам код 307)
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None 

        opener = urllib.request.build_opener(NoRedirectHandler())
        try:
            opener.open(f'http://127.0.0.1:{self.port}/{short_id}')
            self.fail("Should have redirected")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 307)
            self.assertEqual(e.headers.get('Location'), target_url)

if __name__ == '__main__':
    unittest.main()

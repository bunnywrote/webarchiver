import threading
import urllib.request as ul

class asyncDownload(threading.Thread):

   def __init__(self,url,http_timeout):
      threading.Thread.__init__(self)
      self.url = url
      self.http_timeout = http_timeout

   def run(self):
      self.dataToWrite = ul.urlopen(self.url,timeout=self.http_timeout).read()
      print(self.dataToWrite)


url = 'http://www.yahoo.com'
thread = asyncDownload(url,10)
thread.run()
print('this thread is still running')
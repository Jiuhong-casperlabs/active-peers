import concurrent.futures
import urllib.request
from stress_rpc import myfunc, choose_node
URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://nonexistent-subdomain.python.org/']

# Retrieve a single page and report the URL and contents


def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


# We can use a with statement to ensure threads are cleaned up promptly
# max_workers=50 is good
# max_workers=75 is good
# max_workers=100 is good
# max_workers=250 bad
with concurrent.futures.ThreadPoolExecutor(max_workers=75) as executor:
    # Start the load operations and mark each future with its URL
    node_ip = choose_node()
    future_to_url = {executor.submit(
        myfunc, node_ip, x): x for x in range(100000)}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))

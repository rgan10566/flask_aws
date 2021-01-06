from flask import Flask
from collections import Counter
app = Flask(__name__)
@app.route('/countme/<input_str>')
#def hello_world():
#  return 'Hello from Flask! Done by Ramesh G'
def count_me(input_str):
    return '<br>'.join('"{}": {}'.format(let, cnt)
                   for let, cnt in Counter(input_str).most_common())
#    return Counter(input_str).most_common()

if __name__ == '__main__':
  app.run()

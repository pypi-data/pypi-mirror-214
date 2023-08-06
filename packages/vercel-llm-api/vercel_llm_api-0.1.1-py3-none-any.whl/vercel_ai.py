#import requests
import logging
import re
import json
import base64
import quickjs
import queue
import threading
from curl_cffi import requests

logging.basicConfig()
logger = logging.getLogger()

class Client:
  base_url = "https://play.vercel.ai"
  token_url = base_url + "/openai.jpeg" #nice try vercel
  generate_url = base_url + "/api/prompt"

  def __init__(self):
    self.session = requests.Session(impersonate="chrome110")
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "en-US,en;q=0.5",
      "Te": "trailers",
      "Upgrade-Insecure-Requests": "1"
    }
    self.session.headers.update(self.headers)

    self.models = self.get_models()
    self.model_ids = list(self.models.keys())
    self.model_defaults = {}
    for model_id in self.models:
      self.model_defaults[model_id] = self.get_default_params(model_id)

  def get_models(self):
    logger.info("Downloading homepage...")
    html = self.session.get(self.base_url).text
    paths_regex = r'static\/chunks.+?\.js'
    separator_regex = r'"\]\)<\/script><script>self\.__next_f\.push\(\[.,"'

    paths = re.findall(paths_regex, html)
    for i in range(len(paths)):
      paths[i] = re.sub(separator_regex, "", paths[i])
    paths = list(set(paths))

    for path in paths:
      script_url = f"{self.base_url}/_next/{path}"
      logger.info(f"Downloading and parsing {script_url}...")

      script = self.session.get(script_url).text
      models_regex = r'let .="\\n\\nHuman:\",r=(.+?),.='
      matches = re.findall(models_regex, script)

      if matches:
        models_str = matches[0]
        stop_sequences_regex = r'(?<=stopSequences:{value:\[)\D(?<!\])'
        models_str = re.sub(stop_sequences_regex, re.escape('"\\n\\nHuman:"'), models_str)

        context = quickjs.Context()
        json_str = context.eval(f"({models_str})").json()
        return json.loads(json_str)
    
    return []

  def get_token(self):
    logger.info("Fetching token from "+self.token_url)
    b64 = self.session.get(self.token_url).text
    data = json.loads(base64.b64decode(b64))

    script = """
      var globalThis = {{data: "sentinel"}};
      ({script})({key})
    """.format(script=data["c"], key=data["a"])
    
    context = quickjs.Context()
    token_data = json.loads(context.eval(script).json())
    token = {
      "r": token_data,
      "t": data["t"]
    }
    token_string = json.dumps(token, separators=(',', ':')).encode()
    return base64.b64encode(token_string).decode()

  def get_default_params(self, model_id):
    model = self.models[model_id]
    defaults = {}
    for key, param in model["parameters"].items():
      defaults[key] = param["value"]
    return defaults

  def generate(self, model_id, prompt, params={}):
    logger.info(f"Sending to {model_id}: {prompt}")

    token = self.get_token()
    defaults = self.get_default_params(model_id)
    payload = {**defaults, **params, **{
      "prompt": prompt,
      "model": model_id,
    }}

    headers = {**self.headers, **{
      "Accept-Encoding": "gzip, deflate, br",
      "Custom-Encoding": token,
      "Host": "play.vercel.ai",
      "Origin": "https://play.vercel.ai",
      "Referrer": "https://play.vercel.ai",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
    }}

    #bad streaming workaround cause the tls library doesn't support it
    logger.info(f"Waiting for server response")

    chunks_queue = queue.Queue()
    error = None
    response = None

    def callback(data):
      chunks_queue.put(data.decode())
    def request_thread():
      nonlocal response, error
      try:
        response = self.session.post(self.generate_url, json=payload, headers=headers, content_callback=callback)
        response.raise_for_status()
      except Exception as e:
        error = e
    
    thread = threading.Thread(target=request_thread, daemon=True)
    thread.start()
    
    text = ""
    index = 0
    while True:
      try:
        chunk = chunks_queue.get(block=True, timeout=0.1)
      except queue.Empty:
        if error:
          raise error
        elif response:
          break
        else:
          continue

      text += chunk
      lines = text.split("\n")

      if len(lines) - 1 > index:
        new = lines[index:-1]
        for word in new:
          yield json.loads(word)
        index = len(lines) - 1
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_csrf_protect']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0,<1', 'itsdangerous>=2.0.1,<3.0.0', 'pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-csrf-protect',
    'version': '0.3.1',
    'description': 'Stateless implementation of Cross-Site Request Forgery (XSRF) Protection by using Double Submit Cookie mitigation pattern',
    'long_description': '# FastAPI CSRF Protect\n\n[![Build Status](https://travis-ci.com/aekasitt/fastapi-csrf-protect.svg?branch=master)](https://app.travis-ci.com/github/aekasitt/fastapi-csrf-protect)\n[![Package Vesion](https://img.shields.io/pypi/v/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)\n[![Format](https://img.shields.io/pypi/format/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)\n[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)\n[![License](https://img.shields.io/pypi/l/fastapi-csrf-protect)](https://pypi.org/project/fastapi-csrf-protect)\n\n## Features\n\nFastAPI extension that provides stateless Cross-Site Request Forgery (XSRF) Protection support.\nAimed to be easy to use and lightweight, we adopt [Double Submit Cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie) mitigation pattern.\nIf you were familiar with `flask-wtf` library this extension suitable for you.\nThis extension inspired by `fastapi-jwt-auth` 😀\n\n- Storing `fastapi-csrf-token` in cookies or serve it in template\'s context\n\n## 🚧 Breaking Changes (0.3.0 -> 0.3.1)\n\n* The `generate_csrf` method has now been marked for deprecation\n* The recommended method is now `generate_csrf_tokens` which returns a tuple of tokens, first unsigned\n  and the latter signed\n* Recommended pattern is for the first token is aimed for returning as part of context\n* Recommended pattern is for the signed token to be set in client\'s cookie completing [Double Submit Cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie)\n* To prevent token reuse, protected endpoint can unset the signed CSRF Token in client\'s cookies as\n  per example code and recommended pattern.\n\n## Installation\n\nThe easiest way to start working with this extension with pip\n\n```bash\npip install fastapi-csrf-protect\n# or\npoetry add fastapi-csrf-protect\n```\n\n## Getting Started\n\nThe following examples show you how to integrate this extension to a FastAPI App\n\n### Example Login Form\n\n```python\nfrom fastapi import FastAPI, Request, Depends\nfrom fastapi.responses import JSONResponse\nfrom fastapi.templating import Jinja2Templates\nfrom fastapi_csrf_protect import CsrfProtect\nfrom fastapi_csrf_protect.exceptions import CsrfProtectError\nfrom pydantic import BaseModel\n\napp = FastAPI()\ntemplates = Jinja2Templates(directory="templates")\n\nclass CsrfSettings(BaseModel):\n  secret_key: str = "asecrettoeverybody"\n  cookie_samesite: str = "none"\n\n@CsrfProtect.load_config\ndef get_csrf_config():\n  return CsrfSettings()\n\n@app.get("/login")\ndef form(request: Request, csrf_protect: CsrfProtect = Depends()):\n  """\n  Returns form template.\n  """\n  csrf_token, signed_token = csrf_protect.generate_csrf_tokens()\n  response = templates.TemplateResponse(\n    "form.html", {"request": request, "csrf_token": csrf_token}\n  )\n  csrf_protect.set_csrf_cookie(signed_token, response)\n  return response\n\n@app.post("/login", response_class=JSONResponse)\ndef create_post(request: Request, csrf_protect: CsrfProtect = Depends()):\n  """\n  Creates a new Post\n  """\n  csrf_protect.validate_csrf(request)\n  response: JSONResponse = JSONResponse(status_code=200, content={"detail": "OK"})\n  csrf_protect.unset_csrf_cookie(response)  # prevent token reuse\n  return response\n\n@app.exception_handler(CsrfProtectError)\ndef csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):\n  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})\n\n```\n\n## Contributions\n\nTo contribute to the project, fork the repository and clone to your local device and install preferred testing dependency [pytest](https://github.com/pytest-dev/pytest)\nAlternatively, run the following command on your terminal to do so:\n\n```bash\npip install -U poetry\npoetry install\n```\n\nTesting can be done by the following command post-installation:\n\n```bash\npoetry install --with test\npytest\n```\n\n### Run Examples\n\nTo run the provided examples, first you must install extra dependencies [uvicorn](https://github.com/encode/uvicorn) and [jinja2](https://github.com/pallets/jinja/)\nAlternatively, run the following command on your terminal to do so\n\n```bash\npoetry install --with examples\n```\n\nRunning the example utilizing Context and Headers\n\n```bash\nuvicorn examples.login:app\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Sitt Guruvanich',
    'author_email': 'aekazitt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aekasitt/fastapi-csrf-protect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

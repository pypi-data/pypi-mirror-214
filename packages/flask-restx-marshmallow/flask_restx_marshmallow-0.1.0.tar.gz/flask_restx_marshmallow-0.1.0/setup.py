# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_restx_marshmallow']

package_data = \
{'': ['*'], 'flask_restx_marshmallow': ['static/*', 'templates/*']}

install_requires = \
['Flask-Caching>=2.0.2,<3.0.0',
 'Flask-JWT-Extended>=4.5.2,<5.0.0',
 'Flask-SQLAlchemy>=3.0.3,<4.0.0',
 'Flask>=2.3.2,<3.0.0',
 'SQLAlchemy-Utils>=0.41.1,<0.42.0',
 'SQLAlchemy>=2.0.15,<3.0.0',
 'apispec>=6.3.0,<7.0.0',
 'beautifulsoup4>=4.12.2,<5.0.0',
 'filetype>=1.2.0,<2.0.0',
 'flask-restx>=1.1.0,<2.0.0',
 'marshmallow-sqlalchemy>=0.29.0,<0.30.0',
 'marshmallow>=3.19.0,<4.0.0',
 'mysqlclient>=2.1.1,<3.0.0',
 'orjson>=3.9.0,<4.0.0',
 'passlib>=1.7.4,<2.0.0',
 'redis>=4.5.5,<5.0.0',
 'requests>=2.31.0,<3.0.0',
 'sortedcontainers>=2.4.0,<3.0.0',
 'webargs>=8.2.0,<9.0.0']

setup_kwargs = {
    'name': 'flask-restx-marshmallow',
    'version': '0.1.0',
    'description': 'A successful practice combining flask_restx with marshmallow',
    'long_description': '<!--\n * @Description: README for flask_restx_marshmallow\n * @version: 0.1.0\n * @Author: 1746104160\n * @Date: 2023-06-02 13:05:58\n * @LastEditors: 1746104160 shaojiahong2001@outlook.com\n * @LastEditTime: 2023-06-16 18:04:55\n * @FilePath: /flask_restx_marshmallow/README.md\n-->\n# Flask-RESTX-marshmallow\n\nFlask-RESTX-marshmallow is an extension for [Flask](https://flask.palletsprojects.com/en/latest/) and [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/), which is a successful practice combining flask_restx with marshmallow.\n\n## Compatibility\n\nFlask-RESTX-marshmallow requires Python 3.10+.\n\n## Installation\n\nInstall the extension with pip:\n\n```bash\npip install flask-restx-marshmallow\n```\n\nor with poetry:\n\n```bash\npoetry add flask-restx-marshmallow\n```\n\n## Quickstart\n\nWith Flask-RESTX-marshmallow, you only import the api instance to route and document your endpoints.\n\n```python\nimport uuid\n\nimport sqlalchemy as sa\nfrom flask import Flask\nfrom marshmallow import fields, post_load\n\nfrom flask_restx_marshmallow import (\n    Api,\n    JSONParameters,\n    QueryParameters,\n    Resource,\n    SQLAlchemy,\n    StandardSchema,\n)\n\napp = Flask(__name__)\napp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"\napi = Api(\n    app,\n    version="0.1.0",\n    title="example API",\n    description="api interface for example app",\n)\ndb = SQLAlchemy(app)\nns = api.namespace("example", description="example operations")\n\n\nclass Task(db.Model):\n    id = db.Column(db.String(32), primary_key=True)\n    task = db.Column(db.String(80))\n\n    def __init__(self, id, task):\n        self.id = id.hex\n        self.task = task\n\n    def __repr__(self):\n        return "<Task %r>" % self.task\n\n\nclass QueryTaskParameters(QueryParameters):\n    id = fields.UUID(metadata={"description": "The task unique identifier"})\n\n    @post_load\n    def process(self, data, **_kwargs):\n        if "id" in data:\n            return {"data": Task.query.filter_by(id=data["id"].hex).first()}\n        return {"code": 1, "message": "id is required", "success": False}\n\n\nclass CreateTaskParameters(JSONParameters):\n    task = fields.String(\n        required=True, metadata={"description": "The task details"}\n    )\n\n    @post_load\n    def process(self, data, **_kwargs):\n        try:\n            task = Task(id=uuid.uuid4(), task=data["task"])\n            db.session.add(task)\n        except sa.exc.IntegrityError as e:\n            db.session.rollback()\n            return {"code": 1, "message": str(e), "success": False}\n        else:\n            db.session.commit()\n            return {\n                "message": f"create task success with id {uuid.UUID(task.id)}"\n            }\n\n\nclass TaskSchema(StandardSchema):\n    data = fields.Nested(\n        {\n            "id": fields.UUID(\n                metadata={"description": "The task unique identifier"},\n            ),\n            "task": fields.String(metadata={"description": "The task details"}),\n        }\n    )\n\n\n@ns.route("/")\nclass TaskManage(Resource):\n    """task manage"""\n\n    @ns.parameters(params=QueryTaskParameters(), location="query")\n    @ns.response(\n        code=200,\n        description="query task by id",\n        model=TaskSchema(message="query task success"),\n    )\n    def get(self, task):\n        """query task by id"""\n        return task\n\n    @ns.parameters(params=CreateTaskParameters(), location="body")\n    @ns.response(\n        code=200,\n        description="create a new task",\n        model=None,\n        name="CreateSchema",\n        message="create successfully",\n    )\n    def post(self, res):\n        """create a new task"""\n        return res\n\n\nif __name__ == "__main__":\n    with app.app_context():\n        db.create_all()\n    api.register_doc(app)\n    app.run(debug=True)\n```\n',
    'author': '1746104160',
    'author_email': 'shaojiahong2001@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/1746104160/flask-restx-marshmallow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

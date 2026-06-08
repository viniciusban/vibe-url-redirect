from piccolo.conf.apps import AppRegistry

from steerer.engine import DB  # noqa: F401

APP_REGISTRY = AppRegistry(apps=["steerer.piccolo_app"])

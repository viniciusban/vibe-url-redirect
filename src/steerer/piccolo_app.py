from piccolo.conf.apps import AppConfig

from steerer.tables import UrlRoute

APP_CONFIG = AppConfig(
    app_name="steerer",
    migrations_folder_path="migrations",
    table_classes=[UrlRoute],
)

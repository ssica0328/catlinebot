from django.apps import AppConfig


class CatLinebotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cat_linebot'
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

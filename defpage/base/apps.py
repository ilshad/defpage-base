from defpage.base.config import system_params

def get_source_types():
    return [
        {"id":"gd",
         "title":"Google Docs",
         "url":system_params.gd_ui_url,
         "special_attr":"folder_id"}
        ]

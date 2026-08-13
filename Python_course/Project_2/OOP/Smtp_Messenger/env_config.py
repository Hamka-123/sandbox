import pathlib
from dotenv import dotenv_values
import utils

def load_config_with_templates():
    """Загружает конфиг с динамическими шаблонами"""
    env_path = pathlib.Path(__file__).parent.joinpath(".env")
    
    try:
        main_config = dotenv_values(env_path)
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")
        return {}
    
    # Загружаем интеграционный конфиг
    integration_config_path = main_config.get('EMAIL_SOURCE_CONFIG', '')
    integration_config = {}
    
    if integration_config_path:
        full_path = pathlib.Path(__file__).parent.joinpath(integration_config_path)
        if full_path.exists():
            try:
                integration_config = dotenv_values(full_path)
                print(f"✅ Loaded integration config from: {integration_config_path}")
            except Exception as e:
                print(f"❌ Error loading integration config: {e}")
    
    # Динамически загружаем шаблоны
    templates_folder = main_config.get('EMAIL_TEMPLATES_FOLDER', 'messages_templates')
    email_templates = utils.load_templates_from_folder(templates_folder)
    
    # Создаем финальный конфиг
    final_config = {
        **main_config,
        'INTEGRATION_CONFIG': integration_config,
        'EMAIL_TEMPLATES': email_templates
    }
    
    return final_config

# Загружаем конфигурацию
config = load_config_with_templates()
'''
print("\n📧 Configuration:")
print(f"SMTP_APP: {config.get('SMTP_APP')}")
print(f"SMTP_USER: {config.get('SMTP_USER')}")
print(f"SMTP_HOST: {config.get('SMTP_HOST')}")
print(f"SMTP_PORT: {config.get('SMTP_PORT')}")
print(f"EMAIL_SOURCE_NAME: {config.get('EMAIL_SOURCE_NAME')}")

print("\n🎯 Integration Config:")
integration_config = config.get('INTEGRATION_CONFIG', {})
for key, value in integration_config.items():
    print(f"  {key}: {value}")

print(f"\n📝 Templates:")
print(f"  FOLDER: {config.get('EMAIL_TEMPLATES_FOLDER')}")
print(f"  AVAILABLE: {config.get('EMAIL_TEMPLATES')}")
'''
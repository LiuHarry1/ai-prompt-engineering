import os


class BaseConfig():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    AI_SERVICE_DATA_PATH = os.path.join(ROOT_DIR, "..","ai-service-data")

class DevelopmentConfig(BaseConfig):
    TRAINED_MODEL_PATH = "/app/1001090000/data/models"
    NLTK_DATA = os.path.join(TRAINED_MODEL_PATH, "nltk")
    NARRATIVE = "/app/1001090000/data/narrative"
    NARRATIVE_RAW =os.path.join(NARRATIVE, "raw")
    NARRATIVE_FORMATTED = os.path.join(NARRATIVE, "formatted")
    NARRATIVE_SENTENCE_CASE = os.path.join(NARRATIVE, "sentence_case")
    NARRATIVE_SPELL_CORRECTION =  os.path.join(NARRATIVE, "spell_correction")
    NARRATIVE_LIST = os.path.join(NARRATIVE, "list")
    # SPACY_DATA = os.path.join(TRAINED_MODEL_PATH, "spacy", "en_core_web_sm-3.7.1", "en_core_web_sm", "en_core_web_sm-3.7.1")

class LocalConfig(BaseConfig):
    MODEL_PATH = os.path.join(BaseConfig.AI_SERVICE_DATA_PATH, "model")
    NLTK_DATA = os.path.join(BaseConfig.AI_SERVICE_DATA_PATH, "model", "nltk")
    NARRATIVE = os.path.join(BaseConfig.AI_SERVICE_DATA_PATH, "narrative")
    NARRATIVE_RAW = os.path.join(NARRATIVE, "raw")
    NARRATIVE_SENTENCE_CASE = os.path.join(NARRATIVE, "sentence_case")
    NARRATIVE_SPELL_CORRECTION =  os.path.join(NARRATIVE, "spell_correction")
    NARRATIVE_LIST = os.path.join(NARRATIVE, "list")
    NARRATIVE_FORMATTED = os.path.join(NARRATIVE, "formatted")
    # SPACY_DATA = os.path.join(BaseConfig.AI_SERVICE_DATA_PATH, "model", "spacy", "en_core_web_sm-3.7.1", "en_core_web_sm", "en_core_web_sm-3.7.1")

def get_env(var, default=None):
    try:
        return os.environ[var]
    except:
        return default

ai_env = get_env("AI_ENV")

if ai_env == "local":
    Config = LocalConfig()
elif ai_env == "dev":
    Config = DevelopmentConfig()
else:
    Config = LocalConfig()
print("AI_ENV:", ai_env)
print("Config:", Config)


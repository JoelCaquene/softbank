"""
Django settings for core project.
...
"""

from pathlib import Path
import os
# Adições para Produção
import dj_database_url
import whitenoise 
import dotenv
dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SEGURANÇA: Configurando para Produção
# O Render.com irá injetar esta variável de ambiente. 
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-q+)rh&425aq#(5#2l+7_(dpu&jwj6i&q2kfe_*!v!(o4t+#m3u')

# DEBUG deve ser FALSO em produção.
# Verificamos a variável 'RENDER' para determinar o ambiente.
DEBUG = 'RENDER' not in os.environ 

# Domínios permitidos para acessar sua aplicação
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.onrender.com'] 

# Variável do Render que contém o host externo
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Aplicações adicionadas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Suas aplicações
    'plataforma', 

    # Apps de terceiros para deploy
    'cloudinary_storage', # Para gerenciar arquivos de mídia no Cloudinary
    'cloudinary',         # Integração com Cloudinary
    # 'whitenoise.runserver_nostatic', # Removido, pois o WhiteNoise será configurado via MIDDLEWARE e STORAGES
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise deve vir logo após SecurityMiddleware em produção
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# A lógica agora está otimizada: tenta usar DATABASE_URL (Render) e volta para SQLite (Local)
if os.environ.get('DATABASE_URL'):
    # PostgreSQL (Produção)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600  # Tempo máximo de vida da conexão
        )
    }
else:
    # SQLite (Desenvolvimento Local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# ... (deixado como estava) ...
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'pt-br' 
TIME_ZONE = 'Africa/Luanda' 
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Onde collectstatic vai coletar todos os arquivos estáticos

# Configuração de Arquivos Estáticos com WhiteNoise para Produção
if not DEBUG:
    # Use WhiteNoise para servir arquivos estáticos comprimidos e com cache
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    
# Configuração do Cloudinary para arquivos de mídia (Uploads de usuário)
# Se você realmente usa Cloudinary para mídia (uploads de usuário), mantenha.
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL') 
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modelos de Autenticação
AUTH_USER_MODEL = 'plataforma.Usuario'

# URL para onde o Django redireciona para o login
LOGIN_URL = 'login'

# Para segurança CSRF em produção
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com', 'https://*.cloud.cloudinary.com']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Logging middleware
    'chats.middleware.RequestLoggingMiddleware',

    # Time restriction middleware
    'chats.middleware.RestrictAccessByTimeMiddleware',
    "chats.middleware.OffensiveLanguageMiddleware",
]

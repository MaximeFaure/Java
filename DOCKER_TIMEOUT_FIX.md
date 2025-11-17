# Fix Timeout 504 - Configuration Docker pour Symfony/Nginx/PHP

Ce guide explique comment résoudre les erreurs de timeout 504 en augmentant le timeout de 30s à 60s.

## 📁 Fichiers créés

```
docker/
├── nginx/
│   └── nginx.conf          # Configuration nginx avec timeouts à 60s
└── php/
    ├── php.ini             # Configuration PHP avec max_execution_time à 60s
    └── php-fpm.conf        # Configuration PHP-FPM avec request_terminate_timeout à 60s
docker-compose.yml          # Fichier Docker Compose exemple
```

## 🚀 Comment appliquer ces configurations

### Option 1 : Utiliser ces fichiers dans votre projet existant

1. **Copiez les fichiers** dans votre projet Symfony existant

2. **Modifiez votre docker-compose.yml** pour monter ces configurations :

```yaml
services:
  nginx:
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/conf.d/default.conf

  php:
    volumes:
      - ./docker/php/php.ini:/usr/local/etc/php/php.ini
      - ./docker/php/php-fpm.conf:/usr/local/etc/php-fpm.d/www.conf
```

3. **Redémarrez vos conteneurs** :

```bash
docker-compose down
docker-compose up -d
```

### Option 2 : Modifier uniquement certains paramètres

Si vous avez déjà des fichiers de configuration, ajoutez simplement ces lignes :

**Dans nginx.conf :**
```nginx
fastcgi_read_timeout 60s;
fastcgi_send_timeout 60s;
fastcgi_connect_timeout 60s;
```

**Dans php.ini :**
```ini
max_execution_time = 60
max_input_time = 60
```

**Dans php-fpm.conf (www.conf) :**
```ini
request_terminate_timeout = 60s
```

## 🔍 Vérification

Après le redémarrage, vérifiez que les configurations sont bien appliquées :

```bash
# Vérifier nginx
docker exec symfony_nginx nginx -t

# Vérifier PHP
docker exec symfony_php php -i | grep max_execution_time

# Vérifier PHP-FPM
docker exec symfony_php cat /usr/local/etc/php-fpm.d/www.conf | grep request_terminate_timeout
```

## 🧪 Tester

Testez votre API avec curl pour voir si le timeout a bien augmenté :

```bash
time curl -X GET https://votre-api.com/endpoint-lent
```

## ⚡ Points importants

- **Tous les timeouts doivent être cohérents** : nginx, PHP et PHP-FPM doivent avoir des valeurs similaires
- **60 secondes est une solution temporaire** : si vos requêtes prennent plus de 30s, envisagez d'optimiser votre code ou d'utiliser des jobs asynchrones
- **Pensez à adapter** les noms de conteneurs (`symfony_nginx`, `symfony_php`) selon votre configuration

## 🐛 Dépannage

Si le problème persiste :

1. Vérifiez les logs nginx : `docker logs symfony_nginx`
2. Vérifiez les logs PHP : `docker logs symfony_php`
3. Vérifiez que les volumes sont bien montés : `docker inspect symfony_php`
4. Redémarrez complètement Docker : `docker-compose down && docker-compose up -d --force-recreate`

## 📝 Notes

- Version PHP dans docker-compose.yml : `php:8.2-fpm` (ajustez selon vos besoins)
- Les logs sont stockés dans `./docker/logs/`
- N'oubliez pas d'adapter les chemins selon votre structure de projet

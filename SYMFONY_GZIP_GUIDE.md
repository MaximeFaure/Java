# Guide d'intégration GZIP dans Symfony

Ce guide explique comment activer la compression gzip pour votre route PowerBI afin de réduire considérablement le temps de transfert des données.

## 🎯 Objectif

Compresser les réponses JSON de votre API Symfony avec gzip pour réduire la taille des données transférées et accélérer le temps de réponse.

**Gain attendu** : Réduction de 60-90% de la taille des données JSON

## 📦 Fichiers créés

```
symfony-examples/
├── CatalogController_with_gzip.php         # Version simple avec gzip inline
├── CatalogController_with_service.php      # Version recommandée avec service
└── Service/
    └── CompressionService.php              # Service réutilisable de compression
```

## 🚀 Installation - 3 options

### Option 1 : Modification directe du contrôleur (SIMPLE)

Modifiez directement votre contrôleur existant :

```php
#[Route('/showDataPowerBiForCatalog/{password}', name: 'catalog_data_powerBI')]
public function showDataCatalog(string $password): Response
{
    if ($password !== "Nova25CatalogViewOrigami69EDF") {
        $this->logger->warning('Tentative échouée');
        return $this->json(['Erreur' => 'Mot de passe incorrect']);
    }

    try {
        $catalog = $this->catalogRepository->findAll();
    } catch (Exception $e) {
        $this->logger->error("Erreur : " . $e->getMessage());
        throw new BadRequestHttpException("Erreur lors de la récupération.");
    }

    // ⭐ AJOUTEZ CES LIGNES ⭐
    $jsonData = $this->container->get('serializer')->serialize($catalog, 'json');
    $compressed = gzencode($jsonData, 9); // 9 = compression maximum

    $response = new Response($compressed);
    $response->headers->set('Content-Type', 'application/json');
    $response->headers->set('Content-Encoding', 'gzip');
    $response->headers->set('Vary', 'Accept-Encoding');

    return $response;
}
```

**N'oubliez pas d'ajouter** :
```php
use Symfony\Component\HttpFoundation\Response;
```

### Option 2 : Avec le CompressionService (RECOMMANDÉ ⭐)

**Étape 1** : Créez le fichier `src/Service/CompressionService.php`

Copiez le contenu du fichier `symfony-examples/Service/CompressionService.php`

**Étape 2** : Modifiez votre contrôleur

```php
use App\Service\CompressionService;

class CatalogController extends AbstractController
{
    public function __construct(
        private CatalogRepository $catalogRepository,
        private LoggerInterface $logger,
        private CompressionService $compressionService // ⭐ Ajoutez ceci
    ) {}

    #[Route('/showDataPowerBiForCatalog/{password}', name: 'catalog_data_powerBI')]
    public function showDataCatalog(string $password): Response
    {
        if ($password !== "Nova25CatalogViewOrigami69EDF") {
            return $this->compressionService->createGzipJsonResponse(
                ['Erreur' => 'Mot de passe incorrect'],
                [],
                9,
                401
            );
        }

        try {
            $catalog = $this->catalogRepository->findAll();
        } catch (Exception $e) {
            $this->logger->error("Erreur : " . $e->getMessage());
            throw new BadRequestHttpException("Erreur.");
        }

        // ⭐ Une seule ligne ! ⭐
        return $this->compressionService->createGzipJsonResponse($catalog);
    }
}
```

**Avantages** :
- ✅ Réutilisable dans tous vos contrôleurs
- ✅ Logs automatiques du taux de compression
- ✅ Headers informatifs pour le debug
- ✅ Code plus propre et maintenable

### Option 3 : Avec Event Subscriber (AUTOMATIQUE)

Pour compresser **automatiquement toutes** les réponses JSON de votre API :

**Créez** `src/EventSubscriber/GzipResponseSubscriber.php` :

```php
<?php

namespace App\EventSubscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\ResponseEvent;
use Symfony\Component\HttpKernel\KernelEvents;

class GzipResponseSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            KernelEvents::RESPONSE => ['onKernelResponse', -10],
        ];
    }

    public function onKernelResponse(ResponseEvent $event): void
    {
        $request = $event->getRequest();
        $response = $event->getResponse();

        // Vérifier que c'est une réponse JSON
        $contentType = $response->headers->get('Content-Type');
        if (!str_contains($contentType, 'application/json')) {
            return;
        }

        // Vérifier que le client supporte gzip
        $acceptEncoding = $request->headers->get('Accept-Encoding', '');
        if (!str_contains($acceptEncoding, 'gzip')) {
            return;
        }

        // Ne pas compresser si déjà compressé
        if ($response->headers->has('Content-Encoding')) {
            return;
        }

        // Compression
        $content = $response->getContent();
        if (strlen($content) < 256) { // Ne pas compresser les petites réponses
            return;
        }

        $compressed = gzencode($content, 9);
        $response->setContent($compressed);
        $response->headers->set('Content-Encoding', 'gzip');
        $response->headers->set('Vary', 'Accept-Encoding');
    }
}
```

**Avantages** :
- ✅ Compression automatique de toutes les routes API
- ✅ Pas besoin de modifier chaque contrôleur
- ✅ Vérification automatique du support client

## 🔧 Configuration Nginx

La configuration nginx a déjà été mise à jour dans `docker/nginx/nginx.conf` avec :

```nginx
# Configuration GZIP
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types application/json application/javascript text/plain text/css;
gzip_min_length 256;
```

## 🧪 Test et vérification

### 1. Testez la compression

```bash
# Avec curl (doit retourner des données binaires compressées)
curl -H "Accept-Encoding: gzip" \
     http://localhost/showDataPowerBiForCatalog/Nova25CatalogViewOrigami69EDF \
     --compressed \
     -v

# Vérifiez les headers
curl -I -H "Accept-Encoding: gzip" \
     http://localhost/showDataPowerBiForCatalog/Nova25CatalogViewOrigami69EDF
```

Vous devriez voir dans les headers :
```
Content-Encoding: gzip
Vary: Accept-Encoding
X-Compression-Ratio: 85.5%  (si vous utilisez le CompressionService)
```

### 2. Comparez les tailles

**Sans compression** :
```bash
curl http://localhost/showDataPowerBiForCatalog/VOTRE_PASSWORD | wc -c
```

**Avec compression** :
```bash
curl -H "Accept-Encoding: gzip" \
     http://localhost/showDataPowerBiForCatalog/VOTRE_PASSWORD \
     --compressed | wc -c
```

### 3. Vérifiez les logs

Si vous utilisez le `CompressionService`, vérifiez vos logs Symfony :

```bash
tail -f var/log/dev.log | grep "Compression gzip"
```

Vous verrez :
```
Compression gzip: 2.5 MB → 350 KB (gain: 86%)
```

## 📊 Gains de performance attendus

Pour une réponse JSON typique de catalogue :

| Taille originale | Taille compressée | Gain | Temps de transfert (4G) |
|-----------------|-------------------|------|-------------------------|
| 500 KB          | 50 KB             | 90%  | 5s → 0.5s              |
| 1 MB            | 100 KB            | 90%  | 10s → 1s               |
| 5 MB            | 500 KB            | 90%  | 50s → 5s               |
| 10 MB           | 1 MB              | 90%  | 100s → 10s             |

**Note** : Les gains varient selon la nature des données. JSON se compresse très bien (taux typique : 80-95%).

## ⚡ Optimisations supplémentaires

### 1. Utilisez des groupes de sérialisation

Dans vos entités :

```php
use Symfony\Component\Serializer\Annotation\Groups;

class Catalog
{
    #[Groups(['catalog:read'])]
    private ?int $id = null;

    #[Groups(['catalog:read'])]
    private ?string $name = null;

    // Ne pas exposer ce champ dans l'API
    private ?string $internalNotes = null;
}
```

Dans le contrôleur :
```php
return $this->compressionService->createGzipJsonResponse(
    $catalog,
    ['groups' => 'catalog:read']
);
```

### 2. Ajoutez du cache

```php
$response = $this->compressionService->createGzipJsonResponse($catalog);
$response->headers->set('Cache-Control', 'public, max-age=300'); // 5 minutes
$response->setEtag(md5($response->getContent()));
return $response;
```

### 3. Pagination

Si votre catalogue est très volumineux :

```php
// Dans le repository
public function findAllPaginated(int $page = 1, int $limit = 100)
{
    return $this->createQueryBuilder('c')
        ->setFirstResult(($page - 1) * $limit)
        ->setMaxResults($limit)
        ->getQuery()
        ->getResult();
}
```

## 🐛 Dépannage

### Problème : PowerBI ne décompresse pas les données

**Solution** : Assurez-vous que PowerBI envoie le header `Accept-Encoding: gzip`. Si ce n'est pas le cas, utilisez l'Option 3 (Event Subscriber) qui détecte automatiquement le support.

### Problème : Les données sont corrompues

**Vérifiez** :
1. Que nginx ne compresse pas une seconde fois (double compression)
2. Que le header `Content-Encoding: gzip` est bien présent
3. Que vous utilisez `gzencode()` et pas `gzcompress()` ou `gzdeflate()`

### Problème : Pas de gain de performance

**Possible causes** :
1. Les données sont déjà compressées (images, PDF, etc.)
2. La taille des données est trop petite (< 256 bytes)
3. Le goulot d'étranglement est ailleurs (base de données, calculs)

## 📝 Checklist d'implémentation

- [ ] Créer le `CompressionService.php` dans `src/Service/`
- [ ] Modifier votre contrôleur pour utiliser le service
- [ ] Mettre à jour la configuration nginx avec gzip
- [ ] Redémarrer les conteneurs Docker : `docker-compose down && docker-compose up -d`
- [ ] Tester avec curl et vérifier les headers
- [ ] Vérifier les logs pour voir le taux de compression
- [ ] Tester depuis PowerBI

## 🎓 Pour aller plus loin

- **Brotli** : Compression encore meilleure que gzip (mais moins compatible)
- **HTTP/2** : Améliore encore les performances avec la compression
- **CDN** : Mettez en cache les données compressées au niveau CDN

---

✅ Avec ces modifications, votre API devrait être **beaucoup plus rapide** et ne plus avoir de problème de timeout !

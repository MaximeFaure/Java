<?php

namespace App\Controller;

use App\Repository\CatalogRepository;
use Exception;
use Psr\Log\LoggerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\BadRequestHttpException;
use Symfony\Component\Routing\Annotation\Route;

class CatalogController extends AbstractController
{
    private CatalogRepository $catalogRepository;
    private LoggerInterface $logger;

    public function __construct(
        CatalogRepository $catalogRepository,
        LoggerInterface $logger
    ) {
        $this->catalogRepository = $catalogRepository;
        $this->logger = $logger;
    }

    #[Route('/showDataPowerBiForCatalog/{password}', name: 'catalog_data_powerBI')]
    public function showDataCatalog(string $password): Response
    {
        if ($password !== "Nova25CatalogViewOrigami69EDF") {
            $this->logger->warning('showDataPowerBiForCatalog : Tentative de connection échoué (Mot de passe incorrect)');
            return $this->json(['Erreur' => 'Le mot de passe renseignée est incorrect']);
        }

        try {
            $catalog = $this->catalogRepository->findAll();
        } catch (Exception $e) {
            $this->logger->error(
                "showDataPowerBiForCatalog :
                    La récuperation des données du Catalog pour PowerBi a échoué
                    Détail de l'erreur : " . $e->getMessage()
            );
            throw new BadRequestHttpException(
                "Une erreur est survenue lors de la récuperation des données."
            );
        }

        $this->logger->info('showDataPowerBiForCatalog : Requete de visualisation PowerBI pour les données du Catalog');

        // Sérialiser les données en JSON
        $jsonData = $this->container->get('serializer')->serialize(
            $catalog,
            'json',
            ['groups' => 'catalog:read'] // Optionnel : utilisez des groupes de sérialisation
        );

        // ⭐ Compression GZIP ⭐
        $compressed = gzencode($jsonData, 9); // 9 = niveau de compression maximum (1-9)

        // Créer la réponse avec les données compressées
        $response = new Response($compressed);
        $response->headers->set('Content-Type', 'application/json');
        $response->headers->set('Content-Encoding', 'gzip');
        $response->headers->set('Vary', 'Accept-Encoding');

        // Cache control (optionnel mais recommandé pour PowerBI)
        $response->headers->set('Cache-Control', 'public, max-age=300'); // 5 minutes de cache

        return $response;
    }

    /**
     * ⭐ VERSION ALTERNATIVE avec méthode réutilisable ⭐
     */
    #[Route('/showDataPowerBiForCatalog/v2/{password}', name: 'catalog_data_powerBI_v2')]
    public function showDataCatalogV2(string $password): Response
    {
        if ($password !== "Nova25CatalogViewOrigami69EDF") {
            $this->logger->warning('showDataPowerBiForCatalog : Tentative de connection échoué (Mot de passe incorrect)');
            return $this->json(['Erreur' => 'Le mot de passe renseignée est incorrect']);
        }

        try {
            $catalog = $this->catalogRepository->findAll();
        } catch (Exception $e) {
            $this->logger->error("showDataPowerBiForCatalog : " . $e->getMessage());
            throw new BadRequestHttpException("Une erreur est survenue lors de la récuperation des données.");
        }

        $this->logger->info('showDataPowerBiForCatalog : Requete de visualisation PowerBI pour les données du Catalog');

        return $this->createGzipJsonResponse($catalog);
    }

    /**
     * Méthode réutilisable pour créer une réponse JSON compressée avec gzip
     */
    private function createGzipJsonResponse($data, int $compressionLevel = 9): Response
    {
        // Sérialiser les données
        $jsonData = $this->container->get('serializer')->serialize(
            $data,
            'json',
            ['groups' => 'catalog:read']
        );

        // Mesurer la taille avant compression (pour logs)
        $originalSize = strlen($jsonData);

        // Compression gzip
        $compressed = gzencode($jsonData, $compressionLevel);
        $compressedSize = strlen($compressed);

        // Logger le taux de compression
        $compressionRatio = round((1 - $compressedSize / $originalSize) * 100, 2);
        $this->logger->info(sprintf(
            'Compression gzip: %d bytes → %d bytes (gain: %s%%)',
            $originalSize,
            $compressedSize,
            $compressionRatio
        ));

        // Créer la réponse
        $response = new Response($compressed);
        $response->headers->set('Content-Type', 'application/json');
        $response->headers->set('Content-Encoding', 'gzip');
        $response->headers->set('Vary', 'Accept-Encoding');
        $response->headers->set('X-Original-Size', (string)$originalSize);
        $response->headers->set('X-Compressed-Size', (string)$compressedSize);
        $response->headers->set('X-Compression-Ratio', $compressionRatio . '%');

        return $response;
    }
}

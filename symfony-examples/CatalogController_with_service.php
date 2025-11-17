<?php

namespace App\Controller;

use App\Repository\CatalogRepository;
use App\Service\CompressionService;
use Exception;
use Psr\Log\LoggerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\BadRequestHttpException;
use Symfony\Component\Routing\Annotation\Route;

/**
 * ⭐ VERSION RECOMMANDÉE : Utilisation du CompressionService ⭐
 */
class CatalogController extends AbstractController
{
    private CatalogRepository $catalogRepository;
    private LoggerInterface $logger;
    private CompressionService $compressionService;

    public function __construct(
        CatalogRepository $catalogRepository,
        LoggerInterface $logger,
        CompressionService $compressionService
    ) {
        $this->catalogRepository = $catalogRepository;
        $this->logger = $logger;
        $this->compressionService = $compressionService;
    }

    #[Route('/showDataPowerBiForCatalog/{password}', name: 'catalog_data_powerBI')]
    public function showDataCatalog(string $password): Response
    {
        if ($password !== "Nova25CatalogViewOrigami69EDF") {
            $this->logger->warning('showDataPowerBiForCatalog : Tentative de connection échoué (Mot de passe incorrect)');

            // Même les erreurs peuvent être compressées
            return $this->compressionService->createGzipJsonResponse(
                ['Erreur' => 'Le mot de passe renseignée est incorrect'],
                [],
                9,
                401
            );
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

        // ⭐ Utilisation du service de compression ⭐
        return $this->compressionService->createGzipJsonResponse(
            $catalog,
            ['groups' => 'catalog:read'], // Optionnel : groupes de sérialisation
            9 // Niveau de compression maximum
        );
    }
}

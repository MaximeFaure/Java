<?php

namespace App\Service;

use Psr\Log\LoggerInterface;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Serializer\SerializerInterface;

/**
 * Service pour gérer la compression gzip des réponses API
 */
class CompressionService
{
    private SerializerInterface $serializer;
    private LoggerInterface $logger;

    public function __construct(
        SerializerInterface $serializer,
        LoggerInterface $logger
    ) {
        $this->serializer = $serializer;
        $this->logger = $logger;
    }

    /**
     * Crée une réponse JSON compressée avec gzip
     *
     * @param mixed $data Les données à sérialiser et compresser
     * @param array $context Contexte de sérialisation (groups, etc.)
     * @param int $compressionLevel Niveau de compression (1-9, 9 = maximum)
     * @param int $status Code HTTP de la réponse
     * @return Response
     */
    public function createGzipJsonResponse(
        $data,
        array $context = [],
        int $compressionLevel = 9,
        int $status = 200
    ): Response {
        // Sérialiser les données en JSON
        $jsonData = $this->serializer->serialize($data, 'json', $context);

        // Mesurer la taille avant compression
        $originalSize = strlen($jsonData);

        // Compression gzip
        $compressed = gzencode($jsonData, $compressionLevel);
        $compressedSize = strlen($compressed);

        // Calculer le taux de compression
        $compressionRatio = $originalSize > 0
            ? round((1 - $compressedSize / $originalSize) * 100, 2)
            : 0;

        // Logger les statistiques
        $this->logger->info(sprintf(
            'Compression gzip: %s → %s (gain: %s%%)',
            $this->formatBytes($originalSize),
            $this->formatBytes($compressedSize),
            $compressionRatio
        ));

        // Créer la réponse
        $response = new Response($compressed, $status);
        $response->headers->set('Content-Type', 'application/json');
        $response->headers->set('Content-Encoding', 'gzip');
        $response->headers->set('Vary', 'Accept-Encoding');

        // Headers informatifs (optionnels, utiles pour le debug)
        $response->headers->set('X-Original-Size', (string)$originalSize);
        $response->headers->set('X-Compressed-Size', (string)$compressedSize);
        $response->headers->set('X-Compression-Ratio', $compressionRatio . '%');

        return $response;
    }

    /**
     * Compresse une chaîne JSON déjà sérialisée
     *
     * @param string $jsonData JSON déjà sérialisé
     * @param int $compressionLevel Niveau de compression (1-9)
     * @return Response
     */
    public function compressJsonString(
        string $jsonData,
        int $compressionLevel = 9,
        int $status = 200
    ): Response {
        $originalSize = strlen($jsonData);
        $compressed = gzencode($jsonData, $compressionLevel);
        $compressedSize = strlen($compressed);

        $compressionRatio = $originalSize > 0
            ? round((1 - $compressedSize / $originalSize) * 100, 2)
            : 0;

        $this->logger->info(sprintf(
            'Compression gzip: %s → %s (gain: %s%%)',
            $this->formatBytes($originalSize),
            $this->formatBytes($compressedSize),
            $compressionRatio
        ));

        $response = new Response($compressed, $status);
        $response->headers->set('Content-Type', 'application/json');
        $response->headers->set('Content-Encoding', 'gzip');
        $response->headers->set('Vary', 'Accept-Encoding');

        return $response;
    }

    /**
     * Formate une taille en bytes en format lisible
     *
     * @param int $bytes
     * @return string
     */
    private function formatBytes(int $bytes): string
    {
        $units = ['B', 'KB', 'MB', 'GB'];
        $bytes = max($bytes, 0);
        $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
        $pow = min($pow, count($units) - 1);
        $bytes /= (1 << (10 * $pow));

        return round($bytes, 2) . ' ' . $units[$pow];
    }

    /**
     * Vérifie si le client supporte la compression gzip
     *
     * @param string|null $acceptEncoding Header Accept-Encoding de la requête
     * @return bool
     */
    public function supportsGzip(?string $acceptEncoding): bool
    {
        if ($acceptEncoding === null) {
            return false;
        }

        return str_contains(strtolower($acceptEncoding), 'gzip');
    }
}

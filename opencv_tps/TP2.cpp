#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

/**
 * TP2 - Range Expansion (Contrast Stretching) avec Histogrammes
 *
 * Ce programme:
 * 1. Lit et affiche une image en niveaux de gris
 * 2. Calcule une expansion de plage pour améliorer le contraste
 * 3. Affiche 4 fenêtres: image originale, image étendue, et leurs histogrammes
 */

// Fonction pour calculer et afficher un histogramme
Mat drawHistogram(Mat& image, const string& title) {
    // Calcul de l'histogramme
    int histSize = 256;
    float range[] = {0, 256};
    const float* histRange = {range};
    bool uniform = true;
    bool accumulate = false;

    Mat hist;
    calcHist(&image, 1, 0, Mat(), hist, 1, &histSize, &histRange, uniform, accumulate);

    // Création de l'image pour afficher l'histogramme
    int hist_w = 512;
    int hist_h = 400;
    int bin_w = cvRound((double)hist_w / histSize);

    Mat histImage(hist_h, hist_w, CV_8UC3, Scalar(255, 255, 255));

    // Normalisation de l'histogramme pour l'affichage
    normalize(hist, hist, 0, histImage.rows - 50, NORM_MINMAX, -1, Mat());

    // Dessiner les barres de l'histogramme
    for(int i = 1; i < histSize; i++) {
        line(histImage,
             Point(bin_w * (i - 1), hist_h - 25 - cvRound(hist.at<float>(i - 1))),
             Point(bin_w * (i), hist_h - 25 - cvRound(hist.at<float>(i))),
             Scalar(0, 0, 0), 2, 8, 0);
    }

    // Ajouter des lignes de référence
    line(histImage, Point(0, hist_h - 25), Point(hist_w, hist_h - 25), Scalar(200, 200, 200), 1);

    // Afficher des informations statistiques
    double minVal, maxVal;
    minMaxLoc(image, &minVal, &maxVal);
    Scalar meanVal = mean(image);

    string info1 = "Min: " + to_string((int)minVal) + " Max: " + to_string((int)maxVal);
    string info2 = "Mean: " + to_string((int)meanVal[0]);

    putText(histImage, info1, Point(10, hist_h - 10),
            FONT_HERSHEY_SIMPLEX, 0.4, Scalar(0, 0, 255), 1);
    putText(histImage, info2, Point(10, 20),
            FONT_HERSHEY_SIMPLEX, 0.4, Scalar(0, 0, 255), 1);

    return histImage;
}

// Fonction pour effectuer l'expansion de plage (contrast stretching)
Mat rangeExpansion(Mat& image) {
    Mat expanded_image;

    // Trouver les valeurs min et max de l'image
    double minVal, maxVal;
    minMaxLoc(image, &minVal, &maxVal);

    cout << "Valeurs originales - Min: " << minVal << ", Max: " << maxVal << endl;

    // Si l'image utilise déjà toute la plage, pas besoin d'expansion
    if (minVal == 0 && maxVal == 255) {
        cout << "L'image utilise déjà toute la plage [0, 255]" << endl;
        return image.clone();
    }

    // Appliquer la transformation d'expansion de plage
    // Formule: new_value = (old_value - min) * 255 / (max - min)
    expanded_image = Mat::zeros(image.size(), image.type());

    double range = maxVal - minVal;

    if (range > 0) {
        for (int y = 0; y < image.rows; y++) {
            for (int x = 0; x < image.cols; x++) {
                uchar pixel = image.at<uchar>(y, x);
                uchar new_pixel = saturate_cast<uchar>((pixel - minVal) * 255.0 / range);
                expanded_image.at<uchar>(y, x) = new_pixel;
            }
        }
        cout << "Expansion de plage effectuée: [" << minVal << ", " << maxVal
             << "] -> [0, 255]" << endl;
    } else {
        // Image uniforme (tous les pixels ont la même valeur)
        cout << "Image uniforme détectée (tous les pixels = " << minVal << ")" << endl;
        expanded_image = Mat(image.size(), image.type(), Scalar(127));
    }

    return expanded_image;
}

int main(int argc, char** argv) {
    cout << "=== TP2 - Range Expansion et Histogrammes ===" << endl;

    // Déterminer le chemin de l'image
    string imagePath;
    if (argc > 1) {
        imagePath = argv[1];
    } else {
        imagePath = "AI_totoro.png";  // Image par défaut
    }

    cout << "Chargement de l'image: " << imagePath << endl;

    // Charger l'image en niveaux de gris
    Mat original_image = imread(imagePath, IMREAD_GRAYSCALE);

    // Vérifier si l'image est bien chargée
    if (original_image.empty() || !original_image.data) {
        cout << "ERREUR: Impossible de charger l'image!" << endl;
        cout << "Utilisation: " << argv[0] << " [chemin_image]" << endl;
        cout << "Ou placez 'AI_totoro.png' dans le répertoire courant" << endl;
        return -1;
    }

    cout << "Image chargée avec succès: " << original_image.cols << "x"
         << original_image.rows << " pixels" << endl;

    // Effectuer l'expansion de plage
    cout << "\nCalcul de l'expansion de plage..." << endl;
    Mat expanded_image = rangeExpansion(original_image);

    // Calculer et dessiner les histogrammes
    cout << "Génération des histogrammes..." << endl;
    Mat hist_original = drawHistogram(original_image, "Original Histogram");
    Mat hist_expanded = drawHistogram(expanded_image, "Expanded Histogram");

    // Créer les fenêtres et afficher les images
    cout << "\nAffichage des résultats dans 4 fenêtres..." << endl;

    namedWindow("1. Original Image", WINDOW_AUTOSIZE);
    namedWindow("2. Expanded Image", WINDOW_AUTOSIZE);
    namedWindow("3. Original Histogram", WINDOW_AUTOSIZE);
    namedWindow("4. Expanded Histogram", WINDOW_AUTOSIZE);

    imshow("1. Original Image", original_image);
    imshow("2. Expanded Image", expanded_image);
    imshow("3. Original Histogram", hist_original);
    imshow("4. Expanded Histogram", hist_expanded);

    // Positionner les fenêtres pour une meilleure visualisation
    moveWindow("1. Original Image", 50, 50);
    moveWindow("2. Expanded Image", 700, 50);
    moveWindow("3. Original Histogram", 50, 550);
    moveWindow("4. Expanded Histogram", 700, 550);

    cout << "\n=== Instructions ===" << endl;
    cout << "- Observez la différence entre l'image originale et l'image étendue" << endl;
    cout << "- Comparez les histogrammes pour voir l'amélioration du contraste" << endl;
    cout << "- Appuyez sur 's' pour sauvegarder l'image étendue" << endl;
    cout << "- Appuyez sur 'q' ou ESC pour quitter" << endl;

    // Boucle principale
    while (true) {
        int key = waitKey(30) & 0xFF;

        // Quitter avec ESC ou 'q'
        if (key == 27 || key == 'q') {
            cout << "\nFermeture du programme..." << endl;
            break;
        }

        // Sauvegarder l'image étendue avec 's'
        if (key == 's') {
            string outputPath = "expanded_image.png";
            imwrite(outputPath, expanded_image);
            cout << "Image étendue sauvegardée: " << outputPath << endl;

            // Sauvegarder aussi les histogrammes
            imwrite("histogram_original.png", hist_original);
            imwrite("histogram_expanded.png", hist_expanded);
            cout << "Histogrammes sauvegardés" << endl;
        }
    }

    destroyAllWindows();
    return 0;
}

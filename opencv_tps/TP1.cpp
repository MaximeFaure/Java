#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

// variables pour l'image et la ligne
Mat original_image, display_image;
int selected_line = -1;
bool line_selected = false;

// fonction qui dessine le graphique du profil
void drawIntensityProfile(Mat& image, int line_y) {
    int graph_width = image.cols;
    int graph_height = 300;
    Mat graph = Mat::zeros(graph_height, graph_width, CV_8UC3);
    graph = Scalar(255, 255, 255); // fond blanc

    // recuperer les valeurs de gris de la ligne
    vector<uchar> intensity_values;
    for (int x = 0; x < image.cols; x++) {
        intensity_values.push_back(image.at<uchar>(line_y, x));
    }

    // dessiner le profil point par point
    for (int x = 0; x < graph_width - 1; x++) {
        // calcul de la position y (inverse car opencv commence en haut)
        int y1 = graph_height - (intensity_values[x] * (graph_height - 40) / 255) - 20;
        int y2 = graph_height - (intensity_values[x + 1] * (graph_height - 40) / 255) - 20;

        // trace la ligne entre 2 points
        line(graph, Point(x, y1), Point(x + 1, y2), Scalar(0, 0, 0), 1);
    }

    imshow("Intensity Profile", graph);
}

// callback quand on clique sur l'image
void onMouse(int event, int x, int y, int flags, void* userdata) {
    if (event == EVENT_LBUTTONDOWN) {
        selected_line = y;
        line_selected = true;

        // copie de l'image originale
        display_image = original_image.clone();

        // conversion gris vers couleur pour dessiner en rouge
        if (display_image.channels() == 1) {
            cvtColor(display_image, display_image, COLOR_GRAY2BGR);
        }

        // trace la ligne rouge horizontale
        line(display_image, Point(0, y), Point(display_image.cols, y), Scalar(0, 0, 255), 2);

        imshow("Display Image", display_image);

        // afficher le profil d'intensite
        drawIntensityProfile(original_image, y);

        cout << "Ligne selectionnee: y = " << y << endl;
    }
}

int main(int argc, char** argv) {
    cout << "=== DEBUT DU PROGRAMME ===" << endl;

    // chemin vers l'image
    string imagePath = "test.jpg";
    cout << "Chargement de: " << imagePath << endl;

    original_image = imread(imagePath, IMREAD_GRAYSCALE);

    cout << "Lecture terminee" << endl;

    // verif si l'image est bien chargee
    if (!original_image.data) {
        cout << "ERREUR: Image non trouvee!" << endl;
        return -1;
    }

    cout << "Image OK: " << original_image.cols << "x" << original_image.rows << endl;

    display_image = original_image.clone();

    // creation fenetre et callback souris
    cout << "Creation fenetre..." << endl;
    namedWindow("Display Image", WINDOW_AUTOSIZE);
    setMouseCallback("Display Image", onMouse, nullptr);

    cout << "Affichage image..." << endl;
    imshow("Display Image", display_image);

    cout << "Attente clic (appuyez q pour quitter)..." << endl;

    // boucle principale
    while (true) {
        int key = waitKey(30) & 0xFF;

        // quitter avec echap ou q
        if (key == 27 || key == 'q') {
            cout << "Fermeture..." << endl;
            break;
        }

        // touche r pour reset
        if (key == 'r') {
            display_image = original_image.clone();
            imshow("Display Image", display_image);
            destroyWindow("Intensity Profile");
            line_selected = false;
            cout << "Reset - cliquez pour nouvelle ligne" << endl;
        }
    }

    destroyAllWindows();
    return 0;
}

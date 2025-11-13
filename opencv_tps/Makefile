# Makefile pour les TPs OpenCV
# Utilise pkg-config pour trouver les flags OpenCV

CXX = g++
CXXFLAGS = -std=c++11 -Wall
OPENCV_FLAGS = `pkg-config --cflags --libs opencv4`

# Si opencv4 n'est pas trouvé, essayer opencv
ifeq ($(shell pkg-config --exists opencv4; echo $$?),1)
    OPENCV_FLAGS = `pkg-config --cflags --libs opencv`
endif

# Cibles
all: tp1 tp2

tp1: TP1.cpp
	@echo "Compilation de TP1..."
	$(CXX) $(CXXFLAGS) TP1.cpp -o tp1 $(OPENCV_FLAGS)
	@echo "TP1 compilé avec succès!"

tp2: TP2.cpp
	@echo "Compilation de TP2..."
	$(CXX) $(CXXFLAGS) TP2.cpp -o tp2 $(OPENCV_FLAGS)
	@echo "TP2 compilé avec succès!"

# Nettoyage
clean:
	@echo "Nettoyage des fichiers compilés..."
	rm -f tp1 tp2
	rm -f expanded_image.png histogram_*.png
	@echo "Nettoyage terminé!"

# Règles pour exécuter les programmes
run_tp1: tp1
	./tp1

run_tp2: tp2
	./tp2

# Télécharger l'image de test pour TP2
download_test_image:
	@echo "Téléchargement de l'image de test..."
	wget -O AI_totoro.png https://mavromatis.org/dl/AI_totoro.png
	@echo "Image téléchargée!"

.PHONY: all clean run_tp1 run_tp2 download_test_image

# Objetivos

1. Identificar correctamente qué imágenes de mascotas son perros (incluso si la raza no está clasificada) y qué imágenes no lo son.
2. Clasificar correctamente la raza del perro, para las imágenes que son de perros.
3. Determinar qué modelo de arquitectura _CNN_ (_ResNet_, _AlexNet_, o _VGG_) se ajusta mejor a los objetivos 1 y 2.
4. Considerar el tiempo necesario para alcanzar de la mejor forma los objetivos 1 y 2 y determinar si una solución alternativa habría dado una solución _"suficientemente buena"_, teniendo en cuenta el tiempo que lleva ejecutar cada uno de los objetivos.

# Tarea

Editar el programa `check_images.py` y completarlo para alcanzar los objetivos anteriores.


# Program Outline
Repeat below for all three image classification algorithms (e.g. input algorithm as command line argument):

1. Time your program
   * Use Time Module to compute program runtime
2. Get program Inputs from the user
   * Use command line arguments to get user inputs
3. Create Pet Images Labels
   * Use the pet images filenames to create labels
   * Store the pet image labels in a data structure (e.g. dictionary)
4. Create Classifier Labels and Compare Labels
   * Use the Classifier function classify the images and create the classifier labels
    * Compare Classifier Labels to Pet Image Labels
    * Store Pet Labels, Classifier Labels, and their comparison in a complex data structure (e.g. dictionary of lists)
5. Classifying Labels as "Dogs" or "Not Dogs"
    * Classify all Labels (Pet & Classifier) as "Dogs" or "Not Dogs" using dognames.txt file
    * Store new classifications in the complex data structure (e.g. dictionary of lists)
6. Calculate the Results
    * Use Labels and their classifications to determine how well the algorithm worked on classifying images.
7. Print the Results


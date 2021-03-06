#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# PROGRAMMER: Roberto Hernando
# DATE CREATED: 16/04/2020
# REVISED DATE:             <=(Date Revised - if any)
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()
    
    # 2. Define get_input_args() function to create & retrieve command
    # line arguments
    in_arg = get_input_args()
    #check_command_line_arguments(in_arg)
    
    # 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function    
    answers_dic = get_pet_labels(in_arg.dir)
    # check_creating_pet_image_labels(answers_dic)

    # 4. Define classify_images() function to create the classifier 
    # labels with the classifier function using in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)
    # check_classifying_images(result_dic)

    # 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, in_arg.dogfile)
    # check_classifying_labels_as_dogs(result_dic)

    # 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(result_dic)
    # check_calculating_results(result_dic, results_stats_dic)

    # 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results(result_dic, results_stats_dic, in_arg.arch, True, True)

    # 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    # 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format    
    tot_time = end_time - start_time
    print("\n** Total Elapsed Runtime:", str( int( (tot_time / 3600) ) ) + ":" + 
          str( int(  ( (tot_time % 3600) / 60 )  ) ) + ":" + 
          str( int( ( (tot_time % 3600) % 60 ) ) ))


def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguments are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='pet_images/', type=str, 
                        help='ruta del directorio de fotos')
    parser.add_argument('--arch', default='vgg', type=str, 
                        help='algoritmo de clasificación de imágenes')
    parser.add_argument('--dogfile', default='dognames.txt', type=str, 
                        help='fichero de texto con las etiquetas asociadas')
    return parser.parse_args()


def get_pet_labels(images_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these labels as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
    petlabes_dic = dict()
    img_files = listdir(images_dir)
    for img_file in img_files:
            word_list_img_file = img_file.split('_')[:-1]
            img_label = ""
            for word in word_list_img_file:
                img_label += word.lower() + " " 
            img_label = img_label.strip()   
            petlabes_dic[img_file] = img_label
    return(petlabes_dic)


def classify_images(images_dir, petlabel_dic, model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its key is the
                     pet image filename & its value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
    results_dic = dict()
    for img_file, img_label in petlabel_dic.items():
        class_label = classifier(images_dir + img_file, model).lower()
        result = 0
        if img_label in class_label:
            for label in class_label.split(','):
                if img_label == label.lower().strip():
                    result = 1
                    continue
                else:
                    for label_word in label.split(' '):
                        if img_label == label_word.lower().strip():
                            result = 1
                            continue
        results_dic [img_file] = [img_label, class_label, result]
    return(results_dic)


def adjust_results4_isadog(results_dic, dogsfile):
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line.
                Dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """           
    with open(dogsfile, 'r') as f:
        file_data = f.read()
    for img, result in results_dic.items():
        idx3 = idx4 = 0
        if result[0] in file_data:
            idx3 = 1
        if result[1] in file_data:
            idx4 = 1
        result.append(idx3)
        result.append(idx4)
        



def calculates_results_stats(results_dic):
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    n_images = len(results_dic)
    n_dog_images = 0 
    n_not_dog_images = 0 
    correct_dog = 0
    correct_not_dog = 0
    correct_breed = 0

    for img, result in results_dic.items():
        if result[3] == 1:
            n_dog_images +=1
            if result[4] == 1:
                correct_dog += 1
                if result[2] == 1:
                    correct_breed += 1
        else:
            n_not_dog_images += 1
            if result[4] == 0:
                correct_not_dog += 1

    calculates_results_stats = dict()
    calculates_results_stats['n_images'] = n_images
    calculates_results_stats['n_dogs_img'] = n_dog_images        
    calculates_results_stats['n_notdogs_img'] = n_not_dog_images        
    calculates_results_stats['pct_correct_dogs'] = correct_dog / n_dog_images * 100
    calculates_results_stats['pct_correct_notdogs'] = correct_not_dog / n_not_dog_images * 100
    calculates_results_stats['pct_correct_breed'] = correct_breed / n_dog_images * 100

    return(calculates_results_stats)



def print_results(results_dic, results_stats, model, print_incorrect_dogs = False,
                  print_incorrect_breed = False):
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    # Prints summary statistics over the run
    print("\n\n*** Results Summary for CNN Model Architecture",model.upper(), 
          "***")
    print("%20s: %3d" % ('N Images', results_stats['n_images']))
    print("%20s: %3d" % ('N Dog Images', results_stats['n_dogs_img']))
    print("%20s: %3d" % ('N Not-Dog Images', results_stats['n_notdogs_img']))

    # Prints summary statistics (percentages) on Model Run
    print(" ")
    for key in results_stats:
        if key[0] == "p":
            print("%20s: %5.1f" % (key, results_stats[key]))


    # process through results dict, printing incorrectly classified dogs
    for key in results_dic:

        # Pet Image Label is a Dog - Classified as NOT-A-DOG -OR- 
        # Pet Image Label is NOT-a-Dog - Classified as a-DOG
        if sum(results_dic[key][3:]) == 1:
            print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                        results_dic[key][1]))

    # process through results dict, printing incorrectly classified breeds
    for key in results_dic:

        # Pet Image Label is-a-Dog, classified as-a-dog but is WRONG breed
        if ( sum(results_dic[key][3:]) == 2 and
            results_dic[key][2] == 0 ):
            print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                        results_dic[key][1]))

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()

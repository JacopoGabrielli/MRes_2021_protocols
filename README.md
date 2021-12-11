# Automated Combinatorial Golden Gate and Transformation - Isaac Newtron

## Introduction
The Isaac Newtron team (Jacopo Gabrielli, Leo Gornovskiy, Luis Enrique García Riveira, Menglu Wu, Shi Yi and Sifeng Chen) is presenting a protocol for the automation of combinatorial Golden Gate cloning. In practice, our app can be used to automate cloning protocols where there is a fixed vector backbone (part 1) and a fixed DNA part (part 3) and two variable DNA parts (part 2 and 4) for which multiple variants have to be tested in combination. For example, part 1 could be a generic plasmid backbone, part 3 a 5'UTR + coding sequence, and parts 2 and 4 could be respectively the promoter and the 3'UTR. As the promoter influences the transcription rate, therefore, the amount of mRNA produced and the 3'UTR the mRNA stability. Testing multiple combinations allows to optimise the construct for desired properties of the mRNAs, for example, low quantity and high stability or the opposite. Moreover, it would illuminate the combinatorial behaviour of the two parts, such as possible undesired interactions and folding of the DNA structure due to homologies in the sequences. 

## Contents
The submission comprises 3 files: 
- GUI_Isaac_Newtron.py
- Template_Protocol_Isaac_Newtron.py
- Combinations_Isaac_Newtron.csv

GUI_Isaac_Newtron.py - Constitutes the Graphical User Interface through which the users' designs are uploaded in a ".csv" format. The app also creates and saves a protocol for the combinatorial assembly of the two parts in ".py" format which can be run in the OpenTron without further modifications. Furthermore, the app will create and save a file in ".csv" format informing the user on the final plate layout with the well name written as "Letter + Number" and the combination written as "part 2 part 4".

Template_Protocol_Isaac_Newtron.py - Constitutes the template which GUI_Isaac_Newtron.py uses to write the customised protocol based on the information from the ".csv" file uploaded. 

Combinations_Isaac_Newtron.csv - Constitutes an example of a ".csv" file containing a number of promoters and UTRs listed vertically under their respective headers. This can be modified to the user's needs and uploaded on GUI_Isaac_Newtron.py to generate a customised protocol. 




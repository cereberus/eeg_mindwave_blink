/*
Fast Artificial Neural Network Library (fann)

Script for recognizing blinking artifacts. 
Features of raw EEGS signal were used to train the network.

Now new data is being read from file. 
By default 3 features are taken to input[0], input[1], input[2]
Then output is calculated.

Output:
 * Not blinking:    0
 * Blinking:        1

*/

#include <stdio.h>
#include <stdlib.h>     /* strtof */
#include "floatfann.h"

int main()
{
    FILE *stream_input;
    FILE *stream_output;
    char file_input[] = "data_category.data";
    char file_output[] = "../csv_eeg_ann/categorized_blink";
    char *sample_begin;
    char *sample_end;
    char my_string[100];
    char calc_output[50];
	fann_type *calc_out;
	fann_type input[3];

	struct fann *ann = fann_create_from_file("net_eeg_data_float.net");
    
    stream_input = fopen (file_input, "r");
    fgets (my_string, 100, stream_input);
     
    stream_input = fopen(file_input, "r");
    int i = 0;
    int j = 0;
    float f1; 
    printf("\n");
    while (fgets(my_string,100, stream_input) != NULL) {
            i++;
            if(j<2){
                if((stream_output = fopen(file_output, "a"))!=NULL){
//                     printf("%s\n",my_string);
                    fprintf(stream_output, "%s", my_string); 
                }
                fclose(stream_output);
            }
            else{
                f1 = strtof (my_string, NULL);
                input[j-2]= f1; 
//                 printf("input[%d]: %f\n", j-2, f1);
            }
//             printf("input[%d] = %f\n", j, input[j]);
            j++;
            if(j==5){
                j=0;
//                 printf("\n");
                calc_out = fann_run(ann, input);
                snprintf(calc_output,50,"%f",calc_out[0]);
//                 printf("%s",calc_output);
                if((stream_output = fopen(file_output, "a"))!=NULL){
                    fprintf(stream_output, "%s\n",calc_output); 
                }
                fclose(stream_output);
//                 printf("is it blink or norma (%f,%f,%f) -> %f\n\n",input[0], input[1], input[2], calc_out[0]);
            }
    }   

    fclose (stream_input);

	

	fann_destroy(ann);
	return 0; 
}

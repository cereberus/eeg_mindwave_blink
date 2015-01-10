#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[] ){
    FILE *fp;
    char buffer[70];
    fp = fopen(argv[1], "r");

    while(fgets(buffer,70,fp) != NULL){
        puts(buffer);
    }
    fclose(fp);
    return 0;
}

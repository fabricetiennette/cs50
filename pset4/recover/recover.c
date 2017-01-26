#include <stdio.h>
#include <stdint.h>


const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
 
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        fprintf(stderr, "Could not open file\n");
        return 2;
    }
    

    uint8_t buffer[512];
    
   
    int jpeg_counter = 0;
  

   
    FILE *img = NULL;
    

    while(fread(buffer, BLOCK_SIZE, 1, infile))
    {
     
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff
            && (buffer[3] & 0xf0) == 0xe0)
        {
           
            if (img != NULL)
            {
             
                fclose(img);
            }
            
      
            char filename[8];
            sprintf(filename, "%03i.jpg", jpeg_counter);
            img = fopen(filename, "w");
            jpeg_counter++;
        }
        
       
        if (img != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }
    
 
    if (img != NULL)
    {
        fclose(img);
    }
    

    fclose(infile);
  
    return 0;
    
}
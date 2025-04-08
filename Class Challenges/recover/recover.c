#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[BLOCK_SIZE];

    char filename[8];
    int file_count = 0;
    FILE *img = NULL;
    int jpeg_found = 0;

    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpeg_found == 1)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create image file.\n");
                fclose(card);
                return 1;
            }

            file_count++;

            jpeg_found = 1;
        }

        if (jpeg_found == 1)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);

    return 0;
}

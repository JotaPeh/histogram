#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void cumsum(float *array, int size) {
    float sum = 0;
    for (int i = 0; i < size; i++) {
        sum += array[i];
        array[i] = sum;
    }
    
    for (int i = 0; i < size; i++) {
        array[i] = 255*array[i]/array[size-1];
    }
}

int main(int argc, char *argv[]) {
    long size = 0;

    // Image dimensions
    int total_height = 0;
    int width = 4096;
    int bytespp = 4;

    if (argc != 3 || atoi(argv[2]) % 20 != 0) {
        printf("Use: %s <file.tiff> <height (divisible by 20)>\n", argv[0]);
        return 1;
    }

    int height = atoi(argv[2]);

    const char *file_name = argv[1];
    FILE *files = fopen(file_name, "rb");
    

    if (files == NULL) {
        printf("Error while opening the file %s\n", file_name);
        return 1;
    } else {
        fseek(files, 0, SEEK_END);
        size = ftell(files);
        fclose(files);
        total_height = size / (width*bytespp);
    }

    FILE *fileint = fopen(file_name, "rb");
    fseek(fileint, size % (width*bytespp), SEEK_SET);

    float hist[256] = {0};  
    unsigned char slot;
    for (int i = 0; i < total_height * width * bytespp; i++) {
        if (fread(&slot, 1, 1, fileint) != 1) {
            printf("Error while reading the file %s\n", file_name);
            fclose(fileint);
            return 1;
        } else {
            hist[(int) slot] += 1;
        }
    }

    cumsum(hist, 256);
    uint8_t hist_int[256];
    for (int i = 0; i < 256; i++) {
        hist_int[i] = (uint8_t) hist[i];
    }

    fclose(fileint);
    FILE *fileint2 = fopen(file_name, "rb");
    fseek(fileint2, size % (width*bytespp), SEEK_SET);
    FILE *filefe = fopen("acs_full_equal_C.bin", "ab");
    if (filefe) {
        
        for (int i = 0; i < total_height; i++) {
            for (int j = 0; j < width; j++) {
                for (int k = 0; k < bytespp; k++) {
                    if (fread(&slot, 1, 1, fileint2) != 1) {
                        printf("Error while reading the file %s\n", file_name);
                        return 1;
                    }
                    fwrite(&hist_int[(int) slot], 1, 1, filefe);
                }
            }
        }
    } else {
        printf("Couldn't open acs_full_equal_C.bin.\n");
    }
    
    fclose(fileint2);
    fclose(filefe);
    
    FILE *file = fopen("acs_full_equal_C.bin", "rb");

    int cycles = total_height / height;
    for (int p = 0; p <= cycles; p++) {
        if (total_height < height) {
            height = total_height;
        }
        if(height <= 0) break;
        unsigned char image[height][width][bytespp];
        unsigned char im2[height / 20][width / 20 + 1][bytespp];

        // Read TIFF
        total_height -= height;
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (fread(image[i][j], 1, bytespp, file) != bytespp) {
                    printf("Error while reading the file %s\n", file_name);
                    fclose(file);
                    return 1;
                }
            }
        }

        // "Decimate"
        for (int i = 0; i < height; i += 20) {
            for (int j = 0; j < width + 4; j += 20) {
                for (int k = 0; k < bytespp; k++) {
                    im2[i / 20][j / 20][k] = image[i][j][k];
                }
            }
        }

        FILE *file2 = fopen("acs_half_C.bin", "ab");
        if (file2) {
            fwrite(im2, 1, height * (width + 4)* bytespp / 400, file2);
            fclose(file2);
        } else {
            printf("Couldn't open acs_half_C.bin.\n");
        }

    }

    fclose(file);
    return 0;
}

// // Debug
// printf("jump: %ld \n",size % (4096*4));
// printf("%d\n", total_height);
// for (int j = 50; j < 55; j++) {
//     printf("Pixel (%d, %d): ", 0, j);
//     for (int k = 0; k < bytespp; k++) {
//         printf("%d ", image[0][j][k]);
//     }
//     printf("\n");
// }
// 
// if (cic == 1) {
// for (int j = 0; j < 205; j++) {
//     printf("%d: [ ", j);
//     for (int k = 0; k < bytespp; k++) {
//         printf("%d ", im2[0][j][k]);
//     }
//     printf("]\n");
// }
// }
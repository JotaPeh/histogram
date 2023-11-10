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
        array[i] = array[i]/array[size-1];
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3 || atoi(argv[2]) % 20 != 0) {
        printf("Use: %s <file.tiff> <height (divisible by 20)>\n", argv[0]);
        return 1;
    }
    int height = atoi(argv[2]);
    const char *file_name = argv[1];
    long size = 0;
    int save_half = 1;

    // Image dimensions
    int total_height = 0;
    int th = 0;
    int width = 4096;
    int bytespp = 2;

    // Size
    FILE *file_size  = fopen(file_name, "rb");
    
    if (file_size == NULL) {
        printf("Error while opening the file %s\n", file_name);
        return 1;
    } else {
        fseek(file_size , 0, SEEK_END);
        size = ftell(file_size );
        fclose(file_size );
        total_height = size / (width*bytespp);
        th = total_height;
    }

    FILE *file = fopen(file_name, "rb");
    fseek(file, size % (width*bytespp), SEEK_SET);
    
    // Subsample
    FILE *file_bin_op = fopen("half_C.bin", "wb");
    fclose(file_bin_op);

    int cycles = total_height / height;
    for (int p = 0; p <= cycles; p++) {
        if (total_height < height) {
            height = total_height;
        }
        if(height <= 0) break;
        uint16_t im1[height][width];
        uint16_t im2[height / 20][width / 20 + 1];

        // Read TIFF
        total_height -= height;
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (fread(&im1[i][j], sizeof(uint16_t), 1, file) != 1) {
                    printf("Error while reading the file %s\n", "equal_C.bin");
                    fclose(file);
                    return 1;
                }
            }
        }

        // "Decimate"
        for (int i = 0; i < height; i += 20) {
            for (int j = 0; j < width + 4; j += 20) {
                im2[i / 20][j / 20] = im1[i][j];
            }
        }

        FILE *file_bin = fopen("half_C.bin", "ab");
        if (file_bin) {
            fwrite(im2, sizeof(uint16_t), height * (width + 4) / 400, file_bin);
            fclose(file_bin);
        } else {
            printf("Couldn't open half_C.bin.\n");
        }

    }

    fclose(file);
    
    // Histogram
    FILE *file_hist = fopen("half_C.bin", "rb");
    float cdf[65536] = {0};
    uint16_t slot;
    total_height = th * (width + 4) / 400;

    for (int i = 0; i < total_height; i++) {
        if (fread(&slot, sizeof(uint16_t), 1, file_hist) != 1) {
            printf("Error while reading the file %s\n", "half_C.bin");
            fclose(file_hist);
            return 1;
        } else {
            cdf[slot] += 1;
        }
    }

    cumsum(cdf, 65536);

    fclose(file_hist);

    // Histogram equalize
    FILE *file_hist_2 = fopen("half_C.bin", "rb");
    FILE *file_equal = fopen("equal_C.bin", "wb");

    if (file_equal) {
        for (int i = 0; i < total_height; i++) {
            if (fread(&slot, sizeof(uint16_t), 1, file_hist_2) != 1) {
                printf("Error while reading the file %s\n", "half_C.bin");
                return 1;
            }
            fwrite(&cdf[slot], sizeof(float), 1, file_equal);
        }
    } else {
        printf("Couldn't open equal_C.bin.\n");
    }
    
    fclose(file_hist_2);
    fclose(file_equal);

    if (!save_half) {
        if (remove("half_C.bin") != 0) {
            perror("Error removing the file");
        }
    }

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
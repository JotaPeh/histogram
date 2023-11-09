#include <stdio.h>

// Função para fazer alterações em um vetor


int main() {
    int tamanho = 5;
    int meuVetor[] = {1, 2, 3, 4, 5};

    // Chame a função passando o vetor e o tamanho
    alterarVetor(meuVetor, tamanho);

    // O vetor foi alterado pela função e agora contém os valores alterados
    for (int i = 0; i < tamanho; i++) {
        printf("%d ", meuVetor[i]);
    }

    return 0;
}



# SeamCarving
Content-Aware Resizing using Seam Carving Image Processing


# Objetivo Principal

O objetivo principal desse projeto é implementar o algoritmo de Seam Carving para fazer Resize de imagens levando em conta o conteudo da imagem. O que queremos é aumentar e diminuir o tamanho de uma imagem levando em conta o conteudo da imagem, ou seja, queremos inserir ou remover linhas e colunas sem distorcer o conteudo principal da imagem.

Essa é uma tecnica muito interessante que permite uma imagem se adequar a diferentes formatos sem distorcer a imagem. Uma utilidade citada pelo Paper original diz que uma ideia interessante é utilizar esse algoritmo para imagens em site da web que devem ser visualizadas em dispositivos diferentes que tem aspect ratios diferentes.

Outra utilidade desse algoritmo discutido no Paper original tambem é a capacidade de remover objetos da

# input Images

Qualquer imagem pode ser input para esse algoritmo, entretanto as imagens que se darão melhor são as imagens que são compostas majoritariamente por background e com poucos elementos importantes na imagem.

As imagens utilizadas nessa primeira parte do projeto foram obtidas do exemplo do algoritmo existente na wikipedia:
    Site: https://en.wikipedia.org/wiki/Seam_carving 
E tambem a imagem do quadro "A persistencia da Memoria" do pintor Salvador Dali que foi usada de exemplo em video explicando o algoritmo
    Video: https://www.youtube.com/watch?v=ALcohd1q3dk&ab_channel=TheJuliaProgrammingLanguage
    Imagem: https://i.pinimg.com/originals/c6/24/f5/c624f57595292a5ec8a229386be745d6.jpg

As imagens para o projeto final serão imagens interessantes que nosso grupo consiga encontrar. Mas as imagens mais seguras para fazer os testes caso tenhamos dificuldades de encontrar imagens legais, podemos pegar as imagens do Paper original que apresentou esse conceito de Seam Carving.
    Paper: https://faculty.idc.ac.il/arik/SCWeb/imret/imret.pdf

# Descrição dos Passos


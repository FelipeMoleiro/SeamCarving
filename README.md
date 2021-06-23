# SeamCarving
Content-Aware Resizing using Seam Carving Image Processing

# Alunos

Felipe Guilermmo Santuche Moleiro - 10724010
Mateus Prado Santos - 10851707
Vinicius Ricardo Carvalho - 10724413

# Objetivo Principal

O objetivo principal deste projeto é implementar o algoritmo de Seam Carving para fazer Resize de imagens levando em conta seu conteúdo. O que queremos é aumentar e diminuir o tamanho de uma imagem levando em conta seu conteúdo, ou seja, queremos inserir ou remover linhas e colunas sem distorcer o conteúdo principal da imagem.

Esta é uma tecnica muito interessante que permite uma imagem se adequar a diferentes formatos sem distorcê-la. Uma utilidade citada pelo Paper original diz que uma ideia interessante é utilizar esse algoritmo para imagens em site da web que devem ser visualizadas em dispositivos diferentes que tem aspect ratios diferentes.

Outra utilidade desse algoritmo discutido no Paper original é tambem a capacidade de remover objetos da imagem. Essa técnica permite marcar objetos que queremos remover e o algoritmo vai priorizar a remoção desses pixels durante o processamento.

# input Images

Qualquer imagem pode ser input para esse algoritmo, entretanto as imagens que se darão melhor são as que são compostas majoritariamente por background e com poucos elementos importantes na imagem.

As imagens utilizadas nessa primeira parte do projeto foram obtidas do exemplo do algoritmo existente na wikipedia:
    Site: https://en.wikipedia.org/wiki/Seam_carving 
E tambem a imagem do quadro "A persistencia da Memoria" do pintor Salvador Dali que foi usada de exemplo em video explicando o algoritmo:
    Video: https://www.youtube.com/watch?v=ALcohd1q3dk&ab_channel=TheJuliaProgrammingLanguage
    Imagem: https://i.pinimg.com/originals/c6/24/f5/c624f57595292a5ec8a229386be745d6.jpg

As imagens para o projeto final serão imagens interessantes que nosso grupo consiga encontrar. Mas as imagens mais seguras para fazer os testes caso tenhamos dificuldades de encontrar imagens legais, podemos pegar as imagens do Paper original que apresentou esse conceito de Seam Carving.
    Paper: https://faculty.idc.ac.il/arik/SCWeb/imret/imret.pdf

Para ver os exemplos em uso basta ver o documento "Demonstration Working Algorithm.ipynb"


# Descrição dos Passos

O primeiro passo para fazer esse processamento é a identificação dos pixels mais importantes na tela. Esse passo tambem é o mais importante pois a partir dele que o resto do algoritmo se baseia. Para definir esses pixels mais importantes nos podemos utilizar diversas tecnicas de processamentos de imagens e principalmente de segmentação de imagens.

No Paper descrito o melhor algoritmo para esse calculo de importancia dos pixels foi utilizando uma detecção de bordas com as derivadas parciais. Na nossa implementação parcial decidimos utilizar só esse algoritmo, mas para o projeto final poderia ser interessante testar outros tipos de segmentação. Um caso interessante também seria o uso de detecção de faces ou até mesmo Machine Learning para identificar objetos. Sendo assim, podemos identificar objetos importantes da imagem de diversas formas.

Com o cálculo dos pixels mais importantes da imagem, podemos passar para o proximo passo que é calcular todos os possiveis cortes que poderiam ser feitos na imagem. Obviamente, utilizar a força bruta é possivel, mas totalmente inviável em questão de tempo de execução. Infelizmente, não existe um algoritmo guloso para isso, mas podemos utilizar tecnicas de programação dinamica para encontrar a melhor solução em um tempo razoavel. Para isso, montamos a matriz de baixo para cima e vamos salvando os valores conforme vamos calculando, somando o valor atual com o mínimo dos tres pixels abaixo. Ao fim desse processo, temos o menor caminho possível que corta a imagem.

Por último, temos apenas que remover(ou adicionar, dependendo do algoritmo) esse caminho e repetir esse processo descrito o número de vezes que quisermos. E claro, repetimos esse algoritmo um número de vezes na horizontal e outro na vertical para ajustar os dois parâmetros do resize.

Um outro passo adicional básico que poderia ser colocado nesse processo é a remoção de objetos. Para fazer a remoção de objetos, é necessario, antes de mandar a imagem para o primeiro passo do algoritmo anterior, criar uma máscara informando os pixels da imagem(que representam o objeto) que você deseja remover. Essa identificação dos pixels que deseja remover pode ser feita manualmente ou até mesmo automaticamente utilizando algum outro tipo de processamento de imagens.

# Demonstração Entrega Parcial

Para essa entrega parcial, implementamos o basico do algoritmo, então temos ele funcionando para remover um número arbitrario de colunas da imagem. Ainda restam diversas funcionalidades a serem feitas, mas já é possivel ver o funcionamento e a ideia por tras do algoritmo.

A partir desta implementação, podemos adicionar cortes horizontais, ou mudando algumas partes da implementação, ou simplesmente rotacionando a imagem em 90 graus.

Ainda será necessario implementar a inserção de linhas e colunas, remoção de objetos e técnicas para identificar pixels relevantes e objetos. Entretanto, tudo segue da base implementada nessa entrega parcial.

Para ver os resultados parciais, basta observar o documento "Demonstration Working Algorithm.ipynb"

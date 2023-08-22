import numpy as np
from PIL import Image


def Open_Image_Convert2Matrix(Image_path):
    MatrixofImage = np.asarray(Image.open(Image_path), np.uint8)
    return MatrixofImage

def Covert_to_GrayScale(Image_matrix):
   return

def SegmentationOfShades(Image_matrix, number_of_shades):
    MatrixSegmented = np.zeros((Image_matrix.shape[0],Image_matrix.shape[1]),np.uint8)
    BrigthnessLevels = np.zeros(number_of_shades,np.uint8)
    ColorRange = (256/(number_of_shades-1))
    BrigthnessLevels[0]=0
    for i in range (1, number_of_shades):
         BrigthnessLevels[i] = (ColorRange*i)-1
    
    for i in range(0,Image_matrix.shape[0]):
             for l in range(0,Image_matrix.shape[1]):
                  k = 0
                  ColorRangeFound = 0
                  while(ColorRangeFound!=1):      
                       if(k==(number_of_shades-1) and Image_matrix[i][l]==BrigthnessLevels[k]):
                           ColorRangeFound = 1
                       elif(Image_matrix[i][l]>=BrigthnessLevels[k] and Image_matrix[i][l]<BrigthnessLevels[k+1] ):
                            ColorRangeFound = 1  
                       else :
                           k+=1
                  MatrixSegmented[i][l] =  BrigthnessLevels[k]

    return MatrixSegmented

                          
def ImageGrayScaleTOASCII(Image_matrix,brigthnesAscIILevel):
   NumberOfShadesASCII  = len(brigthnesAscIILevel)
   ColorRange = (256/NumberOfShadesASCII)
   Matrix_Image_Gray_Levels = SegmentationOfShades(Image_matrix, NumberOfShadesASCII)
   ASCII_Image = [""]
   for i in range(0, Matrix_Image_Gray_Levels.shape[0]):
             for l in range(0, Matrix_Image_Gray_Levels.shape[1]):
                 ASCII_Image[i] += brigthnesAscIILevel[int(Matrix_Image_Gray_Levels[i][l]/ColorRange)]
             ASCII_Image.append("")
   return ASCII_Image

def SaveinTXT(ImageInAscII,name):
     txt_file = open((name)+"AscII.txt","w")
     for i in range(0, len(ImageInAscII)-1):
          txt_file.write(ImageInAscII[i])
          txt_file.write("\n")
     txt_file.close()

def Display_ASCII_Image(AscII_image):
     for i in range(0,len(AscII_image)):
        print(AscII_image[i])
     return

def equalizacao_histograma(imagem_original):
  imagem = imagem_original
  imagem_equalizada = np.zeros( (imagem.shape[0],imagem.shape[1]) , np.uint8 )
  incidencia = np.zeros((4,256))
  probabilidade_acumulada = 0
  n_pixels = imagem.shape[0] * imagem.shape[1]

  for i in range(0, imagem.shape[0]):
    for j in range(0, imagem.shape[1]):
       incidencia[0][imagem[i][j]]+=1

  for k in range(0,256):
    incidencia[1][k] = (incidencia[0][k] / n_pixels)

  for k in range(0,256):
    probabilidade_acumulada += incidencia[1][k]
    incidencia[2][k] = probabilidade_acumulada

  for k in range(0,256):
    incidencia[3][k] = np.uint8(255* incidencia[2][k] )


  for y in range(0, imagem_equalizada.shape[0]):
    for z in range(0, imagem_equalizada.shape[1]):
      tom = imagem[y][z]
      imagem_equalizada[y][z] = incidencia[3][tom]

  return imagem_equalizada


def correcao_gama(imagem, c,e,y):
  imagem_modificada = np.zeros((imagem.shape[0],imagem.shape[1]), np.uint8)
  for i in range(0, imagem.shape[0]):
    for j in range(0,imagem.shape[1]):
      aux = ((imagem[i][j]/255)+e)
      g = np.double((pow(aux,y)))
      imagem_modificada[i][j] = np.uint8(g*255)
  return imagem_modificada

def InvertString(x):
  return x[::-1]

shades1 =  ".:-=+#%@"
#shades = "$@B%&WM#*oahkbdpwmZOQLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^'. "
#shades =  InvertString(shades)
imagem_path = input("Qual o caminho da imagem:")
Carachter_per_line = int(input("Quantos caracteres por linha:"))
image = Image.open(imagem_path).convert("L")
size_image = image.size
proportions = size_image[1]/size_image[0]
image = image.resize((Carachter_per_line,int(Carachter_per_line*proportions)))
Matrix_image = np.asarray(image,np.uint8)
Image_eq = equalizacao_histograma(Matrix_image)
Image_eq = correcao_gama(Matrix_image, 1,0,0.5)
Matrix_gray_levels = SegmentationOfShades(Image_eq,len(shades1))
imagem = Image.fromarray(Matrix_gray_levels, mode = "L")
imagem.show()
Matrix_gray_levels = np.asarray(imagem,np.uint8)
Ascii_image = ImageGrayScaleTOASCII(Matrix_gray_levels,shades1)
SaveinTXT(Ascii_image,"Pato")
#Display_ASCII_Image(Ascii_image)

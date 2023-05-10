import treepoem
import os
from PIL import Image, ImageDraw, ImageFont


def datamatrix_create(datamatrix_data: str):
    '''
    Функция для преобразования строки в датаматрикс с названием {строка}.png

    аргументы:
    @damamatrix_data-передаваемая строчка для закодирования её в датаматрикс
    '''

    image = treepoem.generate_barcode(barcode_type="datamatrix",
                                      data=datamatrix_data)
    image.convert("1").resize((200, 200)).save(f"{datamatrix_data}.jpg")
    image_full = Image.new('RGB', (400, 400), (255, 255, 255))
    image_text = Image.new('RGB', (400, 400), (255, 255, 255))
    image_barcode = Image.open(f"{datamatrix_data}.jpg")
    font = ImageFont.truetype("arial.ttf", 60)
    drawer = ImageDraw.Draw(image_text)
    drawer.text(
        (40, 280), f"BOARD ID:\n{datamatrix_data}", font=font, fill='black')
    image_full.paste(image_text, (0, 0))
    image_full.paste(image_barcode, (100, 80))
    image_full.save(f'{datamatrix_data}.jpg')
    os.system(f"lp {datamatrix_data}.jpg")
    os.remove(f"{datamatrix_data}.jpg")

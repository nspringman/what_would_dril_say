import drawBot as db
import random
import json
import os
from colorsys import hls_to_rgb

def rgb(r, g, b):
    return (r / 255, g/255, b/255)
def rgba(r, g, b, a):
    return (r / 255, g/255, b/255, a)

with open('semantic_comparison.json') as f:
    data = json.load(f)

def backgroundSquares(canvasWidth,canvasHeight):
    squareSize = 50
    buffer = 0.2
    base_color = hls_to_rgb(random.random(), 0.5, 1)
    for x in range(0, canvasWidth, squareSize):
        for y in range(0, canvasHeight, squareSize):
            db.fill(base_color[0] + (random.random() * buffer), base_color[1] + (random.random() * buffer), base_color[2] + (random.random() * buffer), 0.3)
            db.rect(x, y, squareSize, squareSize)

def backgroundImage(canvasWidth, canvasHeight):
    background_images = os.listdir('background_images/')
    background_image_path = 'background_images/' + background_images[(int)(len(background_images) * random.random())]
    # https://forum.drawbot.com/topic/180/how-do-i-size-an-image-with-the-imageobject-or-without/4
    srcWidth, srcHeight = db.imageSize(background_image_path)
    dstWidth, dstHeight = canvasWidth, canvasHeight
    factorWidth  = dstWidth  / srcWidth
    factorHeight = dstHeight / srcHeight
    with db.savedState():
        db.scale(factorWidth, factorHeight)
        db.image(background_image_path, (0, 0))

def introSlide(canvasWidth, canvasHeight, question):
    db.newPage(canvasWidth, canvasHeight)
    backgroundImage(canvasWidth, canvasHeight)
    db.fill(*rgb(94, 174, 235))
    # db.rect(0, 0, canvasWidth, canvasHeight)
    backgroundSquares(canvasWidth,canvasHeight)
    db.frameDuration(2)

    db.fill(1,1,1)
    margin_bottom = 0.1 * canvasHeight
    margin_sides = 0.1 * canvasHeight

    text_box_margin = margin_sides * 0.5
    text_box_width = canvasWidth - margin_sides * 2 - text_box_margin * 2
    text_box_height = canvasHeight - margin_sides - margin_bottom - text_box_margin * 2
    
    current_font_size = 10
    db.font('ArialNarrow-Bold', current_font_size)

    # this is not efficient. Don't show anyone I made this
    while True:
        db.fontSize(current_font_size)
        current_font_size += 1
        _, current_text_height = db.textSize(question, 'center', width=text_box_width)
        # print(current_text_height)
        # print(text_box_height)
        if(current_font_size > 150):
            break
        elif(current_text_height > text_box_height):
            current_font_size -= 2
            break

    db.fontSize(current_font_size)

    db.fill(*rgb(255, 252, 61))
    db.textBox(
        question,
        (
            margin_sides + text_box_margin, 
            margin_bottom + text_box_margin,
            text_box_width,
            text_box_height
        ),
        'center'
    )

def polarityBackground(polarity):
    if polarity < -0.1:
        return rgb(227, 30, 0)
    elif polarity < 0.25:
        return rgb(222, 149, 2)
    else:
        return rgb(3, 181, 0)

def feelingSlide(canvasWidth, canvasHeight, polarity):
    db.newPage(canvasWidth, canvasHeight)
    
    background_fill = polarityBackground(polarity)
    
    db.fill(*background_fill)
    db.frameDuration(4)
    db.rect(0, 0, canvasWidth, canvasHeight)

    background_images = os.listdir('background_images/')
    background_image_path = 'background_images/' + background_images[(int)(len(background_images) * random.random())]
    # https://forum.drawbot.com/topic/180/how-do-i-size-an-image-with-the-imageobject-or-without/4
    srcWidth, srcHeight = db.imageSize(background_image_path)
    dstWidth, dstHeight = canvasWidth - 50, canvasHeight- 50
    factorWidth  = dstWidth  / srcWidth
    factorHeight = dstHeight / srcHeight
    with db.savedState():
        db.translate(25, 25)
        with db.savedState():
            db.scale(factorWidth, factorHeight)
            db.image(background_image_path, (0, 0))

    dril_feels_text = db.FormattedString()
    dril_feels_text.append("@dril feels", font="Calibri-Bold", fontSize=150, fill=1, align='center', stroke=background_fill, strokeWidth=0.5)
    db.shadow((0,0), 50, background_fill)
    db.text(dril_feels_text, (canvasWidth / 2, canvasHeight - 300))
    
    if polarity < -0.1:
        drils_feeling = "angry"
        db.font("LucidaBlackletter", 250)
    elif polarity < 0.25:
        drils_feeling = "neutral"
        db.font("Helvetica", 180)
    else:
        drils_feeling = "happy"
        db.font("Cortado", 250)

    db.fill(1)
    db.shadow((0,0), 50, background_fill)
    db.text(drils_feeling, (canvasWidth / 2, 250), align='center')

def answerSlide(canvasWidth, canvasHeight, answer, polarity):
    background_fill = polarityBackground(polarity)
    db.newPage(canvasWidth, canvasHeight)
    db.fill(*background_fill)
    db.rect(0, 0, canvasWidth, canvasHeight)
    db.frameDuration(4)
    background_images = os.listdir('background_images/')
    background_image_path = 'background_images/' + background_images[(int)(len(background_images) * random.random())]
    # https://forum.drawbot.com/topic/180/how-do-i-size-an-image-with-the-imageobject-or-without/4
    srcWidth, srcHeight = db.imageSize(background_image_path)
    dstWidth, dstHeight = canvasWidth - 50, canvasHeight- 50
    factorWidth  = dstWidth  / srcWidth
    factorHeight = dstHeight / srcHeight
    with db.savedState():
        db.translate(25, 25)
        with db.savedState():
            db.scale(factorWidth, factorHeight)
            db.image(background_image_path, (0, 0))

    db.fill(*rgba(*background_fill, 0.1))
    box_width =  0.7 * canvasWidth
    box_height = canvasHeight * 0.7    
    x_0 = (canvasWidth - box_width) / 2
    y_0 = (canvasHeight - box_height) / 2 - 100

    text_box_margin = 40
    text_box_width = box_width - text_box_margin * 2
    text_box_height = box_height - text_box_margin * 2
    
    current_font_size = 10
    db.font('Calibri-Bold', current_font_size)

    # this is not efficient. Don't show anyone I made this
    while True:
        db.fontSize(current_font_size)
        current_font_size += 1
        _, current_text_height = db.textSize(answer, 'left', width=text_box_width)
        if(current_font_size > 150):
            break
        elif(current_text_height > text_box_height):
            current_font_size -= 2
            break

    db.fontSize(current_font_size)
    db.stroke(*background_fill)
    db.strokeWidth(0.5)
    db.fill(*rgb(255, 252, 61))
    db.textBox(
        answer,
        (
            x_0, 
            y_0,
            box_width,
            box_height
        ),
        'left'
    )

    # dril says
    d_says = db.FormattedString()    
    d_says.append("@dril says:", font="Calibri-Bold", fontSize=100, fill=rgb(255, 252, 61), stroke=background_fill, strokeWidth=2)
    # db.shadow((0,0), 50, background_fill)
    db.text(d_says, (x_0, y_0 + box_height + 30))

db.newDrawing()

q_num = 0
# for q in data:
for x in range (0,40):
    q = random.choice(data)
    canvasWidth = 800
    canvasHeight = 800

    directory_path = './output/posts/post_' + str(x)
    try:
        os.mkdir(directory_path, 0o777)
    except OSError as e:
        pass
    introSlide(canvasWidth, canvasHeight, q['question'])
    output_path = directory_path + '/slide_0.png'
    db.saveImage(output_path)

    answer_number = 1
    for answer in q['answers']:
        output_path = directory_path + '/slide_' + str(answer_number) + '_0.png'
        feelingSlide(canvasWidth, canvasHeight, answer['polarity'])
        db.saveImage(output_path)

        output_path = directory_path + '/slide_' + str(answer_number) + '_1.png'
        answerSlide(canvasWidth, canvasHeight, answer['answer'], answer['polarity'])
        db.saveImage(output_path)

        answer_number += 1

    q_num += 1

db.endDrawing()
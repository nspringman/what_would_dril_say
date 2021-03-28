import drawBot as db
import random
import json
import os

def rgb(r, g, b):
    return (r / 255, g/255, b/255)
def rgba(r, g, b, a):
    return (r / 255, g/255, b/255, a)

with open('semantic_comparison.json') as f:
    data = json.load(f)

def backgroundSquares(canvasWidth,canvasHeight):
    squareSize = 25
    buffer = 20
    for x in range(0, canvasWidth, squareSize):
        for y in range(0, canvasHeight, squareSize):
            db.fill(*rgba(18 + (random.random() * buffer), 70 + (random.random() * buffer * 1.5), 40 + (random.random() * buffer), 0.6))
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
    db.rect(0, 0, canvasWidth, canvasHeight)
    # backgroundSquares(canvasWidth,canvasHeight)
    db.frameDuration(2)

    db.fill(1,1,1)
    margin_bottom = 0.3 * canvasHeight
    margin_sides = 0.1 * canvasHeight
    db.polygon(
        (margin_sides, margin_bottom), 
        (canvasWidth - margin_sides, margin_bottom),
        (canvasWidth - margin_sides, canvasHeight - margin_sides),
        (margin_sides, canvasHeight - margin_sides)
    )

    text_box_margin = margin_sides * 0.5
    text_box_width = canvasWidth - margin_sides * 2 - text_box_margin * 2
    text_box_height = canvasHeight - margin_sides - margin_bottom - text_box_margin * 2
    
    current_font_size = 10
    db.font('BodoniSvtyTwoOSITCTT-BookIt', current_font_size)

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

    db.fill(0,0,0)
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

def answerSlide(canvasWidth, canvasHeight, answer, polarity):
    db.newPage(canvasWidth, canvasHeight)
    if polarity < -0.25:
        background_fill = (1, 1-abs(polarity / 0.75), 1-abs(polarity / 0.75))
    elif polarity < 0.25:
        background_fill = (1-abs(abs(polarity) / 0.5), 1-abs(abs(polarity) / 0.5), 1)
    else:
        background_fill = (1, 1, 1-abs(polarity / 0.75))
    db.fill(*background_fill)
    db.frameDuration(4)
    db.rect(0, 0, canvasWidth, canvasHeight)

    background_images = os.listdir('background_images/')
    background_image_path = 'background_images/' + background_images[(int)(len(background_images) * random.random())]
    # https://forum.drawbot.com/topic/180/how-do-i-size-an-image-with-the-imageobject-or-without/4
    srcWidth, srcHeight = db.imageSize(background_image_path)
    dstWidth, dstHeight = canvasWidth * 0.5, canvasWidth * 0.5
    factorWidth  = dstWidth  / srcWidth
    factorHeight = dstHeight / srcHeight
    with db.savedState():
        db.translate(canvasWidth * 0.25, canvasWidth * 0.35)
        with db.savedState():
            db.scale(factorWidth, factorHeight)
            db.image(background_image_path, (10, 10))



    db.newPage(canvasWidth, canvasHeight)
    db.fill(*background_fill)
    db.rect(0, 0, canvasWidth, canvasHeight)
    db.frameDuration(4)

    db.fill(1,1,1)
    box_width =  0.7 * canvasWidth
    box_height = canvasHeight * 0.55
    x_0 = 20 + ((canvasWidth - 40 - box_width) * random.random())
    y_0 = 20 + ((canvasHeight * 0.85 - box_height) * random.random()) # canvasHeight * z gives top margin
    db.polygon(
        (x_0, y_0), 
        (x_0 + box_width, y_0),
        (x_0 + box_width, y_0 + box_height),
        (x_0, y_0 + box_height)
    )

    text_box_margin = 40
    text_box_width = box_width - text_box_margin * 2
    text_box_height = box_height - text_box_margin * 2
    
    current_font_size = 10
    db.font('PingFangHK-Ultralight', current_font_size)

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
    db.fill(0,0,0)
    db.textBox(
        answer,
        (
            x_0 + text_box_margin, 
            y_0 + text_box_margin,
            text_box_width,
            text_box_height
        ),
        'left'
    )

    db.font('CooperBlackMS', 80)
    db.fill(*rgb(235, 64, 52))
    d_says = '@dril says:'
    # _,d_says_height = db.textSize(d_says, 'left', width=canvasWidth * 0.5)
    db.text(d_says, (x_0, y_0 + box_height + 30))

db.newDrawing()

q_num = 0
# for q in data:
for x in range (0,1):
    q = random.choice(data)
    canvasWidth = 800
    canvasHeight = 800

    introSlide(canvasWidth, canvasHeight, q['question'])
    
    for answer in q['answers']:
        answerSlide(canvasWidth, canvasHeight, answer['answer'], random.random())

    output_path = 'output/post_' + str(q_num) + '.gif'
    db.saveImage(output_path)
    q_num += 1
    break #for now, only do one post

db.endDrawing()
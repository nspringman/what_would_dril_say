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
    dstWidth, dstHeight = 500, 500
    factorWidth  = dstWidth  / srcWidth
    factorHeight = dstHeight / srcHeight
    with db.savedState():
        db.scale(factorWidth, factorHeight)
        db.image(background_image_path, (0, 0))

def introSlide(canvasWidth, canvasHeight, question):
    db.newPage(canvasWidth, canvasHeight)
    backgroundImage(canvasWidth, canvasHeight)
    backgroundSquares(canvasWidth,canvasHeight)
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
    db.font('Georgia-Italic', current_font_size)

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

def answerSlide(canvasWidth, canvasHeight, answer):
    db.newPage(canvasWidth, canvasHeight)
    # backgroundSquares(canvasWidth,canvasHeight)
    backgroundImage(canvasWidth, canvasHeight)
    db.frameDuration(4)

    answer = "‘" + answer + "’"

    db.fill(1,1,1)
    margin_bottom = 0.4 * canvasHeight
    margin_sides = 0.15 * canvasHeight
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
    db.font('Georgia', current_font_size)

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

db.newDrawing()

q_num = 0
for q in data:
    canvasWidth = 500
    canvasHeight = 500

    introSlide(canvasWidth, canvasHeight, q['question'])
    
    for answer in q['answers']:
        answerSlide(canvasWidth, canvasHeight, answer['answer'])

    output_path = 'output/post_' + str(q_num) + '.gif'
    db.saveImage(output_path)
    q_num += 1
    break #for now, only do one post

db.endDrawing()
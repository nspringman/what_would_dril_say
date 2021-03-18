import drawBot as db
import random

def rgb(r, g, b):
    return (r / 255, g/255, b/255)

data = [
    {
        'question': 'Men of reddit, what is a man secret that you think every man should know?',
        'answers': [
            {
                'answer': 'seems to me i am one of the only people on this earth who knows exactly how high they stack shit.',
                'similarity': 0.735,
                'sentiment': 0.8,
            },
            {
                'answer': 'there are secret offices all over the country full of men in business attire who consume porn for 9 hrs and go home. they dont even jerk off',
                'similarity': 0.681,
                'sentiment': 0.6,
            },
            {
                'answer': 'i rescind my 2009 tweet "bat man fucks joker", as i now understand, through the wisdom of age, that bat man adheres to a noble moral code',
                'similarity': 0.678,
                'sentiment': 0.3,
            },
            {
                'answer': 'big bird was obviously just a man in a suit. but the other ones were too small to contain men. so what the fuck',
                'similarity': 0.674,
                'sentiment': 0.9,
            },
        ]
    },
]

def backgroundSquares(canvasWidth,canvasHeight):
    squareSize = 10
    buffer = 8
    for x in range(0, canvasWidth - squareSize, squareSize):
        for y in range(0, canvasHeight - squareSize, squareSize):
            db.fill(*rgb(18 + (random.random() * buffer), 70 + (random.random() * buffer * 1.5), 40 + (random.random() * buffer)))
            db.rect(x, y, x+squareSize, y+squareSize)

def introSlide(canvasWidth, canvasHeight, question):
    db.newPage(canvasWidth, canvasHeight)
    backgroundSquares(canvasWidth,canvasHeight)
    db.frameDuration(8)

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
    backgroundSquares(canvasWidth,canvasHeight)
    db.frameDuration(8)

    answer = "‘" + answer + "’"

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
            margin_sides + text_box_margin, 
            margin_bottom + text_box_margin,
            text_box_width,
            text_box_height
        ),
        'left'
    )

db.newDrawing()

for q in data:
    canvasWidth = 500
    canvasHeight = 500

    introSlide(canvasWidth, canvasHeight, q['question'])
    
    for answer in q['answers']:
        answerSlide(canvasWidth, canvasHeight, answer['answer'])

    db.saveImage('output/door.gif')

db.endDrawing()
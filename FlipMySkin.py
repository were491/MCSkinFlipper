from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
Tk().withdraw()

from pathlib import Path

try:
    from PIL import Image
except ModuleNotFoundError:
    input("The PIL (Pillow) module is required to use this program. (Enter)")
    quit()

## Function to make replacing skin parts easier.
def replaceParts(left, right, top, bottom, front, back,
                 coordsLeft, coordsRight, coordsTop,
                 coordsBottom, coordsFront, coordsBack):
    global newSkin # huehuehuehuehuehuehue

    '''make all coords of floats integers'''
    coordsLeft = (int(coordsLeft[0]),int(coordsLeft[1]))
    coordsRight = (int(coordsRight[0]),int(coordsRight[1]))
    coordsTop = (int(coordsTop[0]),int(coordsTop[1]))
    coordsBottom = (int(coordsBottom[0]),int(coordsBottom[1]))
    coordsFront = (int(coordsFront[0]),int(coordsFront[1]))
    coordsBack = (int(coordsBack[0]),int(coordsBack[1]))
    
    '''actually flip'''
    # Don't flip the left and right but paste them onto each other
    newSkin.paste(right, coordsLeft)
    newSkin.paste(left, coordsRight)

    # Rotate the top and bottom 180 and replace with themselves.
    top = top.rotate(180)
    bottom = bottom.rotate(180)

    newSkin.paste(top, coordsTop)
    newSkin.paste(bottom, coordsBottom)

    # Don't flip the front and back but replace them with each other
    newSkin.paste(front, coordsBack)
    newSkin.paste(back, coordsFront)
    return

## Function to safely exit the program (close files before quit).
def safeQuit():
    global skin, newSkin
    skin.close()
    newSkin.close()
    quit()

## Open the skin file to be flipped. askopenfilename returns a path.
path = askopenfilename(filetypes=[("Skin files", "*.png")], title='Select the skin to be flipped...')
if path == '':
    input("Canceled skin selection, exiting program... (Enter)")
    quit()

# While it's a bad idea to open both files instead of creating a "blank canvas",
# This allows us to keep the same settings as the old file.
# Also, this allows us to keep any easter eggs in the original skin.png!
skin = Image.open(path)
newSkin = Image.open(path)

## Find and check size of the skin file.
width, height = skin.size
if width != height or width%64 != 0:
    input("Are you sure you selected the correct skin file?\nMake sure your file is square and its dimensions are multiples of 64. (Enter)")
    safeQuit()

## Ask for skin type (Alex/Steve).
skinType = ''
while skinType not in ('alex','steve'):
    skinType = input("Skin Type (Alex/Steve/Help)? ").lower()
    if skinType == 'help':
        print("Steve skins have square arms, while Alex skins have thinner, rectangular arms.")
        print("You should also be able to find the skin type either through the minecraft.net or minecraft launcher skin settings.")

## Crop each part of the picture to get the necessary parts
    # Head...
headRight = skin.crop((0, height/8, width/8, height/4))
# ^ On a normal skin (64x64) this is from (0,8) to (8,16)
headLeft = skin.crop((width/4, height/8, (3*width)/8, height/4))
# ^ On a normal (64x64) skin this is from (16,8) to (24,16)
headTop = skin.crop((width/8, 0, width/4, width/8))
# ^ On a normal (64x64) skin this is from (8,0) to (16,8)
headBottom = skin.crop((width/4, 0, (3*width)/8, width/8))
# ^ On a normal (64x64) skin this is from (16,0) to (24,8)
headFront = skin.crop((width/8, height/8, width/4, height/4))
# ^ On a normal (64x64) skin this is from (8,8) to (16,16)
headBack = skin.crop(((3*width)/8, height/8, width/2, height/4))
# ^ On a normal (64x64) skin this is from (24,8) to (32,16)

replaceParts(headLeft, headRight, headTop, headBottom, headFront, headBack,
             (width/4, height/8), (0, height/8), (width/8, 0), (width/4, 0),
             (width/8, height/8), ((3*width)/8, height/8))

    # Body...
bodyTop = skin.crop(((5*width)/16, height/4, (7*width)/16, (5*width)/16))
# ^ On a normal (64x64) skin this is from (20,16) to (28,20)
bodyBottom = skin.crop(((7*width)/16, height/4, (9*width)/16, (5*width)/16))
# ^ On a normal (64x64) skin this is from (28,16) to (36,20)
bodyFront = skin.crop(((5*width)/16, (5*height)/16, (7*width)/16, height/2))
# ^ On a normal (64x64) skin this is from (20,20) to (28,32)
bodyBack = skin.crop((width/2, (5*height)/16, (5*width)/8, height/2))
# ^ On a normal (64x64) skin this is from (32,20) to (40,32)
bodyLeft = skin.crop(((7*width)/16, (5*height)/16, width/2, height/2))
# ^ On a normal (64x64) skin this is from (28,20) to (32,32)
bodyRight = skin.crop((width/4, (5*height)/16, (5*width)/16, height/2))
# ^ On a normal (64x64) skin this is from (16,20) to (20,32)

replaceParts(bodyLeft, bodyRight, bodyTop, bodyBottom, bodyFront, bodyBack,
             ((7*width)/16, (5*height)/16), (width/4, (5*height)/16),
             ((5*width)/16, height/4), ((7*width)/16, height/4),
             ((5*width)/16, (5*height)/16), (width/2, (5*height)/16))

## The arms and sleeves will require some special logic since the size varies between Alex and Steve skins.
if skinType == 'alex':
    # NOTE: Swap the arms and sleeves locationally to ensure they are on the right sides.
    # This means the left arm is saved as the right arm etc.
        # Left Arm...
    leftArmLeft = skin.crop(((39*width)/64, (13*height)/16, (43*width)/64, height))
    # ^ Alex: On a normal (64x64) skin this is from (39,52) to (43,64)
    leftArmRight = skin.crop((width/2, (13*height)/16, (9*width)/16, height))
    # ^ Alex: On a normal (64x64) skin this is from (32,52) to (36,64)
    leftArmTop = skin.crop(((9*width)/16, (3*height)/4, (39*width)/64, (13*height)/16))
    # ^ Alex: On a normal (64x64) skin this is from (36,48) to (39,52)
    leftArmBottom = skin.crop(((39*width)/64, (3*height)/4, (21*width)/32, (13*height)/16))
    # ^ Alex: On a normal (64x64) skin this is from (39,48) to (42,52)
    leftArmFront = skin.crop(((9*width)/16, (13*height)/16, (39*width)/64, height))
    # ^ Alex: On a normal (64x64) skin this is from (36,52) to (39,64)
    leftArmBack = skin.crop(((43*width)/64, (13*height)/16, (23*width)/32, height))
    # ^ Alex: On a normal (64x64) skin this is from (43,52) to (46,64)

    replaceParts(leftArmLeft, leftArmRight, leftArmTop, leftArmBottom,
                 leftArmFront, leftArmBack,
                 ((47*width)/64, (5*height)/16), ((5*width)/8, (5*height)/16),
                 ((11*width)/16, height/4), ((47*width)/64, height/4),
                 ((11*width)/16, (5*height)/16), ((51*width)/64, (5*height)/16))

        # Right Arm...
    rightArmLeft = skin.crop(((47*width)/64, (5*height)/16, (51*width)/64, height/2))
    # ^ Alex: On a normal (64x64) skin this is from (47,20) to (51,32)
    rightArmRight = skin.crop(((5*width)/8, (5*height)/16, (11*width)/16, height/2))
    # ^ Alex: On a normal (64x64) skin this is from (40,20) to (44,32)
    rightArmTop = skin.crop(((11*width)/16, height/4, (47*width)/64, (5*height)/16))
    # ^ Alex: On a normal (64x64) skin this is from (44,16) to (47,20)
    rightArmBottom = skin.crop(((47*width)/64, height/4, (25*width)/32, (5*height)/16))
    # ^ Alex: On a normal (64x64) skin this is from (47,16) to (50,20)
    rightArmFront = skin.crop(((11*width)/16, (5*height)/16, (47*width)/64, height/2))
    # ^ Alex: On a normal (64x64) skin this is from (44,20) to (47,32)
    rightArmBack = skin.crop(((51*width)/64, (5*height)/16, (27*width)/32, height/2))
    # ^ Alex: On a normal (64x64) skin this is from (51,20) to (54,32)

    replaceParts(rightArmLeft, rightArmRight, rightArmTop, rightArmBottom,
                 rightArmFront, rightArmBack,
                 ((39*width)/64, (13*height)/16), (width/2, (13*height)/16),
                 ((9*width)/16, (3*height)/4), ((39*width)/64, (3*height)/4),
                 ((9*width)/16, (13*height)/16), ((43*width)/64, (13*height)/16))
    
        # Left Sleeve...
    leftSleeveLeft = skin.crop(((55*width)/64, (13*height)/16, (59*width)/64, height))
    # ^ On a normal (64x64) skin this is from (55,52) to (59,64)
    leftSleeveRight = skin.crop(((3*width)/4, (13*height)/16, (13*width)/16, height))
    # ^ On a normal (64x64) skin this is from (48,52) to (52,64)
    leftSleeveTop = skin.crop(((13*width)/16, (3*height)/4, (55*width)/64, (13*height)/16))
    # ^ On a normal (64x64) skin this is from (52,48) to (55,52)
    leftSleeveBottom= skin.crop(((55*width)/64, (3*height)/4, (29*width)/32, (13*height)/16))
    # ^ On a normal (64x64) skin this is from (55,48) to (58,52)
    leftSleeveFront = skin.crop(((13*width)/16, (13*height)/16, (55*width)/64, height))
    # ^ On a normal (64x64) skin this is from (52,52) to (55,64)
    leftSleeveBack = skin.crop(((59*width)/64, (13*height)/16, (31*width)/32, height))
    # ^ On a normal (64x64) skin this is from (59,52) to (62,64)
    
    replaceParts(leftSleeveLeft, leftSleeveRight, leftSleeveTop, leftSleeveBottom,
                 leftSleeveFront, leftSleeveBack,
                 ((47*width)/64, (9*height)/16), ((5*width)/8, (9*height)/16),
                 ((11*width)/16, height/2), ((47*width)/64, height/2),
                 ((11*width)/16, (9*height)/16), ((51*width)/64, (9*height)/16))
    
        # Right Sleeve...
    rightSleeveLeft = skin.crop(((47*width)/64, (9*height)/16, (51*width)/64, (3*height)/4))
    # ^ On a normal (64x64) skin this is from (47,36) to (51,48)
    rightSleeveRight = skin.crop(((5*width)/8, (9*height)/16, (11*width)/16, (3*height)/4))
    # ^ On a normal (64x64) skin this is from (40,36) to (44,48)
    rightSleeveTop = skin.crop(((11*width)/16, height/2, (47*width)/64, (9*height)/16))
    # ^ On a normal (64x64) skin this is from (44,32) to (47,36)
    rightSleeveBottom = skin.crop(((47*width)/64, height/2, (25*width)/32, (9*height)/16))
    # ^ On a normal (64x64) skin this is from (47,32) to (50,36)
    rightSleeveFront = skin.crop(((11*width)/16, (9*height)/16, (47*width)/64, (3*height)/4))
    # ^ On a normal (64x64) skin this is from (44,36) to (47,48)
    rightSleeveBack = skin.crop(((51*width)/64, (9*height)/16, (27*width)/32, (3*height)/4))
    # ^ On a normal (64x64) skin this is from (51,36) to (54,48)

    replaceParts(rightSleeveLeft, rightSleeveRight, rightSleeveTop, rightSleeveBottom,
                 rightSleeveFront, rightSleeveBack,
                 ((55*width)/64, (13*height)/16), ((3*width)/4, (13*height)/16), 
                 ((13*width)/16, (3*height)/4), ((55*width)/64, (3*height)/4),
                 ((13*width)/16, (13*height)/16), ((59*width)/64, (13*height)/16))

else: # Basically the same as elif skinType == 'steve':
    # NOTE: Swap the arms to ensure they are on the right sides.
        # Left Arm...
    leftArmLeft = skin.crop(((5*width)/8, (13*height)/16, (11*width)/16, height))
    # ^ Steve: On a normal (64x64) skin this is from (40,52) to (44,64)
    leftArmRight = skin.crop((width/2, (13*height)/16, (9*width)/16, height))
    # ^ Steve: On a normal (64x64) skin this is from (32,52) to (36,64)
    leftArmTop = skin.crop(((9*width)/16, (3*height)/4, (5*width)/8, (13*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (36,48) to (40,52)
    leftArmBottom = skin.crop(((5*width)/8, (3*height)/4, (11*width)/16, (13*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (40,48) to (44,52)
    leftArmFront = skin.crop(((9*width)/16, (13*height)/16, (5*width)/8, height))
    # ^ Steve: On a normal (64x64) skin this is from (36,52) to (40,64)
    leftArmBack = skin.crop(((11*width)/16, (13*height)/16, (3*width)/4, height))
    # ^ Steve: On a normal (64x64) skin this is from (44,52) to (48,64)

    replaceParts(leftArmLeft, leftArmRight, leftArmTop, leftArmBottom,
                 leftArmFront, leftArmBack,
                 ((3*width)/4, (5*height)/16), ((5*width)/8, (5*height)/16),
                 ((11*width)/16, height/4), ((3*width)/4, height/4),
                 ((11*width)/16, (5*height)/16), ((13*width)/16, (5*height)/16))

        # Right Arm...
    rightArmLeft = skin.crop(((3*width)/4, (5*height)/16, (13*width)/16, height/2))
    # ^ Steve: On a normal (64x64) skin this is from (48,20) to (52,32)
    rightArmRight = skin.crop(((5*width)/8, (5*height)/16, (11*width)/16, height/2))
    # ^ Steve: On a normal (64x64) skin this is from (40,20) to (44,32)
    rightArmTop = skin.crop(((11*width)/16, height/4, (3*width)/4, (5*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (44,16) to (48,20)
    rightArmBottom = skin.crop(((3*width)/4, height/4, (13*width)/16, (5*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (48,16) to (52,20)
    rightArmFront = skin.crop(((11*width)/16, (5*height)/16, (3*width)/4, height/2))
    # ^ Steve: On a normal (64x64) skin this is from (44,20) to (48,32)
    rightArmBack = skin.crop(((13*width)/16, (5*height)/16, (7*width)/8, height/2))
    # ^ Steve: On a normal (64x64) skin this is from (52,20) to (56,32)

    replaceParts(rightArmLeft, rightArmRight, rightArmTop, rightArmBottom,
                 rightArmFront, rightArmBack,
                 ((5*width)/8, (13*height)/16), (width/2, (13*height)/16),
                 ((9*width)/16, (3*height)/4), ((5*width)/8, (3*height)/4),
                 ((9*width)/16, (13*height)/16), ((11*width)/16, (13*height)/16))

            # Left Sleeve...
    leftSleeveLeft = skin.crop(((7*width)/8, (13*height)/16, (15*width)/16, height))
    # ^ Steve: On a normal (64x64) skin this is from (56,52) to (60,64)
    leftSleeveRight = skin.crop(((3*width)/4, (13*height)/16, (13*width)/16, height))
    # ^ Steve: On a normal (64x64) skin this is from (48,52) to (52,64)
    leftSleeveTop = skin.crop(((13*width)/16, (3*height)/4, (7*width)/8, (13*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (52,48) to (56,52)
    leftSleeveBottom = skin.crop(((7*width)/8, (3*height)/4, (15*width)/16, (13*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (56,48) to (60,52)
    leftSleeveFront = skin.crop(((13*width)/16, (13*height)/16, (7*width)/8, height))
    # ^ Steve: On a normal (64x64) skin this is from (52,52) to (56,64)
    leftSleeveBack = skin.crop(((15*width)/16, (13*height)/16, width, height))
    # ^ Steve: On a normal (64x64) skin this is from (60,52) to (64,64)

    replaceParts(leftSleeveLeft, leftSleeveRight, leftSleeveTop, leftSleeveBottom,
                 leftSleeveFront, leftSleeveBack,
                 ((3*width)/4, (9*height)/16), ((5*width)/8, (9*height)/16),
                 ((11*width)/16, height/2), ((3*width)/4, height/2),
                 ((11*width)/16, (9*height)/16), ((13*width)/16, (9*height)/16))
    
        # Right Sleeve...
    rightSleeveLeft = skin.crop(((3*width)/4, (9*height)/16, (13*width)/16, (3*height)/4))
    # ^ Steve: On a normal (64x64) skin this is from (48,36) to (52,48)
    rightSleeveRight = skin.crop(((5*width)/8, (9*height)/16, (11*width)/16, (3*height)/4))
    # ^ Steve: On a normal (64x64) skin this is from (40,36) to (44,48)
    rightSleeveTop = skin.crop(((11*width)/16, height/2, (3*width)/4, (9*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (44,32) to (48,36)
    rightSleeveBottom = skin.crop(((3*width)/4, height/2, (13*width)/16, (9*height)/16))
    # ^ Steve: On a normal (64x64) skin this is from (48,32) to (52,36)
    rightSleeveFront = skin.crop(((11*width)/16, (9*height)/16, (3*width)/4, (3*height)/4))
    # ^ Steve: On a normal (64x64) skin this is from (44,36) to (48,48)
    rightSleeveBack = skin.crop(((13*width)/16, (9*height)/16, (7*width)/8, (3*height)/4))
    # ^ Steve: On a normal (64x64) skin this is from (52,36) to (56,48)

    replaceParts(rightSleeveLeft, rightSleeveRight, rightSleeveTop, rightSleeveBottom,
                 rightSleeveFront, rightSleeveBack,
                 ((7*width)/8, (13*height)/16), ((3*width)/4, (13*height)/16),
                 ((13*width)/16, (3*height)/4), ((7*width)/8, (3*height)/4),
                 ((13*width)/16, (13*height)/16), ((15*width)/16, (13*height)/16))

# NOTE: Swap the legs and pant sleeves to ensure they are on the right sides.
# Similarly with arms and shirt sleeves, the left pant sleeve ends up on the right etc.
    # Left Leg...
leftLegLeft = skin.crop(((3*width)/8, (13*height)/16, (7*width)/16, height))
# ^ On a normal (64x64) skin this is from (24,52) to (28,64)
leftLegRight = skin.crop((width/4, (13*height)/16, (5*width)/16, height))
# ^ On a normal (64x64) skin this is from (16,52) to (20,64)
leftLegTop = skin.crop(((5*width)/16, (3*height)/4, (3*width)/8, (13*height)/16))
# ^ On a normal (64x64) skin this is from (20,48) to (24,52)
leftLegBottom = skin.crop(((3*width)/8, (3*height)/4, (7*width)/16, (13*height)/16))
# ^ On a normal (64x64) skin this is from (24,48) to (28,52)
leftLegFront = skin.crop(((5*width)/16, (13*height)/16, (3*width)/8, height))
# ^ On a normal (64x64) skin this is from (20,52) to (24,64)
leftLegBack = skin.crop(((7*width)/16, (13*height)/16, width/2, height))
# ^ On a normal (64x64) skin this is from (28,52) to (32,64)

replaceParts(leftLegLeft, leftLegRight, leftLegTop, leftLegBottom,
             leftLegFront, leftLegBack,
             (width/8, (5*height)/16), (0, (5*height)/16),
             (width/16, height/4), (width/8, height/4),
             (width/16, (5*height)/16), ((3*width)/16, (5*height)/16))

    # Right Leg...
rightLegLeft = skin.crop((width/8, (5*height)/16, (3*width)/16, height/2))
# ^ On a normal (64x64) skin this is from (8,20) to (12,32)
rightLegRight = skin.crop((0, (5*height)/16, width/16, height/2))
# ^ On a normal (64x64) skin this is from (0,20) to (4,32)
rightLegTop = skin.crop((width/16, height/4, width/8, (5*height)/16))
# ^ On a normal (64x64) skin this is from (4,16) to (8,20)
rightLegBottom = skin.crop((width/8, height/4, (3*width)/16, (5*height)/16))
# ^ On a normal (64x64) skin this is from (8,16) to (12,20)
rightLegFront = skin.crop((width/16, (5*height)/16, width/8, height/2))
# ^ On a normal (64x64) skin this is from (4,20) to (8,32)
rightLegBack = skin.crop(((3*width)/16, (5*height)/16, width/4, height/2))
# ^ On a normal (64x64) skin this is from (12,20) to (16,32)

replaceParts(rightLegLeft, rightLegRight, rightLegTop, rightLegBottom,
             rightLegFront, rightLegBack,
             ((3*width)/8, (13*height)/16), (width/4, (13*height)/16),
             ((5*width)/16, (3*height)/4), ((3*width)/8, (3*height)/4),
             ((5*width)/16, (13*height)/16), ((7*width)/16, (13*height)/16))

    # Left pant sleeve...
leftLegSleeveLeft = skin.crop((width/8, (13*height)/16, (3*width)/16, height))
# ^ On a normal (64x64) skin this is from (8,52) to (12,64)
leftLegSleeveRight = skin.crop((0, (13*height)/16, width/16, height))
# ^ On a normal (64x64) skin this is from (0,52) to (4,64)
leftLegSleeveTop = skin.crop((width/16, (3*height)/4, width/8, (13*height)/16))
# ^ On a normal (64x64) skin this is from (4,48) to (8,52)
leftLegSleeveBottom = skin.crop((width/8, (3*height)/4, (3*width)/16, (13*height)/16))
# ^ On a normal (64x64) skin this is from (8,48) to (12,52)
leftLegSleeveFront = skin.crop((width/16, (13*height)/16, width/8, height))
# ^ On a normal (64x64) skin this is from (4,52) to (8,64)
leftLegSleeveBack = skin.crop(((3*width)/16, (13*height)/16, width/4, height))
# ^ On a normal (64x64) skin this is from (12,52) to (16,64)

replaceParts(leftLegSleeveLeft, leftLegSleeveRight, leftLegSleeveTop, leftLegSleeveBottom,
             leftLegSleeveFront, leftLegSleeveBack,
             (width/8, (9*height)/16), (0, (9*height)/16),
             (width/16, height/2), (width/8, height/2),
             (width/16, (9*height)/16), ((3*width)/16, (9*height)/16))

    # Right pant sleeve...
rightLegSleeveLeft = skin.crop((width/8, (9*height)/16, (3*width)/16, (3*height)/4))
# ^ On a normal (64x64) skin this is from (8,36) to (12,48)
rightLegSleeveRight = skin.crop((0, (9*height)/16, width/16, (3*height)/4))
# ^ On a normal (64x64) skin this is from (0,36) to (4,48)
rightLegSleeveTop = skin.crop((width/16, height/2, width/8, (9*height)/16))
# ^ On a normal (64x64) skin this is from (4,32) to (8,36)
rightLegSleeveBottom = skin.crop((width/8, height/2, (3*width)/16, (9*height)/16))
# ^ On a normal (64x64) skin this is from (8,32) to (12,36)
rightLegSleeveFront = skin.crop((width/16, (9*height)/16, width/8, (3*height)/4))
# ^ On a normal (64x64) skin this is from (4,36) to (8,48)
rightLegSleeveBack = skin.crop(((3*width)/16, (9*height)/16, width/4, (3*height)/4))
# ^ On a normal (64x64) skin this is from (12,36) to (16,48)

replaceParts(rightLegSleeveLeft, rightLegSleeveRight, rightLegSleeveTop, rightLegSleeveBottom,
             rightLegSleeveFront, rightLegSleeveBack,
             (width/8, (13*height)/16), (0, (13*height)/16),
             (width/16, (3*height)/4), (width/8, (3*height)/4),
             (width/16, (13*height)/16), ((3*width)/16, (13*height)/16))

    # Hat...
hatLeft = skin.crop(((3*width)/4, height/8, (7*width)/8, height/4))
# ^ On a normal (64x64) skin this is from (48,8) to (56,16)
hatRight = skin.crop((width/2, height/8, (5*width)/8, height/4))
# ^ On a normal (64x64) skin this is from (32,8) to (40,16)
hatTop = skin.crop(((5*width)/8, 0, (3*width)/4, height/8))
# ^ On a normal (64x64) skin this is from (40,0) to (48,8)
hatBottom = skin.crop(((3*width)/4, 0, (7*width)/8, height/8))
# ^ On a normal (64x64) skin this is from (48,0) to (56,8)
hatFront = skin.crop(((5*width)/8, height/8, (3*width)/4, height/4))
# ^ On a normal (64x64) skin this is from (40,8) to (48,16)
hatBack = skin.crop(((7*width)/8, height/8, width, height/4))
# ^ On a normal (64x64) skin this is from (56,8) to (64,16)

replaceParts(hatLeft, hatRight, hatTop, hatBottom, hatFront, hatBack,
             ((3*width)/4, height/8), (width/2, height/8),
             ((5*width)/8, 0), ((3*width)/4, 0),
             ((5*width)/8, height/8), ((7*width)/8, height/8))

    # Shirt...
shirtLeft = skin.crop(((7*width)/16, (9*height)/16, width/2, (3*height)/4))
# ^ On a normal (64x64) skin this is from (28,36) to (32, 48)
shirtRight = skin.crop((width/4, (9*height)/16, (5*width)/16, (3*height)/4))
# ^ On a normal (64x64) skin this is from (16,36) to (20,48)
shirtTop = skin.crop(((5*width)/16, height/2, (7*width)/16, (9*height)/16))
# ^ On a normal (64x64) skin this is from (20,32) to (28,36)
shirtBottom = skin.crop(((7*width)/16, height/2, (9*width)/16, (9*height)/16))
# ^ On a normal (64x64) skin this is from (28,32) to (36,36)
shirtFront = skin.crop(((5*width)/16, (9*height)/16, (7*width)/16, (3*height)/4))
# ^ On a normal (64x64) skin this is from (20,36) to (28,48)
shirtBack = skin.crop((width/2, (9*height)/16, (5*width)/8, (3*height)/4))
# ^ On a normal (64x64) skin this is from (32,36) to (40,48)

replaceParts(shirtLeft, shirtRight, shirtTop, shirtBottom, shirtFront, shirtBack,
             ((7*width)/16, (9*height)/16), (width/4, (9*height)/16),
             ((5*width)/16, height/2), ((7*width)/16, height/2),
             ((5*width)/16, (9*height)/16), (width/2, (9*height)/16))



# Save the image
savePath = asksaveasfilename(filetypes=[("Skin files", "*.png")], initialfile="flipped.png", defaultextension=".png", title='Save as...')
while savePath == '' and input("Are you sure you want to exit the program without saving changes? (Yes/No) ").lower() != 'yes':
    savePath = asksaveasfilename(filetypes=[("Skin files", "*.png")], initialfile="flipped.png", defaultextension=".png", title='Save as...')

if savePath == '':
    input("Canceled skin saving, exiting progam without saving... (Enter)")
    safeQuit()

newSkin.save(savePath)

#input("Skin flipped! (Enter to exit program)")
safeQuit()

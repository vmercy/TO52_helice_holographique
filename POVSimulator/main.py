import subprocess
from PIL import Image
from PIL import ImageDraw
from math import pi, sin,cos
from subprocess import STDOUT, Popen, PIPE
from time import sleep

def drillHole(draw, centerPosition, diameter):
    """Adds a transparent hole in draw

    Args:
        draw (Draw): The PIL Draw to modify
        centerPosition (tuple): Pixel coordinates (x,y) of the hole center
        diameter (int): Hole diameter in pixels
    """
    upperLeftCornerCoordinates = (
        centerPosition[0]-diameter/2, centerPosition[1]-diameter/2)
    bottomRightCornerCoordinates = (
        upperLeftCornerCoordinates[0]+diameter, upperLeftCornerCoordinates[1]+diameter)
    draw.ellipse([upperLeftCornerCoordinates,
                  bottomRightCornerCoordinates], fill=(0, 0, 0, 0))

def drillHoles(draw, positions, diameter):
    """Drills several transparent holes in draw

    Args:
        draw (Draw): The PIL Draw to modify
        positions (array): Array of tuples containing pixel coordinates (x,y) of holes centers
        diameter (int): Holes diameter in pixels
    """
    for holeCenter in positions:
        drillHole(draw, holeCenter, diameter)

def computeHolesCenterPositions(maskDiameter, nbHoles, angle):
  """Computes center positions of the holes to drill in mask

  Args:
      maskDiameter (int): The diameter of the mask in pixels
      nbHoles (int): The expected number of holes
      angle (float): The angle of the diameter line where holes must be alligned

  Returns:
      array: Array of (x,y) tuples containing holes center positions
  """
  spaceBetweenHoles = maskDiameter / nbHoles
  radialCoordinates = [] #contains radial coordinate of holes starting from the center of mask
  if(nbHoles%2): # number of holes is odd, so we place the first hole to be concentric with the main disk
    radialOrigin = 0
    nbHoles-=1
  else:
    radialOrigin = spaceBetweenHoles/2
    nbHoles-=2
  radialCoordinates.append(radialOrigin)
  for i in range(0,nbHoles//2):
    radialCoordinates.append(radialOrigin+(i+1)*spaceBetweenHoles)
  holesPositions = []
  for radial in radialCoordinates:
    holesPositions.append((maskDiameter/2+radial*sin(angle), maskDiameter/2+radial*cos(angle)))
    holesPositions.append((maskDiameter/2-radial*sin(angle), maskDiameter/2-radial*cos(angle)))
  return holesPositions

# Configuration variables
maskDiameter = 5000
holesDiameter = 20
nbHoles = 144
maskFileName = 'mask.png'
zoom = 90 #background image zoom in %

# try to make the mask spin above image
# if it doesn't work, pick colors on image on mask holes positions and build new image with them
mask = Image.new('RGBA', (maskDiameter, )*2, (255, 0, 0, 0))
support = Image.new('RGBA', (maskDiameter,)*2, (255,0,0,0))
draw = ImageDraw.Draw(mask)

draw.rectangle([(0, 0), (maskDiameter, maskDiameter)], 'black')

for i in range (0,180,5):
  angle_rad = pi/180.0 * i
  holes = computeHolesCenterPositions(maskDiameter, nbHoles, angle_rad)
  drillHoles(draw, holes, holesDiameter)

mask.save(maskFileName)
#Popen(['xdg-open', 'mask.png'], stdout=PIPE)

imageFileName = 'logo_utbm.png'
outputFileName = 'result.png'
backgroundImage = Image.open(imageFileName)
backgroundImage = backgroundImage.convert('RGBA')
backgroundImageNewSize = maskDiameter*zoom//100
backgroundImage = backgroundImage.resize((backgroundImageNewSize,)*2)
support.paste(backgroundImage, ((maskDiameter-backgroundImageNewSize)//2,)*2)
support.paste(mask, (0,0), mask)
support.save(outputFileName)
from PIL import Image
from PIL import ImageDraw
from math import pi, sin,cos

def drillHole(draw, centerPosition, diameter):
    """Adds a transparent hole in draw

    Args:
        draw (Draw): The PIL Draw to modify
        centerPosition (tuple): Pixel coordinates (x,y) of the hole center
        diameter (int): Hole diameter in px
    """
    upperLeftCornerCoordinates = (
        centerPosition[0]-diameter/2, centerPosition[1]-diameter/2)
    bottomRightCornerCoordinates = (
        upperLeftCornerCoordinates[0]+diameter, upperLeftCornerCoordinates[1]+diameter)
    draw.ellipse([upperLeftCornerCoordinates,
                  bottomRightCornerCoordinates], fill=(0, 0, 0, 0))

def drillLineOfHoles(draw, positions, diameter):
    """Drills multiple transparent aligned holes in draw

    Args:
        draw (Draw): The PIL Draw to modify
        positions (array): Array of tuples containing pixel coordinates (x,y) of holes centers
        diameter (int): Holes diameter in px
    """
    for holeCenter in positions:
        drillHole(draw, holeCenter, diameter)

def computeHolesLineCenterPositions(maskDiameter, nbHoles, angle):
  """Computes center positions of the holes to drill in mask

  Args:
      maskDiameter (int): The diameter of the mask in px
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

def drillHoles(draw, maskDiameter, nbHoles, holesDiameter, angleStep, angleMin = 0, angleMax = 180):
  """Drills all holes on mask

  Args:
      draw (Draw): The PIL Draw to modify
      maskDiameter (int): The diameter of the mask in px
      nbHoles (int): The expected number of holes in each diameter line
      diameter (int): Hole diameter in px
      angleStep (int): The angle between two consecutive lines of holes
      angleMin (int, optional): The angle of the first line of holes. Defaults to 0.
      angleMax (int, optional): The angle of the last line of holes. Defaults to 180.
  """
  for i in range (angleMin,angleMax,angleStep):
    angle_rad = pi/180.0 * i
    holes = computeHolesLineCenterPositions(maskDiameter, nbHoles, angle_rad)
    drillLineOfHoles(draw, holes, holesDiameter)

# Configuration variables
maskDiameter = 5000
holesDiameter = 20
nbHoles = 144
imageFileName = 'logo_utbm.png'
outputFileName = 'result.png'
zoom = 90 #background image zoom in %

if __name__ == "__main__":
  mask = Image.new('RGBA', (maskDiameter, )*2, (255, 0, 0, 0)) # The mask is a black-filled image with transparent holes
  support = Image.new('RGBA', (maskDiameter,)*2, (255,0,0,0)) # The support image is the main image which 
  backgroundImage = Image.open(imageFileName) #

  draw = ImageDraw.Draw(mask)
  draw.rectangle([(0, 0), (maskDiameter, maskDiameter)], 'black') #

  drillHoles(draw, maskDiameter, nbHoles, holesDiameter, 5)
  #maskFileName = 'mask.png'
  #mask.save(maskFileName)
  backgroundImage = backgroundImage.convert('RGBA')
  backgroundImageNewSize = maskDiameter*zoom//100
  backgroundImage = backgroundImage.resize((backgroundImageNewSize,)*2)
  support.paste(backgroundImage, ((maskDiameter-backgroundImageNewSize)//2,)*2)
  support.paste(mask, (0,0), mask)
  support.save(outputFileName)
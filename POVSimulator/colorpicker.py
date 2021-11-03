from PIL import Image
from PIL import ImageDraw
from math import ceil, pi, sin,cos

def renderPickedPointsPreview(filename, pickedColorPoints, ellipsesDiameter):
  """Renders an image containing ellipses at picked points positions with the picked color

  Args:
      filename (string): The rendered image output filename
      pickedColorPoints (array): The list of picked point colors
      ellipsesDiameter ([type]): The diameter of each ellipse representing a picked color point
  """
  maxSizingColorPoint = max(pickedColorPoints, key=(lambda x:max(x[0:1])))
  size = max(maxSizingColorPoint[0:1])
  size+=ellipsesDiameter
  size = ceil(size)
  outputImg = Image.new('RGB', (size, )*2, (0, 0, 0))
  draw = ImageDraw.Draw(outputImg)
  draw.rectangle([(0, 0), (size, )*2], 'black')
  for pickedColorPoint in pickedColorPoints:
    upperLeftCornerCoordinates = (
        pickedColorPoint[0]-ellipsesDiameter/2, pickedColorPoint[1]-ellipsesDiameter/2)
    bottomRightCornerCoordinates = (
        upperLeftCornerCoordinates[0]+ellipsesDiameter, upperLeftCornerCoordinates[1]+ellipsesDiameter)
    draw.ellipse([upperLeftCornerCoordinates,
                  bottomRightCornerCoordinates], fill=pickedColorPoint[2])
  outputImg.save(filename)

def pickColors(pickingPoints, subjectImage):
  """Pick pixel colors on image

  Args:
      pickingPoints (array): Array of tuples containing picking points coordinates
      subjectImage (PIL.Image): The image where colors must be picked

  Returns:
      Array: List of picked colors in the form (x,y,(r,g,b))
  """
  pickedColorPoints = []
  for pickingPoint in pickingPoints:
    pixel = subjectImage.getpixel(pickingPoint)
    pickedColorPoints.append((pickingPoint[0], pickingPoint[1],pixel))
  return pickedColorPoints

def computePickingPointsPositionsOnDiametralLine(pickingAreaDiameter, nbPoints, angle):
  """Computes the coordinates of aligned points where color must be picked on image

  Args:
      pickingAreaDiameter (int): The diameter of the area where points must be picked
      nbPoints (int): The expected number of points
      angle (float): The angle of the diameter line where holes must be alligned

  Returns:
      array: Array of (x,y) tuples containing holes center positions
  """
  spaceBetweenPoints = pickingAreaDiameter / nbPoints
  radialCoordinates = [] #contains radial coordinate of holes starting from the center of mask
  if(nbPoints%2): # number of holes is odd, so we place the first hole to be concentric with the main disk
    radialOrigin = 0
    nbPoints-=1
  else:
    radialOrigin = spaceBetweenPoints/2
    nbPoints-=2
  radialCoordinates.append(radialOrigin)
  for i in range(0,nbPoints//2):
    radialCoordinates.append(radialOrigin+(i+1)*spaceBetweenPoints)
  pointsPositions = []
  for radial in radialCoordinates:
    pointsPositions.append((pickingAreaDiameter/2+radial*sin(angle), pickingAreaDiameter/2+radial*cos(angle)))
    pointsPositions.append((pickingAreaDiameter/2-radial*sin(angle), pickingAreaDiameter/2-radial*cos(angle)))
  return pointsPositions

def getPickingPoints(pickingAreaDiameter, nbPointsPerLine, angleStep, angleMin = 0, angleMax = 180):
  """Builds 

  Args:
      pickingAreaDiameter (int): The diameter of the area where points must be picked
      nbHoles (int): The expected number of holes in each diametral line
      angleStep (int): The angle between two consecutive diametral lines
      angleMin (int, optional): The angle of the first line of holes. Defaults to 0.
      angleMax (int, optional): The angle of the last line of holes. Defaults to 180.

  Returns:
      array: Array of picking points
  """
  points = []
  for i in range (angleMin,angleMax,angleStep):
    angle_rad = pi/180.0 * i
    #TODO: ajouter les coordonnées polaires en passant i à la fonction computePickingPointsPositionsOnLine
    points += computePickingPointsPositionsOnDiametralLine(pickingAreaDiameter, nbPointsPerLine, angle_rad)
  return points

# Configuration variables
nbEllipsesPerDiametralLine = 50
imageFileName = 'logo_utbm_detoure.png'
outputFileName = 'result_picking.png'
angleStep = 5
zoomFactor = 100 #zoom factor in percent

if __name__ == "__main__":
  sourceImg = Image.open(imageFileName)
  sourceImg.convert('RGBA')
  print(sourceImg.mode)
  imgMaxSize = max(sourceImg.size)
  baseImgSize = imgMaxSize*100//zoomFactor
  centeredImage = Image.new('RGB', (baseImgSize,)*2,'black')
  
  #TODO: center image and dezoom
  centeredImage.paste(sourceImg,((baseImgSize-sourceImg.size[0])//2,(baseImgSize-sourceImg.size[1])//2), mask=sourceImg)
  centeredImage.save('TEST.png')

  pickingPoints = getPickingPoints(baseImgSize, nbEllipsesPerDiametralLine, angleStep)
  pickedColors = pickColors(pickingPoints, centeredImage)
  renderPickedPointsPreview(outputFileName, pickedColors, 10)
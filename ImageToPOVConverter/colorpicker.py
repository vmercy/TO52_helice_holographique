from PIL import Image
from PIL import ImageDraw
import json
from math import ceil, pi, sin,cos

def renderPickedPointsPreview(filename, pickedColorPoints, ellipsesDiameter):
  """Renders an image containing ellipses at picked points positions with the picked color

  Args:
      filename (string): The rendered image output filename
      pickedColorPoints (array): The list of picked point colors
      ellipsesDiameter ([type]): The diameter of each ellipse representing a picked color point
  """
  maxSizingColorPoint = max(pickedColorPoints, key=(lambda x:max(x[0][1])))
  size = max(maxSizingColorPoint[0][1])
  size+=ellipsesDiameter
  size = ceil(size)
  outputImg = Image.new('RGB', (size, )*2, (0, 0, 0))
  draw = ImageDraw.Draw(outputImg)
  draw.rectangle([(0, 0), (size, )*2], 'black')
  for pickedColorPoint in pickedColorPoints:
    upperLeftCornerCoordinates = (
        pickedColorPoint[0][1][0]-ellipsesDiameter/2, pickedColorPoint[0][1][1]-ellipsesDiameter/2)
    bottomRightCornerCoordinates = (
        upperLeftCornerCoordinates[0]+ellipsesDiameter, upperLeftCornerCoordinates[1]+ellipsesDiameter)
    draw.ellipse([upperLeftCornerCoordinates,
                  bottomRightCornerCoordinates], fill=pickedColorPoint[1])
  outputImg.save(filename)

def pickColors(pickingPoints, subjectImage):
  """Pick pixel colors on image

  Args:
      pickingPoints (array): Array of tuples containing picking points coordinates
      subjectImage (PIL.Image): The image where colors must be picked

  Returns:
      Array: List of picked colors in the form (((theta,rIndex),(x,y)),(r,g,b)))
  """
  pickedColorPoints = []
  for pickingPoint in pickingPoints:
    pixel = subjectImage.getpixel(pickingPoint[1])
    pickedColorPoints.append((pickingPoint,pixel))
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
  radialCoordinates = []
  if(nbPoints%2): # number of points is odd, so we place the first one on the center
    radialOrigin = 0
    nbPoints-=1
  else:
    radialOrigin = spaceBetweenPoints/2
    nbPoints-=2
    radialCoordinates.append(radialOrigin)
  for i in range(0,nbPoints//2):
    radialCoordinates.append(radialOrigin+(i+1)*spaceBetweenPoints)
  pointsPositions = []
  for radialIndex, radial in enumerate(radialCoordinates):
    pointsPositions.append(((angle, radialIndex),(pickingAreaDiameter/2+radial*sin(angle), pickingAreaDiameter/2+radial*cos(angle))))
    pointsPositions.append(((angle, -radialIndex),(pickingAreaDiameter/2-radial*sin(angle), pickingAreaDiameter/2-radial*cos(angle))))
  return pointsPositions

#def addTrailArcs

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
    points += computePickingPointsPositionsOnDiametralLine(pickingAreaDiameter, nbPointsPerLine, angle_rad)
  if(nbPointsPerLine%2): #if the number of points per line is odd then we add the center point once
    points.append(((0,0),(pickingAreaDiameter//2,)*2))
  return points

def savePickedColors(filename, pickedColors, nbSectors):
  """Saves picked colors to json file

  Args:
      filename (string): name of JSON file to write
      pickedColors (array): array containg picked colors
      nbSectors (int): number of expected sectors

  Returns:
      array: List of cleaned picked colors in the form [((thetaIndex, radialIndex),(r,g,b))]
  """
  cleanedPickedColors = []
  lastTheta = 0
  thetaIndex = 0
  for pickedColor in pickedColors:
    if pickedColor[0][0][0] != lastTheta:
      thetaIndex+=1
    lastTheta = pickedColor[0][0][0]
    cleanedPickedColors.append((thetaIndex, pickedColor[0][0][1], pickedColor[1]))
  with open(filename, 'w') as outfile:
    json.dump(cleanedPickedColors, outfile)
  return cleanedPickedColors

# Configuration variables
nbEllipsesPerDiametralLine = 2*48
imageFileName = 'logo_utbm.png'
outputFileName = 'result_picking.png'
nbSectors = 10 #number of displaying sectors
angleStep = int(180/nbSectors)
zoomFactor = 90 #zoom factor in percent

if __name__ == "__main__":
  sourceImg = Image.open(imageFileName)
  sourceImg.convert('RGBA')
  imgMaxSize = max(sourceImg.size)
  baseImgSize = imgMaxSize*100//zoomFactor
  centeredImage = Image.new('RGB', (baseImgSize,)*2,'black')
  
  centeredImage.paste(sourceImg,((baseImgSize-sourceImg.size[0])//2,(baseImgSize-sourceImg.size[1])//2))
  centeredImage.save('TEST.png')

  pickingPoints = getPickingPoints(baseImgSize, nbEllipsesPerDiametralLine, angleStep)
  pickedColors = pickColors(pickingPoints, centeredImage)

  savePickedColors(imageFileName.replace('.png','.json'), pickedColors, nbSectors)
  renderPickedPointsPreview(outputFileName, pickedColors, 10)
from .TreeNode import TreeNode
from scipy.stats import linregress
import math

def CorrelationDimension(points):
    
    try:
        dimension = getDatasetDimension(points)
    except ValueError as e:
        print(e)

    hypergridSideSize = getHyperSize(points)
    root = TreeNode(dimension)
    sidesizeValues = [math.log(hypergridSideSize, 10)]
    sumSquaredOccupancies = []
    myTree = {i: [] for i in range(dimension + 1)}

    for point in points:
        cellSize = hypergridSideSize
        bounds = [(0, cellSize)] * len(point)
        
        if(root.getCounter(0) == 0):
            root.setRootCounter()
            currentNode = root.addChild(0)
            myTree[0].append(root)
        else:
            root.setRootCounter()
            currentNode = root.getPointer(0)

        for i in range(1, dimension + 1):
            cellSize = cellSize / 2
            
            if cellSize == 0:
                break

            if math.log(cellSize, 10) not in sidesizeValues:
                sidesizeValues.append(math.log(cellSize, 10))

            cell = cellPicker(point, bounds)

            if currentNode not in myTree[i]:
                myTree[i].append(currentNode)

            if currentNode.getCounter(cell) == 0 and i != (dimension):
                currentNode.setCellCounter(cell)
                currentNode.addChild(cell)
                currentNode = currentNode.getPointer(cell)
            else:
                currentNode.setCellCounter(cell)
                currentNode = currentNode.getPointer(cell)

    for level in myTree:
        level_counter = 0
        for node in myTree[level]:
            level_counter += node.getNodeSquareCounter()
        sumSquaredOccupancies.append(math.log(level_counter, 10))

    return linregress(sidesizeValues, sumSquaredOccupancies).slope

def cellPicker(point, bounds):
    cell = []

    # Iterate over each dimension of the point
    for i, coordinate in enumerate(point):
        start, end = bounds[i]
        midpoint = (start + end) / 2  # Midpoint for the current cell (based on the current bounds)
        
        # Determine if the point is in the lower or upper half of the current bounds
        if coordinate < midpoint:
            cell.append(0)  # Inferior half
            bounds[i] = (start, midpoint)  # Update bounds to the inferior half
        else:
            cell.append(1)  # Superior half
            bounds[i] = (midpoint, end)  # Update bounds to the superior half
    
    # Return the binary string representing the cell
    return ''.join(map(str, cell))

def getDatasetDimension(dataset):
    if not dataset:
        raise ValueError("Dataset cannot be empty.")
    
    first_point_dimension = len(dataset[0])
    
    for point in dataset:
        if len(point) != first_point_dimension:
            raise ValueError("Dataset contains points with different dimensions.")
    
    return first_point_dimension

def getHyperSize(dataset):
    flattened_coords = [coordinate for point in dataset for coordinate in point]

    return max(flattened_coords)

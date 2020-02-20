import pprint
import yaml

y = """
solid:
  red: [255, 0, 0]
  green: [0, 255, 0]
  blue: [0, 0, 255]
"""

solid = yaml.safe_load(y)["solid"]

print(type(solid))
print()
print(type(solid["red"]))
print()
print(tuple(solid["red"]))
print()
print("{}".format(solid))





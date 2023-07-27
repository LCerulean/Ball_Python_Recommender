import itertools
#Python class (lol)

class Ball_Python_Package:
  def __init__(self, price=0, snakes=[], package_traits=[]):
    self.price = price
    self.snakes = snakes
    self.package_traits = package_traits


  def build_bp_package(self, snake_list):
    for snake in snake_list:
      self.price += snake["Price"]
      self.snakes.append(snake)
      for trait in snake["Traits"]:
        if trait not in self.package_traits:
          self.package_traits.append(trait)


  def combine_bp_packages(self, package1, package2):
    self.price = package1.price + package2.price
    for snake in package1.snakes:
      self.snakes.append(snake)
    for snake in package2.snakes:
      self.snakes.append(snake)
    for snake in self.snakes:
      for trait in snake["Traits"]:
        if trait not in self.package_traits:
          self.package_traits.append(trait)

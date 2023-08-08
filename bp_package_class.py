#Ball_Python_Package puts together snakes into groups
#TraitValue assigns a value to traits for use in determining the value of Ball_Python_Package traits list

class Ball_Python_Package:
  def __init__(self, price=0, pack_trait_count=0, pack_trait_value=0, snakes=[], package_traits=[]):
    self.price = price
    self.pack_trait_count = pack_trait_count
    self.pack_trait_value = pack_trait_value
    self.snakes = snakes
    self.package_traits = package_traits


  def build_bp_package(self, snake_list):
    for snake in snake_list:
      if snake not in self.snakes:
        self.snakes.append(snake)
    for snake in self.snakes:
      self.price += snake["Price"]
      for trait in snake["Traits"]:
        if trait not in self.package_traits:
          self.package_traits.append(trait)
    for trait in self.package_traits:
      self.pack_trait_count += 1
      trait_value = self.get_trait_value(trait)
      self.pack_trait_value += trait_value


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
    for trait in self.package_traits:
      self.pack_trait_count += 1
      trait_value = self.get_trait_value(trait)
      self.pack_trait_value += trait_value


  def get_trait_value (self, trait):
    recessive_visual_t = ['lavender', 'piebald', 'clown', 'hypo']
    recessive_het_t = ['het lavender', 'het piebald', 'het clown', 'het hypo']
    recessive_pos_het_t = ['pos het lavender', 'pos het piebald', 'pos het clown', 'pos het hypo', '50% het lavender', '50% het piebald', '50% het clown', '50% het hypo', '66% het lavender', '66% het piebald', '66% het clown', '66% het hypo']
    t_not_genetic = ['pet only', 'paradox']

    if trait in recessive_visual_t:
      t_value = 3
    elif trait in recessive_het_t:
      t_value = 2
    elif trait in recessive_pos_het_t:
      t_value = 1
    elif trait in t_not_genetic:
      t_value = 0
    else:
      t_value = 2
    return t_value
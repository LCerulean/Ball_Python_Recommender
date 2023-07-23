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
    return self


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
    return self
  

  def find_all_list_combos(self, snake_list, num_snakes, budget_cap):
    #finding all combos that fit count and budget constraits
    all_combos = []
    for i in range(0,len(snake_list)+1):
      combo = list(itertools.combinations(snake_list,i))
      if len(combo) == num_snakes:
        price = 0
        for snake in combo:
          price += snake["Price"]
        if price <= budget_cap:
          all_combos.append(combo)
    #removing duplicate combos, putting combos in final_combos
    final_combos = []
    for combo in all_combos:
      removed_combo = combo
      all_combos.remove(combo)
      snakes_match = 0
      for snake in removed_combo:
        for remaining_combos in all_combos:
          for remaining_snakes in remaining_combos:
            if remaining_snakes == snake:
              snakes_match += 1
      if snakes_match != num_snakes:
        final_combos.append(removed_combo)
    return final_combos
  
  def find_all_pack_combos(self, male_combos, female_combos, budget, include_in_package_traits = None):
    all_pack_combos = []
    for male_combo in male_combos:
      for female_combo in female_combos:
        if male_combo.price + female_combo.price <= budget:
          combo = self.combine_bp_packages(male_combo,female_combo)
          if include_in_package_traits != None:
            traits_count = 0
            for trait in include_in_package_traits:
              if trait in combo.package_traits:
                traits_count +=1
            if traits_count == len(include_in_package_traits):
              all_pack_combos.append(combo)
          else:
            all_pack_combos.append(combo)
    return all_pack_combos
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
  
  def find_all_pack_combos(self, snake_list, num_snakes, budget_cap):
    all_combos = []
    final_combos = []
    for i in len(snake_list):
      combo = [i]
      count_snakes = 1
      idx_count = 1
      ###NEEDS WORK, NOT YET CREATING ALL POSSIBLE COMBOS###
      while count_snakes < num_snakes:
        combo.append(snake_list[i+idx_count])
        count_snakes += 1
        idx_count += 1
        if count_snakes >= len(snake_list) or idx_count not in len(snake_list):
          break
      if len(combo) == num_snakes and combo not in all_combos:
        all_combos.append(combo)
    #removing combos outside budget_cap
    for combo in all_combos:
      price = 0
      for snake in combo:
        price += snake["Price"]
      if price > budget_cap:
        all_combos.remove(combo)
    #removing duplicate combos, putting combos in final_combos
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
#Builds groups of ball pythons and contains the needed information on each group
class BP_Group:
  def __init__(self, price=0, group_trait_value=0, snakes=[], group_traits=[]):
    self.price = price
    self.group_trait_value = group_trait_value
    self.snakes = snakes
    self.group_traits = group_traits


  def build_bp_group(self, snake_list):
    for snake in snake_list:
      if snake not in self.snakes:
        self.snakes.append(snake)
    for snake in self.snakes:
      self.price += snake.price
      self.group_trait_value += snake.snake_trait_value
      for trait in snake.traits:
        if trait not in self.group_traits:
          self.group_traits.append(trait)


  def combine_bp_groups(self, group1, group2):
    self.price = group1.price + group2.price
    self.group_trait_value = group1.group_trait_value + group2.group_trait_value
    #adding the two snake lists into the package list
    self.snakes = group1.snakes[:] + group2.snakes[:]
    #adding traits to packate_traits if they are not already in the list
    self.group_traits = group1.group_traits[:]
    for trait in group2.group_traits:
      if trait not in self.group_traits:
        self.group_traits.append(trait)



#contains the needed information for each ball python-------------------------------------------------------------------------------------------------------------------------------------
class Snake:
  def __init__(self, title, snake_id, price, sex, snake_trait_value=0, traits={}):
    self.title = title
    self.snake_id = snake_id
    self.price = price
    self.sex = sex
    self.snake_trait_value = snake_trait_value
    self.traits = traits

#find the total value of the traits in the snake and updates the snake's 'trait_value'
  def get_snake_trait_value (self):
    for trait in self.traits:
      self.snake_trait_value += self.traits[trait].trait_value
  


#contains the needed infomation for each trait------------------------------------------------------------------------------------------------------------------------------------------
class Trait:
  def __init__(self, trait_name, trait_type=None, trait_value=0):
    self.trait_name = trait_name
    self.trait_type = trait_type
    self.trait_value = trait_value


  #identifies a trait's type and value
  def update_trait_type_and_value(self, trait_type_dict):
    #updating trait's type if found in trait_type_dict
    if self.trait_name in trait_type_dict['r_visual']:
      self.trait_type = 'r_visual'
    #adding trait to trait_type_dict if not already in there
    if self.trait_type == None:
      is_het = self.trait_name.find('het')
      if is_het != -1:
        #finding which het list trait belongs in
        if is_het == 0:
          trait_type_dict['r_100_het'].append(self.trait_name)
          self.trait_type = 'r_100_het'
        else:
          r_50_66 = self.trait_name.find('%')
          if r_50_66 > -1:
            trait_type_dict['r_50_66_het'].append(self.trait_name)
            self.trait_type = 'r_50_66_het'
          else:
            trait_type_dict['r_pos_het'].append(self.trait_name)
            self.trait_type = 'r_pos_het'
      else:
        #finding if codominante is super or singular
        is_super = self.trait_name.find('super') 
        if is_super != -1:
          trait_type_dict['c_super'].append(self.trait_name)
          self.trait_type = 'c_super'
        else:
          trait_type_dict['c_single'].append(self.trait_name)
          self.trait_type = 'c_single'

    #assigns trait's value
    trait_value_dict = {'r_visual':4, 'r_100_het':3, 'r_50_66_het':1, 'r_pos_het':0, 'c_single':2, 'c_super':3, 'non-genetic':0, 'pet only':-1}
    self.trait_value = trait_value_dict[self.trait_type]
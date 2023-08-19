import json
import itertools
from bp_classes import *

#recessive traits start with 'r_', codominante with 'c_'
trait_type_dict = {'r_visual':['lavender', 'piebald', 'clown', 'hypo'], 'r_100_het':[], 'r_50_66_het':[], 'r_pos_het':[], 'c_single':[], 'c_super':[], 'non-genetic':['paradox'], 'defect':['pet only']}
#list for all snakes in stock
snakes = []
#list for all traits in stock
trait_stock = {}

group_order = {'budget':None, 'discount':None, 'females':0, 'males':0, 'must_have_traits':None, 'must_one_of_traits':None, 'group_traits':None, 'ex_traits':None}

###Setup functions-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#pulls relevant data from json file, converts to desired format in 'snakes' list (each index is a dictionary of individual snake)
def get_shop_stock():
  #convert to read and write to shop_data file, each snake on it's own line
  with open('animals_2.json') as raw_data:
    shop_data = json.load(raw_data) #type is list, indicies are dictionaries
    for snake_data in shop_data:
      if snake_data["State"] == "For Sale":
        snake_info = Snake(title=snake_data['Title*'], snake_id=snake_data['Animal_Id*'], price=snake_data['Price'], sex=snake_data['Sex'], traits={})
        #building trait information and adding to snake_info
        traits_list = convert_snake_traits_to_list(snake_data['Traits'])
        for trait in traits_list:
          t = Trait(trait_name=trait)
          t.update_trait_type_and_value(trait_type_dict)
          snake_info.traits[t.trait_name] = t
          if t.trait_name not in trait_stock:
            trait_stock[t.trait_name] = t
        names_of_traits = ""
        for trait in snake_info.traits:
          names_of_traits += trait + ", "
        #updating snake_trait_value after getting value from traits
        snake_info.get_snake_trait_value()
        #adding snake to stock
        snakes.append(snake_info)
  return snakes
    

#formats snake traits pulled from json file, used in 'get_shop_stock' function
def convert_snake_traits_to_list(snake_traits_data):
  traits_split = snake_traits_data.split(' ')
  traits_list = []
  trait_count = len(traits_split)
  count = 0
  while count < trait_count:
    #joining percents with hets  and their corresponding trait in single string
    if traits_split[count] == "50%" or traits_split[count] == "66%" or traits_split[count] == "pos":
      trait = traits_split[count] + " " + traits_split[count+1] + " " + traits_split[count+2]

      #skipping "albino" in the case of finding lavender, lavender is assumed albino
      if traits_split[count+2] == "lavender":
        count +=1
      count += 2
      traits_list.append(trait)
      if count >= len(traits_split):
        break
    #joining 100% hets with corresponding trait in single string  
    elif traits_split[count] == "het":
      trait = traits_split[count] + " " + traits_split[count+1]
      #skipping "albino" in the case of finding lavender, lavender is assumed albino
      if traits_split[count+1] == "lavender":
        count +=1
      count += 1
      traits_list.append(trait)
      if count >= len(traits_split):
        break
    #checking if visible trait is two words, if so joining into single string before appending list  
    elif traits_split[count] == "black" or traits_split[count] == "yellow" or traits_split[count] == "pet":
      trait = traits_split[count] + " " + traits_split[count+1]
      traits_list.append(trait)
      #skipping 2nd half of two word trait in next loop through traits_split
      count += 1
      if count >= len(traits_split):
        break
    #skipping "albino" in the case of finding lavender, lavender is assumed albino
    elif traits_split[count] == "lavender":
      traits_list.append(traits_split[count])
      count += 1
      if count >= len(traits_split):
        break
    #adding all single word visible traits to list  
    else:
      traits_list.append(traits_split[count])
    count += 1
  return traits_list


#categorizes and prints in stock traits for user
def categorized_in_stock_traits():
  copy_trait_stock = trait_stock.copy()
  #getting max length of traits for standardizing collumns for printing
  len_trait_block = 0
  for trait in copy_trait_stock:
    if len(trait) > len_trait_block:
      len_trait_block = len(trait)
  
  #recessive traits
  r_vis_t , r_100_t , r_50_66_t , r_pos_t = [] , [] , [] , []
  #codominant traits
  c_sing , c_sup = [] , []
  #everthing else
  other_traits = []
  #putting traits in catagory lists
  for trait in copy_trait_stock:
    if copy_trait_stock[trait].trait_type == 'r_visual':
      cat_list = r_vis_t
    elif copy_trait_stock[trait].trait_type == 'r_100_het':
      cat_list = r_100_t
    elif copy_trait_stock[trait].trait_type == 'r_50_66_het':
      cat_list = r_50_66_t
    elif copy_trait_stock[trait].trait_type == 'r_pos_het':
      cat_list = r_pos_t 
    elif copy_trait_stock[trait].trait_type == 'c_super':
      cat_list = c_sup
    elif copy_trait_stock[trait].trait_type == 'c_single':
      cat_list = c_sing
    else:
      cat_list = other_traits
    #adjusting the trait's string length for printing
    add_len = len_trait_block - len(trait)
    if add_len > 0:
      trait_name_adjusted = trait + (" " * add_len)
      cat_list.append(trait_name_adjusted)
    else:
      cat_list.append(trait)

  #rearranging recessive_traits so it lists them from highest to lowest value (visuals, followed by 100% hets, followed by 66%, followed by 50%, ending with pos hets)
  r_vis_t.sort()
  r_100_t.sort()
  r_50_66_t.sort()
  r_pos_t.sort()
  recessive_traits = r_vis_t + r_100_t + r_50_66_t + r_pos_t
  #rearranging codominant traits so supers are placed at top, followed by single codominant traits
  c_sup.sort()
  c_sing.sort()
  codominant_traits = c_sup + c_sing
  
  #adds blanks to shorter list to make both even to simplify printing even columns
  list_len_diff = max(len(recessive_traits), len(codominant_traits)) - min(len(recessive_traits), len(codominant_traits))
  if len(recessive_traits) < len(codominant_traits):
    for num in range(list_len_diff):
      recessive_traits.append(" " * len_trait_block)
  elif len(recessive_traits) > len(codominant_traits):
    for num in range(list_len_diff):
      codominant_traits.append(" " * len_trait_block)
  add_to_other = len(recessive_traits) - len(other_traits)
  for num in range(add_to_other):
    other_traits.append(" ")

  #formats and prints the categorized traits
  trait_col_header = "\nRECESSIVE TRAITS     CODOMINANT TRAITS     OTHER\n"
  list_len_max = max(len(recessive_traits), len(codominant_traits))
  idx = 0
  for num in range(list_len_max):
    trait_col_header += recessive_traits[idx] + "     " + codominant_traits[idx] + "     " + other_traits[idx] + "\n"
    idx += 1
  print(trait_col_header)
  

#updates the price of each snake in list based on discount percent for group_order['num_snakes'], used in cut_by_price function before the cuts are made
def adjust_price_discount(snake_list):
  discounts = {2:15, 3:20, 4:25}
  for i in range(5,10):
    discounts[i] = 30
  for i in range(10,100):
    discounts[i] = 40

  order_group_size = group_order['males'] + group_order['females']
  if order_group_size == 1:
    pass
  else:
    group_discount = discounts[order_group_size]
    for snake in snake_list:
      discount = snake.price/group_discount
      snake.price -= discount


#welcome measage, list of things it can do and provides user with list of in stock traits if desired
def welcome_message():
  print("""
*******************************************************************************
*****************  Welcome to the Ball Python Recommender!  *******************
*******************************************************************************
The purpose of this program is to aid BP breeders in putting together the best
groups for customers based on their budget, desired traits, and number of
snakes in a time efficent manner.  This program by default is using an example
inventory file from the Crescent Serpents MorphMarket shop (it is not current).


To use your own shop file:
-Log into MorphMarket and right click the screen. Select 'view page source'.
-Locate the downloadable json file for your shop (ctrl + f and type json).
-Download the file into the 'Ball Python Recommender' folder as 'animals.json'
-Give it a test!
  """)
  see_traits = input("Would you like to see a list of traits currently in stock? (Y/[any key]) ")
  if len(see_traits) > 0 and see_traits.upper()[0] == "Y":
    categorized_in_stock_traits()
  print("\nLet's get started!")


###function for getting requirements for group and preparing snake list for processing--------------------------------------------------------------------------------------------------------
#adds user input traits requirements to order if in stock/exist, used in take_order function
def add_traits_to_order(user_input, order_trait_requirement, order_trait_list):
  for trait in user_input.split('/'):
    if trait.lower() in trait_stock and trait not in order_trait_list:
      order_trait_list.append(trait)
    elif trait.lower() in order_trait_list:
      print(f"{trait} is already in the order.")
    else:
      print(f"Sorry, {trait} is not in stock.")
  more_traits = input("Did you want to add any others (Y/[any key])? ")
  if more_traits.upper() != 'Y':
    group_order[order_trait_requirement] = order_trait_list


#Gets the parameters from user and puts them in the group_order dictionary
def take_order():
  #getting budget
  prices = []
  for snake in snakes:
    prices.append(snake.price)
  while type(group_order['budget']) != int:
    try:
      budget = int(input(f"\nWhat is the maximum budget? (Minimum of ${min(prices)}0) "))
      if (budget) >= min(prices):
        group_order['budget'] = budget
      else:
        print("Sorry, the budget is too small.")
    except:
      print("Sorry, I didn't understand that. Make sure you're not using extra symbols or spaces.")
  print()
  
  #getting number and sex of snakes for group.
  while group_order['males'] == 0 and group_order['females'] == 0:
    try:
      group_order['males'] = int(input(f"How many males? "))
      group_order['females'] = int(input(f"How many females? "))
    except:
      print("Sorry, I didn't understand that. Make sure you're giving a number.")  
    if group_order['males'] == 0 and group_order['females'] == 0:
      print("Sorry, I can't build a group out of 0 snakes...")
  print()

  print("Let's start picking traits. We're going to go through 4 options, 3 for traits to include and 1 for traits to exclude:\n")
  #getting traits all animals should have
  all_snakes_have_traits = []
  while group_order['must_have_traits'] == None:
    include_traits = input("1. Traits EVERY snake MUST to have, such as 'every snake is piebald, if it's not piebald I don't want it'.\nIf any, type them below seperated by '/' (Example: 'lavender/piebald/mahogany'), else hit [ENTER].\n")
    if include_traits != "":
      add_traits_to_order(include_traits, 'must_have_traits', all_snakes_have_traits)
    else:
      break
  print()
  #getting list of traits each animal should have at least one of from list
  at_least_one_traits = []
  while group_order['must_one_of_traits'] == None:
    include_traits = input("2. Traits EVERY snake must have AT LEAST one of, such as 'every snake is either clown or het clown'.\nIf any, type them below seperated by '/' (Example: 'clown/het clown/66% het clown/50% het clown'), else hit [ENTER].\n")
    if include_traits != "":
      add_traits_to_order(include_traits, 'must_one_of_traits', at_least_one_traits)
    else:
      break
  print()
  #getting traits that should be in the group but not every animal needs to have
  in_the_group_traits = []
  while group_order['group_traits'] == None:
    include_traits = input("3. Traits that MUST be included in the group, but not every snake needs to have, such as 'at least one pastel and one yellow belly'.\nIf any, type them below seperated by '/' (Example: 'pastel/enchi/yellow belly'), else hit [ENTER].\n")
    if include_traits != "":
      add_traits_to_order(include_traits, 'group_traits', in_the_group_traits)
    else:
      break
  print()
  #getting traits to exclude
  ex_traits = []
  while group_order['ex_traits'] == None:
    exclude_traits = input("4. Traits you do NOT want included in the group, such as 'no pet only or snakes with spider'.\nIf any, type them below seperated by '/' (Example: 'pet only/spider/black pastel'), else hit [ENTER].\n ")
    if exclude_traits != "":
        add_traits_to_order(exclude_traits, 'ex_traits', ex_traits)
    else:
      break

  print("\nGot it, finding you snakes...\n")


#divides snake list into two seperate lists (males and females) and removes any doppelgangers
def divide_sexes_and_remove_doppelgangers(list_to_divide):
  males = []
  females = []
  for snake in list_to_divide:
    if snake.sex == 'male':
      males.append(snake)
    elif snake.sex == 'female':
      females.append(snake)
    else:
      continue
  print(f"Sexes split, {len(males)} males and {len(females)} females.")

  print("Checking females for doppelgangers...")
  females_no_doppelgangers = []
  for female in females:
    females_no_doppelgangers.append(female)
    females.remove(female)
    for other_female in females:
      if female.price == other_female.price and female.snake_trait_value == other_female.snake_trait_value and female.title == other_female.title:
        females.remove(other_female)
  print(f"All doppelgangers removed, {len(females)} unique females.")

  print("Checking males for doppelgangers...")
  males_no_doppelgangers = []
  for male in males:
    males_no_doppelgangers.append(male)
    males.remove(male)
    for other_male in males:
      if male.price == other_male.price and male.snake_trait_value == other_male.snake_trait_value and male.title == other_male.title:
        males.remove(other_male)
  print(f"All doppelgangers removed, {len(males)} unique males.")

  return males_no_doppelgangers, females_no_doppelgangers


###functions for remvoing snakes that do not fit requirements, or cutting to improve group quality----------------------------------------------------------------------------------------------
#removes any snakes that do not fit the required sex (if any)
def cut_by_sex(list_to_cut):
  cut = []
  if group_order['females'] != 0:
    for snake in list_to_cut:
      if snake.sex == 'female':
        cut.append(snake)
  if group_order['males'] != 0:
    for snake in list_to_cut:
      if snake.sex == 'male':
        cut.append(snake)
  return cut


#removes any snakes that do not have traits requirements, used for: "all_snake_traits", 'must_have_traits', and 'ex_traits' in group order dict
def cut_by_trait(list_to_cut, trait_requirement):
  cut = []
  if trait_requirement == 'must_have_traits':
    required_count = len(group_order['must_have_traits'])
    for snake in list_to_cut:
      required_count_have = 0
      for trait in group_order['must_have_traits']:
        if trait in snake.traits:
          required_count_have += 1
      if required_count_have == required_count: 
        cut.append(snake)
  elif trait_requirement == 'must_one_of_traits':
    for snake in list_to_cut:
      for trait in snake.traits:
        if trait in group_order['must_one_of_traits'] and snake not in cut:
          cut.append(snake)
  elif trait_requirement == 'ex_traits':
    for snake in list_to_cut:
      exclude_snake = 'N'
      for trait in group_order['ex_traits']:
        if trait in snake.traits:
          exclude_snake = 'Y'
          break
      if exclude_snake == 'N':
        cut.append(snake)
  
  return cut


#removes any snakes that do not have the required number of traits (if any)
def remove_snakes_outside_budget(list_to_cut, budget, num_snakes, sex):
  group_possible = True
  if num_snakes != 0:
    price_list = []
    price_dict = {}
    min_snakes = num_snakes
    for snake in list_to_cut:
      price_list.append(snake.price)
      if snake.price not in price_dict:
        price_dict[snake.price] = [snake]
      else:
        price_dict[snake.price].append(snake)
    price_list.sort()
    one_snake_short_price = 0
    for price in price_list[0:(min_snakes-1)]:
      one_snake_short_price += price
    if one_snake_short_price >= budget:
      print(f"Sorry, it looks like a group with {min_snakes} {sex} is over your budget.")
      group_possible = False
    else:
      while one_snake_short_price + price_list[-1] > budget:
        if price_list[-1] in price_dict:
          price_dict.pop(price_list[-1])
        price_list.remove(price_list[-1])
      if len(price_list) < min_snakes:
        print(f"Sorry, it looks like a group with {min_snakes} {sex} is over your budget.")
        group_possible = False
    
    if group_possible == True:
      in_budget_snakes = []
      for key in price_dict:
        snakes_to_add = price_dict[key]
        for snake in snakes_to_add:
          in_budget_snakes.append(snake)

      min_price = 0
      for price in price_list[0:(min_snakes)]:
        min_price += price

  if group_possible == True:
    return in_budget_snakes, min_price
  else:
    return [], None
    

#removes any snakes that are outside of budget, also returns min price for male and female groups
def cut_by_price(list_to_cut):
  group_possible = True
  print("Adjusting snake prices for discount...")
  adjust_price_discount(list_to_cut)
  print("Discount applied. Dividing sexes and removing doppelgangers...")
  divide_sexes = divide_sexes_and_remove_doppelgangers(list_to_cut)
  males_no_dop = divide_sexes[0]
  females_no_dop = divide_sexes[1]
  #removing any male or female prices too expensive for group in individual sex list if sex is in group_order
  if group_order['males'] != 0:
    remove_overpriced_males = remove_snakes_outside_budget(males_no_dop, group_order['budget'], group_order['males'], 'males')
    males_in_budget = remove_overpriced_males[0]
    min_males_price = remove_overpriced_males[1]
    if len(males_in_budget) < group_order['males']:
      group_possible = False
      print("Not enough males within budget.")
  if group_order['females'] != 0:  
    remove_overpriced_females = remove_snakes_outside_budget(females_no_dop, group_order['budget'], group_order['females'], 'females')
    females_in_budget = remove_overpriced_females[0]
    min_females_price = remove_overpriced_females[1]
    if len(females_in_budget) < group_order['females']:
      group_possible = False
      print("Not enough females within budget.")
  #removing any additional snakes too expensive for group order when both sexes are in group_order
  if group_order['males'] != 0 and group_order['females'] != 0 and group_possible == True:
    budget_for_males = group_order['budget'] - min_females_price
    recheck_males_in_budget = remove_snakes_outside_budget(males_in_budget, budget_for_males, group_order['males'], 'males')
    males_in_budget = recheck_males_in_budget[0]

    budget_for_females = group_order['budget'] - min_males_price
    recheck_females_in_budget = remove_snakes_outside_budget(females_in_budget, budget_for_females, group_order['females'], 'females')
    females_in_budget = recheck_females_in_budget[0]

    if len(males_in_budget) + len(females_in_budget) < group_order['males'] + group_order['females']:
      group_possible = False
      print("Cannot make a groupage within budget with both males and females.")
        
  if group_possible == True:
    return males_in_budget, females_in_budget, min_males_price, min_females_price
  else:
    return [], [], None, None


#combination of cut functions, cuts out any snakes that do not fit individual criteria for group and returns male and female lists,also returns minimum price for male and female groups
def cut_snakes():
  group_possible = True
  #removing any snakes that are not of desired sex (if any)
  if group_order['males'] == 0 or group_order['females'] == 0:
    try:
      cut1 = cut_by_sex(snakes)
      print(f"\nMaking cut, removing undesired sex. {len(cut1)} snakes in bag.")
    except:
      group_possible = False
  else:
    cut1 = snakes[:]
    print(f"Order males and females: {len(cut1)} possible snakes.")
  
  #removing any snakes that do not have mandatory traits
  if group_order['must_have_traits'] != None and group_possible == True:
    cut2 = cut_by_trait(cut1,'must_have_traits')
    if len(cut2) == 0:
      print(f"Sorry, there aren't any available snakes with {group_order['must_have_traits']}\n")
      group_possible = False
    else:
      print(f"\nMaking cut, removing snakes that do not have required traits: {group_order['must_have_traits']}. {len(cut2)} snakes in bag.")
  else:
    cut2 = cut1[:]
    print(f"No required traits all snakes must have: {len(cut2)} possible snakes.")
  
  #removing snakes that do not have a trait from list of 'at least one' traits
  if group_order['must_have_traits'] != None and group_possible == True:
    cut3 = cut_by_trait(cut2, 'must_have_traits')
    if len(cut3) == 0:
      print(f"Sorry, there aren't any available snakes left with {group_order['must_one_of_traits']}\n")
      group_possible = False
    else:
      print(f"\nMaking cut, removing snakes that do not have at least one of these traits: {group_order['must_one_of_traits']}. {len(cut3)} snakes in bag.")
  else:
    cut3 = cut2[:]
    print(f"No required traits snakes must have at least one of: {len(cut3)} possible snakes.")
  
  #removing snakes that have a trait from the list 'ex_traits'
  if group_order['ex_traits'] != None and group_possible == True:
    cut4 = cut_by_trait(cut3, 'ex_traits')
    if len(cut4) == 0:
      print(f"Sorry, there aren't any available snakes left that don't have one of these undesired traits: {group_order['ex_traits']}\n")
      group_possible = False
    else:
      print(f"\nMaking cut, removing snakes that have any of these undesired traits: {group_order['ex_traits']}. {len(cut4)} snakes in bag.")
  else:
    cut4 = cut3[:]
    print(f"No traits to exclude: {len(cut4)} possible snakes.")
  
  #removing any remaining snakes that are too expensive for budget
  try:
    print("Last cut, cutting by price...")
    final_cut = cut_by_price(cut4)
    print(f"Cut complete, {len(final_cut[0])} possible males and {len(final_cut[1])} possible females.")
    if final_cut != None and group_possible == True:
      males_list = final_cut[0]
      females_list = final_cut[1]
      min_male_group_price = final_cut[2]
      min_female_group_price = final_cut[3]
      print(f"\nRemoving snakes outside of budget and splitting by sex... {len(males_list)} males and {len(females_list)} females in bag.\n")
      return males_list,females_list, min_male_group_price, min_female_group_price
    else:
      return None
  except:
    return None


#only keeps groups with reasonably balanced snake prices, to avoid extreem value differences within groups (ex. $2000 and $50 snakes in same group)
def balanced_snake_price_groups_only(group_list_to_cut):
  balanced_groups = []
  try:
    for group in group_list_to_cut:
      min_reasonable_price = group.price // ((len(group.snakes) - 1) * 10)
      group_balanced = True
      for snake in group.snakes:
        if snake['Price'] < min_reasonable_price:
          group_balanced = False
      if group_balanced == True:
        balanced_groups.append(group)
    if len(balanced_groups) > 1:
      return balanced_groups
    else:
      return group_list_to_cut
  except:
    return group_list_to_cut


#Removes near idential groups (such as when groups are same price and have all the same traits due to sibling snakes with identical traits)
def remove_doppelganger_groups(group_list_to_cut):
  copy_list_to_cut = group_list_to_cut[:]
  cut_list = []
  for group in copy_list_to_cut:
    cut_list.append(group)
    copy_list_to_cut.remove(group)
    for other_group in copy_list_to_cut:
      if group.price == other_group.price and group.group_trait_value == other_group.group_trait_value:
        if len(group.group_traits) == len(other_group.group_traits):
          traits_match = True
          for trait in group.group_traits:
            if trait not in other_group.group_traits:
              traits_match = False
          if traits_match == True:
            copy_list_to_cut.remove(other_group)
  return cut_list

         
###group making functions------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#finding all combos that fit count and budget constraits, converting each combo to a Ball_Python_group: functions 'balanced_snake_price_groups_only' and 'remove_doppelganger' used to cut out less desirable and near duplicate groups
def find_combos_lists_to_groups(snake_list, num_snakes, budget_cap):
  all_combos = []
  pos_combos = itertools.combinations(snake_list, num_snakes)
  list_combos = list(pos_combos)
  print(f"Found {len(list_combos)} combos. Removing combos outside of budget...")
  for combo in list_combos:
    combo_group = BP_Group(price=0, group_trait_value=0, snakes=[], group_traits=[])
    combo_group.build_bp_group(combo)
    if combo_group.price <= budget_cap:  
      all_combos.append(combo_group)
  print(f"Complete, {len(all_combos)} combos inside budget. Removing unbalanced combos...")
  balanced_combos = balanced_snake_price_groups_only(all_combos)
  print(f"Complete, {len(balanced_combos)} combos.  Removing doppelganger combos...")
  unique_combos = remove_doppelganger_groups(balanced_combos)
  print(f"Complete, {len(unique_combos)} combos remainging")
  return unique_combos


#combines the male/female groups and returns a list of the groups that fit the budget and trait requirements: functions 'shrink_to_specific', 'balanced_snake_price_groups_only' and 'within_75_percent_budget' built in to cut out groups that are less than ideal
def find_balanced_combos(budget, combo_groups1, combo_groups2=None, include_in_group_traits = None):
  all_group_combos = []
  shrunk_combos1 = shrink_to_specific(combo_groups1, 250)
  if combo_groups2 != None:
    shrunk_combos2 = shrink_to_specific(combo_groups2, 250)
    for combo1 in shrunk_combos1:
      for combo2 in shrunk_combos2:
        mf_combo_price = combo1.price + combo2.price
        if  mf_combo_price <= budget:
          combo = BP_Group(price=0, group_trait_value=0, snakes=[], group_traits=[])
          combo.combine_bp_groups(combo1,combo2)
          if include_in_group_traits != None:
            traits_count = 0
            for trait in include_in_group_traits:
              if trait in combo.group_traits:
                traits_count +=1
            if traits_count == len(include_in_group_traits):
              all_group_combos.append(combo)
          else:
            all_group_combos.append(combo)
  else:
    for combo1 in shrunk_combos1:
      if include_in_group_traits != None:
        traits_count = 0
        for trait in include_in_group_traits:
          if trait in combo1.group_traits:
            traits_count +=1
        if traits_count == len(include_in_group_traits):
          all_group_combos.append(combo1)
      else:
        all_group_combos.append(combo1)
  balanced_combos = balanced_snake_price_groups_only(all_group_combos)
  balanced_combos_75 = within_75_percent_budget(balanced_combos)
  balanced_combos_final = shrink_to_specific(balanced_combos_75, 50)
  return balanced_combos_final


###arragement functions for identifying best groups-----------------------------------------------------------------------------------------------------------------------------------------------
#arranges list of groups by overall value of included traits in each group
def arrange_by_highest_group_trait_value(group_list_arrange):
  copy_list_to_arrange = group_list_arrange[:]
  num_groups = len(copy_list_to_arrange)
  max_value_groups = []
  while len(max_value_groups) != num_groups:
    max_value = 0
    for group in copy_list_to_arrange:
      if group.group_trait_value > max_value:
        max_value = group.group_trait_value
    for group in copy_list_to_arrange:
      if group.group_trait_value == max_value:
        max_value_groups.append(group)
        copy_list_to_arrange.remove(group)
  return max_value_groups


#arranges list of groups by lowest to highest price (used in 'shrink_to_specific' function in the case of too many possible options)
def arrange_by_price(group_list_arrange):
  copy_list_to_arrange = group_list_arrange[:]
  num_groups = len(copy_list_to_arrange)
  cheap_groups = []
  while len(cheap_groups) != num_groups:
    price_min = copy_list_to_arrange[0].price
    for group in copy_list_to_arrange:
      if group.price < price_min:
        price_min = group.price
    for group in copy_list_to_arrange:
      if group.price == price_min:
        cheap_groups.append(group)
        copy_list_to_arrange.remove(group)
  return cheap_groups


###Performance enhancers, cuts less desireable items to improve speed-----------------------------------------------------------------------------------------------------------------------------
#shrinks list of groups if length specified, used to prevent performance/freezing issues caused by too many possibilities
def shrink_to_specific(list_to_shrink, shrink_to_num):
  if len(list_to_shrink) > shrink_to_num:
    cut_by = (len(list_to_shrink) - shrink_to_num)
    print(f"Snakes to be cut: {cut_by}")
    arranged_price_list = arrange_by_price(list_to_shrink)
    print("list arranged by price, shrinking now...")
    shrunk_list = arranged_price_list[cut_by:]
    print(f"List shrunk: {len(shrunk_list)}")
    return shrunk_list
  else:
    return list_to_shrink


#cuts out groups that are less than 75% of the budget
def within_75_percent_budget(group_list_to_cut):
  within_75_groups = []
  for group in group_list_to_cut:
    if group.price >= int(group_order['budget'] * 0.75):
      within_75_groups.append(group)
  if len(within_75_groups) < 5:
    return group_list_to_cut
  else:
    return within_75_groups


###formated return of best results-------------------------------------------------------------------------------------------------------------------------------------------------------------
#Prints best 3 groups
def top_3_return(best_groups):
  if len(best_groups) >= 3:
    top_overall_groups = best_groups[:3]
  else:
    top_overall_groups = best_groups

  max_len_id = 0
  max_len_title = 0
  for group in top_overall_groups:
    for snake in group.snakes:
      if len(snake.snake_id) > max_len_id:
        max_len_id = len(snake.snake_id)
      if len(snake.title) > max_len_title:
        max_len_title = len(snake.title)
  for group in top_overall_groups:
    for snake in group.snakes:
      if len(snake.snake_id) < max_len_id:
        add_len = max_len_id - len(snake.snake_id)
        snake.snake_id += " " * add_len
      if len(snake.title) < max_len_title:
        add_len = max_len_title - len(snake.title)
        snake.title += " " * add_len


  print("\n----------------------------")
  print(f"Top {len(top_overall_groups)} Best Overall Groups:")
  print("----------------------------\n")
  gap = " " * 10
  count = 1
  for group in top_overall_groups:
    print(f"[Group {count}: ${group.price:.2f}]")
    count += 1
    for snake in group.snakes:
      print(f" {snake.snake_id}  {snake.title}  Price: ${snake.price:.2f}")
    print()
     


get_shop_stock()
copy_snake_list = snakes[:]
# in_stock_traits()
welcome_message()

#taking order and returning all possible snakes that fit requirements
possible_snakes = None
while possible_snakes == None:
  take_order()
  possible_snakes = cut_snakes()
  if possible_snakes == None:
    # in the case that the order is impossible to fill, resets group_order so no traits left in lists from previous attempt, also reset snakes so price discount does not carry over from previous attempt
    group_order = {'budget':None, "num_snakes":0, "discount":None, 'females':0, 'males':0, 'must_have_traits':None, 'must_have_traits':None, "group_traits":None, 'ex_traits':None, 'trait_count':None}
    snakes = copy_snake_list
    print("Let's try again. Are there any requirements you could lower or do without?\n")
possible_males = possible_snakes[0]
possible_females = possible_snakes[1]
min_male_group_price = possible_snakes[2]
min_female_group_price = possible_snakes[3]

#getting possible groups for males and/or females based on group order
if group_order['males'] > 0:
  possible_male_combos = find_combos_lists_to_groups(possible_males, group_order['males'], (group_order['budget']-min_female_group_price))
  print(f"Found {len(possible_male_combos)} possible male combos.")
if group_order['females'] > 0:
  possible_female_combos = find_combos_lists_to_groups(possible_females, group_order['females'],(group_order['budget']-min_male_group_price))
  print(f"Found {len(possible_female_combos)} possible female combs.")

#calculating final groups for orders that contain both males and females
if group_order['males'] > 0 and group_order['females'] > 0:
  print("Combining male and female combos...")
  possible_male_and_female_combos = find_balanced_combos(group_order['budget'], possible_male_combos, possible_female_combos, group_order['group_traits'])
  print(f"{len(possible_male_and_female_combos)} possible male/female combos")
  # by_best_group = arrange_by_best_overall_group(possible_male_and_female_combos)
  by_best_group = arrange_by_highest_group_trait_value(possible_male_and_female_combos)
#calculating final groups for orders that contain only males
elif group_order['males'] > 0:
  print("\nFinding best overall male groups...")
  just_males = find_balanced_combos(group_order['budget'], possible_male_combos, group_order['group_traits'])
  # by_best_group = arrange_by_best_overall_group(just_males)
  by_best_group = arrange_by_highest_group_trait_value(just_males)
#calculating final groups for orders that contain only females
else:
  print("\nFinding best overall female groups...")
  just_females = find_balanced_combos(group_order['budget'], possible_female_combos, group_order['group_traits'])
  # by_best_group = arrange_by_best_overall_group(just_females)
  by_best_group = arrange_by_highest_group_trait_value(just_females)

top_3_return(by_best_group)
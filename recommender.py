import json
import itertools
from max_heap import MaxHeap 
from bp_package_class import *

snakes = []
trait_stock = []
discounts = {1:None, 2:10, 3:15, 4:20}
for i in range(5,10):
  discounts[i] = 25
for i in range(10,100):
  discounts[i] = 30

package_order = {"budget":None, "num_snakes":0, "discount":None, "females":0, "males":0, "all_snakes_traits":None, "one_of_traits":None, "pack_traits":None, "ex_traits":None, "trait_count":None}


#pulls relevant data from json file, converts to desired format in 'snakes' list (each index is a dictionary of individual snake)
def get_shop_stock():
  #convert to read and write to shop_data file, each snake on it's own line
  with open('animals_2.json') as raw_data:
    shop_data = json.load(raw_data) #type is list, indicies are dictionaries
    # print(shop_data)
    for snake_data in shop_data:
      if snake_data["State"] == "For Sale":
        snake_info = {'Title*':'', 'Animal_Id*':'', 'Maturity*':'', 'Price':'', 'Sex':'', 'Traits':[], 'Prey_State':'', 'Prey_Food':''}
        
        #converting traits string value to list of traits
        for key in snake_info:
          if key == "Traits":
            traits_split = snake_data[key].split(" ")
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

            snake_info["Traits"] = traits_list

          else:
          #copying relevant info from json file for each snake and putting it in list
            snake_info[key] = snake_data[key]
        
        snakes.append(snake_info)
  return snakes
    

#compiles a list of in stock traits the user can select from if looking for specific traits
def in_stock_traits():
  for snake in snakes:
    for trait in snake["Traits"]:
      if trait not in trait_stock:
        trait_stock.append(trait)
  trait_stock.sort()
  return trait_stock


#categorizes and prints in stock traits for user
def categorized_in_stock_traits():
  formatted_traits = []
  recessive_traits = []
  codominant_traits = []

  #standardizing trait string length for printing
  len_trait_block = 0
  for trait in trait_stock:
    if len(trait) > len_trait_block:
      len_trait_block = len(trait)
  for trait in trait_stock:
    add_len = len_trait_block - len(trait)
    if add_len > 0:
      trait += (" " * add_len)
      formatted_traits.append(trait)
    else:
      formatted_traits.append(trait)

  #separates recessive and codominant traits and puts recessive traits in a better order for display
  for trait in formatted_traits:
    if trait.find("lavender") >= 0 or trait.find("piebald") >= 0 or trait.find("clown") >= 0 or trait.find("hypo") >= 0:
      recessive_traits.append(trait)
    else:
      codominant_traits.append(trait)
  #rearranging recessive_traits so it doesn't look like crap
  reordering_recessives = []
  for trait in recessive_traits:
    if trait.find("het") == -1:
      reordering_recessives.append(trait)
  for trait in recessive_traits:
    if trait.find("het") >= 0 and trait.find("%") == -1:
      reordering_recessives.append(trait)
  for trait in recessive_traits:
    if trait[0] == "6":
      reordering_recessives.append(trait)
  for trait in recessive_traits:
    if trait not in reordering_recessives:
      reordering_recessives.append(trait)
  recessive_traits = reordering_recessives
  
  #adds blanks to shorter list to make both even to simplify printing even columns
  list_len_diff = max(len(recessive_traits), len(codominant_traits)) - min(len(recessive_traits), len(codominant_traits))
  if len(recessive_traits) < len(codominant_traits):
    for num in range(list_len_diff):
      recessive_traits.append(" " * len_trait_block)
  elif len(recessive_traits) > len(codominant_traits):
    for num in range(list_len_diff):
      codominant_traits.append(" " * len_trait_block)
  else:
    pass
       
  #formats and prints the categorized traits
  trait_col_header = "RECESSIVE TRAITS     CODOMINANT TRAITS\n"
  list_len_max = max(len(recessive_traits), len(codominant_traits))
  idx = 0
  for num in range(list_len_max):
    trait_col_header += recessive_traits[idx] + "     " + codominant_traits[idx] + "\n"
    idx += 1
  print(trait_col_header)
  

#graphics display, welcome, list of things it can do
def welcome_message():
  welcome = """
*********************************************************************
************  Welcome to the Ball Python Recommender!  **************
*********************************************************************
The purpose of this program is to aid BP breeders in putting together 
the best packages for customers based on their budget, desired traits,
and number of snakes in a time efficent manner.  This program by 
default is using an example inventory file from the Crescent Serpents 
MorphMarket shop.


To use your own shop file:
-Log into MorphMarket and right click the screen. Select 'view page source'.
-Locate the downloadable json file for your shop (ctrl + f and type json).
-Download the file into the 'Ball Python Recommender' folder as 'animals.json'
-Give it a test!
  """
  print(welcome)
  see_traits = input("Would you like to see a list of traits currently in stock? (Y/N) ")
  print()
  if len(see_traits) > 0 and see_traits.upper()[0] == "Y":
    categorized_in_stock_traits()
  print("\nLet's get started!")


#LONG ONE, gets the parameters from user and puts them in the package_order dictionary
def take_order():
  
  budget_max = None
  num_snakes = 0
  sex = None

  all_snakes_have_traits = []
  at_least_one_traits = []
  in_the_pack_traits = []
  ex_traits = []
  trait_count = None

  #getting budget
  while budget_max == None:
    budget = input("\nWhat is the maximum budget? (Minimum of $50) ")
    try:
      budget = int(budget)
      if (budget) >= 50:
        budget_max = budget
      else:
        print("Sorry, the budget is too small.")
    except:
      print("Sorry, I didn't understand that. Make sure you're not using extra symbols or spaces.")
  package_order["budget"] = budget_max

  print()
  
  #getting number and sex of snakes for package.
  while package_order['num_snakes'] == 0:
    try:
      package_order['males'] = int(input(f"How many males? "))
    except:
      print("Sorry, I didn't understand that. Make sure you're giving a number.")
    try:
      package_order['females'] = int(input(f"How many females? "))
    except:
      print("Sorry, I didn't understand that. Make sure you're giving a number.")
    
    if package_order['males'] == 0 and package_order['females'] == 0:
      print("Sorry, I can't build a package out of 0 snakes...")
    else:
      package_order['num_snakes'] = package_order['males'] + package_order['females']

  
  print()

  #getting traits to include
  print("Let's start picking traits. We're going to go through 3 options of traits to include and 1 option to exclude:\n")
  while len(all_snakes_have_traits) == 0 and len(at_least_one_traits)== 0 and len(in_the_pack_traits) == 0:
    #getting traits all animals should have
    include_traits_all = input("1. Are there any traits that EVERY snake MUST to have? Such as 'every snake is piebald' (Y/N) ")
    if include_traits_all.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        include_traits_all = input("Okay, which traits? (Example: 'lavender/yellow belly/clown') ")
        for trait in include_traits_all.split("/"):
          if trait in trait_stock and trait not in all_snakes_have_traits:
            all_snakes_have_traits.append(trait)
          else:
            print(f"Sorry, {trait} is not in stock.")
        more_traits = input("Were there any other traits all the snakes must have? (Y/N) ")
      package_order["all_snakes_traits"] = all_snakes_have_traits
    else:
      all_snakes_have_traits.append(None)
    
    print()

    #getting list of traits each animal should have at least one of from list
    include_traits_at_least_one = input("2. Are there any traits EVERY snake must have AT LEAST one of? Such as 'every snake is either lavender or het lavender' (Y/N) ")
    if include_traits_at_least_one.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        include_traits_at_least_one = input("Okay, which trait(s)? (Example: 'lavender/het lavender/66% het lavender/50% het lavender') ")
        for trait in include_traits_at_least_one.split("/"):
          if trait in trait_stock and trait not in at_least_one_traits:
            at_least_one_traits.append(trait)
          else:
            print(f"Sorry, {trait} is not in stock.")
        more_traits = input("Were there any other traits all the snakes must have at least one of? (Y/N) ")
      package_order["one_of_traits"] = at_least_one_traits
    else:
      at_least_one_traits.append(None)

    print()

    #getting traits that should be in the package but not every animal needs to have
    include_traits_pack = input("3. Are there any traits that MUST be included in the PACKAGE, but not every snake needs to have? Such as 'at least one pastel and one yellow belly' (Y/N) ")
    if include_traits_pack.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        include_traits_pack = input("Okay, what trait(s) do you want included in the package? (Example: pastel/black head/enchi) ")
        for trait in include_traits_pack.split("/"):
          if trait in trait_stock and trait not in in_the_pack_traits:
            in_the_pack_traits.append(trait)
          else:
            print(f"Sorry, {trait} is not in stock.")
        more_traits= input("Were there any other traits you want included in the package? (Y/N) ")
      package_order["pack_traits"] = in_the_pack_traits
    else:
      in_the_pack_traits.append(None)

  print()

  #getting traits to exclude
  while len(ex_traits) == 0:
    exclude = input("4. Are there any traits you do NOT want included in the package? Such as 'no snake will have spider' (Y/N) ")
    if exclude.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        exclude = input("What traits do you want to exclude? (Example: fire/black pastel/pet only) ")
        for trait in exclude.split("/"):
          if trait in trait_stock and trait not in in_the_pack_traits:
            ex_traits.append(trait)
          else:
            print(f"Great news, {trait} is not in stock. No need to worry about that one!")
        more_traits= input("Were there any other traits you want to exclude in the package? (Y/N) ")
      package_order["ex_traits"] = ex_traits
    else:
      ex_traits.append(None)
    
  print()

  #getting number of traits per snake
  trait_min = None
  trait_max = None
  while trait_count == None:
    trait_count_yes = input("Would you like to specify the number of traits in each snake? (Y/N) ")
    if trait_count_yes.upper() == "Y":
      while trait_min is None:
        try:
          trait_min = int(input("What is the minimum number of traits you would like to have? "))
        except:
          print("Sorry, your answer needs to be a number")
      trait_max_yes = input("Would you like to specify a maximum number of traits in each snake? (Y/N) ")
      if trait_max_yes.upper() == "Y":
        while trait_max is None:
          try:
            trait_max = int(input("What is the maximum number of traits you would like to have? ")) + 1
          except:
            print("Sorry, your answer needs to be a number")
      if trait_max != None:
        trait_count = range(trait_min, trait_max)
      else:
        trait_count = trait_min
      package_order["trait_count"] = trait_count
    else:
      break


#sorts LISTS of snakes by specified key in snake dict
def heapsort_snakes_by(list_to_sort, sort_by):
  sort = []
  max_heap = MaxHeap()
  for snake in list_to_sort:
    idx = snake[sort_by]
    max_heap.add(idx)
  while max_heap.count > 0:
    max_value = max_heap.retrieve_max()
    sort.insert(0, max_value)
  return sort


#arranges list of packages by most to least pack traits
def arrange_by_most_pack_traits(package_list_arrange):
  copy_list_to_arrange = package_list_arrange[:]
  num_packs = len(copy_list_to_arrange)
  max_packs = []
  while len(max_packs) != num_packs:
    max_traits = 0
    for pack in copy_list_to_arrange:
      if len(pack.package_traits) > max_traits:
        max_traits = len(pack.package_traits)
    for pack in copy_list_to_arrange:
      if len(pack.package_traits) == max_traits:
        max_packs.append(pack)
        copy_list_to_arrange.remove(pack)
  return max_packs


#arranges list of packages by overall value of included traits in each package
def arrange_by_highest_pack_trait_value(package_list_arrange):
  copy_list_to_arrange = package_list_arrange[:]
  num_packs = len(copy_list_to_arrange)
  max_value_packs = []
  while len(max_value_packs) != num_packs:
    max_value = 0
    for pack in copy_list_to_arrange:
      if pack.pack_trait_value > max_value:
        max_value = pack.pack_trait_value
    for pack in copy_list_to_arrange:
      if pack.pack_trait_value == max_value:
        max_value_packs.append(pack)
        copy_list_to_arrange.remove(pack)
  return max_value_packs


#arranges list of packages by lowest to highest price (used in 'shrink_to_specific' function in the case of too many possible options)
def arrange_by_price(package_list_arrange):
  copy_list_to_arrange = package_list_arrange[:]
  num_packs = len(copy_list_to_arrange)
  cheap_packs = []
  while len(cheap_packs) != num_packs:
    price_min = copy_list_to_arrange[0].price
    for pack in copy_list_to_arrange:
      if pack.price < price_min:
        price_min = pack.price
    for pack in copy_list_to_arrange:
      if pack.price == price_min:
        cheap_packs.append(pack)
        copy_list_to_arrange.remove(pack)
  return cheap_packs


#arranges list of packages by best overall, taking into account trait count and trait value
def arrange_by_best_overall_package(package_list_arrange):
  print("arranging by most pack traits...")
  best_trait_count = arrange_by_most_pack_traits(package_list_arrange)
  print(f"Best trait count package: ({best_trait_count[0].pack_trait_count}){best_trait_count[0].package_traits}, this package's trait value: {best_trait_count[0].pack_trait_value}\n")
  print("arranging by highest pack trait value...")
  best_value = arrange_by_highest_pack_trait_value(package_list_arrange)
  print(f"Best trait value package: ({best_value[0].pack_trait_count}){best_value[0].package_traits}, this package's trait value: {best_value[0].pack_trait_value}\n")
  #using index positions of packs in both best price and best traits to generate a "value" score for arranging packs by best overall
  idx_dict = {}
  print("Getting trait index...")
  for trait_pack in best_trait_count:
    trait_idx = best_trait_count.index(trait_pack)
    for value_pack in best_value:
      if value_pack == trait_pack:
        value_idx = best_value.index(value_pack)
    idx_key = trait_idx + value_idx
    if idx_key in idx_dict:
      while idx_key in idx_dict:
        idx_key += 1
    idx_dict[idx_key] = trait_pack
  #rearranging package list by overall best packages
  num_packs = len(package_list_arrange)
  best_packs = []
  print("Rearranging packs by best...")
  while len(best_packs) != num_packs:
    min_idx = min(idx_dict)
    best_packs.append(idx_dict[min_idx])
    idx_dict.pop(min_idx)
  print("Rearranging finished!")
  return best_packs


#only keeps packs with reasonably balanced snake prices, to avoid situations where most snakes in pack worth $1000+ and then a $75 snake thrown in with them
def balanced_snake_price_packs_only(package_list_to_cut):
  balanced_packs = []
  try:
    for pack in package_list_to_cut:
      min_reasonable_price = pack.price // ((len(pack.snakes) - 1) * 10)
      pack_balanced = True
      for snake in pack.snakes:
        if snake['Price'] < min_reasonable_price:
          pack_balanced = False
      if pack_balanced == True:
        balanced_packs.append(pack)
    if len(balanced_packs) > 1:
      return balanced_packs
    else:
      return package_list_to_cut
  except:
    return package_list_to_cut


#removes any snakes that do not fit the required sex (if any)
def cut_by_sex(list_to_cut):
  cut = []
  if package_order["females"] != 0:
    for snake in list_to_cut:
      if snake["Sex"] == "female":
        cut.append(snake)
  if package_order["males"] != 0:
    for snake in list_to_cut:
      if snake["Sex"] == "male":
        cut.append(snake)
  return cut


#removes any snakes that do not have traits requirements, works with "all_snake_traits", "one_of_traits", and "ex_traits"
def cut_by_trait(list_to_cut, trait_requirement):
  cut = []

  if trait_requirement == "all_snakes_traits":
    required_count = len(package_order["all_snakes_traits"])
    for snake in list_to_cut:
      required_count_have = 0
      for trait in package_order["all_snakes_traits"]:
        if trait in snake["Traits"]:
          required_count_have += 1
      if required_count_have == required_count: 
        cut.append(snake)

  elif trait_requirement == "one_of_traits":
    for snake in list_to_cut:
      for trait in snake["Traits"]:
        if trait in package_order["one_of_traits"] and snake not in cut:
          cut.append(snake)

  elif trait_requirement == "ex_traits":
    for snake in list_to_cut:
      exclude_snake = "N"
      for trait in package_order["ex_traits"]:
        if trait in snake["Traits"]:
          exclude_snake = "Y"
          break
      if exclude_snake == "N":
        cut.append(snake)
  
  return cut


#removes any snakes that do not have the required number of traits
def cut_by_trait_num(list_to_cut):
  cut = []
  #if only given min
  if type(package_order["trait_count"]) is int:
      for snake in list_to_cut:
        trait_count = 0
        for trait in snake["Traits"]:
          trait_count += 1
        if trait_count >= package_order["trait_count"]:
          cut.append(snake)
  #if given a min and max
  else:
    for snake in list_to_cut:
      trait_count = 0
      for trait in snake["Traits"]:
        trait_count += 1
      if trait_count in package_order["trait_count"]:
        cut.append(snake)
  return cut


#removes any snakes that are outside of budget, also returns min price for male and female packages
def cut_by_price(list_to_cut):
  package_possible = True
  
  #removing any male prices too expensive for package in individual sex list
  if package_order["males"] != 0:
    min_males = package_order["males"]
    male_price_list = heapsort_snakes_by(divide_sexes(list_to_cut)[0],"Price")
    one_male_short = 0
    for price in male_price_list[0:(min_males-1)]:
      one_male_short += price
    if one_male_short >= package_order["budget"]:
      print(f"Sorry, it looks like a package with {min_males} males is over your budget.")
      package_possible = False
    else:
      while one_male_short + male_price_list[-1] > package_order["budget"]:
        male_price_list.remove(male_price_list[-1])
      if len(male_price_list) < min_males:
        print(f"Sorry, it looks like a package with {min_males} males is over your budget.")
        package_possible = False
  
  #removing any female prices too expensive for package in individual sex list
  if package_order["females"] != 0:
    min_females = package_order["females"]
    female_price_list = heapsort_snakes_by(divide_sexes(list_to_cut)[1],"Price")
    one_female_short = 0
    for price in female_price_list[0:(min_females-1)]:
      one_female_short += price
    if one_female_short >= package_order["budget"]:
      print(f"Sorry, it looks like a package with {min_females} females is over your budget.")
      package_possible = False
    else:
      while one_female_short + female_price_list[-1] > package_order["budget"]:
        female_price_list.remove(female_price_list[-1])
      if len(female_price_list) < min_females:
        print(f"Sorry, it looks like a package with {min_females} females is over your budget.")
        package_possible = False
  
  #comparing male and female price lists against each other to remove any snakes outside budget when both sexes in package
  min_males_price = 0
  min_female_price = 0
  if package_possible == True:
    package_still_possible = True
    if package_order["males"] != 0 and package_order["females"] != 0:
      #checking females prices against min male group price, removing if out of budget
      for price in male_price_list[0:(min_males)]:
        min_males_price += price
      while min_males_price + female_price_list[-1] > package_order["budget"]:
        female_price_list.remove(female_price_list[-1])
      if len(female_price_list) < min_females:
        print(f"Sorry, it looks like a package with {min_females} females is over your budget.")
        package_still_possible = False
      #checking males prices against min female group price, removing if out of budget
      for price in female_price_list[0:(min_females)]:
        min_female_price += price
      while min_female_price + male_price_list[-1] > package_order["budget"]:
        male_price_list.remove(male_price_list[-1])
      if len(male_price_list) < min_males:
        print(f"Sorry, it looks like a package with {min_males} males is over your budget.")
        package_still_possible = False
    
    #removing any snakes with prices not in price lists 
    male_list = []
    female_list = []
    
    if package_order["males"] != 0:
      male_list = divide_sexes(list_to_cut)[0]
      for snake in male_list:
        if snake["Price"] not in male_price_list:
          male_list.remove(snake)
    if package_order["females"] != 0:      
      female_list = divide_sexes(list_to_cut)[1]
      for snake in female_list:
        if snake["Price"] not in female_price_list:
          female_list.remove(snake)
        
  if package_still_possible:
    return male_list, female_list, min_males_price, min_female_price
  else:
    return None


#divides snakes in list by sex, returning two lists: males, females
def divide_sexes(list_to_divide):
  males = []
  females = []
  for snake in list_to_divide:
    if snake["Sex"] == "male":
      males.append(snake)
    elif snake["Sex"] == "female":
      females.append(snake)
    else:
      continue
  return males, females


#cuts out any snakes that do not fit individual criteria for package and returns male and female lists,also returns minimum price for male and female packages
def cut_snakes():
  package_possible = True
  #removing any snakes that are not of desired sex (if any)
  if package_order["males"] == 0 or package_order["females"] == 0:
    try:
      cut1 = cut_by_sex(snakes)
      print(f"\nMaking cut, removing undesired sex. {len(cut1)} snakes in bag.")
    except:
      package_possible = False
  else:
    cut1 = snakes[:]
  
  #removing any snakes that do not have mandatory traits
  if package_order["all_snakes_traits"] != None and package_possible == True:
    cut2 = cut_by_trait(cut1,"all_snakes_traits")
    if len(cut2) == 0:
      print(f"Sorry, there aren't any available snakes with {package_order['all_snakes_traits']}\n")
      package_possible = False
    else:
      print(f"\nMaking cut, removing snakes that do not have required traits: {package_order['all_snakes_traits']}. {len(cut2)} snakes in bag.")
  else:
    cut2 = cut1[:]
  
  #removing snakes that do not have a trait from list of 'at least one' traits
  if package_order["one_of_traits"] != None and package_possible == True:
    cut3 = cut_by_trait(cut2, "one_of_traits")
    if len(cut3) == 0:
      print(f"Sorry, there aren't any available snakes left with {package_order['one_of_traits']}\n")
      package_possible = False
    else:
      print(f"\nMaking cut, removing snakes that do not have at least one of these traits: {package_order['one_of_traits']}. {len(cut3)} snakes in bag.")
  else:
    cut3 = cut2[:]
  
  #removing snakes that have a trait from the list 'ex_traits'
  if package_order["ex_traits"] != None and package_possible == True:
    cut4 = cut_by_trait(cut3, "ex_traits")
    if len(cut4) == 0:
      print(f"Sorry, there aren't any available snakes left that don't have one of these undesired traits: {package_order['ex_traits']}\n")
      package_possible = False
    else:
      print(f"\nMaking cut, removing snakes that have any of these undesired traits: {package_order['ex_traits']}. {len(cut4)} snakes in bag.")
  else:
    cut4 = cut3[:]
  
  #removing snakes that do not have desired number of traits
  if package_order["trait_count"] != None and package_possible == True:
    cut5 = cut_by_trait_num(cut4)
    if len(cut5) == 0:
      print(f"Sorry, there aren't any available snakes left that don't have the desired number of traits: {package_order['trait_count']}\n")
      package_possible = False
    else:
      print(f"\nMaking cut, removing snakes that do not have the desired number of traits: {package_order['trait_count']}. {len(cut5)} snakes in bag.")
  else:
    cut5 = cut4[:]
  
  #removing any remaining snakes that are too expensive for budget
  try:
    final_cut = cut_by_price(cut5)
    if final_cut != None and package_possible == True:
      males_list = final_cut[0]
      females_list = final_cut[1]
      min_male_package_price = final_cut[2]
      min_female_package_price = final_cut[3]
      print(f"\nRemoving snakes outside of budget and splitting by sex... {len(males_list)} males and {len(females_list)} females in bag.\n")
      return males_list,females_list, min_male_package_price, min_female_package_price
    else:
      return None
  except:
    return None


#shrinks list of packages if length specified
def shrink_to_specific(list_to_shrink, shrink_to_num):
  if len(list_to_shrink) > shrink_to_num:
    cut_by = (len(list_to_shrink) - shrink_to_num)
    arranged_price_list = arrange_by_price(list_to_shrink)
    shrunk_list = arranged_price_list[cut_by:]
    return shrunk_list
  else:
    return list_to_shrink


#finding all combos that fit count and budget constraits, converting each combo to a Ball_Python_Package
#functions 'balanced_snake_price_packs_only' and 'remove_doppelganger' used to cut out less desirable and near duplicate packs
def find_combos_lists_to_packs(snake_list, num_snakes, budget_cap):
  all_combos = []
  pos_combos = itertools.combinations(snake_list, num_snakes)
  list_combos = list(pos_combos)
  for combo in list_combos:
    combo_pack = Ball_Python_Package(snakes=combo)
    combo_pack.build_bp_package(combo)
    if combo_pack.price <= budget_cap:  
      all_combos.append(combo_pack)
  balanced_combos = balanced_snake_price_packs_only(all_combos)
  unique_combos = remove_doppelganger_packs(balanced_combos)
  return unique_combos


#In mixed sex packages, combines the male and female packages and returns a list of the packages that fit the budget and have the required traits in the package
#functions 'shrink_to_specific', 'balanced_snake_price_packs_only' and 'within_75_percent_budget' built in to cut out packages that are less than ideal
def find_balanced_combos(budget, combo_packs1, combo_packs2=None, include_in_package_traits = None):
  all_pack_combos = []
  shrunk_combos1 = shrink_to_specific(combo_packs1, 250)
  if combo_packs2 != None:
    shrunk_combos2 = shrink_to_specific(combo_packs2, 250)
    for combo1 in shrunk_combos1:
      for combo2 in shrunk_combos2:
        mf_combo_price = combo1.price + combo2.price
        if  mf_combo_price <= budget:
          combo = Ball_Python_Package(price=0, snakes=[], package_traits=[])
          combo.combine_bp_packages(combo1,combo2)
          if include_in_package_traits != None:
            traits_count = 0
            for trait in include_in_package_traits:
              if trait in combo.package_traits:
                traits_count +=1
            if traits_count == len(include_in_package_traits):
              all_pack_combos.append(combo)
          else:
            all_pack_combos.append(combo)
  else:
    for combo1 in shrunk_combos1:
      if include_in_package_traits != None:
        traits_count = 0
        for trait in include_in_package_traits:
          if trait in combo1.package_traits:
            traits_count +=1
        if traits_count == len(include_in_package_traits):
          all_pack_combos.append(combo1)
      else:
        all_pack_combos.append(combo1)
  balanced_combos = balanced_snake_price_packs_only(all_pack_combos)
  balanced_combos_75 = within_75_percent_budget(balanced_combos)
  balanced_combos_final = shrink_to_specific(balanced_combos_75, 50)
  return balanced_combos_final


#cuts out packs that are less than 75% of the budget
def within_75_percent_budget(package_list_to_cut):
  within_75_packages = []
  for pack in package_list_to_cut:
    if pack.price >= int(package_order["budget"] * 0.75):
      within_75_packages.append(pack)
  if len(within_75_packages) < 5:
    return package_list_to_cut
  else:
    return within_75_packages


#Removes near idential packs (such as when packs are same price and have all the same traits due to sibling snakes with identical traits)
def remove_doppelganger_packs(package_list_to_cut):
  copy_list_to_cut = package_list_to_cut[:]
  cut_list = []
  for pack in copy_list_to_cut:
    cut_list.append(pack)
    copy_list_to_cut.remove(pack)
    for other_pack in copy_list_to_cut:
      if pack.price == other_pack.price:
        if len(pack.package_traits) == len(other_pack.package_traits):
          traits_match = True
          for trait in pack.package_traits:
            if trait not in other_pack.package_traits:
              traits_match = False
        if traits_match == True:
          copy_list_to_cut.remove(other_pack)
  return cut_list

              


get_shop_stock()
in_stock_traits()
welcome_message()

#taking order and returning all possible snakes that fit requirements
possible_snakes = None
while possible_snakes == None:
  take_order()
  possible_snakes = cut_snakes()
  if possible_snakes == None:
    # in the case that the order is impossible to fill, resets package_order so no traits left in lists from previous attempt
    package_order = {"budget":None, "num_snakes":0, "discount":None, "females":0, "males":0, "all_snakes_traits":None, "one_of_traits":None, "pack_traits":None, "ex_traits":None, "trait_count":None}
    print("Let's try again. Are there any requirements you could lower or do without?\n")
possible_males = possible_snakes[0]
possible_females = possible_snakes[1]
min_male_pack_price = possible_snakes[2]
min_female_pack_price = possible_snakes[3]

#getting possible packages for males and/or females based on package order
if package_order['males'] > 0:
  possible_male_combos = find_combos_lists_to_packs(possible_males, package_order['males'], (package_order['budget']-min_female_pack_price))
  print(f"Found {len(possible_male_combos)} possible male combos.")
if package_order['females'] > 0:
  possible_female_combos = find_combos_lists_to_packs(possible_females, package_order['females'],(package_order['budget']-min_male_pack_price))
  print(f"Found {len(possible_female_combos)} possible female combs.")

#calculating final packages for orders that contain both males and females
if package_order['males'] > 0 and package_order['females'] > 0:
  print("Combining male and female combos...")
  possible_male_and_female_combos = find_balanced_combos(package_order['budget'], possible_male_combos, possible_female_combos, package_order['pack_traits'])
  print(f"{len(possible_male_and_female_combos)} possible male/female combos")
  by_best_pack = arrange_by_best_overall_package(possible_male_and_female_combos)
#calculating final packages for orders that contain only males
elif package_order['males'] > 0:
  print("\nFinding best overall male packages...")
  just_males = find_balanced_combos(package_order['budget'], possible_male_combos, package_order['pack_traits'])
  by_best_pack = arrange_by_best_overall_package(just_males)
#calculating final packages for orders that contain only females
else:
  print("\nFinding best overall female packages...")
  just_females = find_balanced_combos(package_order['budget'], possible_female_combos, package_order['pack_traits'])
  by_best_pack = arrange_by_best_overall_package(just_females)

#reducing to top 3 packages
if len(by_best_pack) >= 3:
  top_overall_packs = by_best_pack[:3]
else:
  top_overall_packs = by_best_pack


print("\n----------------------------")
print(f"Top {len(top_overall_packs)} Best Overall Packages:")
print("----------------------------\n")
count = 1
for pack in top_overall_packs:
  print(f"Pack {count}: Price: ${pack.price}0   Number of Unique Traits: {len(pack.package_traits)}")
  count += 1
  for snake in pack.snakes:
    print(f"        {snake['Animal_Id*']}: {snake['Title*']}   Price: ${snake['Price']}0")
  print()




  #return (up to) top 3 lists:
    #overall best package
    #lowest price package
    #highest trait count package
  #user selects which package they want, prints out all the snakes that make up that package (in a nice format)


  #need to add:
  #auto-complete/correct in the case the user enters traits that do not match list
    #goes through letter by letter to give user options that they might have meant

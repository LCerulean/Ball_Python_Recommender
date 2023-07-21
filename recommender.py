import json
from max_heap import MaxHeap 
from bp_package_class import Ball_Python_Package

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
  with open('animals.json') as raw_data:
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
              if traits_split[count] == "50%" or traits_split[count] == "66%":
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
    if trait.find("lavender") >= 0 or trait.find("piebald") >= 0 or trait.find("clown") >= 0:
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
The purpose of this program is to aid you in picking the best snake(s)
for your budget and project from the Crescent Serpents shop.

Options you can pick from include:
-Number of snakes in package: specific number or range (min and max)
-Sex: males, females, or both (and the ratio of males/females if both)
-Traits to include/exclude: in package or in each animal
-Trait count minimum: in package or in each animal
  """
  print(welcome)
  see_traits = input("Would you like to see a list of traits currently in stock? (Y/N) ")
  print()
  if see_traits.upper() == "Y":
    categorized_in_stock_traits()
  print("\nLet's get started!")


#gets the parameters from user and puts them in the package_order dictionary
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
    budget = input("\nWhat is your maximum budget? (Minimum of $50) ")
    try:
      budget = int(budget)
      if (budget) >= 50:
        budget_max = budget
      else:
        print("Sorry, you're budget range is too small.")
    except:
      print("Sorry, I didn't understand that. Make sure you're not using extra symbols or spaces.")
  package_order["budget"] = budget_max
  print(f"\nGot it, budget ${budget}\n")
  
  #getting number of snakes
  while num_snakes == 0:
    count = 0
    for snake in snakes:
      count += 1
    try:
      num_snakes = int(input("How many snakes are you looking for? "))
      if num_snakes <= count:
        package_order["discount"] = discounts[num_snakes]
        print(f"\nGot it, you are looking for {num_snakes} snakes.\n")
      else:
        print("Sorry, there aren't enough snakes in stock.")
    except:
      print("Sorry, I didn't understand that. Make sure you're giving a number.")
  package_order["num_snakes"] = num_snakes
  
  #getting sex/ratio of snakes
  while sex == None:
    sex_type = input("Are you looking for males, females, or both? ")
    if sex_type.lower() == "females" or sex_type.lower() == "males":
      sex = sex_type.lower()
      package_order[sex] = num_snakes
      print(f"\nGot it, package will be made up of only {sex}.\n")
    elif sex_type.lower() == "both":
      try:
        num_males = int(input(f"Okay, out of {num_snakes} snakes, how many do you want to be males? "))
        package_order["males"] = num_males
        package_order["females"] = num_snakes - num_males
        print(f"\nGot it, {package_order['males']} males and {package_order['females']} females.\n")
        sex = "both"
      except:
          print("Sorry, I didn't understand that. Make sure you're giving a number.")
    else:
      print("Sorry, that's not an option. Please type 'males' 'females' or 'both'.")
  
  #getting traits to include
  print("Let's start picking traits. We're going to go through 3 options:\n-Traits EVERY snake MUST have (Example: every snake is lavender)\n-Traits that EVERY snake must have AT LEAST one of (Example: every snake should be lavender or het lavender)\n-Traits not every snake needs to have, but should be in the package (Example: one or more of the snakes should have pastel, fire, or yellow belly)\n")
  while len(all_snakes_have_traits) == 0 and len(at_least_one_traits)== 0 and len(in_the_pack_traits) == 0:
    include_traits_all = input("Are there any traits that you want EVERY snake to have? (Y/N) ")
    if include_traits_all.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        include_traits_all = input("Okay, what trait(s) do you want ALL the snakes to have? (Example: 'lavender/yellow belly/clown') ")
        for trait in include_traits_all.split("/"):
          if trait in trait_stock and trait not in all_snakes_have_traits:
            all_snakes_have_traits.append(trait)
          else:
            print(f"Sorry, {trait} is not in stock.")
        more_traits = input("Were there any other traits you want ALL the snakes to have? (Y/N) ")
      package_order["all_snakes_traits"] = all_snakes_have_traits
      print(f"\nGot it, all the snakes in the package will have each of these traits: {all_snakes_have_traits}\n")
    else:
      all_snakes_have_traits.append(None)
      print("\nGot it, no specific traits that each snake needs to have.\n")
      
    include_traits_at_least_one = input("Are there any traits you want all the snakes to have at least one of? (Y/N) ")
    if include_traits_at_least_one.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        include_traits_at_least_one = input("Okay, what trait(s) do you want all the snakes to have at least one of? (Example: 'lavender/het lavender/66% het lavender/50% het lavender') ")
        for trait in include_traits_at_least_one.split("/"):
          if trait in trait_stock and trait not in at_least_one_traits:
            at_least_one_traits.append(trait)
          else:
            print(f"Sorry, {trait} is not in stock.")
        more_traits = input("Were there any other traits you want all the snakes to have at least one of? (Y/N) ")
      package_order["one_of_traits"] = at_least_one_traits
      print(f"\nGot it, all the snakes in the package will have at least one of these traits: {at_least_one_traits}\n")
    else:
      at_least_one_traits.append(None)
      print("\nGot it, no specific traits that each snake to have at least one of.\n")  

    include_traits_pack = input("Okay, were there any traits would you like included in the package but not every snake needs to have? (Y/N) ")
    if include_traits_pack.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        include_traits_pack = input("Okay, what trait(s) do you want included in the package? (Example: pastel/black head/clown/lavender) ")
        for trait in include_traits_pack.split("/"):
          if trait in trait_stock and trait not in in_the_pack_traits:
            in_the_pack_traits.append(trait)
          else:
            print(f"Sorry, {trait} is not in stock.")
        more_traits= input("Were there any other traits you want included in the package? (Y/N) ")
      package_order["pack_traits"] = in_the_pack_traits
      print(f"\nGot it, the package should include these traits: {in_the_pack_traits}\n")
    else:
      in_the_pack_traits.append(None)
      print("\nGot it, no specific traits to include in the package.\n")

  #getting traits to exclude
  while len(ex_traits) == 0:
    exclude = input("Are there any traits you do NOT want included in the package? (Y/N) ")
    if exclude.upper() == "Y":
      more_traits = "Y"
      while more_traits.upper() == "Y":
        exclude = input("What traits do you want to exclude? (Example: fire/black pastel/pet only) ")
        for trait in exclude.split("/"):
          if trait in trait_stock and trait not in in_the_pack_traits:
            ex_traits.append(trait)
          else:
            print(f"{trait} is not in stock, so no need to worry about that one!")
        more_traits= input("Were there any other traits you want to exclude in the package? (Y/N) ")
      package_order["ex_traits"] = ex_traits
      print(f"\nGot it, no snake in the package will have any of these traits: {ex_traits}\n")
    else:
      ex_traits.append(None)
      print("\nGot it, no excluded traits in the package.\n")
    
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
      if trait_max == None:
        print(f"\nGot it, only snakes with at least {trait_count} traits will be included.\n")
      else:
        print(f"\nGot it, only snakes with {trait_min}-{trait_max - 1} traits will be included.\n")
    else:
      break

    #return this in a dictionary?


#will use to sort lists when needed
def heapsort_snakes(list_to_sort, sort_by):
  sort = []
  max_heap = MaxHeap()
  for snake in list_to_sort:
    idx = snake[sort_by]
    max_heap.add(idx)
  while max_heap.count > 0:
    max_value = max_heap.retrieve_max()
    sort.insert(0, max_value)
  return sort


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


#removes any snakes that are outside of budget
def cut_by_price(list_to_cut):
  cut_lists = []
  package_possible = True
  
  #removing any male prices too expensive for package in individual sex list
  if package_order["males"] != 0:
    min_males = package_order["males"]
    male_price_list = heapsort_snakes(divide_sexes(list_to_cut)[0],"Price")
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
    female_price_list = heapsort_snakes(divide_sexes(list_to_cut)[1],"Price")
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
  if package_possible == True:
    package_still_possible = True
    if package_order["males"] != 0 and package_order["females"] != 0:
      #checking females prices against min male group price, removing if out of budget
      min_males_price = 0
      for price in male_price_list[0:(min_males)]:
        min_males_price += price
      while min_males_price + female_price_list[-1] > package_order["budget"]:
        female_price_list.remove(female_price_list[-1])
      if len(female_price_list) < min_females:
        print(f"Sorry, it looks like a package with {min_females} females is over your budget.")
        package_still_possible = False
      #checking males prices against min female group price, removing if out of budget
      min_female_price = 0
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
    return male_list, female_list
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


#cuts out any snakes that do not fit individual criteria for package
def cut_snakes():
  package_possible = True
  #removing any snakes that are not of desired sex (if any)
  if package_order["males"] == 0 or package_order["females"] == 0:
    try:
      cut1 = cut_by_sex(snakes)
      print(f"\nMaking cut, removing undesired sex. {len(cut1)} snakes in bag.\n")
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
      print(f"\nMaking cut, removing snakes that do not have required traits: {package_order['all_snakes_traits']}. {len(cut2)} snakes in bag.\n")
  else:
    cut2 = cut1[:]
  
  #removing snakes that do not have a trait from list of 'at least one' traits
  if package_order["one_of_traits"] != None and package_possible == True:
    cut3 = cut_by_trait(cut2, "one_of_traits")
    if len(cut3) == 0:
      print(f"Sorry, there aren't any available snakes left with {package_order['one_of_traits']}\n")
      package_possible = False
    else:
      print(f"\nMaking cut, removing snakes that do not have at least one of these traits: {package_order['one_of_traits']}. {len(cut3)} snakes in bag.\n")
  else:
    cut3 = cut2[:]
  
  #removing snakes that have a trait from the list 'ex_traits'
  if package_order["ex_traits"] != None and package_possible == True:
    cut4 = cut_by_trait(cut3, "ex_traits")
    if len(cut4) == 0:
      print(f"Sorry, there aren't any available snakes left that don't have one of these undesired traits: {package_order['ex_traits']}\n")
      package_possible = False
    else:
      print(f"\nMaking cut, removing snakes that have any of these undesired traits: {package_order['ex_traits']}. {len(cut4)} snakes in bag.\n")
  else:
    cut4 = cut3[:]
  
  #removing snakes that do not have desired number of traits
  if package_order["trait_count"] != None and package_possible == True:
    cut5 = cut_by_trait_num(cut4)
    if len(cut5) == 0:
      print(f"Sorry, there aren't any available snakes left that don't have the desired number of traits: {package_order['trait_count']}\n")
      package_possible = False
    else:
      print(f"\nMaking cut, removing snakes that do not have the desired number of traits: {package_order['trait_count']}. {len(cut5)} snakes in bag.\n")
  else:
    cut5 = cut4[:]
  
  #removing any remaining snakes that are too expensive for budget
  try:
    final_cut = cut_by_price(cut5)
    if final_cut != None and package_possible == True:
      males_list = final_cut[0]
      females_list = final_cut[1]
      print(f"\nMaking final cut, removing snakes outside of budget... Splitting by sex... {len(males_list)} males and {len(females_list)} females in bag.\n")
      return males_list,females_list
    else:
      return None
  except:
    return None
  
  

get_shop_stock()
in_stock_traits()
welcome_message()

possible_snakes = None
while possible_snakes == None:
  take_order()
  possible_snakes = cut_snakes()
  if possible_snakes == None:
    #reset package_order so no traits left in lists from previous attempt
    package_order = {"budget":None, "num_snakes":0, "discount":None, "females":0, "males":0, "all_snakes_traits":None, "one_of_traits":None, "pack_traits":None, "ex_traits":None, "trait_count":None}
    print("Let's try again. Are there any requirements you could lower or do without?\n")
possible_males = possible_snakes[0]
possible_females = possible_snakes[1]



#multiple functions needed:
  #each package a node
    #if both males and females, build all possible packages that fit budget, then combine male/female packages in all possible packages that fit budget
    #remove all packages that do not fit "include in package traits" (if none, keep packages that are closest to fitting requirement)
  #sort packages by:
    #package price, lowest to highest
    #trait count, highest to lowest
  #new sort, but new index is sum of index of package in the two previous sorts, lowest index is the best package
  #return 3 lists:
    #overall best package
    #lowest price package
    #highest trait count package
  #user selects which package they want, prints out all the snakes that make up that package (in a nice format)

import json

#should allow input of shop link
#builds a recommended group of ball pythons for purchase based on:
  # age/maturity
  # genes wanted (option for either all animals have said gene, or just want gene somewhere in the package)
  # genes NOT wanted
  # gene count
  # snake count
  # sex -can be split male/female with specific amounts or ratios, or just all
  # individual price or budget
  # take into account shipping price and store discounts


snakes = []
trait_stock = []
package_order = {"budget":None, "num_snakes":None, "females":None, "males":None, "sex_ratio":None, "all_snakes_traits":None, "one_of_traits":None, "pack_traits":None, "ex_traits":None, "trait_count":None}

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
              #joining percents with hets  and their corrisponding trait in single string
              if traits_split[count] == "50%" or traits_split[count] == "66%":
                trait = traits_split[count] + " " + traits_split[count+1] + " " + traits_split[count+2]
                #skipping "albino" in the case of finding lavender, lavender is assumed albino
                if traits_split[count+2] == "lavender":
                  count +=1
                count += 2
                traits_list.append(trait)
                if count >= len(traits_split):
                  break

              #joinging 100% hets with corrisponding trait in single string  
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

  #seperates recessive and codominant traits and puts recessive traits in a better order for display
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

#gets the parameters from user and puts them in the package order dictionary
def take_order():
  
  budget_range = None
  num_snakes = None

  sex = None
  num_males = None
  sex_ratio = None

  all_snakes_have_traits = []
  at_least_one_traits = []
  in_the_pack_traits = []
  ex_traits = []
  trait_count = None

  #getting budget
  while budget_range == None:
    budget = input("Let's get started!\nWhat is your budget? Write it as a range, such as '150-200'\n(recommended minimum range of $50) ")
    try:
      budget_range = range(int(budget.split("-")[0]),int(budget.split("-")[-1]))
    except:
      print("Sorry, I didn't understand that. Make sure you're not using extra symbols or spaces.")
  package_order["budget"] = budget_range
  print(f"\nGot it, budget {budget_range}\n")
  
  #getting number of snakes
  while num_snakes == None:
    num_snakes_type = input("Are you looking for a specific number of snakes, or a range? (specific/range) ")
    if num_snakes_type.lower() == "specific":
      try:
        num_snakes = int(input("Okay, what is the specific number you are looking for? "))
      except:
        print("Sorry, I didn't understand that. Make sure you're giving a number.")
    elif num_snakes_type.lower() == "range":
      num_snakes = input("Okay, what is the min and max number of snakes you are looking for? (Example: '2-3') ")
      try:
        num_snakes = range(int(num_snakes.split("-")[0]),int(num_snakes.split("-")[-1]))
      except:
        print("Sorry, I didn't understand that. Make sure you're not using extra symbols or spaces.")
    else:
      print("Sorry, I didn't understand that.")
  package_order["num_snakes"] = num_snakes
  print(f"\nGot it, you are looking for {num_snakes} snakes.\n")

  #getting sex/ratio of snakes
  while sex == None and num_males == None and sex_ratio == None:
    sex_type = input("Are you looking for males, females, or both? ")
    if sex_type.lower() == "females" or sex_type.lower() == "males":
      sex = sex_type.lower()
      package_order[sex] = num_snakes
      print(f"\nGot it, package will be made up of only {sex}.\n")
    elif sex_type.lower() == "both":
      if type(num_snakes) == int:
        try:
          num_males = int(input(f"Okay, out of {num_snakes} snakes, how many do you want to be males? "))
          package_order["males"] = num_males
          package_order["females"] = num_snakes - num_males
          print(f"\nGot it, {num_males} males and {num_snakes - num_males} females.\n")
        except:
          print("Sorry, I didn't understand that. Make sure you're giving a number.")
      else:
        sex_count = input("Okay, what ratio of males/females are you looking for? (Example: '2/3') ")
        try:
          sex_ratio = range(int(sex_count.split("/")[0]),int(sex_count.split("/")[-1]))
          package_order["sex_ratio"] = sex_ratio
          print(f"\nGot it, {sex_count.split('/')[0]} males to {sex_count.split('/')[-1]} females.\nIf we can't hit that ratio exactly then we will try to get it as close as possible.\n")
        except:
          print("Sorry, I didn't understand that. Make sure you're not using extra symbols or spaces.")
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

    include_traits_pack = input("Okay, were there any traits you want included in the package but not each snake needs to have? (Y/N) ")
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
        more_traits= input("Were there any other traits you want exclude in the package? (Y/N) ")
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
            trait_max = int(input("What is the maximum number of traits you would like to have? "))
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
        print(f"\nGot it, only snakes with {trait_count} traits will be included.\n")
    else:
      break

    #return this in a dictionary?
       
#does the thing, makes the magic happen, gives the user best option       
def bag_of_snakes(snakes, order):
  pass
    #multiple functions needed:
      # -each Python is a node?
      # -stack? multiple stacks? finding best "route"?
      #   -split male/female first (for each, if include excluded genes, wrong number of genes, or over budget, skip)
      #   -stack for price (order least to most)
      #   -stack for gene count (order most to least)
      # -goes through the price and gene stack to find best package deal


get_shop_stock()
in_stock_traits()
welcome_message()
take_order()

print(f"Package order: {package_order}")
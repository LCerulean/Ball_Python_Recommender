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
  all_traits = trait_stock
  recessive_traits = []
  codominant_traits = []
  
  #seperates recessive and codominant traits and puts recessive traits in a better order for display
  for trait in all_traits:
    if trait == "lavender" or trait == "piebald" or trait == "clown":
      recessive_traits.append(trait)
      all_traits.remove(trait)
  for trait in all_traits:
    if trait[:3] == "het":
      recessive_traits.append(trait)
      all_traits.remove(trait)
  for trait in all_traits:
    if trait[2] == '%':
      recessive_traits.append(trait)
      all_traits.remove(trait)
  for trait in all_traits:
    codominant_traits.append(trait)
    
  list_len_diff = max(len(recessive_traits), len(codominant_traits)) - min(len(recessive_traits), len(codominant_traits))
  if len(recessive_traits) < len(codominant_traits):
    for num in range(list_len_diff):
      recessive_traits.append("")
  elif len(recessive_traits) > len(codominant_traits):
    for num in range(list_len_diff):
      codominant_traits.append("")
  else:
    pass
      
    
  #formats and prints the categorized traits
  formatted_traits = "RECESSIVE TRAITS     CODOMINANT TRAITS\n"
  list_len_max = max(len(recessive_traits), len(codominant_traits))
  idx = 0
  for num in range(list_len_max):
    formatted_traits += recessive_traits[idx] + "     " + codominant_traits[idx] + "\n"
    idx += 1
  print(formatted_traits)
  

#graphics display, welcome, list of things it can do
def welcome_message():
  pass
    #Opening message

#gets the parameters from user
def take_order():
  pass
    #input on:
    # -budget range (min range of 50)
    # -number of snakes: specific number or max
    # -males/females/both
    #   -if both, what ratio
    # -specific genes to include (if any)
    #   -if yes, should any of these genes be present in ALL animals
    # -specific genes to exclude (if any)
    # -specific gene count (written as "=< x" or "=> x") if any
    # -priority: most for money, greatest gene diversity
    
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
# for snake in snakes:
#   print(snake)
print(in_stock_traits())
categorized_in_stock_traits()
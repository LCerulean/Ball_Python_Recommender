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

#pulls data from web, converts to desired format using Python class, writes data to the shop_data file
def format_shop_stock():
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
              #checking if trait is two words, if so joining into single string before appending list
              ## NOT joining hets or percents with traits, leaving seperate for search
              if traits_split[count] == "black" or traits_split[count] == "yellow" or traits_split[count] == "lavender" or traits_split[count] == "pet":
                trait = traits_split[count] + " " + traits_split[count+1]
                traits_list.append(trait)
                #skipping 2nd half of two word trait in next loop through traits_split
                count += 1
                if count >= len(traits_split):
                  break
              else:
                traits_list.append(traits_split[count])
              count += 1

            snake_info["Traits"] = traits_list
          else:
          #copying relevant info from json file for each snake and putting it in list
            snake_info[key] = snake_data[key]
        
        snakes.append(snake_info)
  return snakes
    

def get_in_stock_traits():
  in_stock = []
  for snake in snakes:
    for trait in snake["Traits"]:
      if trait != "het" and trait != "50%" and trait != "66%":
        if trait not in in_stock:
          in_stock.append(trait)
  return in_stock


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


format_shop_stock()
print(get_in_stock_traits())

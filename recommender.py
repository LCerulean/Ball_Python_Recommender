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
def download_snakes():
  #asks user input for link
  #checks if can connect to link, returns error if not

  #convert to read and write to shop_data file, each snake on it's own line
  with open('animals.json') as raw_data:
    shop_data = json.load(raw_data) #type is list, indicies are dictionaries
    # print(shop_data)
    print(type(shop_data[0]))
    

#takes the snake data and uses Python class to create instances for each one in the shop, then adds to snakes list
def format_snakes(file):
  pass
    #open file in read
    #loop through each line, making Python instance for each
      #add in all the data for the snake
      #add the Python to the snakes list

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


download_snakes()
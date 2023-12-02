# Ball_Python_Recommender
This project started as a portfolio project for Codecademy's Computer Science Career Path. The goal of this project was to "build a basic recommendation program for a topic of your choice."  I chose, rather than going "basic", to built something that would return optimal recommendations and that I could actually make use of in my small business.

## Purpose and Use:
The purpose of this program is to aid ball python breeders using the MorphMarket platform in putting together the best groups for customers based on their budget, desired traits, and number of snakes in a time efficient manner.  This program by default is using an example inventory file from the _Crescent Serpents_ MorphMarket shop (it is not current, the shop is now closed).


__To use your own MorphMarket shop file:__  
-Log into MorphMarket and right click the screen. Select 'view page source'.  
-Locate the downloadable json file for your shop (ctrl + f and type json).  
-Download the file into the 'Ball Python Recommender' folder as 'animals.json'  
-Give it a test!  
-NOTE: Only traits I was working with are included. To add more recessive traits, add the trait name to "*trait_type_dict*" on line 6 of the recommender.  If adding a trait that is made up of two words and does not start with "black" or "yellow" (already covered), you must add the starting word into the function: "*convert_snake_traits_to_list*" on line 90 in the bp_classes file (in the same format as the others listed in that line).

## What the Program Can Do:
-Built groups of ball pythons from the shop based on a given budget and return the top 3 groups.  
-Include specific numbers of males and females in the group.  
-Trait Selection Options:  
    ---Choose traits that ALL the snakes must have.  
    ---Choose traits that snakes must have AT LEAST one of.  
    ---Choose traits that must be in the final package but not every snake needs to have.  
    ---Choose traits to exclude from the package.  
-If in choosing a trait the user misspells the trait name, the program will attempt to spell check and return the closest match from the traits in stock.  

## How Trait Value is Assigned:
-Visual recessives are given the highest value (4) due to the fact they hold their value better and take more work to make (if starting with hets).  
-100% hets and supers are next highest (3) due to the fact they can produce visual recessives.  
-Codominant traits are in the middle (2).  
-50% and 66% hets are given lower value (1) since they run the risk of not actually carrying the trait.  
-Non-genetic traits, such as paradox are given no value (0), because although some collectors and pet owners will want them for their unique look, they are not able (or unlikely) to pass on the trait.  As this program is designed for packages, it is assumed a fellow breeder is the buyer, in which case the abililty to pass on the trait is important.  
-Defects, such as small kinks that would have a snake labeled as "pet only" are assigned a negative value (-1).
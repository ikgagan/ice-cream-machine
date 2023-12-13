
from enum import Enum
# make a tests folder under the folder you're putting these files in
# add an empty __init__.py to the tests folder
from IcecreamExceptions import ExceededRemainingChoicesException, InvalidChoiceException, NeedsCleaningException, OutOfStockException, InvalidPaymentException, InvalidCombinationException, NoItemChosenException
class Usable:
    name = ""
    quantity = 0
    cost = 99

    def __init__(self, name, quantity = 10, cost=99):
        self.name = name
        self.quantity = quantity
        self.cost = cost

    def use(self):
        self.quantity -= 1
        if (self.quantity < 0):
            raise OutOfStockException
        return self.quantity 

    def in_stock(self):
        return self.quantity > 0

class Container(Usable):
    pass

class Flavor(Usable):
    pass

class Toppings(Usable):
    pass

class STAGE(Enum):
    Container = 1
    Flavor = 2
    Toppings = 3
    Pay = 4

class IceCreamMachine:
    # Constants https://realpython.com/python-constants/
    USES_UNTIL_CLEANING = 100
    MAX_SCOOPS = 3
    MAX_TOPPINGS = 3


    containers = [Container(name="Waffle Cone", cost=1.5), Container(name="Sugar Cone", cost=1), Container("Cup", cost=1)]
    flavors = [Flavor(name="Vanilla", quantity=100, cost=1), Flavor(name="Chocolate", quantity=100, cost=1), Flavor(name="Strawberry", quantity=100, cost=1)]
    toppings = [Toppings(name="Sprinkles", quantity=200, cost=.25), Toppings(name="Chocolate Chips", quantity=200, cost=.25), Toppings(name="M&Ms", quantity=200, cost=.25), \
    Toppings(name="Gummy Bears", quantity=200, cost=.25), Toppings(name="Peanuts", quantity=200, cost=.25)] 


    # variables
    remaining_uses = USES_UNTIL_CLEANING
    remaining_scoops = MAX_SCOOPS
    remaining_toppings = MAX_TOPPINGS
    total_sales = 0
    total_icecreams = 0

    inprogress_icecream = []
    currently_selecting = STAGE.Container

    # rules
    # 1 - container must be chosen first
    # 2 - can only use items if there's quantity remaining
    # 3 - scoops can't exceed max
    # 4 - toppings can't exceed max
    # 5 - a container and at least 1 scoop or toppings must be selected
    # 6 - proper cost must be calculated and shown to the user
    # 7 - cleaning must be done after certain number of uses before any more icecreams can be made
    # 8 - total sales should calculate properly based on cost calculation
    # 9 - total_icecreams should increment properly after a payment
    

    def pick_container(self, choice):
        for c in self.containers:
            # Gagan Indukala Krishna Murthy - gi36 - 1st March 2023
            # added lower to take input as caps and not give a error
            if c.name.lower() == choice.lower():
                c.use()
                self.inprogress_icecream.append(c)
                return
        raise InvalidChoiceException

    def pick_flavor(self, choice):
        if self.remaining_uses <= 0:
            raise NeedsCleaningException
        if self.remaining_scoops <= 0:
            raise ExceededRemainingChoicesException
        for f in self.flavors:
            # Gagan Indukala Krishna Murthy - gi36 - 1st March 2023
            # added lower to take input as caps and not give a error
            if f.name.lower() == choice.lower():
                f.use()
                self.inprogress_icecream.append(f)
                self.remaining_scoops -= 1
                self.remaining_uses -= 1
                return
        raise InvalidChoiceException

    def pick_toppings(self, choice):
        if self.remaining_toppings <= 0:
            raise ExceededRemainingChoicesException
        for t in self.toppings:
            # Gagan Indukala Krishna Murthy - gi36 - 1st March 2023
            # added lower to take input as caps and not give a error
            if t.name.lower() == choice.lower():
                t.use()
                self.inprogress_icecream.append(t)
                self.remaining_toppings -= 1
                return
        raise InvalidChoiceException

    def reset(self):
        self.remaining_scoops = self.MAX_SCOOPS
        self.remaining_toppings = self.MAX_TOPPINGS
        self.inprogress_icecream = []
        self.currently_selecting = STAGE.Container

    def clean_machine(self):
        self.remaining_uses = self.USES_UNTIL_CLEANING
        
    def handle_container(self, container):
        self.pick_container(container)
        self.currently_selecting = STAGE.Flavor

    def handle_flavor(self, flavor):
        if not self.inprogress_icecream:
            raise InvalidCombinationException
        elif flavor == "next":
            self.currently_selecting = STAGE.Toppings
        else:
            self.pick_flavor(flavor)

    def handle_toppings(self, toppings):
        if not self.inprogress_icecream:
            raise InvalidCombinationException
        if toppings == "done" and any(item in self.flavors + self.toppings for item in self.inprogress_icecream):
            self.currently_selecting = STAGE.Pay
        elif toppings == "done":
            raise NoItemChosenException
        else:
            self.pick_toppings(toppings)

    def handle_pay(self, expected, total):
        if total == f"{expected:.2f}":
            print("Thank you! Enjoy your icecream!")
            self.total_icecreams += 1
            self.total_sales += expected # only if successful
            self.reset()
        else:
            raise InvalidPaymentException
            
    def calculate_cost(self):
        # Gagan Indukala Krishna Murthy - gi36 - 1st March 2023
        # Summary: Keeping cost initially as zero
        self.cost = 0
        # adding the input item cost from the user in a loop for ever input of items.
        for item in self.inprogress_icecream:
            self.cost += item.cost
        return round(self.cost, 2) # round the numbers after decimal

    def run(self):
        try:
            if self.currently_selecting == STAGE.Container:
                # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                container = input(f"Would you like a {', '.join(list(map(lambda c:c.name.lower(), filter(lambda c: c.in_stock(), self.containers))))}?\n")
                self.handle_container(container)
            elif self.currently_selecting == STAGE.Flavor:
                flavor = input(f"Would you like {', '.join(list(map(lambda f:f.name.lower(), filter(lambda f: f.in_stock(), self.flavors))))}? Or type next.\n")
                try:
                    self.handle_flavor(flavor)
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary: If the flavor is exceeded more than 3 then we are automatically going to the next stage after displaying line 176 as output to the user
                    # Changed to toppings stage
                except ExceededRemainingChoicesException:
                    print("Sorry! You've exceeded the maximum number of flavors that you can select, please choose a topping")
                    self.currently_selecting = STAGE.Toppings
            elif self.currently_selecting == STAGE.Toppings:
                toppings = input(f"Would you like {', '.join(list(map(lambda t:t.name.lower(), filter(lambda t: t.in_stock(), self.toppings))))}? Or type done.\n")
                try:
                    self.handle_toppings(toppings)
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary:If the toppings is exceeded more than 3 then we are automatically going to the next stage after displaying line 187 as output to the user
                    # Changed to displaying the total cost stage and getting paid from the user
                except ExceededRemainingChoicesException:
                    print("Sorry! You've exceeded the maximum number of toppings; proceeding to the payment portal")
                    self.currently_selecting = STAGE.Pay
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary: If there is no flavours or toppings choosen then NoItemChosenException will be executed and we are redirecting to the flavour stage
                except NoItemChosenException:
                    print("Please choose at least one scoop or topping.")
                    self.currently_selecting = STAGE.Flavor
            elif self.currently_selecting == STAGE.Pay:
                expected = self.calculate_cost()
                total = input(f"Your total is ${expected:.2f}, please enter the exact value.\n")
                try:
                    self.handle_pay(expected, total)
                    # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
                    # Summary: If the amount entered by  the user doesnot match the total amount line 203 will be printed.
                    # user will be given another change to enter the right amount
                except InvalidPaymentException:
                    print("You've entered a wrong amount. Please try again :)")
                    self.run()
                choice = input("What would you like to do? (icecream or quit)\n")
                if choice == "quit":
                    exit()
        # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
        # Summary: If any of the above input items from the user is out of stock then line 212
        # and the user will be redirected to select differnt items
        except OutOfStockException:
            print("The selected option is out of stock. Please select another option")
        # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
        # Summary: If the USES_UNTIL_CLEANING exceed 100 then the user will be promted with line 217 as the output
        # when the user types "yes" then the line 219 is shown as the output and continued with normal activities 
        except NeedsCleaningException:
            choice = input("Sorry, The machine needs cleaning! Please type yes to clean the machine \n")
            if choice.lower() == "yes":
                print("The machine has been cleaned, you can continue")
                self.clean_machine()
        # Gagan Indukala Krishna Murthy - gi36 - 2nd March 2023
        # In any of the above stage if the user has entered a invalid choice the InvalidChoiceException is called 
        # and asked the user to choose again with the given options 
        except InvalidChoiceException:
            print("You've entered an invalid choice. Please choose from the given options")
        self.run()

    def start(self):
        self.run()

    
if __name__ == "__main__":
    icm = IceCreamMachine()
    icm.start()
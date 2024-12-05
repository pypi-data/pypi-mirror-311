import os
import typer
import sys
from pc_builder.components.gpu import loadGPUsfromJSON
from pc_builder.components.psu import loadPSUsfromJSON
from pc_builder.components.motherboard import loadMBsfromJSON
from pc_builder.components.cpu import loadCPUsfromJSON
from pc_builder.components.cpucooler import loadCPUCoolersfromJSON
from pc_builder.components.ram import loadRAMsfromJSON
from pc_builder.components.ssd import loadSSDsfromJSON
from pc_builder.components.hdd import loadHDDsfromJSON
from pc_builder.components.case import loadCasesfromJSON
from pc_builder.suggestions.cpu import suggestCompatibleCPUs
from pc_builder.suggestions.cpucooler import suggestCompatibleCPUcoolers
from pc_builder.suggestions.gpu import suggestCompatibleGPUs
from pc_builder.suggestions.motherboard import suggestCompatibleMotherboards
from pc_builder.suggestions.psu import suggestCompatiblePSUs
from pc_builder.suggestions.case import suggestCompatibleCases
from pc_builder.suggestions.ram import suggestCompatibleRAMs
from pc_builder.suggestions.ssd import suggestCompatibleSSDs
from pc_builder.suggestions.hdd import suggestCompatibleHDDs


def clearScreen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


app = typer.Typer()


class UserPC:
    def __init__(self):
        self.components = {
            "gpu": [],
            "psu": [],
            "motherboard": [],
            "cpu": [],
            "cpucooler": [],
            "ram": [],
            "ssd": [],
            "hdd": [],
            "case": [],
        }
        self.totalPrice = 0.0
        # self.budget = 1000.0
        # self.useCase = "work"

    def addComponent(self, componentType, part):
        price = float(part.price.replace("€", "").replace("$", "").strip())
        self.components[componentType].append(part)
        self.totalPrice += price

    def removeComponent(self, componentType, index):
        if componentType in self.components and index < len(
            self.components[componentType]
        ):
            price = float(
                self.components[componentType][index]
                .price.replace("€", "")
                .replace("$", "")
                .strip()
            )
            self.totalPrice -= price
            del self.components[componentType][index]

    def display(self):
        # Define the order of components to be displayed
        displayOrder = [
            "gpu",
            "cpu",
            "cpucooler",
            "motherboard",
            "case",
            "psu",
        ]

        # Display the components in the defined order
        for componentType in displayOrder:
            if self.components[componentType]:
                for part in self.components[componentType]:
                    typer.echo(
                        f"{componentType.upper()}: {cleanName(part.name)} - {part.price}"
                    )

        # Display the MEMORY section
        ramParts = self.components["ram"]
        if ramParts:
            typer.echo(typer.style("\n--- MEMORY ---", fg=typer.colors.YELLOW))
            for part in ramParts:
                typer.echo(f"RAM: {cleanName(part.name)} - {part.price}")

        # Display the STORAGE section
        ssdParts = self.components["ssd"]
        hddParts = self.components["hdd"]
        if ssdParts or hddParts:
            typer.echo(typer.style("\n--- STORAGE ---", fg=typer.colors.YELLOW))
            for part in ssdParts:
                typer.echo(f"SSD: {cleanName(part.name)} - {part.price}")
            typer.echo("---------------")
            for part in hddParts:
                typer.echo(f"HDD: {cleanName(part.name)} - {part.price}")

        # Display the total price
        typer.echo(
            typer.style(
                f"\n--- PRICE ---\nTotal Price: €{self.totalPrice:.2f}",
                fg=typer.colors.BLUE,
            )
        )


userPC = UserPC()


@app.command()
def main():
    clearScreen()
    """Welcome to the PC Builder App"""
    typer.echo(typer.style("Welcome to the PC Builder App", fg=typer.colors.YELLOW))
    start()


def start():
    clearScreen()
    """Main Menu"""
    while True:
        typer.echo(typer.style("\n--- Main Menu ---", fg=typer.colors.YELLOW))
        typer.echo(typer.style("1) Add details to purchase", fg=typer.colors.CYAN))
        typer.echo(typer.style("2) View purchase", fg=typer.colors.CYAN))
        # Handle Main Menu display according to whether there are components added or no
        if any(userPC.components[component] for component in userPC.components):
            typer.echo(typer.style("3) Remove component", fg=typer.colors.RED))
            typer.echo(typer.style("4) Finish build", fg=typer.colors.GREEN))
            typer.echo(typer.style("5) Exit", fg=typer.colors.BRIGHT_RED))
        else:
            typer.echo(typer.style("3) Exit", fg=typer.colors.BRIGHT_RED))

        choice = typer.prompt("Choose an option", type=int)

        if choice == 1:
            chooseComponent()
        elif choice == 2:
            viewPurchase()
        elif choice == 3 and not any(
            userPC.components[component] for component in userPC.components
        ):
            typer.echo(
                typer.style(
                    "Thank you for using the PC Builder App!", fg=typer.colors.GREEN
                )
            )
            break
        elif choice == 3 and any(
            userPC.components[component] for component in userPC.components
        ):
            removeComponent()
        elif choice == 4 and any(
            userPC.components[component] for component in userPC.components
        ):
            finishBuild()
        elif choice == 5 and any(
            userPC.components[component] for component in userPC.components
        ):
            typer.echo(
                typer.style(
                    "Thank you for using the PC Builder App!", fg=typer.colors.GREEN
                )
            )
            break
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def chooseComponent():
    clearScreen()
    """Select and add components to your build."""
    while True:
        typer.echo(typer.style("\n--- Choose a Component ---", fg=typer.colors.YELLOW))
        typer.echo("1) GPU")
        typer.echo("2) PSU")
        typer.echo("3) Motherboard")
        typer.echo("4) CPU")
        typer.echo("5) CPU cooler")
        typer.echo("6) RAM")
        typer.echo("7) SSD")
        typer.echo("8) HDD")
        typer.echo("9) Case")
        typer.echo(typer.style("10) Back to Main Menu", fg=typer.colors.CYAN))

        choice = typer.prompt("Choose a component to add", type=int)

        if choice == 1:
            clearScreen()
            selectComponent("gpu")
        elif choice == 2:
            clearScreen()
            selectComponent("psu")
        elif choice == 3:
            clearScreen()
            selectComponent("motherboard")
        elif choice == 4:
            clearScreen()
            selectComponent("cpu")
        elif choice == 5:
            clearScreen()
            selectComponent("cpucooler")
        elif choice == 6:
            clearScreen()
            selectComponent("ram")
        elif choice == 7:
            clearScreen()
            selectComponent("ssd")
        elif choice == 8:
            clearScreen()
            selectComponent("hdd")
        elif choice == 9:
            clearScreen()
            selectComponent("case")
        elif choice == 10:
            clearScreen()
            return  # Return to Main Menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def formatSpecifications(specs):
    """Format the specifications of a part for better readability."""
    typer.echo(typer.style("\nFull Specifications:", fg=typer.colors.YELLOW))

    # Iterate over each specification and print in readable format
    for key, value in specs.items():
        # Skip none or empty values
        if value is None or value == "":
            continue

        # If the value is a list, join non-None values
        if isinstance(value, list):
            readableValue = ", ".join(
                [str(v) for v in value if v is not None and v != ""]
            )
        else:
            readableValue = str(value)

        # Print only if there is a valid value
        if readableValue:
            print(f"{key.replace('_', ' ').capitalize()}: {readableValue}")


def cleanName(name):
    """Remove text within the last set of parentheses and any redundant repeating words in the component name."""
    # Find the last opening parenthesis
    lastOpen = name.rfind("(")
    if lastOpen != -1:
        # Remove the text in the last parentheses and the parentheses themselves
        name = name[:lastOpen].strip()

    # Simplify repeating words in the component name
    words = name.split()
    uniqueWords = []
    for word in words:
        if word not in uniqueWords:
            uniqueWords.append(word)
    return " ".join(uniqueWords)


def ramLimitCheck(componentType, selectedPart):
    ramLimit = 4
    ramAmount = 0

    for stick in userPC.components["ram"]:
        stickStr = stick.specs.modules[0]
        stickAmount, _ = stickStr.split(" x ")
        stickAmount = int(stickAmount)
        ramAmount += stickAmount

    if ramAmount == ramLimit:
        typer.echo(
            typer.style(
                f"Error: You have reached a {componentType.upper()} limit. There are no motherboards that support more than 4 RAM sticks",
                fg=typer.colors.RED,
            )
        )
        return False

    if selectedPart:
        stick = selectedPart
        stickStr = stick.specs.modules[0]
        stickAmount, _ = stickStr.split(" x ")
        stickAmount = int(stickAmount)
        ramAmount += stickAmount

    if ramAmount > ramLimit:
        typer.echo(
            typer.style(
                f"Error: You have reached a {componentType.upper()} limit. There are no motherboards that support more than 4 RAM sticks",
                fg=typer.colors.RED,
            )
        )
        return False

    return True


def selectComponent(componentType):
    userPC.selectedPart = []
    """Select a component from available options."""

    noLimitParts = ["ram", "hdd", "ssd"]

    # Check if the component already exists in the user's build
    if (
        componentType not in noLimitParts
        and componentType in userPC.components
        and userPC.components[componentType]
    ):
        typer.echo(
            typer.style(
                f"Error: You already have a {componentType.upper()} in your build. Remove it first if you want to add a new one.",
                fg=typer.colors.RED,
            )
        )
        return

    if componentType == "ram":
        selectedPart = ""
        check = ramLimitCheck(componentType, selectedPart)
        if not check:
            return

    if componentType == "hdd":
        sataLimit = 8
        sataDeviceAmount = 0
        for ssd in userPC.components["ssd"]:
            interfaceType = ssd.specs.interface[0]
            if "SATA" in interfaceType:
                sataDeviceAmount += 1

        sataDeviceAmount += len(userPC.components["hdd"])
        if sataDeviceAmount == sataLimit:
            typer.echo(
                typer.style(
                    f"Error: You have reached a {componentType.upper()} limit. There are no motherboards that support more than 8 SATA devices",
                    fg=typer.colors.RED,
                )
            )
            return

    parts = getComponents(componentType)

    pageSize = 10
    totalParts = len(parts)
    totalPages = (totalParts + pageSize - 1) // pageSize
    currentPage = 0

    while True:
        startIdx = currentPage * pageSize
        endIdx = min(startIdx + pageSize, totalParts)

        typer.echo(
            typer.style(
                f"\n--- {componentType.upper()} Selection (Page {currentPage + 1}/{totalPages}) ---",
                fg=typer.colors.YELLOW,
            )
        )

        # Display parts for the current page
        for i, part in enumerate(parts[startIdx:endIdx], start=1):
            cleanedName = cleanName(part.name)
            typer.echo(f"{i}) {cleanedName} - {part.price}")

        # Show page navigation if applicable
        if currentPage < totalPages - 1:
            typer.echo(typer.style(f"{pageSize + 1}) Next Page", fg=typer.colors.BLUE))

        if currentPage > 0:
            typer.echo(
                typer.style(f"{pageSize + 2}) Previous Page", fg=typer.colors.MAGENTA)
            )

        typer.echo(
            typer.style(
                f"{pageSize + (3 if totalPages > 1 else 1)}) Exit to Component Menu",
                fg=typer.colors.RED,
            )
        )

        choice = typer.prompt(
            f"Choose a {componentType.upper()} or navigate pages", type=int
        )

        # Handle selection of a component
        if 1 <= choice <= pageSize and (startIdx + choice - 1) < totalParts:
            userPC.selectedPart = selectedPart = parts[startIdx + choice - 1]
            if componentType == "ram":
                check = ramLimitCheck(componentType, selectedPart)
                if not check:
                    return

            if componentType == "ssd":
                mLimit = 6
                ssdAmount = 0
                for ssd in userPC.components["ssd"]:
                    interfaceType = ssd.specs.interface[0]
                    if "M.2" in interfaceType:
                        ssdAmount += 1
                    if ssdAmount == mLimit:
                        typer.echo(
                            typer.style(
                                f"Error: You have reached a M.2 {componentType.upper()} limit. There are no motherboards that support more than 6 M.2 type SSDs",
                                fg=typer.colors.RED,
                            )
                        )
                        return
                sataLimit = 8
                sataDeviceAmount = 0
                for ssd in userPC.components["ssd"]:
                    interfaceType = ssd.specs.interface[0]
                    if "SATA" in interfaceType:
                        sataDeviceAmount += 1

                sataDeviceAmount += len(userPC.components["hdd"])
                if sataDeviceAmount == sataLimit:
                    typer.echo(
                        typer.style(
                            f"Error: You have reached a SATA {componentType.upper()} limit. There are no motherboards that support more than 8 SATA devices",
                            fg=typer.colors.RED,
                        )
                    )
                    return

            typer.echo(
                typer.style(
                    f"Checking compatibility for {cleanName(selectedPart.name)}...",
                    fg=typer.colors.YELLOW,
                )
            )
            isCompatible, comp = selectedPart.checkCompatibility(userPC)
            typer.echo(
                typer.style(
                    f"Compatibility check result: {isCompatible}",
                    fg=typer.colors.BRIGHT_YELLOW,
                )
            )

            # Display detailed incompatibility messages, filtering out empty messages
            if not isCompatible:
                displayIncompatibilityMessages(comp, componentType, userPC)

            if isCompatible:
                cleanedName = cleanName(selectedPart.name)
                typer.echo(
                    typer.style(
                        f"\nYou selected {cleanedName} for {selectedPart.price}",
                        fg=typer.colors.GREEN,
                    )
                )
                formatSpecifications(selectedPart.specs.to_dict())

                confirmChoice = typer.prompt(
                    "Do you want to add this to your build? (y/n)", type=str
                )

                if confirmChoice.lower() == "y":
                    userPC.addComponent(componentType, selectedPart)
                    typer.echo(
                        typer.style(
                            f"{componentType.upper()} added to your build.",
                            fg=typer.colors.GREEN,
                        )
                    )
                    return  # Exit to Main Menu after adding component
                else:
                    typer.echo(
                        typer.style("Selection cancelled.", fg=typer.colors.GREEN)
                    )

        # Next Page
        elif choice == pageSize + 1 and currentPage < totalPages - 1:
            currentPage += 1
        # Previous Page
        elif choice == pageSize + 2 and currentPage > 0:
            currentPage -= 1
        # Exit to Component Menu
        elif choice == pageSize + (3 if totalPages > 1 else 1):
            clearScreen()
            return  # Properly exit to the component menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def displayIncompatibilityMessages(comp, componentType, userPC):
    """Display any incompatibility messages."""
    # Filter out empty messages
    filteredMessages = {key: value for key, value in comp.messages.items() if value}

    if filteredMessages:
        typer.echo(
            typer.style(f"\nIssues with {componentType.upper()}:", fg=typer.colors.RED)
        )
        for key, msgs in filteredMessages.items():
            for message in msgs:
                typer.echo(f" - {message}")

        suggestAlternatives = typer.prompt(
            "Would you like to see a few compatible alternatives? (y/n)", type=str
        )
        if suggestAlternatives.lower() == "y":
            suggestComponent(userPC, componentType, comp)


def suggestComponent(userPC, componentType, comp):
    clearScreen()
    # Dictionary for all the suggestion functions
    suggestionFunctions = {
        "cpu": suggestCompatibleCPUs,
        "psu": suggestCompatiblePSUs,
        "gpu": suggestCompatibleGPUs,
        "case": suggestCompatibleCases,
        "cpucooler": suggestCompatibleCPUcoolers,
        "motherboard": suggestCompatibleMotherboards,
        "ram": suggestCompatibleRAMs,
        "ssd": suggestCompatibleSSDs,
        "hdd": suggestCompatibleHDDs,
    }
    suggestFunc = suggestionFunctions.get(componentType)

    if suggestFunc:
        while True:
            suggestedParts = suggestFunc(
                userPC, comp
            )  # Get 5 suggestions for the build
            been = 0
            if not suggestedParts:
                typer.echo(
                    typer.style(
                        f"\n<<< WARNING! No {componentType.upper()} suggestions could be made for your current build >>>",
                        fg=typer.colors.BRIGHT_RED,
                    )
                )
                differentMessage = {"hdd", "ssd", "ram"}
                if componentType not in differentMessage:
                    typer.echo(
                        typer.style(
                            f"<<< Please review the compatibility messages below again, as they may indicate the source of the issue and review your current build >>>",
                            fg=typer.colors.BRIGHT_GREEN,
                        )
                    )
                    for component, componentMessages in comp.messages.items():
                        if componentMessages:
                            typer.echo(
                                typer.style(
                                    f"\n--- {component.upper()} Compatibility Issues ---",
                                    fg=typer.colors.WHITE,
                                )
                            )
                    for message in componentMessages:
                        typer.echo(
                            typer.style(f" - {message}", fg=typer.colors.BRIGHT_WHITE)
                        )
                        return
                else:
                    been = 1
                    typer.echo(
                        typer.style(
                            f"<<< This might indicate that you have exceeded motherboard limits for the {componentType.upper()} part >>>",
                            fg=typer.colors.RED,
                        )
                    )
                    if userPC.selectedPart:
                        suggestAlternatives = typer.prompt(
                            "Would you like to see if we can find a suitable motherboard for your build? (y/n)",
                            type=str,
                        )
                        if suggestAlternatives.lower() == "y":
                            userPC.addComponent(componentType, userPC.selectedPart)
                            suggestComponent(userPC, "motherboard", comp)
                            userPC.removeComponent(
                                componentType, len(userPC.components[componentType]) - 1
                            )
                            if len(userPC.components["motherboard"]) == 2:
                                userPC.removeComponent(
                                    "motherboard",
                                    len(userPC.components["motherboard"]) - 2,
                                )
                                formatSpecifications(
                                    userPC.selectedPart.specs.to_dict()
                                )

                                confirmChoice = typer.prompt(
                                    "Do you want to add this to your build? (y/n)",
                                    type=str,
                                )

                                if confirmChoice.lower() == "y":
                                    userPC.addComponent(
                                        componentType, userPC.selectedPart
                                    )
                                    typer.echo(
                                        typer.style(
                                            f"{componentType.upper()} added to your build.",
                                            fg=typer.colors.GREEN,
                                        )
                                    )
                                    return
                            else:
                                return
            if (
                componentType == "ssd"
                and been != 1
                and userPC.selectedPart
                and hasattr(userPC.selectedPart, "specs")
                and hasattr(userPC.selectedPart.specs, "interface")
            ):
                ssdType = (
                    "M.2"
                    if any(
                        "M.2" in interface
                        for interface in userPC.selectedPart.specs.interface
                    )
                    else "SATA"
                )
                typer.echo(
                    typer.style(
                        f"\nSuggested compatible {ssdType} {componentType.upper()}s:",
                        fg=typer.colors.YELLOW,
                    )
                )
            else:
                typer.echo(
                    typer.style(
                        f"\nSuggested compatible {componentType.upper()}s:",
                        fg=typer.colors.YELLOW,
                    )
                )

            for i, part in enumerate(suggestedParts, start=1):
                typer.echo(f"{i}) {cleanName(part.name)} - {part.price}")

            # Giving user an option to choose
            skipOption = len(suggestedParts) + 1
            typer.echo(
                typer.style(
                    f"{skipOption}) Skip adding a suggested part",
                    fg=typer.colors.YELLOW,
                )
            )

            choice = typer.prompt(
                f"Choose a suggested {componentType} to add or skip", type=int
            )

            if choice == skipOption:
                typer.echo(
                    typer.style(
                        f"Skipping the addition of a suggested {componentType}.",
                        fg=typer.colors.GREEN,
                    )
                )
                break
            elif 1 <= choice <= len(suggestedParts):
                selectedPart = suggestedParts[choice - 1]
                typer.echo(
                    typer.style(
                        f"You selected {cleanName(selectedPart.name)} for {selectedPart.price}",
                        fg=typer.colors.YELLOW,
                    )
                )
                formatSpecifications(selectedPart.specs.to_dict())

                confirmChoice = typer.prompt(
                    "Do you want to add this to your build? (y/n)", type=str
                )

                if confirmChoice.lower() == "y":
                    userPC.addComponent(componentType, selectedPart)
                    typer.echo(
                        typer.style(
                            f"{componentType.upper()} added to your build.",
                            fg=typer.colors.GREEN,
                        )
                    )
                    break
                else:
                    typer.echo(
                        typer.style(
                            "\nSelection cancelled. You can choose another part or skip.",
                            fg=typer.colors.RED,
                        )
                    )
            else:
                typer.echo(
                    typer.style(
                        "Invalid choice. Please try again.", fg=typer.colors.RED
                    )
                )
                clearScreen()
    else:
        typer.echo(
            typer.style(
                f"\nNo compatible alternatives found for {componentType}.",
                fg=typer.colors.RED,
            )
        )


def viewPurchase():
    clearScreen()
    """View the current purchase and total price."""
    typer.echo(typer.style("\n--- Current Build ---", fg=typer.colors.YELLOW))
    userPC.display()


def getComponents(componentType):
    """Fetch components based on the type (GPU or PSU)"""
    try:
        if componentType == "gpu":
            return loadGPUsfromJSON()
        elif componentType == "psu":
            return loadPSUsfromJSON()
        elif componentType == "motherboard":
            return loadMBsfromJSON()
        elif componentType == "cpu":
            return loadCPUsfromJSON()
        elif componentType == "cpucooler":
            return loadCPUCoolersfromJSON()
        elif componentType == "ram":
            return loadRAMsfromJSON()
        elif componentType == "ssd":
            return loadSSDsfromJSON()
        elif componentType == "hdd":
            return loadHDDsfromJSON()
        elif componentType == "case":
            return loadCasesfromJSON()
    except Exception as e:
        typer.echo(
            typer.style(
                f"An error occurred while fetching {componentType.upper()} data. Please try again later.",
                fg=typer.colors.RED,
            )
        )
    return []


def finishBuild():
    clearScreen()
    """Finalize and display the build"""
    typer.echo(typer.style("\n--- Final Build ---", fg=typer.colors.YELLOW))
    userPC.display()

    while True:
        typer.echo(typer.style("1) Confirm build", fg=typer.colors.GREEN))
        typer.echo(typer.style("2) Return to Main Menu", fg=typer.colors.MAGENTA))
        action = typer.prompt("Choose an option", type=int)

        if action == 1:
            typer.echo(
                typer.style(
                    "Build confirmed. Thank you for using the PC Builder App!",
                    fg=typer.colors.GREEN,
                )
            )
            sys.exit()  # Exit the program
        elif action == 2:
            clearScreen()
            return  # Return to go back to main menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


def removeComponent():
    clearScreen()
    """Remove a component from the build if it exists."""

    # List component types that are available to remove
    componentOptions = [
        ("gpu", "Remove GPU"),
        ("psu", "Remove PSU"),
        ("motherboard", "Remove motherboard"),
        ("cpu", "Remove CPU"),
        ("cpucooler", "Remove CPU cooler"),
        ("ram", "Remove RAM"),
        ("ssd", "Remove SSD"),
        ("hdd", "Remove HDD"),
        ("case", "Remove case"),
    ]

    while True:
        typer.echo(
            typer.style(
                "\n--- Select a Component to Remove ---", fg=typer.colors.YELLOW
            )
        )
        optionNum = 1
        validOptions = {}
        componentsExist = False

        # Display only the components that are in the user's build
        for compType, label in componentOptions:
            if userPC.components[compType]:
                componentsExist = True
                typer.echo(f"{optionNum}) {label}")
                validOptions[optionNum] = compType
                optionNum += 1

        # Dynamically add option to remove all components if any exist
        if componentsExist:
            typer.echo(
                typer.style(
                    f"{optionNum}) Remove all components", fg=typer.colors.BRIGHT_RED
                )
            )
            removeAllOption = optionNum
            optionNum += 1

        typer.echo(
            typer.style(f"{optionNum}) Back to previous menu", fg=typer.colors.CYAN)
        )

        choice = typer.prompt("Choose a component to remove", type=int)

        if choice in validOptions:
            compType = validOptions[choice]

            # Handle components that allow multiple instances
            if compType in ["ram", "ssd", "hdd"]:
                typer.echo(f"\n--- Available {compType.upper()}s ---")
                for i, part in enumerate(userPC.components[compType], start=1):
                    typer.echo(f"{i}) {cleanName(part.name)} - {part.price}")

                partChoice = typer.prompt(
                    f"Select {compType.upper()} to remove or choose '0' to remove all",
                    type=int,
                )

                # Check if user wants to remove all
                if partChoice == 0:
                    confirm = typer.prompt(
                        f"Are you sure you want to remove all {compType.upper()}s? (y/n)",
                        type=str,
                    )
                    if confirm.lower() == "y":
                        for part in userPC.components[compType]:
                            price = float(
                                part.price.replace("€", "").replace("$", "").strip()
                            )
                            userPC.totalPrice -= price
                        userPC.components[compType] = []
                        typer.echo(
                            typer.style(
                                f"All {compType.upper()}s removed from your build.",
                                fg=typer.colors.GREEN,
                            )
                        )
                    else:
                        typer.echo(
                            typer.style("Operation cancelled.", fg=typer.colors.RED)
                        )
                elif 1 <= partChoice <= len(userPC.components[compType]):
                    partToRemove = userPC.components[compType][partChoice - 1]
                    confirm = typer.prompt(
                        f"Are you sure you want to remove {cleanName(partToRemove.name)}? (y/n)",
                        type=str,
                    )
                    if confirm.lower() == "y":
                        userPC.removeComponent(compType, partChoice - 1)
                        typer.echo(
                            typer.style(
                                f"{compType.upper()} removed from your build.",
                                fg=typer.colors.GREEN,
                            )
                        )
                    else:
                        typer.echo(
                            typer.style("Operation cancelled.", fg=typer.colors.GREEN)
                        )
                else:
                    typer.echo(
                        typer.style(
                            "Invalid choice, please try again.", fg=typer.colors.RED
                        )
                    )
                    clearScreen()

            else:
                partToRemove = userPC.components[compType][0]
                confirm = typer.prompt(
                    f"Are you sure you want to remove {cleanName(partToRemove.name)}? (y/n)",
                    type=str,
                )
                if confirm.lower() == "y":
                    userPC.removeComponent(compType, 0)
                    typer.echo(
                        typer.style(
                            f"{compType.upper()} removed from your build.",
                            fg=typer.colors.GREEN,
                        )
                    )
                else:
                    typer.echo(
                        typer.style("Operation cancelled.", fg=typer.colors.GREEN)
                    )

            # Display updated build
            typer.echo(typer.style("\n--- Updated Build ---", fg=typer.colors.YELLOW))
            userPC.display()

        # Handle 'Remove all components' choice dynamically
        elif componentsExist and choice == removeAllOption:
            confirm = typer.prompt(
                "Are you sure you want to remove all components? (y/n)", type=str
            )
            if confirm.lower() == "y":
                for key in userPC.components:
                    userPC.components[key] = []
                userPC.totalPrice = 0.00
                typer.echo(
                    typer.style(
                        "All components have been removed from your build.",
                        fg=typer.colors.GREEN,
                    )
                )
                userPC.display()
            else:
                typer.echo(typer.style("Operation cancelled.", fg=typer.colors.GREEN))

        elif choice == optionNum:
            clearScreen()
            return

        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clearScreen()


if __name__ == "__main__":
    app()

from core.options import OptionType

def moneyness(option):
    """
    @param : option = call/put
    @return : OTM / ATM / ITM
    """
    spot = option.spot
    strike = option.strike
    option_type = option.option_type

    if option_type == OptionType.CALL:
        if spot > strike:
            return "ITM"
        elif spot < strike:
            return "OTM"
        else:
            return "ATM"

    elif option_type == OptionType.PUT:
        if spot < strike:
            return "ITM"
        elif spot > strike:
            return "OTM"
        else:
            return "ATM"
        
    else:
        return -1
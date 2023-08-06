import functools

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def stylize_power(b, p):
    match p:
        case 0:
            return ""
        case 1:
            return b
        case other:
            return b+str(p).translate(SUP)

def f_as_text(b,power_touples,accuracy):
    return functools.reduce(
        lambda acc, i : acc+
        ("" if round(b[i],accuracy)==0 else 
        (("+" if b[i]>=0 else "-") if i != 0 else "")+
        str(abs(b[i]) if accuracy == -1 else abs(round(b[i],accuracy)))+
        ((stylize_power("x", power_touples[i][0]))+
         stylize_power("y", power_touples[i][1]))), 
        range(len(b)), "")
import secrets
from Crypto.Util import number

# A 80-digit prime number, large enough to fit a 32-digit ASCII string inside
PRIME = 129479447415585597871905821327149102955741615431505088722657023019046791467370341893064620026051317254679144875220660930579382546275227796295312577191579111963016239665891306521763649374587440356274420753832196468449910099073419814438899248142702525149640010196075365251503434053384014264300740568021395537536294019007974233665688418414437315368445652648468156646884332330448990129644396098768696762331627327048245959406737341177413349448052046782872751654376230975977666143609993253188642166622646686696345000207797138936266164220179744303967213842480565429775785404627835052430090800586687064789697500271038846697985900335127569089300318742213956290101631566086363678477382884201183406737355398157549111480033809556618935720674596426669169731597545778889134997750409440598399169439971407641736959371542966033120829023902991185192607007305753282671529295779502664186272892936501314794134516289313349768541719877677590251177843979995052355233460049299557169449107873211006286005850484258737222969367058109637984312216563752566606208118920620000409200668438706774768357879996592565884566961818415098801682787030174243994813011729540634000904400508775322213269161355551444072467186963671090261662057114056011880406824749701752430664619310643709205789632860714455285963787409315049281286159169626232985432936185940070411978251603619494314462557984580759577892005393971602687656290831122622412577950119637690717849165488360178874364651508685309178197705717753590921458183270956712342207889618695172025861475231


# n_length = 5000
# PRIME = number.getPrime(n_length)

def encrypt(secret, threshold, total_shares):
    # First, generate t random numbers, with the secret at poly(0)
    poly = [secrets.randbelow(PRIME) for t in range(threshold)]
    poly[0] = secret

    # Next, we evaluate the polynomial at x \in {1..t}
    # (skip x=0, as that is secret)
    shares = [
        (x, _evaluate(poly, x, PRIME))
        for x in range(total_shares + 1)
    ]

    # Skip the secret
    return shares[1:]


def _evaluate(poly, x, prime):
    res = 0
    for coeff in reversed(poly):
        res = (res * x) % prime
        res = (res + coeff) % prime
    return res


def decrypt(msgdiction, threshold, total_shares):
    # 遍历字典中的每一项
    finaldiction = {}
    for key, shares in msgdiction.items():
        if len(shares) == 1:
            # If there's one share, then shares[0] == secret
            return None
        # return _interpolate(shares, PRIME)
        secrets = _interpolate(shares, PRIME)
        finaldiction.update({key: secrets})
    return finaldiction


# 恢复出每个文件的秘密
def _interpolate(shares, prime):
    secret = 0
    for x_j, y_j in shares:
        l_j = _lagrange_poly_at(x_j, shares, prime)
        secret = (secret + ((y_j * l_j) % prime)) % prime
    return secret


def _lagrange_poly_at(x_j, xs, prime):
    acc = 1
    for x, _ in xs:
        if x != x_j:
            dem = (x - x_j) % prime
            div = _div_mod(x, dem, prime)
            acc = (acc * div) % prime
    return acc


# Since (n / m) is n * 1/m, (n / m) mod p is n * m^-1 mod p
def _div_mod(n, m, prime):
    return (n * _inverse(m, prime)) % prime


# Implementation taken from
def _inverse(m, p):
    (t, new_t) = (0, 1)
    (r, new_r) = (p, m)
    while new_r != 0:
        quot = r // new_r
        (t, new_t) = (new_t, t - (quot * new_t))
        (r, new_r) = (new_r, r - (quot * new_r))
    if t < 0:
        t += p
    return t % p

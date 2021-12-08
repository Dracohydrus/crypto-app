import sys
import api_utils as APIUtils
import crypto_utils as CryptoUtils
import time

instrument_name = sys.argv[1]

# will constantly run and grab the average, buy, and sell price based on a trade tax

while True:
    prices = APIUtils.getBuySellPrice(str(instrument_name))
    print(instrument_name,prices["average"],prices["buy"], prices["sell"])
    time.sleep(5)

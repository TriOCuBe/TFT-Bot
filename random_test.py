from tft_bot.constants import CONSTANTS

expected_champs = 8
targets = CONSTANTS["game"]["coordinates"]["board"][:expected_champs]

print(targets)
print(len(targets))
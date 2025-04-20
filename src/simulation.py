import simpy
from src.models.donor import Donor
from src.models.receiver import Receiver
from src.models.distribution_center import DistributionCenter

env = simpy.Environment()

receivers = [
    Receiver("Banque Alimentaire"),
    Receiver("Association Nour")
]

distribution_center = DistributionCenter(receivers)
donor = Donor("Supermarché Carrefour")

env.process(donor.donate(env, distribution_center))
env.run(until=7)

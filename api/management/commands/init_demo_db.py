from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from api.models import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        h = Building.objects.create(name='H')
        e = Building.objects.create(name='E')
        b = Building.objects.create(name='B')

        court = WashingProgram.objects.create(name="Cycle court", duration=timedelta(minutes=30))
        couleurs = WashingProgram.objects.create(name="Couleurs", duration=timedelta(minutes=48))
        long = WashingProgram.objects.create(name="Cycle long", duration=timedelta(hours=1, minutes=20))
        sechage = WashingProgram.objects.create(name="Séchage court", duration=timedelta(minutes=20))

        m1: WashingMachine = WashingMachine.objects.create(name="Machine n°1",
                                                           short_name="n°1",
                                                           number=1,
                                                           machine_type='washing_machine',
                                                           cost=1,
                                                           building=h,
                                                           )
        m2: WashingMachine = WashingMachine.objects.create(name="Sèche-linge n°2",
                                                           short_name="n°2",
                                                           number=2,
                                                           machine_type='dryer',
                                                           cost=2,
                                                           building=h, )
        m1.programs.add(court, couleurs)
        m2.programs.add(sechage)

        hugo = Resident.objects.create(adhesion_id=2,
                                       email="hugh.nata@insal-yon.fr",
                                       rfid_uid="0100",
                                       washing_tokens_count=4)
        self.stdout.write(self.style.SUCCESS("yay !"))

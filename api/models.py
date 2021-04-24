from dataclasses import dataclass
from typing import Tuple, List

from django.db import models, transaction
# Create your models here.
from django.utils.timezone import now


class Building(models.Model):
    """
    un batiment
    """

    class Meta:
        verbose_name = "Bâtiment"

    name = models.CharField(max_length=255, verbose_name="Nom")

    def __str__(self):
        return self.name


class WashingProgram(models.Model):
    class Meta:
        verbose_name = "Programe"

    name = models.CharField(max_length=255, verbose_name="Nom")
    duration = models.DurationField(verbose_name="Durée")

    def __str__(self):
        return f"{self.name} - {self.duration}"


class WashingMachine(models.Model):
    """
    Une machine à laver
    """

    class Meta:
        verbose_name = "Machine à laver"
        verbose_name_plural = "Machines à laver"

    name = models.CharField(max_length=255, verbose_name="Nom")
    short_name = models.CharField(max_length=10, verbose_name="Nom court")
    number = models.IntegerField(verbose_name="Numéro")
    machine_type = models.CharField(choices=[
        ('washing_machine', 'Machine à laver'),
        ('dryer', 'Sèche-linge'),
    ], max_length=64, verbose_name="Type de machine")
    cost = models.IntegerField(default=1, verbose_name="Coût d'une utilisation")
    building = models.ForeignKey(to=Building, null=False, on_delete=models.PROTECT, verbose_name="Bâtiment")
    enabled = models.BooleanField(default=False, verbose_name="Activée (non HS)")

    timer = models.DateTimeField(null=True, verbose_name="Date+heure de fin de cycle", default=None, blank=True)
    # si None, la machine est libre

    programs = models.ManyToManyField(to=WashingProgram, related_name='machine')

    @property
    def available(self) -> bool:
        return self.timer is None or self.timer < now()

    def program_valid_for_machine(self, program: WashingProgram):
        return program in self.programs.all()

    def run_program(self, program: WashingProgram):
        self.timer = now() + program.duration

    def reset_availability(self):
        """
        Affiche la machine comme disponible (pour le dev ou en cas de problème)
        """
        self.timer = None
        self.save()

    def __str__(self):
        return f"{self.name} bat. {self.building.name}, " + ("libre" if self.available else "occupée")


class Resident(models.Model):
    """
    Un mec qui habite dans les résidences, qui peut avoir ou pas une carte VA,
    et qui achète des jetons
    """

    class Meta:
        verbose_name = "Habitant des résidences"
        verbose_name_plural = "Habitants des résidences"

    adhesion_id = models.IntegerField(verbose_name="ID sur Adhésion")
    email = models.EmailField(unique=True, verbose_name="Email adhésion")
    # has_valid_membership = models.BooleanField(default=False,verbose_name="Possède une Adhésion valide (carte VA)")

    rfid_uid = models.CharField(max_length=255, verbose_name="ID du badge RFID")

    washing_tokens_count = models.IntegerField(default=0, verbose_name="Nombre de jetons")

    def __str__(self):
        return f"#{self.adhesion_id} {self.email}"


OPERATIONAL_STATUSES = {
    0: "La machine a été lancée",
    1: "Erreur inconnue",
    10: "la machine est occupée",
    11: "crédit insuffisant",
    12: "Programme sélectionné invalide",
}


def use_machine(user: Resident, machine: WashingMachine, program: WashingProgram) -> Tuple[
    bool, WashingMachine, Resident, List[int]]:
    """
    Le booléen renvoyé indique le succès de l'opération, et la liste des codes d'erreurs à la fin
    """
    with transaction.atomic():
        if (machine.available  # machine libre
        ) and (user.washing_tokens_count > machine.cost  # il reste des jetons à la personne
        ) and (machine.program_valid_for_machine(program)):  # le programe sélectionné est valide pour cette machine

            user.washing_tokens_count -= machine.cost  # on déduit le jeton du compte
            machine.run_program(program)  # on prévoit l'heure de fin de cycle

            user.save()
            machine.save()
            return True, machine, user, []
        else:
            errors = []
            if not machine.available:
                errors.append(10)
            if user.washing_tokens_count < machine.cost:
                errors.append(11)
            if not machine.program_valid_for_machine(program):
                errors.append(12)
            return False, machine, user, errors

    # noinspection PyUnreachableCode
    return False, machine, user, [1]  # erreur inconnue


@dataclass
class RunRequest:
    resident: Resident
    program: WashingProgram
    # machine:WashingMachine


@dataclass
class RunResponse:
    operation_status: bool
    machine: WashingMachine
    resident: Resident
    program: WashingProgram
    errors: List[int]
    details: List[str]

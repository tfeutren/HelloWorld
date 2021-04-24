from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import *
# Create your views here.
from api.serializers import *


class WashingMachineViewset(viewsets.ReadOnlyModelViewSet):
    """
    Gestion des machines à laver
    Voir particulièremenr l'endpoint /run_program/
    """
    queryset = WashingMachine.objects.filter(enabled=True)
    serializer_class = WashingMachineSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get', 'POST'])
    def run_program(self, request: Request, pk: int):
        """
        Permet de lancer une machine
        paramètres:
        {
            "resident": "6467987", # UID du badge RFID
            "program": 1, # ID du programme à lancer
        }
        """
        if request.method == 'GET':
            return Response({})
        else:
            serializer = RunRequestSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                run_request = serializer.save()
                # resident = Resident.objects.get(rfid_uid=run_request.rfid_uid)
                machine: WashingMachine = self.get_object()
                program: WashingProgram = run_request.program  # l'objet est récup car c'est un RelatedField
                resident: Resident = run_request.resident
                print(machine, program, resident)

                operation_status_ok, machine, resident,errors = use_machine(resident, machine, program)
                if operation_status_ok:
                    details=[OPERATIONAL_STATUSES[0]]
                else:
                    details = [OPERATIONAL_STATUSES[err] for err in errors]
                rr = RunResponse(operation_status=operation_status_ok,
                                 machine=machine,
                                 resident=resident,
                                 errors=errors,
                                 details=details,
                                 program=program)
                rrs = RunResponseSerializer(rr)
                return Response(rrs.data, status=status.HTTP_200_OK if operation_status_ok else status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        # permet d'afficher le joli formulaire dans l'explorateur d'API pour l'action `.../run_program/`
        if self.action == 'run_program':
            return RunRequestSerializer
        return super(WashingMachineViewset, self).get_serializer_class()
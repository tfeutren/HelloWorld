import requests


def run_machine(machine_id: int, resident_rfid_uid: str, program_id: int):
    r = requests.post(f'http://localhost:8000/machines/{machine_id}/run_program/', data={
        "resident": resident_rfid_uid,  # UID du badge RFID
        "program": program_id,  # ID du programme à lancer
    })
    # exemple de réponse:
    #d = {
    #    'machine': {
    #        'id': 1, 'available': False, 'programs': [
    #            {'id': 1, 'name': 'Cycle court', 'duration': '00:30:00'},
    #            {'id': 2, 'name': 'Couleurs', 'duration': '00:48:00'}
    #        ],
    #        'building': 'H',
    #        'name': 'Machine n°1',
    #        'short_name': 'n°1',
    #        'number': 1,
    #        'machine_type': 'washing_machine',
    #        'cost': 1,
    #        'timer': '2021-04-24T11:34:35.122545Z'
    #    },
    #    'operation_status': False,
    #    'resident': {
    #        'id': 1,
    #        'adhesion_id': 2,
    #        'email': 'hugh.nata@insal-yon.fr',
    #        'rfid_uid': '0100',
    #        'washing_tokens_count': 3}, 'errors': [10], 'details': [
    #        'la machine est occupée'
    #    ]
    #}

    res = r.json()
    print(res)
    print(f"\nprogramme '{res['program']['name']}' sur la machine '{res['machine']['name']}' du bâtiment '{res['machine']['building']}'")
    print("    utilisateur :",res['resident']['email'])
    print("         status :","succès" if res['operation_status'] else "échec")
    print("        détails :",", ".join(res['details']))
    print("jetons restants :",res['resident']['washing_tokens_count'])


if __name__ == '__main__':
    run_machine(1, "0100", 2)

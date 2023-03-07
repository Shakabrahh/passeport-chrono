import configparser
import datetime
import logging
import time
from pathlib import Path
from typing import List, NamedTuple

import playsound
import requests


class Creneau(NamedTuple):
    ville: str
    date: str
    heure: str
    url: str


class CreneauNotFoundError(Exception):
    pass


def obtenir_creneaux_disponibles(config: dict) -> List[Creneau]:
    params = {
        k: v
        for k, v in config.items()
        if k
        in [
            "longitude",
            "latitude",
            "end_date",
            "radius_km",
            "address",
            "reason",
            "documents_number",
        ]
    }
    params["start_date"] = datetime.date.today().strftime("%Y-%m-%d")

    try:
        with requests.Session() as session:
            response = session.get(config["api_url"], params=params)
            response.raise_for_status()
            data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.exception(f"Une erreur s'est produite lors de la demande : {e}")
        raise CreneauNotFoundError("Erreur lors de la demande")

    creneaux_disponibles = []
    for item in data:
        try:
            for creneau_disponible in item["available_slots"]:
                date_heure = datetime.datetime.fromisoformat(
                    creneau_disponible["datetime"][:-6]
                )
                jour, heure = date_heure.strftime("%d/%m/%Y %H:%M").split()

                creneaux_disponibles.append(
                    Creneau(
                        item["city_name"],
                        jour,
                        heure,
                        creneau_disponible["callback_url"],
                    )
                )
        except (IndexError, KeyError, ValueError) as e:
            logging.exception(f"Format de données inattendu reçu : {e}")
            raise CreneauNotFoundError("Format de données inattendu")

    if not creneaux_disponibles:
        raise CreneauNotFoundError("Aucun créneau n'a été trouvé")

    return creneaux_disponibles


def afficher_info_creneaux(creneaux: List[Creneau]) -> None:
    for creneau in creneaux:
        message = f"Créneau disponible à {creneau.ville} le {creneau.date} à {creneau.heure} ! URL : {creneau.url}"
        logging.info(message)


def jouer_son(config: dict) -> None:
    try:
        playsound.playsound(config["sound_file_path"])
    except (FileNotFoundError, TypeError) as e:
        logging.exception(f"Erreur lors de la lecture du fichier audio : {e}")


def configurer_logger(config: dict) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config["log_file_path"], mode="w", encoding="utf-8"),
        ],
    )


def charger_configuration(fichier_configuration: Path) -> dict:
    config_parser = configparser.ConfigParser()
    with open(fichier_configuration, encoding="utf-8") as fichier:
        config_parser.read_file(fichier)
    return dict(config_parser["DEFAULT"])


def traiter_info_creneaux(creneaux: List[Creneau], config: dict) -> None:
    if creneaux:
        afficher_info_creneaux(creneaux)
        jouer_son(config)


def main(config: dict) -> None:
    configurer_logger(config)
    while True:
        try:
            info_creneaux = obtenir_creneaux_disponibles(config)
            traiter_info_creneaux(info_creneaux, config)
        except CreneauNotFoundError as erreur:
            logging.info(str(erreur))
        time.sleep(int(config["sleep_time_sec"]))


if __name__ == "__main__":
    CHEMIN_FICHIER_CONFIG = Path(__file__).resolve().parent / "config.ini"
    configuration = charger_configuration(CHEMIN_FICHIER_CONFIG)
    main(configuration)

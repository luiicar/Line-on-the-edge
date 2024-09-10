import logging
import asyncio

from tapgobuspackage.config import file_log
from tapgobuspackage.file_opener import open_json
from tapgobuspackage.parser import init_lxml, init_pd, clear_params
from tapgobuspackage.coordinates import get_gpsd_connection
from tapgobuspackage.tap import define_tap
from tapgobuspackage.line import calculateLine
from tapgobuspackage.stop import calculateStops
from tapgobuspackage.validation import calculateValidations
from tapgobuspackage.simulation import simulate

# Configurazione del logging
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(asctime)s - %(name)s %(message)s')

# Creazione di un logger specifico per questo modulo con nome personalizzato
logger = logging.getLogger(" ")


async def main():
    sim_file = "database/infomobility-C63.json"

    open_json(0, file_log, option="clear")
    logger.info("Inizializzazione Tap&Go on Bus in corso...")
    await init_lxml()
    await init_pd()
    await clear_params()
    connected = await get_gpsd_connection()
    if connected:
        logger.info("Connessione al GPS Deamon riuscita.")
    else:
        logger.info("Connessione al GPS Deamon fallita.")
    logger.info("Inizializzazione Tap&Go on Bus completata!")

    # Crea i task per le funzioni
    line_task = asyncio.create_task(calculateLine())
    stops_task = asyncio.create_task(calculateStops())
    validations_task = asyncio.create_task(calculateValidations())
    tap_task = asyncio.create_task(define_tap())
    if sim_file == None or sim_file == "":
        await asyncio.gather(stops_task, line_task, tap_task, validations_task) # Attende che tutti i task sia completati
    else:
        simulate_task = asyncio.create_task(simulate(sim_file))
        await asyncio.gather(simulate_task, stops_task, line_task, tap_task, validations_task) # Attende che tutti i task sia completati


# Esegue il loop principale
asyncio.run(main())

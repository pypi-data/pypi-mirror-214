# ############################################################################################################
#  @author Oliver Consterla Araya                                                                            #
#  @version 2023613.14.58                                                                                    #
#  @since 2023                                                                                               #
# ############################################################################################################

import configparser
import os
import subprocess
if not os.path.isfile('config.ini'):
    # Llamar al script initConfig.py para descargar el archivo config.ini
    subprocess.run(["python", "initConfig.py"])
import time
import keyboard
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from moviepy.editor import VideoFileClip
import pyglet
from pydub import AudioSegment
from pydub.playback import play as play_audio
from logger import log
import cv2

try:
    # Lee la configuración desde el archivo externo config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        video_folder = config['DEFAULT']['video_folder']
    except KeyError as e:
        log("La clave 'video_folder' no está definida en el archivo config.ini.")
        log(e)
        exit(1)

    try:
        framerate_option = config.get('Framerate', 'option')
    except configparser.NoSectionError:
        log("La sección 'Framerate' no está definida en el archivo config.ini.")
        framerate_option = 'original_player'
    except configparser.NoOptionError:
        log("La opción 'option' no está definida en la sección 'Framerate' del archivo config.ini.")
        framerate_option = 'original_player'

    # Rutas de carpetas
    watch_folder = config.get('Paths', 'WatchFolder')
    ignore_folder = config.get('Paths', 'IgnoreFolder')

    # Lista de reproducción
    playlist = []
    played_videos = set()

    # Clase de manipulador de eventos para detectar cambios en la carpeta
    class FileCreatedEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory and event.src_path.endswith('.mp4'):
                video_path = event.src_path
                try:
                    if not video_path.startswith(ignore_folder) and not os.path.dirname(video_path) == watch_folder:
                        playlist.append(video_path)
                except Exception as e:
                    log(f"Error processing video: {video_path}")
                    log(e)

    # Función para reproducir los videos en la lista de reproducción
    def play_videos():
        while True:
            if len(playlist) == 0:
                time.sleep(1)
                continue

            video_filename = playlist.pop(0)
            video_path = os.path.join(video_folder, video_filename)
            if video_path not in played_videos:
                try:
                    log(f'Reproduciendo: {video_path}')

                    # Simula la tecla "page up" antes de iniciar la reproducción
                    keyboard.press('page up')
                    keyboard.release('page up')

                    # Extrae el audio del video utilizando pydub
                    video = VideoFileClip(video_path)
                    audio = video.audio
                    audio_path = 'temp_audio.wav'
                    audio.write_audiofile(audio_path, codec='pcm_s16le')

                    # Obtén la tasa de cuadros por segundo original del video
                    cap = cv2.VideoCapture(video_path)
                    fps = None

                    # Actualiza el valor de fps según la opción seleccionada
                    if framerate_option == 'original_player':
                        # Mantener la tasa de cuadros por segundo original del reproductor
                        pass
                    elif framerate_option == 'original_video':
                        # Obtén la tasa de cuadros por segundo original del video
                        cap = cv2.VideoCapture(video_path)
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        cap.release()
                    elif framerate_option == '15':
                        fps = 15
                    elif framerate_option == '30':
                        fps = 30
                    elif framerate_option == '45':
                        fps = 45
                    elif framerate_option == '60':
                        fps = 60

                    # Reproduce el audio con pyglet
                    audio_player = pyglet.media.Player()
                    audio = pyglet.media.load(audio_path)
                    audio_player.queue(audio)
                    audio_player.play()

                    # Registra el evento de finalización de reproducción del audio
                    @audio_player.event
                    def on_player_eos():
                        audio_player.delete()
                        os.remove(audio_path)

                    # Muestra el video sin audio utilizando MoviePy a la tasa de cuadros por segundo seleccionada
                    if fps is None:
                        video.preview(fullscreen=False, audio=False)
                    else:
                        video.preview(fullscreen=False, audio=False, fps=fps)
                    video.close()

                    played_videos.add(video_path)
                    log(f'Terminado: {video_path}')

                    # Elimina el video de la lista de reproducción
                    if video_path in played_videos:
                        played_videos.remove(video_path)
                    if video_path in playlist:
                        playlist.remove(video_path)

                    # Simula la tecla "page down" después de reproducir el último video
                    if len(playlist) == 0:
                        log(f'Lista terminada')
                        time.sleep(2)
                        keyboard.press('page down')
                        keyboard.release('page down')

                except Exception as e:
                    if len(playlist) == 0:
                        log(f'Lista terminada con excepciones')
                        time.sleep(2)
                        keyboard.press('page down')
                        keyboard.release('page down')
                    log("Error al reproducir el video: " + video_path)
                    log("Error: " + str(e))
                    continue

                    # Configura el observador para detectar cambios en la carpeta
    event_handler = FileCreatedEventHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=True)
    observer.start()

    # Inicia la reproducción de videos
    try:
        play_videos()
    except Exception as e:
        log(f"Excepción al reproducir videos fin: {str(e)}")

    ## Detiene el observador cuando se cierra la ventana
    ## keyboard.wait('esc')
    observer.stop()
    observer.join()
except Exception as e:
    log(f"Excepción no controlada: {str(e)}")
from .logger import Logger

class LogManager:
    def __init__(self, *args, **kwargs) -> None:
        for logger in args + tuple(kwargs.values()):
            if not isinstance(logger, Logger):
                raise TypeError(f"All arguments must be of type 'Logger', not '{type(logger).__name__}'")
        # Store loggers in a dictionary by uppercased names
        self.loggers = {**kwargs, **{logger.file.split('.', 1)[0].upper(): logger for logger in args}}

    def __getattr__(self, name: str) -> Logger:
        # Access the logger by its name
        if name in self.loggers:
            return self.loggers[name]
        raise AttributeError(f"'LogManager' object has no attribute '{name}'")

    def __getitem__(self, name: str) -> Logger:
        # Access the logger by its name using subscript notation
        if name in self.loggers:
            return self.loggers[name]
        raise KeyError(f"'LogManager' object has no logger '{name}'")

    def add_logger(self, name: str, file: str = 'gaza.log') -> None:
        """
        Ajoute un nouveau logger dans le gestionnaire de logs.

        Args:
            name (str): Le nom du logger à ajouter.
            file (str, optional):   Le nom du fichier journal dans lequel enregistrer les messages.
                                    Par défaut, 'gaza.log'.

        Retourne:
            None
        """
        self.loggers[name] = Logger(file)

    def log(self, name: str, msg_type: str | list[str], msg_content: str, content_size_limit: int = 150) -> None:
        """
        Enregistre un message dans le fichier journal d'un logger spécifié.

        Args:
            name (str): Le nom du logger dans lequel enregistrer le message.
            msg_type (str | list[str]): Le ou les types du message à enregistrer.
            msg_content (str): Le contenu du message à enregistrer.
            content_size_limit (int, optional): La limite de taille du contenu du message.
                                                Par défaut, elle est fixée à 150 caractères.

        Retourne:
            None
        """
        if name in self.loggers:
            self.loggers[name].log(msg_type, msg_content, content_size_limit)
        else:
            raise ValueError(f"Le logger '{name}' n'existe pas.")

    def clear_logs(self, name: str, archive: bool = True, saving_folder: str = None) -> bool:
        """
        Efface le contenu d'un fichier log d'un logger spécifié et l'archive éventuellement dans un dossier spécifié.

        Args:
            name (str): Le nom du logger dont le fichier log sera effacé.
            archive (bool, optional):   Si True, le fichier log sera archivé avant d'être effacé.
                                        Par défaut, True.
            saving_folder (str, optional): Chemin d'accès du dossier dans lequel l'archive du fichier log
                                            sera sauvegardée. Si aucun dossier n'est spécifié ou si le dossier n'existe pas,
                                            l'archive sera sauvegardée dans le même dossier que le fichier log d'origine.
                                            Par défaut, None.

        Retourne:
            bool: True si le fichier log a été effacé et éventuellement archivé avec succès, False sinon.
        """
        if name in self.loggers:
            return self.loggers[name].clear_logs(archive, saving_folder)
        else:
            print(f"Le logger '{name}' n'existe pas.")
            return False

    def print_logs(self, name: str, limit: int = 10) -> None:
        """
        Affiche les derniers messages enregistrés dans le fichier log d'un logger spécifié.

        Args:
            name (str): Le nom du logger dont les messages seront affichés.
            limit (int, optional): Le nombre de messages à afficher. Par défaut, 10.

        Retourne:
            None
        """
        if name in self.loggers:
            self.loggers[name].print_logs(limit)
        else:
            raise ValueError(f"Le logger '{name}' n'existe pas.")

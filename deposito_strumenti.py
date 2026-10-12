from operator import attrgetter

# CLASSE STRUMENTO
class Strumento:
    """Modella un singolo strumento musicale nel deposito."""

    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento  # Codice univoco (es. S1, S2...)
        self.tipo = tipo  # Tipo di strumento (es. Chitarra)
        self.marca = marca  # Marca dello strumento
        self.anno_acquisto = int(anno_acquisto)  # Anno di acquisto
        self.valore = float(valore)  # Valore in euro

    def __str__(self):
        """Rappresentazione testuale leggibile dello strumento."""
        return (f"[{self.id_strumento}] {self.tipo} - Marca: {self.marca} "
                f"(Anno: {self.anno_acquisto}, Valore: €{self.valore:.2f})")

    def __repr__(self):
        return self.__str__()

# CLASSE PRESTITO
class Prestito:
    """Modella il prestito di uno strumento a un allievo."""

    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito  # Codice univoco del prestito (es. P1, P2...)
        self.data = data  # Data in cui è avvenuto il prestito
        self.id_strumento = id_strumento  # Codice dello strumento prestato
        self.cognome_allievo = cognome_allievo  # Cognome dell'allievo

    def __str__(self):
        """Rappresentazione testuale leggibile del prestito."""
        return (f"Prestito {self.id_prestito} | Data: {self.data} | "
                f"Strumento ID: {self.id_strumento} | Allievo: {self.cognome_allievo}")

    def __repr__(self):
        return self.__str__()


# CLASSE DEPOSITO STRUMENTI
class DepositoStrumenti:
    """Gestisce l'inventario degli strumenti e i relativi prestiti."""

    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati del deposito."""
        self.nome = nome  # Nome del deposito
        self.responsabile = responsabile  # Nome del responsabile
        self.strumenti = {}  # Dizionario ID -> Oggetto Strumento
        self.prestiti = {}  # Dizionario ID -> Oggetto Prestito

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti da un file CSV.
        Solleva FileNotFoundError se il file non esiste.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                for riga in file:
                    riga = riga.strip()
                    if not riga:
                        continue  # Salta eventuali righe vuote

                    campi = riga.split(',')
                    if len(campi) == 5:
                        id_strumento, tipo, marca, anno_acquisto, valore = campi
                        # Crea l'oggetto Strumento e lo memorizza nel dizionario
                        nuovo_str = Strumento(id_strumento, tipo, marca, anno_acquisto, valore)
                        self.strumenti[id_strumento] = nuovo_str
        except FileNotFoundError:
            raise FileNotFoundError(f"Il file {file_path} non è stato trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito assegnandogli un ID progressivo (es. S1, S2...).
        Restituisce il riferimento allo strumento aggiunto.
        """
        # Determina il prossimo codice progressivo basato sugli strumenti esistenti
        if self.strumenti:
            # Estrae il numero dall'ID esistente (es. 'S3' -> 3)
            numeri = [int(id_str[1:]) for id_str in self.strumenti.keys() if
                      id_str.startswith('S') and id_str[1:].isdigit()]
            prossimo_num = max(numeri) + 1 if numeri else 1
        else:
            prossimo_num = 1

        id_strumento = f"S{prossimo_num}"

        # Crea il nuovo strumento
        nuovo_str = Strumento(id_strumento, tipo, marca, anno_acquisto, valore)
        self.strumenti[id_strumento] = nuovo_str

        return nuovo_str

    def strumenti_ordinati_per_marca(self):
        """Restituisce un elenco degli strumenti ordinati alfabeticamente per marca."""
        lista_strumenti = list(self.strumenti.values())
        # Utilizza sorted con attrgetter per ordinare in base all'attributo 'marca'
        return sorted(lista_strumenti, key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito verificando che lo strumento esista e non sia già in prestito.
        Restituisce il riferimento al prestito creato.
        """
        # 1. Verifica se lo strumento esiste nel deposito
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: Lo strumento con ID {id_strumento} non esiste nel sistema.")

        # 2. Verifica se lo strumento è già attualmente in prestito
        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception(f"Errore: Lo strumento {id_strumento} è già attualmente in prestito.")

        # 3. Genera un codice univoco per il prestito (es. P1, P2...)
        prossimo_num = len(self.prestiti) + 1
        id_prestito = f"P{prossimo_num}"
        while id_prestito in self.prestiti:
            prossimo_num += 1
            id_prestito = f"P{prossimo_num}"

        # 4. Crea il prestito e lo memorizza
        nuovo_prest = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[id_prestito] = nuovo_prest

        return nuovo_prest

    def termina_prestito(self, id_prestito):
        """Termina un prestito rimuovendolo dal sistema in base al suo ID."""
        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: Il codice prestito {id_prestito} non corrisponde ad alcun prestito attivo.")

        # Rimuove il prestito dal dizionario
        del self.prestiti[id_prestito]
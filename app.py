from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# For session management (not directly used here)
app.secret_key = 'your_secret_key'

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '').replace(
    "postgres://aphorismsdb_user:UxX03JBPW4Lf1DDbFcXC5s8Vqoy7eO8F@dpg-ctfgci3tq21c73bupmc0-a:5432/aphorismsDB",
    "postgresql://aphorismsdb_user:UxX03JBPW4Lf1DDbFcXC5s8Vqoy7eO8F@dpg-ctfgci3tq21c73bupmc0-a:5432/aphorismsDB")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Replace is for compatibility

# Initialize the database
db = SQLAlchemy(app)

# Define the Aphorism model


class Aphorism_it(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {"id": self.id, "text": self.text, "author": self.author, "created_at": self.created_at}


class Aphorism_en(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {"id": self.id, "text": self.text, "author": self.author, "created_at": self.created_at}
# Create tables (run once during setup)


@app.before_first_request
def create_tables():
    db.create_all()


def populate_tables():
    # Populate Category1 table
    for aphorism in aphorisms["en"]:
        new_aphorism = Aphorism_en(text=aphorism)
        db.session.add(new_aphorism)

    # Populate Category2 table
    for aphorism in aphorisms["it"]:
        new_aphorism = Aphorism_it(text=aphorism)
        db.session.add(new_aphorism)

    db.session.commit()
    print("Tables populated successfully!")


# List of aphorisms
aphorisms = {
    'it': [
        {"text": "Penso che il cervello sia l'anima, non credo alla vita dopo la morte ne tanto meno a un paradiso in versione condominiale, dove rincontrare amici, nemici, parenti, conoscenti.", "author": "Margherita Hack"},
        {"text": "Gli uomini sono donne che non ce l'hanno fatta.", "author": "Unknown"},
        {"text": "La nostra pazienza è illimitata, ma non passiva e inerte.",
         "author": "Antonio Gramsci"},
        {"text": "La vita non è una questione di come sopravvivere alla tempesta, ma di come danzare nella pioggia.",
         "author": "Kahlil Gibran"},
        {"text": "Finito il gioco il re e il pedone tornano nella stessa scatola.",
         "author": "Unknown"},
        {"text": "L'arte è la magia liberata dalla menzogna della verità.",
            "author": "Unknown"},
        {"text": "Nessun maggior dolore, che ricordarsi del tempo felice, nella miseria.",
         "author": "Dante Alighieri"},
        {"text": "La rivoluzione è sempre per tre quarti fantasia e per un quarto realtà.",
         "author": "Bakunin"},
        {"text": "La passione per la distruzione è anche una passione creativa.",
         "author": "Bakunin"},
        {"text": "Sei capace di farmi sentire escluso dal niente.", "author": "Unknown"},
        {"text": "Sei una prepotenza della natura.", "author": "Unknown"},
        {"text": "Non so niente ma mi piace tutto.", "author": "Paolo Sorrentino"},
        {"text": "Quando sai tutto muori presto e solo. Sai l'indicibile.",
         "author": "Paolo Sorrentino"},
        {"text": "La peggior solitudine è essere privi di un'amicizia sincera.",
         "author": "Francis Bacon"},
        {"text": "La speranza è una buona prima colazione, ma è una pessima cena.",
         "author": "Francis Bacon"},
        {"text": "Le donne sono amanti per gli uomini giovani, compagne per la mezza età e infermiere per i vecchi.",
         "author": "Francis Bacon"},
        {"text": "Un uomo che medita la vendetta, mantiene le sue ferite sempre sanguinanti.",
         "author": "Francis Bacon"},
        {"text": "Ho sempre sognato di dipingere il sorriso, ma non ci sono mai riuscito.",
         "author": "Francis Bacon"},
        {"text": "L'amore è una malattia ribelle, che ha la sua cura in se stessa, in cui chi è malato non vuole guarirne e chi ne è infermo non desidera riaversi.", "author": "Unknown"},
        {"text": "Mai ti è dato un desiderio senza che ti sia dato anche il potere di realizzarlo.",
         "author": "Richard Bach"},
        {"text": "A ciascuno di noi il fato ha destinato una donna, se riusciamo a sfuggirle siamo salvi.", "author": "Unknown"},
        {"text": "A volte il cuore vede cose che sono invisibili agli occhi.",
         "author": "Unknown"},
        {"text": "A provocare un sorriso è quasi sempre un altro sorriso.",
            "author": "Unknown"},
        {"text": "Avere la coscienza pulita è segno di cattiva memoria.",
            "author": "Unknown"},
        {"text": "Cerca di ottenere sempre ciò che ami o dovrai accontentarti di amare ciò che ottieni.", "author": "Unknown"},
        {"text": "Dio e il soldato, durante la carestia e la guerra, vengono pregati, ma quando vi è la pace Dio è dimenticato e il soldato disprezzato.", "author": "Unknown"},
        {"text": "È incredibile quante cose si trovano mentre cerchi qualcos'altro.",
         "author": "Unknown"},
        {"text": "Errare è umano e dare la colpa a un altro è ancora più umano.",
         "author": "Unknown"},
        {"text": "Felicitá è non fermarsi mai a pensare se la si ha.", "author": "Unknown"},
        {"text": "I veri amici sono rari perchè è poca la domanda.", "author": "Unknown"},
        {"text": "Il bacio è un dolce trovarsi dopo essersi a lungo cercati.",
         "author": "Unknown"},
        {"text": "Il lavoro duro paga nel lungo periodo. La pigrizia paga subito.",
         "author": "Unknown"},
        {"text": "In amore importanti sono l'incontro e la rottura, tra i due, è solo riempimento.",
         "author": "Unknown"},
        {"text": "Intelligenza: quando ti accorgi che il ragionamento del tuo principale non fila. Saggezza: quando eviti di farglielo notare.", "author": "Unknown"},
        {"text": "La depressione è la rabbia senza entusiasmo.", "author": "Unknown"},
        {"text": "L'adulazione è l'arte di dire a una persona quello che pensa di sé stessa.",
         "author": "Unknown"},
        {"text": "L'amore non vede i difetti, l'amicizia li ama.", "author": "Unknown"},
        {"text": "L'ansia è come una sedia a dondolo: sei sempre in movimento, ma non avanzi di un passo.", "author": "Unknown"},
        {"text": "L'esperienza è il tipo di insegnante più difficile. Prima ti fa l'esame, e poi ti spiega la lezione.", "author": "Unknown"},
        {"text": "L'ipocondria è l'unica malattia che non ho.", "author": "Unknown"},
        {"text": "Meglio avere un leone a capo di un esercito di pecore, che una pecora a capo di un esercito di leoni.", "author": "Unknown"},
        {"text": "Meglio la gioia di un sorriso triste che la tristezza di non saper sorridere.",
         "author": "Unknown"},
        {"text": "Non andate ai funerali degli altri, tanto loro non verranno al vostro.",
         "author": "Unknown"},
        {"text": "Non pretendo di avere tutte le risposte. A dire la verità non m'interessano nemmeno tutte le domande.", "author": "Unknown"},
        {"text": "Sperare vuol dire rischiare la delusione. Ma il rischio va affrontato perchè il massimo rischio nella vita è di non rischiare mai. Soltanto chi rischia è libero.", "author": "Unknown"},
        {"text": "Per amore della rosa, si sopportano le spine.", "author": "Unknown"},
        {"text": "Quello che io dico e quello che tu senti non sono sempre la stessa cosa.",
         "author": "Unknown"},
        {"text": "Ricorda sempre che sei unico, esattamente come tutti gli altri.",
         "author": "Unknown"},
        {"text": "Se non sei parte della soluzione, allora sei parte del problema.",
         "author": "Unknown"},
        {"text": "Se sei felice non gridare troppo: la tristezza ha il sonno leggero.",
         "author": "Unknown"},
        {"text": "Se tutto sembra venirti incontro, probabilmente sei nella corsia sbagliata.",
         "author": "Unknown"},
        {"text": "Si può dimenticare il male ricevuto, ma quello fatto mai!",
         "author": "Unknown"},
        {"text": "Il tempo per leggere, come il tempo per amare, dilata il tempo per vivere...",
         "author": "Daniel Pennac"},
        {"text": "Chi dice che è impossibile... non dovrebbe disturbare chi ce la sta facendo.",
         "author": "A. Einstein"},
        {"text": "L'uomo dorme, solo la morte potrà svegliarlo.", "author": "Unknown"},
        {"text": "Io non sono un poeta, sono un uomo con la passione della poesia. Io non sono un musicista, sono un uomo con la passione della musica. Io non sono un maestro, sono un uomo con la sete del sapere. Io non sono un artista, sono un uomo che ama dipingere ogni angolo della terra. Io non sono un politico, sono un uomo che pensa ai problemi del mondo. E per tutto quello che sono e per tutto quello che non sono, una vita sola non basta, Potrei averne un'altra, per favore?", "author": "Arnoldo Fó"},
        {"text": "Di ciò che posso essere io per me, non solo non potete saper nulla voi, ma nulla neppure io stesso.",
         "author": "L. Pirandello"},
        {"text": "Tutto va preso con moderazione, anche la moderazione.",
         "author": "Oscar Wilde"},
        {"text": "Quello che mi ha sorpreso di più negli uomini dell'Occidente è che perdono la salute per fare i soldi e poi perdono i soldi per recuperare la salute. Pensano tanto al futuro che dimenticano di vivere il presente in tale maniera che non riescono a vivere né il presente, né il futuro. Vivono come se non dovessero morire mai e muoiono come se non avessero mai vissuto.", "author": "D.L."},
        {"text": "Posso offrirti qualcosa da bere o vuoi direttamente i soldi??",
         "author": "Unknown"},
        {"text": "La creatività del cervello dell'Homo Sapiens si esprime elaborando congegni meccanici semplici e perfetti, così rispondenti allo scopo da non richiedere modifiche, o congegni più rozzi e imperfetti che, per la loro stessa imperfezione, si prestano a essere ristrutturati.", "author": "Rita Levi-Montalcini"},
        {"text": "Qualsiasi cosa sia la creatività, è una parte nella soluzione di un problema.",
         "author": "Brian Aldiss"},
        {"text": "La vera creatività comincia spesso dove termina il linguaggio.",
         "author": "Arthur Koestler"},
        {"text": "Solo ed in cattiva compagnia.", "author": "Unknown"},
        {"text": "Faccio tutto, ma non so niente. Non so niente, ma imparo tutto.",
         "author": "Unknown"},
        {"text": "Le persone si dicono: 'Mi piaci'. Perché non si dicono: 'Ti amo'? Perché l'amore è impegno, coinvolgimento, rischio, responsabilità. L'attrazione è solo momentanea: oggi puoi piacermi, domani no; non c'è rischio in questo. Quando dici ad una persona: 'Ti amo', corri un rischio. Stai affermando: 'Ti amo: continuerò ad amarti, ti amerò anche domani. Puoi dipendere da me, è una promessa'.", "author": "Osho"},
        {"text": "Economista è un retore che insegna come far fallire una birreria in un deserto.",
         "author": "Pietro Bonazza"},
        {"text": "La diversità è un valore, non un problema.", "author": "Unknown"},
        {"text": "Non esistono fatti, ma solo interpretazioni.", "author": "Unknown"},
        {"text": "Non risolvere un problema con la stessa mentalità che l'ha generato.",
         "author": "Einstein"},
        {"text": "L'uomo che cerca di indovinare, di solito perde.", "author": "Unknown"},
        {"text": "Noi esseri umani siamo portati a proiettare il nostro pensiero oltre il presente, sia andando a ritroso nel passato, sia proiettandoci nel futuro.", "author": "Unknown"},
        {"text": "Non pensare di essere sulla strada giusta, soltanto perché è un sentiero battuto.", "author": "Unknown"},
        {"text": "Il vero snob teme di confessare che si annoia quando si annoia e che si diverte quando si diverte.", "author": "Unknown"},
        {"text": "Per estirpare un albero si deve iniziare recidendone le radici.",
         "author": "Proverbio cinese"},
        {"text": "Lei è un'aristocratica, di quelle che non temono contestazioni, perché lei ha la nobiltà impressa nell'animo. Che cos'è un'aristocratica? È una donna che, sebbene circondata dalla volgarità, non ne viene sfiorata.", "author": "L'eleganza del riccio"},
        {"text": "Ero a pranzo. Oggi. Alla ricerca di qualcosa che poteva sorprendermi. Nell'attesa bevevo caffè e fumavo una sigaretta. Vedevo da lontano arrivare un signore nella mia direzione. Aveva all'incirca sessanta anni. Prese una sedia e iniziò a raccontare la sua storia d'amore. All'età di sedici anni conobbe una ragazza. Lei ne aveva quattordici. Iniziarono insieme un'avventura che durò 3 anni. Poi la sorte decise di separarli. Lui partì per il Venezuela e lei rimase a Roma. Con tanto dispiacere continuarono ognuno la propria vita, ma l'amaro che tormentava i loro pensieri quotidiani non li abbandonò. Lei si sposò due volte, e fallì in tutte e due i matrimoni. Il ricordo del suo primo amore non svanì mai. Lo cercava in ogni cosa, in ogni posto. Così prese la decisione di continuare la sua vita sola e in sofferenza. Lui tuttavia si sposò una sola volta, ma non l'amò mai. La ragazza con cui aveva fatto ogni prima esperienza le aveva marchiato il cuore. Passarono 40 anni. Lei un giorno decise di scrivergli una lettera. Lui con il cuore in gola la volle subito incontrare. Fu solo la lontananza a dividerli in tenera età, ma il forte amore viveva il loro ogni giorno. Ora, uniti affrontano il mondo, mano nella mano, amandosi più che mai. Quando provi qualcosa di vero per una persona, non potrai mai smettere di provare, bensì vivrà per sempre in te e tornerà a salvarti. Anime gemelle. In due corpi, un unico cuore.", "author": "Unknown"},
        {"text": "L'illusione di sapere e comprensione che può risultare dall'avere informazioni sempre disponibili, prontamente e senza sforzo.", "author": "Tania Lombrozo"},
        {"text": "Il fatto che così tante persone scelgono di vivere in modi che riducono la comunione di propositi e di destino a pochi altri intorno a sé e di considerare tutto il resto come una minaccia per la propria vita e i propri valori è molto preoccupante, perché è una forma di tribalismo contemporaneo.", "author": "Margaret Levi"},
        {"text": "Un bambino entra nel negozio di un barbiere. Il barbiere parla sottovoce con il cliente: 'Questo è il più stupido bambino che si è mai visto, vuoi vedere??' Il barbiere prende nella mano destra 5 euro e nella sinistra una moneta da 2 euro, poi chiama il bambino e dice: 'Quale vuoi?!?' Il bambino prende la moneta di 2 euro e va a prendere un gelato. 'Vedi?! Che ti ho detto io? Non imparerà mai!' Disse il barbiere al cliente. Appena finito, il cliente esce dal negozio, e vede il bimbo leccando il suo gelato. Gli chiede: 'Ma perché non hai preso i 5 euro invece di prendere 2??' Il bambino risponde mentre lecca il gelato: 'Perché il giorno in cui prenderò 5 euro, il gioco sarà finito..'", "author": "Unknown"},
        {"text": "Accontentiamoci di far riflettere, non tentiamo di convincere.",
         "author": "G. Braque"},
        {"text": "Tutto ciò che amo perde metà del suo piacere se tu non sei lì a dividerlo con me.",
         "author": "Woody Allen"},
        {"text": "Allora tutto il film della mia vita mi è passato davanti agli occhi in un momento! E io non ero nel cast!", "author": "Unknown"},
        {"text": "Che cosa non mi piace della morte? Forse l'ora.", "author": "Unknown"},
        {"text": "Chi è malvagio nel profondo del cuore probabilmente la sa lunga.",
         "author": "Unknown"},
        {"text": "Cos'è bianco-nero-bianco-nero-bianco-nero-bianco-nero-bianco? Una suora che ruzzola dagli scalini.", "author": "Unknown"},
        {"text": "Nulla è vero o falso, ma è il pensarlo che lo rende tale.",
         "author": "Shakespeare"},
        {"text": "L'uomo dice che il tempo passa; il tempo dice che l'uomo passa.",
         "author": "Unknown"},
        {"text": "Difficile non è sapere, ma saper far uso di quello che si sa.",
         "author": "Han Fei Tzu"},
        {"text": "La libertà è la possibilità di dubitare, la possibilità di sbagliare, la possibilità di cercare, di esperimentare, di dire no a una qualsiasi autorità, letteraria artistica filosofica religiosa sociale, e anche politica.", "author": "Ignazio Silone"},
        {"text": "Il brutto di non voler cambiare è il rischio di viversi una vita non a pieno.",
         "author": "Unknown"},
        {"text": "L'anima di una persona è nascosta nel suo sguardo, per questo abbiamo paura di farci guardare negli occhi.", "author": "Jim Morrison"},
        {"text": "La gente vive per anni e anni, ma in realtà è solo in una piccola parte di quegli anni che vive davvero, e cioè negli anni in cui riesce a fare ciò per cui è nata. Allora, lì, è felice. Il resto del tempo è tempo che passa ad aspettare o a ricordare.", "author": "A. Baricco"},
        {"text": "Ogni piccola attenzione che si dà con il cuore può essere un mattone per costruire un grande rapporto.", "author": "Unknown"},
        {"text": "La realtà che ho io per voi è nella forma che voi mi date; ma è realtà per voi e non per me; la realtà che voi avete per me è nella forma che io vi do; ma è realtà per me e non per voi; e per me stesso io non ho altra realtà se non nella forma che riesco a darmi. E come? Ma costruendomi, appunto.", "author": "Luigi Pirandello"},
        {"text": "Preoccupati più della tua coscienza che della reputazione. La tua coscienza è quello che tu sei, la tua reputazione è ciò che gli altri pensano di te. Quello che gli altri pensano di te è un problema loro.", "author": "C. Chaplin"},
        {"text": "Almeno la sera, soprattutto la sera, vorrei incontrare una persona per parlarle, per far circolare le emozioni, darmi aria, scoprire me stesso tramite lei, la mia sensibilità mai formulata se non pallidamente sulla carta. La sera il senso di vuoto, seppure non angoscioso, genera una malinconia superflua e fastidiosa nei miei pensieri, perché la malinconia li blocca su se stessa e li sciupa e da solo non riesco a staccarmene per andare oltre il mio turbamento.", "author": "Aldo Busi"},
        {"text": "Perché come in un gioco, il personaggio a cui si vuol più bene è il mostro. Senza di lui nulla avrebbe più senso.", "author": "Unknown"},
        {"text": "Il lavoro allontana da noi tre grandi mali: la noia, il vizio e il bisogno.",
         "author": "Voltaire"},
        {"text": "Le medesime passioni hanno nell'uomo e nella donna ritmi diversi, per questo i sessi continuano a fraintendersi.", "author": "Nietzsche"},
        {"text": "Anche oggi, come ogni giorno, ho messo da parte un po di tempo per fare un bel niente.",
         "author": "Raymond Carver"},
        {"text": "Realtà: il sogno di un filosofo impazzito.", "author": "A. Bierce"},
        {"text": "Probabilmente, se l'amore non è eterno è perché i ricordi non rimangono veri per sempre, e perché la vita è fatta di un perpetuo rinnovarsi delle cellule.", "author": "Proust"},
        {"text": "Lo capii subito, smisi di cercare la 'ragazza dei sogni'; me ne bastava una che non fosse un incubo.", "author": "Unknown"},
        {"text": "\"Perché continui a dargli corda?\" \"Sono ottimista, magari s'impicca.\"",
         "author": "Unknown"},
        {"text": "Non è la specie più forte a sopravvivere, e nemmeno la più intelligente. Sopravvive la specie più predisposta al cambiamento.", "author": "Unknown"},
        {"text": "Ogni essere umano, nel corso della propria esistenza, può adottare due atteggiamenti: costruire o piantare. I costruttori possono passare anni impegnati nel loro compito, ma presto o tardi concludono quello che stavano facendo. Allora si fermano, e restano lì, limitati dalle loro stesse pareti. Quando la costruzione è finita, la vita perde di significato. Quelli che piantano soffrono con le tempeste e le stagioni, raramente riposano. Ma, al contrario di un edificio, il giardino non cessa mai di crescere. Esso richiede l'attenzione del giardiniere, ma, nello stesso tempo, gli permette di vivere come in una grande avventura.", "author": "Paulo Coelho"},
        {"text": "Avevo vent'anni... Non permetterò a nessuno di dire che questa è la più bella età della vita...",
         "author": "Paul Nizan"},
        {"text": "Che tu possa avere il vento in poppa, che il sole ti risplenda in viso e che il vento del destino ti porti in alto a danzare con le stelle.", "author": "Boston George"},
        {"text": "Inevitabile destino di ogni sognatore è il risveglio.",
            "author": "Unknown"},
        {"text": "Solo quando rinunci ad ogni cosa, né più mete conosci né più brami, né la felicità più a nome chiami, allora al cuor non più l'onda affannosa del tempo arriva, e l'anima tua posa.", "author": "Hermann Hesse"},
        {"text": "Tutti coloro che cadono hanno le ali.", "author": "Anselm Kiefer"},
        {"text": "La fanciullezza è una stanza vuota come l'inizio del mondo.",
         "author": "Anselm Kiefer"},
        {"text": "Per rispetto, ascolto sempre quello che mi dicono. Per coerenza, faccio sempre quello che voglio.",
         "author": "Paul Newman"},
        {"text": "Da un labirinto si esce, da una linea retta no.",
         "author": "Miguel Angel Arcas"},
        {"text": "Mentre l'orchestra di fiori si sgretola, io ballo.", "author": "Unknown"},
        {"text": "Le basse pretese sono quello più ambiziose.", "author": "Luca Scipio"},
        {"text": "Il predatore è sicuro di sé, il dittatore è ansioso di perdere il potere.",
         "author": "Unknown"},
        {"text": "Tutto va preso con moderazione, anche la moderazione.",
         "author": "Oscar Wilde"},
        {"text": "L'unico posto dove si ha solidarieta' verso gli altri e' il bagno.",
         "author": "Unknown"},
        {"text": "Una persona creativa e' pronta a qualsiasi cosa perché sicuramente se lo e' gia' immaginata almeno una volta.", "author": "Unknown"},
        {"text": "Vorrei avere la perseveranza delle mosche.", "author": "Unknown"},
        {"text": "Sono le dieci. E' tutto chiuso qui a L'Aja. Tranne i bordelli. Quelli sono come gli ospedali.", "author": "Unknown"},
        {"text": "Nel porto di Agadir, le luci e la notte. Buena Vista Social Club, vino bianco e pesce.",
         "author": "Sconosciuto"},
        {"text": "Per capire le persone, ascolta ciò che non dicono.",
         "author": "Sconosciuto"},
        {"text": "Puoi prendere il mio cibo, ma non puoi prendere il mio gusto.",
         "author": "Sconosciuto"},
        {"text": "Ti bacerei! Dormirei con te! Ti sposerei anche.",
            "author": "Sconosciuto"},
        {"text": "Ho così tanti difetti che ho dovuto sviluppare diverse abilità per bilanciarli.",
         "author": "Sconosciuto"},
        {"text": "Non capisco perché le donne non apprezzino quando un uomo riesce finalmente a riflettere la loro bellezza.", "author": "Sconosciuto"},
        {"text": "La religione è qualcosa di cui abbiamo davvero bisogno nella nostra vita, come lo yoga, gli sconti e i biscotti.", "author": "Sconosciuto"},
        {"text": "Dopo averti visto, il mio concetto di bellezza è cambiato.",
         "author": "Sconosciuto"},
        {"text": "Se mi ferisci inconsciamente, fa male, ma quando vuoi ferirmi di proposito, non ha alcun effetto.",
         "author": "Sconosciuto"},
        {"text": "Il mondo è uno spazio ad alta dimensionalità. Riduci e goditelo.",
         "author": "Sconosciuto"},
        {"text": "Venezia è una La Mecca per i turisti, una patria perduta per i locali, un'accademia per gli artisti e un orgasmo multiplo per gli amanti della bellezza.", "author": "Sconosciuto"},
        {"text": "Dentro di me ci sono due me. Uno è intelligente e uno è stupido. Quello intelligente deve spiegare a quello stupido come funzionano le cose e lasciargli il merito di spiegarle agli altri.", "author": "Sconosciuto"},
        {"text": "Vivendo con tre ragazze di vent'anni, ho imparato il femminismo, la genitorialità e 'nanana'.",
         "author": "Sconosciuto"},
        {"text": "Un giorno opossum, un giorno colibrì.", "author": "Sconosciuto"},
        {"text": "Amo i modi bruschi che nascondono intenzioni gentili.",
         "author": "Sconosciuto"},
        {"text": "Nel mondo ci sono tre tipi di amici: quelli che ci amano, quelli che ci proteggono e quelli che ci odiano.", "author": "Chamfort"},
        {"text": "I regali sono come i consigli: fanno piacere soprattutto a chi li dà.",
         "author": "E. Henriot"},
        {"text": "Un patrimonio non si improvvisa. Si costruisce.",
            "author": "Sconosciuto"},
        {"text": "Le cattive decisioni fanno migliori storie.",
         "author": "Trovato in Grecia"},
        {"text": "Il fallimento non è definitivo, vincere non è definitivo; conta solo il coraggio di continuare.",
         "author": "Sconosciuto"},
        {"text": "La vita è come andare in bicicletta. Per mantenere l'equilibrio, devi continuare a muoverti.",
         "author": "Albert Einstein"},
        {"text": "Puoi giudicare facilmente il carattere di un uomo dal modo in cui tratta coloro che non possono fare nulla per lui.", "author": "Goethe"},
        {"text": "La verità è sempre incredibile.", "author": "Sconosciuto"},
        {"text": "Perdonami per cercarti così goffamente, dentro di te.",
         "author": "Sconosciuto"},
        {"text": "Fingi finché non riesci.", "author": "Sconosciuto"},
        {"text": "Ingannami una volta, vergogna a te. Ingannami due volte, vergogna a me.",
         "author": "Sconosciuto"},
        {"text": "Vedo la gioia della vita, la gentilezza e le carezze. Questo è per te, amore mio, te lo dovevo e l'ho fatto. Ora sono solo per te. Sono libero dai miei obblighi, possiamo avvicinarci e guardarci dentro. Non ti ho evitato, ti ho protetto. E ora sono solo per te. Anima mia, ti amo.", "author": "Sconosciuto"},
        {"text": "Non reinventare la ruota.", "author": "Sconosciuto"},
        {"text": "Un giorno un uomo bello, elegante e orgoglioso del suo aspetto venne a incontrare Socrate. Socrate gli disse: 'Parla, così potrò vederti.'", "author": "Sconosciuto"},
        {"text": "Ho deciso di essere felice, perché fa bene alla salute.",
         "author": "Voltaire"},
        {"text": "Cambia tutto tranne tua moglie e i tuoi figli.",
            "author": "Sconosciuto"},
        {"text": "Studia la scienza dell'arte. Studia l'arte della scienza. Sviluppa i tuoi sensi—impara soprattutto a vedere. Realizza che tutto è connesso a tutto il resto.", "author": "Leonardo Da Vinci"},
        {"text": "Occhi schiavi, mente affilata come una lama.",
            "author": "Sconosciuto"},
        {"text": "Tuttofare, padrone di nulla.", "author": "Sconosciuto"},
        {"text": "Ero un uomo migliore con te come donna di quanto non lo sia mai stato con una donna da uomo.",
         "author": "Sconosciuto"},
        {"text": "Chi è abituato a viaggiare, come le pecore, sa che è sempre necessario partire un giorno.",
         "author": "L'Alchimista"},
        {"text": "L'ora più buia era quella che veniva prima del sorgere del sole.",
         "author": "L'Alchimista"},
        {"text": "Una ricerca inizia sempre con la Fortuna del Principiante e termina sempre con la Prova del Conquistatore.", "author": "L'Alchimista"},
        {"text": "Allora ci guardiamo e ci amiamo, e io le do vita e calore e lei mi dà una ragione per vivere.",
         "author": "L'Alchimista"},
        {"text": "Tutto ciò che accade una volta potrebbe non accadere mai più. Ma tutto ciò che accade due volte, accadrà certamente una terza.", "author": "L'Alchimista"},
        {"text": "Il talento che hai è il dono che Dio ha fatto a te, ciò che fai con il tuo talento è il dono che fai a Dio.", "author": "L'Alchimista"},
        {"text": "La scienza dice la prima parola su tutto, e l'ultima parola su niente.",
         "author": "Victor Hugo"},
        {"text": "Fino a quando il leone non imparerà a scrivere, ogni storia glorificherà il cacciatore.",
         "author": "Proverbio africano"}
    ],
    'en': [
        {
            "text": "I think the brain is the soul. I don't believe in life after death, much less in a communal-style paradise where I would meet friends, enemies, relatives, and acquaintances again.",
            "author": "Margherita Hack"
        },
        {
            "text": "Men are women who didn't make it.",
            "author": "Unknown"
        },
        {
            "text": "Our patience is unlimited, but not passive and inert.",
            "author": "Antonio Gramsci"
        },
        {
            "text": "Life is not about surviving the storm but about learning to dance in the rain.",
            "author": "Kahlil Gibran"
        },
        {
            "text": "When the game is over, the king and the pawn go back into the same box.",
            "author": "Unknown"
        },
        {
            "text": "Art is magic freed from the lie of truth.",
            "author": "Unknown"
        },
        {
            "text": "There is no greater sorrow than to recall a happy time in misery.",
            "author": "Dante Alighieri"
        },
        {
            "text": "Revolution is always three-quarters fantasy and one-quarter reality.",
            "author": "Bakunin"
        },
        {
            "text": "The passion for destruction is also a creative passion.",
            "author": "Bakunin"
        },
        {
            "text": "You are capable of making me feel excluded from nothing.",
            "author": "Unknown"
        },
        {
            "text": "You are a force of nature.",
            "author": "Unknown"
        },
        {
            "text": "I know nothing, but I like everything.",
            "author": "Paolo Sorrentino"
        },
        {
            "text": "When you know everything, you die soon and alone. You know the unspeakable.",
            "author": "Paolo Sorrentino"
        },
        {
            "text": "The worst solitude is being deprived of sincere friendship.",
            "author": "Francis Bacon"
        },
        {
            "text": "Hope is a good breakfast but a bad supper.",
            "author": "Francis Bacon"
        },
        {
            "text": "Women are mistresses for young men, companions for middle age, and nurses for the old.",
            "author": "Francis Bacon"
        },
        {
            "text": "A man who contemplates revenge keeps his wounds bleeding.",
            "author": "Francis Bacon"
        },
        {
            "text": "I always dreamed of painting a smile, but I never succeeded.",
            "author": "Francis Bacon"
        },
        {
            "text": "Love is a rebellious illness that contains its own cure, in which the sick do not want to heal, and the afflicted do not wish to recover.",
            "author": "Unknown"
        },
        {
            "text": "You are never given a wish without also being given the power to make it come true.",
            "author": "Richard Bach"
        },
        {
            "text": "Each of us is destined for a woman; if we manage to escape her, we are saved.",
            "author": "Unknown"
        },
        {
            "text": "Sometimes the heart sees things that are invisible to the eyes.",
            "author": "Unknown"
        },
        {
            "text": "A smile is almost always caused by another smile.",
            "author": "Unknown"
        },
        {
            "text": "Having a clear conscience is a sign of a bad memory.",
            "author": "Unknown"
        },
        {
            "text": "Try to always get what you love, or you will have to love what you get.",
            "author": "Unknown"
        },
        {
            "text": "God and the soldier are prayed to during famine and war, but when peace comes, God is forgotten, and the soldier is despised.",
            "author": "Unknown"
        },
        {
            "text": "It's incredible how many things you find while looking for something else.",
            "author": "Unknown"
        },
        {
            "text": "To err is human; to blame someone else is even more human.",
            "author": "Unknown"
        },
        {
            "text": "Happiness is never stopping to think about whether you have it.",
            "author": "Unknown"
        },
        {
            "text": "True friends are rare because the demand is low.",
            "author": "Unknown"
        },
        {
            "text": "A kiss is a sweet reunion after a long search.",
            "author": "Unknown"
        },
        {
            "text": "Hard work pays off in the long run. Laziness pays off right away.",
            "author": "Unknown"
        },
        {
            "text": "In love, the important moments are the meeting and the breakup; everything in between is just filler.",
            "author": "Unknown"
        },
        {
            "text": "Intelligence: when you notice your boss's reasoning doesn't make sense. Wisdom: when you avoid pointing it out.",
            "author": "Unknown"
        },
        {
            "text": "Depression is anger without enthusiasm.",
            "author": "Unknown"
        },
        {
            "text": "Flattery is the art of telling someone what they think of themselves.",
            "author": "Unknown"
        },
        {
            "text": "Love overlooks flaws; friendship loves them.",
            "author": "Unknown"
        },
        {
            "text": "Anxiety is like a rocking chair: you're always in motion but never moving forward.",
            "author": "Unknown"
        },
        {
            "text": "Experience is the hardest teacher. It gives you the test first and the lesson afterward.",
            "author": "Unknown"
        },
        {
            "text": "Hypochondria is the only illness I don't have.",
            "author": "Unknown"
        },
        {
            "text": "Better to have a lion leading an army of sheep than a sheep leading an army of lions.",
            "author": "Unknown"
        },
        {
            "text": "Better the joy of a sad smile than the sadness of not knowing how to smile.",
            "author": "Unknown"
        },
        {
            "text": "Don't go to others' funerals; they won't come to yours.",
            "author": "Unknown"
        },
        {
            "text": "I don't pretend to have all the answers. Honestly, I don't even care about all the questions.",
            "author": "Unknown"
        },
        {
            "text": "To hope is to risk disappointment. But risk must be faced, for the greatest risk in life is never taking any. Only those who take risks are free.",
            "author": "Unknown"
        },
        {
            "text": "For the love of the rose, one endures the thorns.",
            "author": "Unknown"
        },
        {
            "text": "What I say and what you hear are not always the same thing.",
            "author": "Unknown"
        },
        {
            "text": "Always remember that you are unique, just like everyone else.",
            "author": "Unknown"
        },
        {
            "text": "If you are not part of the solution, then you are part of the problem.",
            "author": "Unknown"
        },
        {
            "text": "If you are happy, don't shout too loud: sadness is a light sleeper.",
            "author": "Unknown"
        },
        {
            "text": "If everything seems to be coming your way, you are probably in the wrong lane.",
            "author": "Unknown"
        },
        {
            "text": "You can forget the wrongs done to you, but never those you have done.",
            "author": "Unknown"
        },
        {
            "text": "Time for reading, like time for loving, expands time for living.",
            "author": "Daniel Pennac"
        },
        {
            "text": "Those who say it's impossible should not interrupt those who are doing it.",
            "author": "A. Einstein"
        },
        {
            "text": "Man sleeps; only death can awaken him.",
            "author": "Unknown"
        },
        {
            "text": "I am not a poet, but a man with a passion for poetry. I am not a musician, but a man with a passion for music. I am not a master, but a man thirsty for knowledge. I am not an artist, but a man who loves to paint every corner of the earth. I am not a politician, but a man who thinks about the world's problems. For all that I am and all that I am not, one life is not enough. May I have another, please?",
            "author": "Arnoldo Fó"
        },
        {
            "text": "Of what I can be to myself, not only can you know nothing, but neither can I.",
            "author": "L. Pirandello"
        },
        {
            "text": "Everything should be taken in moderation, including moderation.",
            "author": "Oscar Wilde"
        },
        {
            "text": "What surprised me most about Western men is that they lose their health to make money and then lose their money to recover their health. They think so much about the future that they forget to live the present, so they cannot live either the present or the future. They live as if they will never die and die as if they had never lived.",
            "author": "D.L."
        },
        {
            "text": "Can I offer you a drink, or should I just give you money?",
            "author": "Unknown"
        },
        {
            "text": "We must agree on one thing: I have been wronged!",
            "author": "Unknown"
        },
        {
            "text": "An eye for an eye leaves the whole world blind.",
            "author": "Unknown"
        },
        {
            "text": "The modern method of achieving peace of mind is to ask yourself if you're sure the situation is really your problem.",
            "author": "Unknown"
        },
        {
            "text": "If the path before you is clear, you're probably on someone else's.",
            "author": "Unknown"
        },
        {
            "text": "The wise learn from everyone. The average learns from their own mistakes. The fool learns from no one.",
            "author": "Unknown"
        },
        {
            "text": "Do not love what you do not know.",
            "author": "Unknown"
        },
        {"text": "Love must not be the target but the bow.", "author": "Unknown"},
        {"text": "There are no facts, only interpretations.", "author": "Unknown"},
        {"text": "Do not solve a problem with the same mentality that created it.",
         "author": "Einstein"},
        {"text": "The man who tries to guess usually loses.", "author": "Unknown"},
        {"text": "We human beings are inclined to project our thoughts beyond the present, both looking backward to the past and projecting ourselves into the future.", "author": "Unknown"},
        {"text": "Do not think you are on the right path, just because it is a well-trodden path.",
         "author": "Unknown"},
        {"text": "The true snob fears to confess that he is bored when he is bored and that he is enjoying himself when he enjoys himself.", "author": "Unknown"},
        {"text": "To uproot a tree, you must begin by cutting its roots.",
         "author": "Chinese proverb"},
        {"text": "She is an aristocrat, one of those who do not fear objections, because nobility is imprinted in her soul. What is an aristocrat? She is a woman who, though surrounded by vulgarity, is not touched by it.", "author": "The Elegance of the Hedgehog"},
        {"text": "I was having lunch. Today. In search of something that could surprise me. While waiting, I drank coffee and smoked a cigarette. I saw from afar a gentleman approaching in my direction. He was about sixty years old. He took a chair and began to tell his love story. At the age of sixteen, he met a girl. She was fourteen. They started an adventure together that lasted three years. Then fate decided to separate them. He left for Venezuela, and she stayed in Rome. With much sorrow, they continued their lives, but the bitterness tormenting their daily thoughts never left them. She married twice and failed both marriages. The memory of her first love never faded. She looked for it in everything, everywhere. So, she decided to continue her life alone and in pain. However, he married only once but never loved her. The girl with whom he had his first experiences had marked his heart. Forty years passed. One day, she decided to write him a letter. He, with his heart in his throat, immediately wanted to meet her. It was only the distance that separated them at a tender age, but the deep love lived every day in their hearts. Now, united, they face the world hand in hand, loving each other more than ever. When you feel something true for someone, you can never stop feeling it; it will live forever in you and come back to save you. Soulmates. Two bodies, one heart.", "author": "Unknown"},
        {"text": "The illusion of knowing and understanding that comes from having information always available, quickly, and effortlessly.", "author": "Tania Lombrozo"},
        {"text": "The fact that so many people choose to live in ways that reduce shared purpose and destiny to just a few others around them and consider everything else a threat to their life and values is very concerning, because it is a form of contemporary tribalism.", "author": "Margaret Levi"},
        {"text": "A child enters a barber's shop. The barber whispers to the customer: 'This is the dumbest child ever, want to see??' The barber takes 5 euros in his right hand and a 2-euro coin in his left hand, then calls the child and says, 'Which one do you want?!?' The child takes the 2-euro coin and goes to buy an ice cream. 'See?! I told you! He will never learn!' said the barber to the customer. When he finished, the customer went out of the shop and saw the child licking his ice cream. He asked, 'Why didn't you take the 5 euros instead of the 2??' The child replied, licking his ice cream: 'Because the day I take the 5 euros, the game will be over...'", "author": "Unknown"},
        {"text": "Let's settle for making people think, not try to convince them.",
         "author": "G. Braque"},
        {"text": "Everything I love loses half of its pleasure if you are not there to share it with me.",
         "author": "Woody Allen"},
        {"text": "Then the entire movie of my life passed before my eyes in a moment! And I wasn't in the cast!", "author": "Unknown"},
        {"text": "What do I not like about death? Perhaps the hour.", "author": "Unknown"},
        {"text": "Those who are evil deep in their hearts probably know a lot.",
         "author": "Unknown"},
        {"text": "What is white-black-white-black-white-black-white-black? A nun rolling down the stairs.", "author": "Unknown"},
        {"text": "Nothing is true or false, but it is the thinking that makes it so.",
         "author": "Shakespeare"},
        {"text": "Man says that time passes; time says that man passes.",
            "author": "Unknown"},
        {"text": "The difficult thing is not knowing, but knowing how to use what you know.",
         "author": "Han Fei Tzu"},
        {"text": "Freedom is the ability to doubt, the ability to make mistakes, the ability to seek, to experiment, to say no to any authority, literary, artistic, philosophical, religious, social, and even political.", "author": "Ignazio Silone"},
        {"text": "The bad thing about not wanting to change is the risk of living a life not to its fullest.", "author": "Unknown"},
        {"text": "A person's soul is hidden in their gaze, which is why we fear being looked in the eye.",
         "author": "Jim Morrison"},
        {"text": "People live for years and years, but in reality, they truly live only for a small part of those years, in the years when they are able to do what they were born for. Then, there, they are happy. The rest of the time is just time spent waiting or remembering.", "author": "A. Baricco"},
        {"text": "Every small attention given with the heart can be a brick to build a great relationship.", "author": "Unknown"},
        {"text": "The reality I have for you is in the form you give me; but it is reality for you and not for me; the reality you have for me is in the form I give you; but it is reality for me and not for you; and for myself, I have no other reality than in the form I manage to give myself. And how? By building myself, of course.", "author": "Luigi Pirandello"},
        {"text": "Worry more about your conscience than your reputation. Your conscience is what you are; your reputation is what others think of you. What others think of you is their problem.", "author": "C. Chaplin"},
        {"text": "At least in the evening, especially in the evening, I would like to meet someone to talk to, to circulate emotions, to give myself air, to discover myself through them, my sensitivity never fully expressed except faintly on paper. In the evening, the sense of emptiness, though not anguishing, generates an unnecessary and annoying melancholy in my thoughts, because melancholy freezes them and spoils them, and alone I cannot detach myself from it to move beyond my turmoil.", "author": "Aldo Busi"},
        {"text": "Because, like in a game, the character you love the most is the monster. Without him, nothing would make sense.", "author": "Unknown"},
        {"text": "Work keeps three great evils away from us: boredom, vice, and need.",
         "author": "Voltaire"},
        {"text": "The same passions in men and women have different rhythms, which is why the sexes continue to misunderstand each other.", "author": "Nietzsche"},
        {"text": "Even today, like every day, I set aside some time to do nothing.",
         "author": "Raymond Carver"},
        {"text": "Reality: the dream of a mad philosopher.", "author": "A. Bierce"},
        {"text": "Probably, if love is not eternal, it is because memories do not remain true forever, and because life is made of a perpetual renewal of cells.", "author": "Proust"},
        {"text": "I understood right away, I stopped looking for the 'dream girl'; I just needed one who wasn’t a nightmare.", "author": "Unknown"},
        {"text": "\"Why do you keep encouraging him?\" \"I'm optimistic, maybe he'll hang himself.\"", "author": "Unknown"},
        {"text": "It is not the strongest species that survive, nor the most intelligent. The species most able to adapt survives.", "author": "Unknown"},
        {"text": "Every human being, during their life, can adopt two attitudes: to build or to plant. Builders can spend years working on their task, but sooner or later they finish what they were doing. Then they stop and remain there, limited by their own walls. When the building is finished, life loses its meaning. Those who plant suffer with storms and seasons, rarely resting. But, unlike a building, the garden never stops growing. It requires the gardener's attention but also allows them to live as if in a great adventure.", "author": "Paulo Coelho"},
        {"text": "I was twenty... I will not let anyone say that this is the best age of life...",
         "author": "Paul Nizan"},
        {"text": "May you have the wind at your back, the sun shining on your face, and may the winds of destiny carry you far.", "author": "Unknown"},
        {"text": "In the port of Agadir, the lights and the night. Buena Vista Social Club, white wine, and fish.", "author": "Unknown"},
        {"text": "To understand people, listen to what they do not say.",
            "author": "Unknown"},
        {"text": "You can take my food, but you cannot take my taste.",
            "author": "Unknown"},
        {"text": "I would kiss you! I would sleep with you! I would even marry you.",
         "author": "Unknown"},
        {"text": "I have so many flaws that I had to develop several skills to balance them.",
         "author": "Unknown"},
        {"text": "I do not understand why women do not appreciate when a man finally manages to reflect their beauty.", "author": "Unknown"},
        {"text": "Religion is something we really need in our life, like yoga, discounts, and cookies.", "author": "Unknown"},
        {"text": "After seeing you, my concept of beauty has changed.",
            "author": "Unknown"},
        {"text": "If you hurt me unconsciously, that hurts, but when you want to hurt me on purpose, that has no effect.", "author": "Unknown"},
        {"text": "The world is a high-dimensional space. Reduce and enjoy it.",
         "author": "Unknown"},
        {"text": "Venice is a Mecca for tourists, a lost homeland for locals, an academy for artists, and a multiple orgasm for beauty lovers.", "author": "Unknown"},
        {"text": "Inside me, there are two selves. One is smart, and one is stupid. The smart one has to explain things to the stupid one, and the stupid one gets to show off by explaining them to people.", "author": "Unknown"},
        {"text": "By living with three 20-year-old girls, I learned about feminism, parenthood, and 'nanana.'", "author": "Unknown"},
        {"text": "One day opossum, one day hummingbird.", "author": "Unknown"},
        {"text": "I love rough manners concealing gentle intentions.", "author": "Unknown"},
        {"text": "In the world, there are three types of friends: those who love us, those who protect us, and those who hate us.", "author": "Chamfort"},
        {"text": "Gifts are like advice: they please mostly those who give them.",
         "author": "E. Henriot"},
        {"text": "A legacy cannot be improvised. It must be built.", "author": "Unknown"},
        {"text": "Bad decisions make better stories.", "author": "Found in Greece"},
        {"text": "Failure is not definitive, winning is not definitive; only the courage to keep going matters.", "author": "Unknown"},
        {"text": "Life is like riding a bicycle. To keep your balance, you must keep moving.",
         "author": "Albert Einstein"},
        {"text": "You can easily judge the character of a man by how he treats those who can do nothing for him.", "author": "Goethe"},
        {"text": "Truth is always unbelievable.", "author": "Unknown"},
        {"text": "Forgive me for searching for you so clumsily, inside you.",
         "author": "Unknown"},
        {"text": "Fake it till you make it.", "author": "Unknown"},
        {"text": "Fool me once, shame on you. Fool me twice, shame on me.",
            "author": "Unknown"},
        {"text": "I see the joy of life, kindness, and caresses. This is for you, my love, I owed it to you and I did it. Now I am just for you. I am free from my obligations, we can come closer and look inside. I did not avoid you, I protected you. And now I am just for you. My soul, I love you.", "author": "Unknown"},
        {"text": "Do not reinvent the wheel.", "author": "Unknown"},
        {"text": "One day, a handsome, elegant man, proud of his appearance, came to meet Socrates. Socrates said to him: 'Speak so that I may see you.'", "author": "Unknown"},
        {"text": "I have decided to be happy, because it is good for my health.",
         "author": "Voltaire"},
        {"text": "Change everything except your wife and children.", "author": "Unknown"},
        {"text": "Study the science of art. Study the art of science. Develop your senses—especially learn how to see. Realize that everything connects to everything else.", "author": "Leonardo Da Vinci"},
        {"text": "Eyes enslaved, mind as sharp as a razor blade.", "author": "Unknown"},
        {"text": "Jack of all trades, master of none.", "author": "Unknown"},
        {"text": "I was a better man with you as a woman than I ever was with a woman as a man.",
         "author": "Unknown"},
        {"text": "Those accustomed to traveling, like sheep, know that it is always necessary to leave one day.",
         "author": "The Alchemist"},
        {"text": "The darkest hour was the one that came before the sun's birth.",
         "author": "The Alchemist"},
        {"text": "A quest always begins with the Beginner's Luck and always ends with the Conqueror's Test.",
         "author": "The Alchemist"},
        {"text": "Then we gaze at each other and love each other, and I give her life and warmth, and she gives me a reason to live.", "author": "The Alchemist"},
        {"text": "Everything that happens once may never happen again. But everything that happens twice will certainly happen a third time.", "author": "The Alchemist"},
        {"text": "The talent you have is the gift God has given you, what you do with your talent is the gift you give to God.",
         "author": "The Alchemist"},
        {"text": "Science says the first word on everything, and the last word on nothing.",
         "author": "Victor Hugo"},
        {"text": "Until the lion learns how to write, every story will glorify the hunter.",
         "author": "African Proverb"}
    ]}


@ app.route('/')
def home():
    # Get the selected language from the session or default to English
    lang = session.get('lang', 'en')
    return render_template('index.html', language=lang)


@ app.route('/set_language', methods=['POST'])
def set_language():
    """Set the selected language in the session."""
    lang = request.form.get('lang', 'en')
    session['lang'] = lang
    return jsonify({'message': 'Language updated', 'lang': lang})


# @ app.route('/get_aphorisms', methods=['GET'])
# def get_aphorisms():
#     """Get aphorisms for the selected language."""
#     lang = session.get('lang', 'en')
#     return jsonify(aphorisms.get(lang, aphorisms['en']))


# @ app.route('/add_aphorism', methods=['POST'])
# def add_aphorism():
#     """Add a new aphorism to the current language."""
#     lang = session.get('lang', 'en')
#     new_text = request.form.get('aphorism')
#     new_author = request.form.get('author', 'Unknown')

#     if new_text:
#         aphorisms[lang].append({"text": new_text, "author": new_author})
#         return jsonify({'message': 'Aphorism added successfully!'}), 200
#     return jsonify({'message': 'Invalid input.'}), 400


# # Route to add an aphorism
# @app.route('/aphorisms', methods=['POST'])
# def add_aphorism():
#     data = request.json
#     text = data.get('text')
#     author = data.get('author', 'Unknown')

#     if not text:
#         return jsonify({"error": "Aphorism text is required"}), 400

#     aphorism = Aphorism(text=text, author=author)
#     db.session.add(aphorism)
#     db.session.commit()

#     return jsonify(aphorism.to_dict()), 201

# # Route to fetch all aphorisms
# @app.route('/aphorisms', methods=['GET'])
# def get_aphorisms():
#     aphorisms = Aphorism.query.order_by(Aphorism.created_at.desc()).all()
#     return jsonify([a.to_dict() for a in aphorisms])


@ app.route('/get_aphorisms', methods=['GET'])
def get_aphorisms():
    """Get aphorisms for the selected language."""
    lang = session.get('lang', 'en')
    aphorisms[lang] = f"Aphorism_{lang}".query.order_by(
        f"Aphorism_{lang}".created_at.desc()).all()
    return jsonify([a.to_dict() for a in aphorisms[lang]])


@app.route('/add_aphorisms', methods=['POST'])
def add_aphorism():
    try:
        # Parse incoming JSON data
        lang = session.get('lang', 'en')
        data = request.json
        text = data.get('text')
        # Default author if not provided
        author = data.get('author', 'Anonymous')

        if not text:
            return jsonify({"error": "Aphorism text is required"}), 400

        # Create a new aphorism entry
        aphorism = f"Aphorism_{lang}"(text=text, author=author)
        db.session.add(aphorism)
        db.session.commit()

        return jsonify({"message": "Aphorism added successfully!", "aphorism": aphorism.to_dict()}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():  # Ensure the app context is active
        create_tables()      # Create tables
        populate_tables()    # Populate tables
        app.run(debug=True)

    # {"text": "Penso che il cervello sia l'anima, non credo alla vita dopo la morte ne tanto meno a un paradiso in versione condominiale, dove rincontrare amici, nemici, parenti, conoscenti.", "author": "Margherita Hack"},
    # {"text": "Gli uomini sono donne che non ce l'hanno fatta.", "author": "Unknown"},
    # {"text": "La nostra pazienza è illimitata, ma non passiva e inerte.", "author": "Antonio Gramsci"},
    # {"text": "La vita non è una questione di come sopravvivere alla tempesta, ma di come danzare nella pioggia.", "author": "Kahlil Gibran"},
    # {"text": "Finito il gioco il re e il pedone tornano nella stessa scatola.", "author": "Unknown"},
    # {"text": "L'arte è la magia liberata dalla menzogna della verità.", "author": "Unknown"},
    # {"text": "Nessun maggior dolore, che ricordarsi del tempo felice, nella miseria.", "author": "Dante Alighieri"},
    # {"text": "La rivoluzione è sempre per tre quarti fantasia e per un quarto realtà.", "author": "Bakunin"},
    # {"text": "La passione per la distruzione è anche una passione creativa.", "author": "Bakunin"},
    # {"text": "Sei capace di farmi sentire escluso dal niente.", "author": "Unknown"},
    # {"text": "Sei una prepotenza della natura.", "author": "Unknown"},
    # {"text": "Non so niente ma mi piace tutto.", "author": "Paolo Sorrentino"},
    # {"text": "Quando sai tutto muori presto e solo. Sai l'indicibile.", "author": "Paolo Sorrentino"},
    # {"text": "La peggior solitudine è essere privi di un'amicizia sincera.", "author": "Francis Bacon"},
    # {"text": "La speranza è una buona prima colazione, ma è una pessima cena.", "author": "Francis Bacon"},
    # {"text": "Le donne sono amanti per gli uomini giovani, compagne per la mezza età e infermiere per i vecchi.", "author": "Francis Bacon"},
    # {"text": "Un uomo che medita la vendetta, mantiene le sue ferite sempre sanguinanti.", "author": "Francis Bacon"},
    # {"text": "Ho sempre sognato di dipingere il sorriso, ma non ci sono mai riuscito.", "author": "Francis Bacon"},
    # {"text": "L'amore è una malattia ribelle, che ha la sua cura in se stessa, in cui chi è malato non vuole guarirne e chi ne è infermo non desidera riaversi.", "author": "Unknown"},
    # {"text": "Mai ti è dato un desiderio senza che ti sia dato anche il potere di realizzarlo.", "author": "Richard Bach"},
    # {"text": "A ciascuno di noi il fato ha destinato una donna, se riusciamo a sfuggirle siamo salvi.", "author": "Unknown"},
    # {"text": "A volte il cuore vede cose che sono invisibili agli occhi.", "author": "Unknown"},
    # {"text": "A provocare un sorriso è quasi sempre un altro sorriso.", "author": "Unknown"},
    # {"text": "Avere la coscienza pulita è segno di cattiva memoria.", "author": "Unknown"},
    # {"text": "Cerca di ottenere sempre ciò che ami o dovrai accontentarti di amare ciò che ottieni.", "author": "Unknown"},
    # {"text": "Dio e il soldato, durante la carestia e la guerra, vengono pregati, ma quando vi è la pace Dio è dimenticato e il soldato disprezzato.", "author": "Unknown"},
    # {"text": "È incredibile quante cose si trovano mentre cerchi qualcos'altro.", "author": "Unknown"},
    # {"text": "Errare è umano e dare la colpa a un altro è ancora più umano.", "author": "Unknown"},
    # {"text": "Felicitá è non fermarsi mai a pensare se la si ha.", "author": "Unknown"},
    # {"text": "I veri amici sono rari perchè è poca la domanda.", "author": "Unknown"},
    # {"text": "Il bacio è un dolce trovarsi dopo essersi a lungo cercati.", "author": "Unknown"},
    # {"text": "Il lavoro duro paga nel lungo periodo. La pigrizia paga subito.", "author": "Unknown"},
    # {"text": "In amore importanti sono l'incontro e la rottura, tra i due, è solo riempimento.", "author": "Unknown"},
    # {"text": "Intelligenza: quando ti accorgi che il ragionamento del tuo principale non fila. Saggezza: quando eviti di farglielo notare.", "author": "Unknown"},
    # {"text": "La depressione è la rabbia senza entusiasmo.", "author": "Unknown"},
    # {"text": "L'adulazione è l'arte di dire a una persona quello che pensa di sé stessa.", "author": "Unknown"},
    # {"text": "L'amore non vede i difetti, l'amicizia li ama.", "author": "Unknown"},
    # {"text": "L'ansia è come una sedia a dondolo: sei sempre in movimento, ma non avanzi di un passo.", "author": "Unknown"},
    # {"text": "L'esperienza è il tipo di insegnante più difficile. Prima ti fa l'esame, e poi ti spiega la lezione.", "author": "Unknown"},
    # {"text": "L'ipocondria è l'unica malattia che non ho.", "author": "Unknown"},
    # {"text": "Meglio avere un leone a capo di un esercito di pecore, che una pecora a capo di un esercito di leoni.", "author": "Unknown"},
    # {"text": "Meglio la gioia di un sorriso triste che la tristezza di non saper sorridere.", "author": "Unknown"},
    # {"text": "Non andate ai funerali degli altri, tanto loro non verranno al vostro.", "author": "Unknown"},
    # {"text": "Non pretendo di avere tutte le risposte. A dire la verità non m'interessano nemmeno tutte le domande.", "author": "Unknown"},
    # {"text": "Sperare vuol dire rischiare la delusione. Ma il rischio va affrontato perchè il massimo rischio nella vita è di non rischiare mai. Soltanto chi rischia è libero.", "author": "Unknown"},
    # {"text": "Per amore della rosa, si sopportano le spine.", "author": "Unknown"},
    # {"text": "Quello che io dico e quello che tu senti non sono sempre la stessa cosa.", "author": "Unknown"},
    # {"text": "Ricorda sempre che sei unico, esattamente come tutti gli altri.", "author": "Unknown"},
    # {"text": "Se non sei parte della soluzione, allora sei parte del problema.", "author": "Unknown"},
    # {"text": "Se sei felice non gridare troppo: la tristezza ha il sonno leggero.", "author": "Unknown"},
    # {"text": "Se tutto sembra venirti incontro, probabilmente sei nella corsia sbagliata.", "author": "Unknown"},
    # {"text": "Si può dimenticare il male ricevuto, ma quello fatto mai!", "author": "Unknown"},
    # {"text": "Il tempo per leggere, come il tempo per amare, dilata il tempo per vivere...", "author": "Daniel Pennac"},
    # {"text": "Chi dice che è impossibile... non dovrebbe disturbare chi ce la sta facendo.", "author": "A. Einstein"},
    # {"text": "L'uomo dorme, solo la morte potrà svegliarlo.", "author": "Unknown"},
    # {"text": "Io non sono un poeta, sono un uomo con la passione della poesia. Io non sono un musicista, sono un uomo con la passione della musica. Io non sono un maestro, sono un uomo con la sete del sapere. Io non sono un artista, sono un uomo che ama dipingere ogni angolo della terra. Io non sono un politico, sono un uomo che pensa ai problemi del mondo. E per tutto quello che sono e per tutto quello che non sono, una vita sola non basta, Potrei averne un'altra, per favore?", "author": "Arnoldo Fó"},
    # {"text": "Di ciò che posso essere io per me, non solo non potete saper nulla voi, ma nulla neppure io stesso.", "author": "L. Pirandello"},
    # {"text": "Tutto va preso con moderazione, anche la moderazione.", "author": "Oscar Wilde"},
    # {"text": "Quello che mi ha sorpreso di più negli uomini dell'Occidente è che perdono la salute per fare i soldi e poi perdono i soldi per recuperare la salute. Pensano tanto al futuro che dimenticano di vivere il presente in tale maniera che non riescono a vivere né il presente, né il futuro. Vivono come se non dovessero morire mai e muoiono come se non avessero mai vissuto.", "author": "D.L."},
    # {"text": "Posso offrirti qualcosa da bere o vuoi direttamente i soldi??", "author": "Unknown"},
    # {"text": "La creatività del cervello dell'Homo Sapiens si esprime elaborando congegni meccanici semplici e perfetti, così rispondenti allo scopo da non richiedere modifiche, o congegni più rozzi e imperfetti che, per la loro stessa imperfezione, si prestano a essere ristrutturati.", "author": "Rita Levi-Montalcini"},
    # {"text": "Qualsiasi cosa sia la creatività, è una parte nella soluzione di un problema.", "author": "Brian Aldiss"},
    # {"text": "La vera creatività comincia spesso dove termina il linguaggio.", "author": "Arthur Koestler"},
    # {"text": "Solo ed in cattiva compagnia.", "author": "Unknown"},
    # {"text": "Faccio tutto, ma non so niente. Non so niente, ma imparo tutto.", "author": "Unknown"},
    # {"text": "Le persone si dicono: 'Mi piaci'. Perché non si dicono: 'Ti amo'? Perché l'amore è impegno, coinvolgimento, rischio, responsabilità. L'attrazione è solo momentanea: oggi puoi piacermi, domani no; non c'è rischio in questo. Quando dici ad una persona: 'Ti amo', corri un rischio. Stai affermando: 'Ti amo: continuerò ad amarti, ti amerò anche domani. Puoi dipendere da me, è una promessa'.", "author": "Osho"},
    # {"text": "Economista è un retore che insegna come far fallire una birreria in un deserto.", "author": "Pietro Bonazza"},
    # {"text": "La diversità è un valore, non un problema.", "author": "Unknown"},
    # {"text": "Non esistono fatti, ma solo interpretazioni.", "author": "Unknown"},
    # {"text": "Non risolvere un problema con la stessa mentalità che l'ha generato.", "author": "Einstein"},
    # {"text": "L'uomo che cerca di indovinare, di solito perde.", "author": "Unknown"},
    # {"text": "Noi esseri umani siamo portati a proiettare il nostro pensiero oltre il presente, sia andando a ritroso nel passato, sia proiettandoci nel futuro.", "author": "Unknown"},
    # {"text": "Non pensare di essere sulla strada giusta, soltanto perché è un sentiero battuto.", "author": "Unknown"},
    # {"text": "Il vero snob teme di confessare che si annoia quando si annoia e che si diverte quando si diverte.", "author": "Unknown"},
    # {"text": "Per estirpare un albero si deve iniziare recidendone le radici.", "author": "Proverbio cinese"},
    # {"text": "Lei è un'aristocratica, di quelle che non temono contestazioni, perché lei ha la nobiltà impressa nell'animo. Che cos'è un'aristocratica? È una donna che, sebbene circondata dalla volgarità, non ne viene sfiorata.", "author": "L'eleganza del riccio"},
    # {"text": "Ero a pranzo. Oggi. Alla ricerca di qualcosa che poteva sorprendermi. Nell'attesa bevevo caffè e fumavo una sigaretta. Vedevo da lontano arrivare un signore nella mia direzione. Aveva all'incirca sessanta anni. Prese una sedia e iniziò a raccontare la sua storia d'amore. All'età di sedici anni conobbe una ragazza. Lei ne aveva quattordici. Iniziarono insieme un'avventura che durò 3 anni. Poi la sorte decise di separarli. Lui partì per il Venezuela e lei rimase a Roma. Con tanto dispiacere continuarono ognuno la propria vita, ma l'amaro che tormentava i loro pensieri quotidiani non li abbandonò. Lei si sposò due volte, e fallì in tutte e due i matrimoni. Il ricordo del suo primo amore non svanì mai. Lo cercava in ogni cosa, in ogni posto. Così prese la decisione di continuare la sua vita sola e in sofferenza. Lui tuttavia si sposò una sola volta, ma non l'amò mai. La ragazza con cui aveva fatto ogni prima esperienza le aveva marchiato il cuore. Passarono 40 anni. Lei un giorno decise di scrivergli una lettera. Lui con il cuore in gola la volle subito incontrare. Fu solo la lontananza a dividerli in tenera età, ma il forte amore viveva il loro ogni giorno. Ora, uniti affrontano il mondo, mano nella mano, amandosi più che mai. Quando provi qualcosa di vero per una persona, non potrai mai smettere di provare, bensì vivrà per sempre in te e tornerà a salvarti. Anime gemelle. In due corpi, un unico cuore.", "author": "Unknown"},
    # {"text": "L'illusione di sapere e comprensione che può risultare dall'avere informazioni sempre disponibili, prontamente e senza sforzo.", "author": "Tania Lombrozo"},
    # {"text": "Il fatto che così tante persone scelgono di vivere in modi che riducono la comunione di propositi e di destino a pochi altri intorno a sé e di considerare tutto il resto come una minaccia per la propria vita e i propri valori è molto preoccupante, perché è una forma di tribalismo contemporaneo.", "author": "Margaret Levi"},
    # {"text": "Un bambino entra nel negozio di un barbiere. Il barbiere parla sottovoce con il cliente: 'Questo è il più stupido bambino che si è mai visto, vuoi vedere??' Il barbiere prende nella mano destra 5 euro e nella sinistra una moneta da 2 euro, poi chiama il bambino e dice: 'Quale vuoi?!?' Il bambino prende la moneta di 2 euro e va a prendere un gelato. 'Vedi?! Che ti ho detto io? Non imparerà mai!' Disse il barbiere al cliente. Appena finito, il cliente esce dal negozio, e vede il bimbo leccando il suo gelato. Gli chiede: 'Ma perché non hai preso i 5 euro invece di prendere 2??' Il bambino risponde mentre lecca il gelato: 'Perché il giorno in cui prenderò 5 euro, il gioco sarà finito..'", "author": "Unknown"},
    # {"text": "Accontentiamoci di far riflettere, non tentiamo di convincere.", "author": "G. Braque"},
    # {"text": "Tutto ciò che amo perde metà del suo piacere se tu non sei lì a dividerlo con me.", "author": "Woody Allen"},
    # {"text": "Allora tutto il film della mia vita mi è passato davanti agli occhi in un momento! E io non ero nel cast!", "author": "Unknown"},
    # {"text": "Che cosa non mi piace della morte? Forse l'ora.", "author": "Unknown"},
    # {"text": "Chi è malvagio nel profondo del cuore probabilmente la sa lunga.", "author": "Unknown"},
    # {"text": "Cos'è bianco-nero-bianco-nero-bianco-nero-bianco-nero-bianco? Una suora che ruzzola dagli scalini.", "author": "Unknown"},
    # {"text": "Nulla è vero o falso, ma è il pensarlo che lo rende tale.", "author": "Shakespeare"},
    # {"text": "L'uomo dice che il tempo passa; il tempo dice che l'uomo passa.", "author": "Unknown"},
    # {"text": "Difficile non è sapere, ma saper far uso di quello che si sa.", "author": "Han Fei Tzu"},
    # {"text": "La libertà è la possibilità di dubitare, la possibilità di sbagliare, la possibilità di cercare, di esperimentare, di dire no a una qualsiasi autorità, letteraria artistica filosofica religiosa sociale, e anche politica.", "author": "Ignazio Silone"},
    # {"text": "Il brutto di non voler cambiare è il rischio di viversi una vita non a pieno.", "author": "Unknown"},
    # {"text": "L'anima di una persona è nascosta nel suo sguardo, per questo abbiamo paura di farci guardare negli occhi.", "author": "Jim Morrison"},
    # {"text": "La gente vive per anni e anni, ma in realtà è solo in una piccola parte di quegli anni che vive davvero, e cioè negli anni in cui riesce a fare ciò per cui è nata. Allora, lì, è felice. Il resto del tempo è tempo che passa ad aspettare o a ricordare.", "author": "A. Baricco"},
    # {"text": "Ogni piccola attenzione che si dà con il cuore può essere un mattone per costruire un grande rapporto.", "author": "Unknown"},
    # {"text": "La realtà che ho io per voi è nella forma che voi mi date; ma è realtà per voi e non per me; la realtà che voi avete per me è nella forma che io vi do; ma è realtà per me e non per voi; e per me stesso io non ho altra realtà se non nella forma che riesco a darmi. E come? Ma costruendomi, appunto.", "author": "Luigi Pirandello"},
    # {"text": "Preoccupati più della tua coscienza che della reputazione. La tua coscienza è quello che tu sei, la tua reputazione è ciò che gli altri pensano di te. Quello che gli altri pensano di te è un problema loro.", "author": "C. Chaplin"},
    # {"text": "Almeno la sera, soprattutto la sera, vorrei incontrare una persona per parlarle, per far circolare le emozioni, darmi aria, scoprire me stesso tramite lei, la mia sensibilità mai formulata se non pallidamente sulla carta. La sera il senso di vuoto, seppure non angoscioso, genera una malinconia superflua e fastidiosa nei miei pensieri, perché la malinconia li blocca su se stessa e li sciupa e da solo non riesco a staccarmene per andare oltre il mio turbamento.", "author": "Aldo Busi"},
    # {"text": "Perché come in un gioco, il personaggio a cui si vuol più bene è il mostro. Senza di lui nulla avrebbe più senso.", "author": "Unknown"},
    # {"text": "Il lavoro allontana da noi tre grandi mali: la noia, il vizio e il bisogno.", "author": "Voltaire"},
    # {"text": "Le medesime passioni hanno nell'uomo e nella donna ritmi diversi, per questo i sessi continuano a fraintendersi.", "author": "Nietzsche"},
    # {"text": "Anche oggi, come ogni giorno, ho messo da parte un po di tempo per fare un bel niente.", "author": "Raymond Carver"},
    # {"text": "Realtà: il sogno di un filosofo impazzito.", "author": "A. Bierce"},
    # {"text": "Probabilmente, se l'amore non è eterno è perché i ricordi non rimangono veri per sempre, e perché la vita è fatta di un perpetuo rinnovarsi delle cellule.", "author": "Proust"},
    # {"text": "Lo capii subito, smisi di cercare la 'ragazza dei sogni'; me ne bastava una che non fosse un incubo.", "author": "Unknown"},
    # {"text": "\"Perché continui a dargli corda?\" \"Sono ottimista, magari s'impicca.\"", "author": "Unknown"},
    # {"text": "Non è la specie più forte a sopravvivere, e nemmeno la più intelligente. Sopravvive la specie più predisposta al cambiamento.", "author": "Unknown"},
    # {"text": "Ogni essere umano, nel corso della propria esistenza, può adottare due atteggiamenti: costruire o piantare. I costruttori possono passare anni impegnati nel loro compito, ma presto o tardi concludono quello che stavano facendo. Allora si fermano, e restano lì, limitati dalle loro stesse pareti. Quando la costruzione è finita, la vita perde di significato. Quelli che piantano soffrono con le tempeste e le stagioni, raramente riposano. Ma, al contrario di un edificio, il giardino non cessa mai di crescere. Esso richiede l'attenzione del giardiniere, ma, nello stesso tempo, gli permette di vivere come in una grande avventura.", "author": "Paulo Coelho"},
    # {"text": "Avevo vent'anni... Non permetterò a nessuno di dire che questa è la più bella età della vita...", "author": "Paul Nizan"},
    # {"text": "Che tu possa avere il vento in poppa, che il sole ti risplenda in viso e che il vento del destino ti porti in alto a danzare con le stelle.", "author": "Boston George"},
    # {"text": "Inevitabile destino di ogni sognatore è il risveglio.", "author": "Unknown"},
    # {"text": "Solo quando rinunci ad ogni cosa, né più mete conosci né più brami, né la felicità più a nome chiami, allora al cuor non più l'onda affannosa del tempo arriva, e l'anima tua posa.", "author": "Hermann Hesse"},
    # {"text": "Tutti coloro che cadono hanno le ali.", "author": "Anselm Kiefer"},
    # {"text": "La fanciullezza è una stanza vuota come l'inizio del mondo.", "author": "Anselm Kiefer"},
    # {"text": "Per rispetto, ascolto sempre quello che mi dicono. Per coerenza, faccio sempre quello che voglio.", "author": "Paul Newman"},
    # {"text": "Da un labirinto si esce, da una linea retta no.", "author": "Miguel Angel Arcas"},
    # {"text": "Mentre l'orchestra di fiori si sgretola, io ballo.", "author": "Unknown"},
    # {"text": "Le basse pretese sono quello più ambiziose.", "author": "Luca Scipio"},
    # {"text": "Il predatore è sicuro di sé, il dittatore è ansioso di perdere il potere.", "author": "Unknown"},
    # {"text": "Tutto va preso con moderazione, anche la moderazione.", "author": "Oscar Wilde"},
    # {"text": "L'unico posto dove si ha solidarieta' verso gli altri e' il bagno.", "author": "Unknown"},
    # {"text": "Una persona creativa e' pronta a qualsiasi cosa perché sicuramente se lo e' gia' immaginata almeno una volta.", "author": "Unknown"},
    # {"text": "Vorrei avere la perseveranza delle mosche.", "author": "Unknown"},
    # {"text": "Sono le dieci. E' tutto chiuso qui a L'Aja. Tranne i bordelli. Quelli sono come gli ospedali.", "author": "Unknown"},
    # {"text": "Dans le port d'Agadir, les lumières et la nuit. Buena Vista Social Club, du vin blanc et du poisson.", "author": "Unknown"},
    # {"text": "To understand people, listen to what they do not say.", "author": "Unknown"},
    # {"text": "You can take my food but you cannot take my taste.", "author": "Unknown"},
    # {"text": "I would kiss you! I would sleep with you! I would even marry you.", "author": "Unknown"},
    # {"text": "I have so many flaws that I had to develop several skills to balance them.", "author": "Unknown"},
    # {"text": "I do not understand why women do not like when a man finally manages to reflect their beauty.", "author": "Unknown"},
    # {"text": "Religion is something we really need in our life, like yoga, discounts, and cookies.", "author": "Unknown"},
    # {"text": "After seeing you, my concept of beauty has changed.", "author": "Unknown"},
    # {"text": "If you hurt me unconsciously, that hurts, but when you want to hurt me on purpose, that does not have any effect.", "author": "Unknown"},
    # {"text": "The world is a high-dimensional space. Reduce and enjoy it.", "author": "Unknown"},
    # {"text": "Venice is a La Mecca for tourists, a lost homeland for locals, an academy for artists, and a multiple orgasm for beauty lovers.", "author": "Unknown"},
    # {"text": "I have two me in myself. One is smart, and one is stupid. The smart one has to explain the stupid one how things work and let the stupid one show off by explaining them to people.", "author": "Unknown"},
    # {"text": "By living with three 20-year-old girls, I learned about feminism, parenthood, and 'nanana'.", "author": "Unknown"},
    # {"text": "One day opossum, one day hummingbird.", "author": "Unknown"},
    # {"text": "I love rough manners concealing gentle intentions.", "author": "Unknown"},
    # {"text": "En el mundo se tiene tres clases de amigos: los que nos aman, los que nos cuidan y los que nos aborrecen.", "author": "Chamfort"},
    # {"text": "Les cadeaux sont comme les conseils: ils font plaisir surtout à ceux qui les donnent.", "author": "E. Henriot"},
    # {"text": "Un patrimoine, cela ne s'improvise pas. Cela se construit.", "author": "Unknown"},
    # {"text": "Bad decisions make better stories.", "author": "Found in Greece"},
    # {"text": "Failure is not definitive, winning is not definitive only worth the courage to keep on going.", "author": "Unknown"},
    # {"text": "Life is like riding a bike. To keep your balance, you must keep moving.", "author": "Albert Einstein"},
    # {"text": "You can easily judge the character of a man by how he treats those who can do nothing for him.", "author": "Goethe"},
    # {"text": "Truth is always unbelievable.", "author": "Unknown"},
    # {"text": "Perdóname por ir così buscándote tan torpemente, dentro de ti.", "author": "Unknown"},
    # {"text": "Fake it till you make it.", "author": "Unknown"},
    # {"text": "Dupe-moi une fois, honte à toi. Dupe-moi deux fois, honte à moi.", "author": "Unknown"},
    # {"text": "Je voix la joie de la vie, la gentillesse et les caresses. Ça c'est pour toi, mon amour, je te le douvais et je l'ai fait. Maintenant, je suis que pour toi. Je suis libre de mes obligations, on peut se reprocher et regarder dedans. Je ne t'ai pas évite, je t'ai protégé. Et maintenant c'est que pour toi. Mon âme, je t'aime.", "author": "Unknown"},
    # {"text": "Don't create a wheel again.", "author": "Unknown"},
    # {"text": "Un jour un homme beau, élégant et fier de son apparence vint rencontrer Socrate. Socrate lui dit : 'Parle pour que je te vois.'", "author": "Unknown"},
    # {"text": "J'ai décidé d'être heureux, parce que c'est bon pour la santé.", "author": "Voltaire"},
    # {"text": "Changez tout sauf ta femme et tes enfants.", "author": "Unknown"},
    # {"text": "Study the science of art. Study the art of science. Develop your senses—especially learn how to see. Realize that everything connects to everything else.", "author": "Leonardo Da Vinci"},
    # {"text": "Eyes slaved, mind is a razor blade.", "author": "Unknown"},
    # {"text": "Jack of all the subjects, king of none.", "author": "Unknown"},
    # {"text": "I was a better man with you as a woman than I ever was with a woman as a man.", "author": "Unknown"},
    # {"text": "Quien está acostumbrado a viajar, como las ovejas, sabe que siempre es necesario partir un día.", "author": "El Alquimista"},
    # {"text": "La hora más oscura era la que venía antes del nacimiento del sol.", "author": "El Alquimista"},
    # {"text": "Una búsqueda comienza siempre con la Suerte del Principiante y termina siempre con la Prueba del Conquistador.", "author": "El Alquimista"},
    # {"text": "Entonces nos contemplamos y nos queremos, y yo le doy vida y calor y ella me da una razón para vivir.", "author": "El Alquimista"},
    # {"text": "Todo lo que sucede una vez puede que no suceda nunca más. Pero todo lo que sucede dos veces, sucederá, ciertamente, una tercera.", "author": "El Alquimista"},
    # {"text": "El talento que tienes es el regalo que Dios ha hecho a ti, lo que haces con tu talento es el regalo que tú haces a Dios.", "author": "El Alquimista"},
    # {"text": "Science says the first word on everything, and the last word on nothing.", "author": "Victor Hugo"},
    # {"text": "Until the lion learns how to write, every story will glorify the hunter.", "author": "African Proverb"}

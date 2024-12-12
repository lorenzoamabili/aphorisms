from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management (not directly used here)

# List of aphorisms
aphorisms = [
    {"text": "Penso che il cervello sia l'anima, non credo alla vita dopo la morte ne tanto meno a un paradiso in versione condominiale, dove rincontrare amici, nemici, parenti, conoscenti.", "author": "Margherita Hack"},
    {"text": "Gli uomini sono donne che non ce l'hanno fatta.", "author": "Unknown"},
    {"text": "La nostra pazienza è illimitata, ma non passiva e inerte.", "author": "Antonio Gramsci"},
    {"text": "You can easily judge the character of a man by how he treats those who can do nothing for him.", "author": "Goethe"},
    {"text": "Truth is always unbelievable.", "author": "Unknown"},
    {"text": "La vita non è una questione di come sopravvivere alla tempesta, ma di come danzare nella pioggia.", "author": "Kahlil Gibran"},
    {"text": "Perdóname por ir così buscándote tan torpemente, dentro de ti.", "author": "Unknown"},
    {"text": "Fake it till you make it.", "author": "Unknown"},
    {"text": "Don't create a wheel again.", "author": "Unknown"},
    {"text": "Study the science of art. Study the art of science. Develop your senses—especially learn how to see. Realize that everything connects to everything else.", "author": "Leonardo Da Vinci"},
    {"text": "Eyes slaved, mind is a razor blade.", "author": "Unknown"},
    {"text": "Jack of all the subjects, king of none.", "author": "Unknown"},
    {"text": "Quien está acostumbrado a viajar, como las ovejas, sabe que siempre es necesario partir un día.", "author": "El Alquimista"},
    {"text": "La hora más oscura era la que venía antes del nacimiento del sol.", "author": "El Alquimista"},
    {"text": "Una búsqueda comienza siempre con la Suerte del Principiante y termina siempre con la Prueba del Conquistador.", "author": "El Alquimista"},
    {"text": "Entonces nos contemplamos y nos queremos, y yo le doy vida y calor y ella me da una razón para vivir.", "author": "El Alquimista"},
    {"text": "Todo lo que sucede una vez puede que no suceda nunca más. Pero todo lo que sucede dos veces, sucederá, ciertamente, una tercera.", "author": "El Alquimista"},
    {"text": "El talento que tienes es el regalo que Dios ha hecho a ti, lo que haces con tu talento es el regalo que tú haces a Dios.", "author": "El Alquimista"},
    {"text": "Science says the first word on everything, and the last word on nothing.", "author": "Victor Hugo"},
    {"text": "Until the lion learns how to write, every story will glorify the hunter.", "author": "African Proverb"},
    {"text": "Finito il gioco il re e il pedone tornano nella stessa scatola.", "author": "Unknown"},
    {"text": "L'arte è la magia liberata dalla menzogna della verità.", "author": "Unknown"},
    {"text": "Nessun maggior dolore, che ricordarsi del tempo felice, nella miseria.", "author": "Dante Alighieri"},
    {"text": "La rivoluzione è sempre per tre quarti fantasia e per un quarto realtà.", "author": "Bakunin"},
    {"text": "La passione per la distruzione è anche una passione creativa.", "author": "Bakunin"},
    {"text": "La peggior solitudine è essere privi di un'amicizia sincera.", "author": "Francis Bacon"},
    {"text": "La speranza è una buona prima colazione, ma è una pessima cena.", "author": "Francis Bacon"},
    {"text": "Le donne sono amanti per gli uomini giovani, compagne per la mezza età e infermiere per i vecchi.", "author": "Francis Bacon"},
    {"text": "Un uomo che medita la vendetta, mantiene le sue ferite sempre sanguinanti.", "author": "Francis Bacon"},
    {"text": "Ho sempre sognato di dipingere il sorriso, ma non ci sono mai riuscito.", "author": "Francis Bacon"},
    {"text": "L'amore è una malattia ribelle, che ha la sua cura in se stessa, in cui chi è malato non vuole guarirne e chi ne è infermo non desidera riaversi.", "author": "Unknown"},
    {"text": "Mai ti è dato un desiderio senza che ti sia dato anche il potere di realizzarlo.", "author": "Richard Bach"},
    {"text": "A ciascuno di noi il fato ha destinato una donna, se riusciamo a sfuggirle siamo salvi.", "author": "Unknown"},
    {"text": "A volte il cuore vede cose che sono invisibili agli occhi.", "author": "Unknown"},
    {"text": "A provocare un sorriso è quasi sempre un altro sorriso.", "author": "Unknown"},
    {"text": "Avere la coscienza pulita è segno di cattiva memoria.", "author": "Unknown"},
    {"text": "Cerca di ottenere sempre ciò che ami o dovrai accontentarti di amare ciò che ottieni.", "author": "Unknown"},
    {"text": "Dio e il soldato, durante la carestia e la guerra, vengono pregati, ma quando vi è la pace Dio è dimenticato e il soldato disprezzato.", "author": "Unknown"},
    {"text": "È incredibile quante cose si trovano mentre cerchi qualcos'altro.", "author": "Unknown"},
    {"text": "Errare è umano e dare la colpa a un altro è ancora più umano.", "author": "Unknown"},
    {"text": "Felicitá è non fermarsi mai a pensare se la si ha.", "author": "Unknown"},
    {"text": "I veri amici sono rari perchè è poca la domanda.", "author": "Unknown"},
    {"text": "Il bacio è un dolce trovarsi dopo essersi a lungo cercati.", "author": "Unknown"},
    {"text": "Il lavoro duro paga nel lungo periodo. La pigrizia paga subito.", "author": "Unknown"},
    {"text": "In amore importanti sono l'incontro e la rottura, tra i due, è solo riempimento.", "author": "Unknown"},
    {"text": "Intelligenza: quando ti accorgi che il ragionamento del tuo principale non fila. Saggezza: quando eviti di farglielo notare.", "author": "Unknown"},
    {"text": "La depressione è la rabbia senza entusiasmo.", "author": "Unknown"},
    {"text": "L'adulazione è l'arte di dire a una persona quello che pensa di sé stessa.", "author": "Unknown"},
    {"text": "L'amore non vede i difetti, l'amicizia li ama.", "author": "Unknown"},
    {"text": "L'ansia è come una sedia a dondolo: sei sempre in movimento, ma non avanzi di un passo.", "author": "Unknown"},
    {"text": "L'esperienza è il tipo di insegnante più difficile. Prima ti fa l'esame, e poi ti spiega la lezione.", "author": "Unknown"},
    {"text": "L'ipocondria è l'unica malattia che non ho.", "author": "Unknown"},
    {"text": "Meglio avere un leone a capo di un esercito di pecore, che una pecora a capo di un esercito di leoni.", "author": "Unknown"},
    {"text": "Meglio la gioia di un sorriso triste che la tristezza di non saper sorridere.", "author": "Unknown"},
    {"text": "Non andate ai funerali degli altri, tanto loro non verranno al vostro.", "author": "Unknown"},
    {"text": "Non pretendo di avere tutte le risposte. A dire la verità non m'interessano nemmeno tutte le domande.", "author": "Unknown"},
    {"text": "Sperare vuol dire rischiare la delusione. Ma il rischio va affrontato perchè il massimo rischio nella vita è di non rischiare mai. Soltanto chi rischia è libero.", "author": "Unknown"},
    {"text": "Per amore della rosa, si sopportano le spine.", "author": "Unknown"},
    {"text": "Quello che io dico e quello che tu senti non sono sempre la stessa cosa.", "author": "Unknown"},
    {"text": "Ricorda sempre che sei unico, esattamente come tutti gli altri.", "author": "Unknown"},
    {"text": "Se non sei parte della soluzione, allora sei parte del problema.", "author": "Unknown"},
    {"text": "Se sei felice non gridare troppo: la tristezza ha il sonno leggero.", "author": "Unknown"},
    {"text": "Se tutto sembra venirti incontro, probabilmente sei nella corsia sbagliata.", "author": "Unknown"},
    {"text": "Si può dimenticare il male ricevuto, ma quello fatto mai!", "author": "Unknown"},
    {"text": "I was a better man with you as a woman than I ever was with a woman as a man.", "author": "Unknown"},
    {"text": "Il tempo per leggere, come il tempo per amare, dilata il tempo per vivere...", "author": "Daniel Pennac"},
    {"text": "Un jour un homme beau, élégant et fier de son apparence vint rencontrer Socrate. Socrate lui dit : 'Parle pour que je te vois.'", "author": "Unknown"},
    {"text": "Failure is not definitive, winning is not definitive only worth the courage to keep on going.", "author": "Unknown"},
    {"text": "Chi dice che è impossibile... non dovrebbe disturbare chi ce la sta facendo.", "author": "A. Einstein"},
    {"text": "L'uomo dorme, solo la morte potrà svegliarlo.", "author": "Unknown"},
    {"text": "Io non sono un poeta, sono un uomo con la passione della poesia. Io non sono un musicista, sono un uomo con la passione della musica. Io non sono un maestro, sono un uomo con la sete del sapere. Io non sono un artista, sono un uomo che ama dipingere ogni angolo della terra. Io non sono un politico, sono un uomo che pensa ai problemi del mondo. E per tutto quello che sono e per tutto quello che non sono, una vita sola non basta, Potrei averne un'altra, per favore?", "author": "Arnoldo Fó"},
    {"text": "Di ciò che posso essere io per me, non solo non potete saper nulla voi, ma nulla neppure io stesso.", "author": "L. Pirandello"},
    {"text": "Tutto va preso con moderazione, anche la moderazione.", "author": "Oscar Wilde"},
    {"text": "Quello che mi ha sorpreso di più negli uomini dell'Occidente è che perdono la salute per fare i soldi e poi perdono i soldi per recuperare la salute. Pensano tanto al futuro che dimenticano di vivere il presente in tale maniera che non riescono a vivere né il presente, né il futuro. Vivono come se non dovessero morire mai e muoiono come se non avessero mai vissuto.", "author": "D.L."},
    {"text": "Posso offrirti qualcosa da bere o vuoi direttamente i soldi??", "author": "Unknown"},
    {"text": "La creatività del cervello dell'Homo Sapiens si esprime elaborando congegni meccanici semplici e perfetti, così rispondenti allo scopo da non richiedere modifiche, o congegni più rozzi e imperfetti che, per la loro stessa imperfezione, si prestano a essere ristrutturati.", "author": "Rita Levi-Montalcini"},
    {"text": "Qualsiasi cosa sia la creatività, è una parte nella soluzione di un problema.", "author": "Brian Aldiss"},
    {"text": "La vera creatività comincia spesso dove termina il linguaggio.", "author": "Arthur Koestler"},
    {"text": "Solo ed in cattiva compagnia.", "author": "Unknown"},
    {"text": "Le persone si dicono: 'Mi piaci'. Perché non si dicono: 'Ti amo'? Perché l'amore è impegno, coinvolgimento, rischio, responsabilità. L'attrazione è solo momentanea: oggi puoi piacermi, domani no; non c'è rischio in questo. Quando dici ad una persona: 'Ti amo', corri un rischio. Stai affermando: 'Ti amo: continuerò ad amarti, ti amerò anche domani. Puoi dipendere da me, è una promessa'.", "author": "Osho"},
    {"text": "Economista è un retore che insegna come far fallire una birreria in un deserto.", "author": "Pietro Bonazza"},
    {"text": "La diversità è un valore, non un problema.", "author": "Unknown"},
    {"text": "Non esistono fatti, ma solo interpretazioni.", "author": "Unknown"},
    {"text": "Non risolvere un problema con la stessa mentalità che l'ha generato.", "author": "Einstein"},
    {"text": "L'uomo che cerca di indovinare, di solito perde.", "author": "Unknown"},
    {"text": "Noi esseri umani siamo portati a proiettare il nostro pensiero oltre il presente, sia andando a ritroso nel passato, sia proiettandoci nel futuro.", "author": "Unknown"},
    {"text": "Non pensare di essere sulla strada giusta, soltanto perché è un sentiero battuto.", "author": "Unknown"},
    {"text": "Il vero snob teme di confessare che si annoia quando si annoia e che si diverte quando si diverte.", "author": "Unknown"},
    {"text": "Changez tout sauf ta femme et tes enfants.", "author": "Unknown"},
    {"text": "Per estirpare un albero si deve iniziare recidendone le radici.", "author": "Proverbio cinese"},
    {"text": "Esaltazione della tua personalità", "author": "Unknown"},
    {"text": "Lei è un'aristocratica, di quelle che non temono contestazioni, perché lei ha la nobiltà impressa nell'animo. Che cos'è un'aristocratica? È una donna che, sebbene circondata dalla volgarità, non ne viene sfiorata.", "author": "L'eleganza del riccio"},
    {"text": "Ero a pranzo. Oggi. Alla ricerca di qualcosa che poteva sorprendermi. Nell'attesa bevevo caffè e fumavo una sigaretta. Vedevo da lontano arrivare un signore nella mia direzione. Aveva all'incirca sessanta anni. Prese una sedia e iniziò a raccontare la sua storia d'amore. All'età di sedici anni conobbe una ragazza. Lei ne aveva quattordici. Iniziarono insieme un'avventura che durò 3 anni. Poi la sorte decise di separarli. Lui partì per il Venezuela e lei rimase a Roma. Con tanto dispiacere continuarono ognuno la propria vita, ma l'amaro che tormentava i loro pensieri quotidiani non li abbandonò. Lei si sposò due volte, e fallì in tutte e due i matrimoni. Il ricordo del suo primo amore non svanì mai. Lo cercava in ogni cosa, in ogni posto. Così prese la decisione di continuare la sua vita sola e in sofferenza. Lui tuttavia si sposò una sola volta, ma non l'amò mai. La ragazza con cui aveva fatto ogni prima esperienza le aveva marchiato il cuore. Passarono 40 anni. Lei un giorno decise di scrivergli una lettera. Lui con il cuore in gola la volle subito incontrare. Fu solo la lontananza a dividerli in tenera età, ma il forte amore viveva il loro ogni giorno. Ora, uniti affrontano il mondo, mano nella mano, amandosi più che mai. Quando provi qualcosa di vero per una persona, non potrai mai smettere di provare, bensì vivrà per sempre in te e tornerà a salvarti. Anime gemelle. In due corpi, un unico cuore.", "author": "Unknown"},
    {"text": "L'illusione di sapere e comprensione che può risultare dall'avere informazioni sempre disponibili, prontamente e senza sforzo.", "author": "Tania Lombrozo"},
    {"text": "Il fatto che così tante persone scelgono di vivere in modi che riducono la comunione di propositi e di destino a pochi altri intorno a sé e di considerare tutto il resto come una minaccia per la propria vita e i propri valori è molto preoccupante, perché è una forma di tribalismo contemporaneo.", "author": "Margaret Levi"},
    {"text": "Un bambino entra nel negozio di un barbiere. Il barbiere parla sottovoce con il cliente: 'Questo è il più stupido bambino che si è mai visto, vuoi vedere??' Il barbiere prende nella mano destra 5 euro e nella sinistra una moneta da 2 euro, poi chiama il bambino e dice: 'Quale vuoi?!?' Il bambino prende la moneta di 2 euro e va a prendere un gelato. 'Vedi?! Che ti ho detto io? Non imparerà mai!' Disse il barbiere al cliente. Appena finito, il cliente esce dal negozio, e vede il bimbo leccando il suo gelato. Gli chiede: 'Ma perché non hai preso i 5 euro invece di prendere 2??' Il bambino risponde mentre lecca il gelato: 'Perché il giorno in cui prenderò 5 euro, il gioco sarà finito..'", "author": "Unknown"},
    {"text": "Accontentiamoci di far riflettere, non tentiamo di convincere.", "author": "G. Braque"},
    {"text": "Tutto ciò che amo perde metà del suo piacere se tu non sei lì a dividerlo con me.", "author": "Woody Allen"},
    {"text": "Allora tutto il film della mia vita mi è passato davanti agli occhi in un momento! E io non ero nel cast!", "author": "Unknown"},
    {"text": "Che cosa non mi piace della morte? Forse l'ora.", "author": "Unknown"},
    {"text": "Chi è malvagio nel profondo del cuore probabilmente la sa lunga.", "author": "Unknown"},
    {"text": "Cos'è bianco-nero-bianco-nero-bianco-nero-bianco-nero-bianco? Una suora che ruzzola dagli scalini.", "author": "Unknown"},
    {"text": "Nulla è vero o falso, ma è il pensarlo che lo rende tale.", "author": "Shakespeare"},
    {"text": "L'uomo dice che il tempo passa; il tempo dice che l'uomo passa.", "author": "Unknown"},
    {"text": "Difficile non è sapere, ma saper far uso di quello che si sa.", "author": "Han Fei Tzu"},
    {"text": "La libertà è la possibilità di dubitare, la possibilità di sbagliare, la possibilità di cercare, di esperimentare, di dire no a una qualsiasi autorità, letteraria artistica filosofica religiosa sociale, e anche politica.", "author": "Ignazio Silone"},
    {"text": "Dupe-moi une fois, honte à toi. Dupe-moi deux fois, honte à moi.", "author": "Unknown"},
    {"text": "L'anima di una persona è nascosta nel suo sguardo, per questo abbiamo paura di farci guardare negli occhi.", "author": "Jim Morrison"},
    {"text": "La gente vive per anni e anni, ma in realtà è solo in una piccola parte di quegli anni che vive davvero, e cioè negli anni in cui riesce a fare ciò per cui è nata. Allora, lì, è felice. Il resto del tempo è tempo che passa ad aspettare o a ricordare.", "author": "A. Baricco"},
    {"text": "Ogni piccola attenzione che si dà con il cuore può essere un mattone per costruire un grande rapporto.", "author": "Unknown"},
    {"text": "La realtà che ho io per voi è nella forma che voi mi date; ma è realtà per voi e non per me; la realtà che voi avete per me è nella forma che io vi do; ma è realtà per me e non per voi; e per me stesso io non ho altra realtà se non nella forma che riesco a darmi. E come? Ma costruendomi, appunto.", "author": "Luigi Pirandello"},
    {"text": "Preoccupati più della tua coscienza che della reputazione. La tua coscienza è quello che tu sei, la tua reputazione è ciò che gli altri pensano di te. Quello che gli altri pensano di te è un problema loro.", "author": "C. Chaplin"},
    {"text": "Almeno la sera, soprattutto la sera, vorrei incontrare una persona per parlarle, per far circolare le emozioni, darmi aria, scoprire me stesso tramite lei, la mia sensibilità mai formulata se non pallidamente sulla carta. La sera il senso di vuoto, seppure non angoscioso, genera una malinconia superflua e fastidiosa nei miei pensieri, perché la malinconia li blocca su se stessa e li sciupa e da solo non riesco a staccarmene per andare oltre il mio turbamento.", "author": "Aldo Busi"},
    {"text": "Il lavoro allontana da noi tre grandi mali: la noia, il vizio e il bisogno.", "author": "Voltaire"},
    {"text": "Le medesime passioni hanno nell'uomo e nella donna ritmi diversi, per questo i sessi continuano a fraintendersi.", "author": "Nietzsche"},
    {"text": "Anche oggi, come ogni giorno, ho messo da parte un po di tempo per fare un bel niente.", "author": "Raymond Carver"},
    {"text": "Realtà: il sogno di un filosofo impazzito.", "author": "A. Bierce"},
    {"text": "J'ai décidé d'être heureux, parce que c'est bon pour la santé.", "author": "Voltaire"},
    {"text": "Probabilmente, se l'amore non è eterno è perché i ricordi non rimangono veri per sempre, e perché la vita è fatta di un perpetuo rinnovarsi delle cellule.", "author": "Proust"},
    {"text": "Lo capii subito, smisi di cercare la 'ragazza dei sogni'; me ne bastava una che non fosse un incubo.", "author": "Unknown"},
    {"text": "\"Perché continui a dargli corda?\" \"Sono ottimista, magari s'impicca.\"", "author": "Unknown"},
    {"text": "Non è la specie più forte a sopravvivere, e nemmeno la più intelligente. Sopravvive la specie più predisposta al cambiamento.", "author": "Unknown"},
    {"text": "Ogni essere umano, nel corso della propria esistenza, può adottare due atteggiamenti: costruire o piantare. I costruttori possono passare anni impegnati nel loro compito, ma presto o tardi concludono quello che stavano facendo. Allora si fermano, e restano lì, limitati dalle loro stesse pareti. Quando la costruzione è finita, la vita perde di significato. Quelli che piantano soffrono con le tempeste e le stagioni, raramente riposano. Ma, al contrario di un edificio, il giardino non cessa mai di crescere. Esso richiede l'attenzione del giardiniere, ma, nello stesso tempo, gli permette di vivere come in una grande avventura.", "author": "Paulo Coelho"},
    {"text": "En el mundo se tiene tres clases de amigos: los que nos aman, los que nos cuidan y los que nos aborrecen.", "author": "Chamfort"},
    {"text": "Avevo vent'anni... Non permetterò a nessuno di dire che questa è la più bella età della vita...", "author": "Paul Nizan"},
    {"text": "Che tu possa avere il vento in poppa, che il sole ti risplenda in viso e che il vento del destino ti porti in alto a danzare con le stelle.", "author": "Boston George"},
    {"text": "Inevitabile destino di ogni sognatore è il risveglio.", "author": "Unknown"},
    {"text": "Les cadeaux sont comme les conseils: ils font plaisir surtout à ceux qui les donnent.", "author": "E. Henriot"},
    {"text": "Solo quando rinunci ad ogni cosa, né più mete conosci né più brami, né la felicità più a nome chiami, allora al cuor non più l'onda affannosa del tempo arriva, e l'anima tua posa.", "author": "Hermann Hesse"},
    {"text": "Un patrimoine, cela ne s'improvise pas. Cela se construit.", "author": "Unknown"},
    {"text": "Bad decisions make better stories.", "author": "Found in Greece"},
    {"text": "Tutti coloro che cadono hanno le ali.", "author": "Anselm Kiefer"},
    {"text": "La fanciullezza è una stanza vuota come l'inizio del mondo.", "author": "Anselm Kiefer"},
    {"text": "Life is like riding a bike. To keep your balance, you must keep moving.", "author": "Albert Einstein"},
    {"text": "Per rispetto, ascolto sempre quello che mi dicono. Per coerenza, faccio sempre quello che voglio.", "author": "Paul Newman"},
    {"text": "Da un labirinto si esce, da una linea retta no.", "author": "Miguel Angel Arcas"},
    {"text": "Mentre l'orchestra di fiori si sgretola, io ballo.", "author": "Unknown"},
    {"text": "Le basse pretese sono quello più ambiziose.", "author": "Luca Scipio"},
    {"text": "Il predatore è sicuro di sé, il dittatore è ansioso di perdere il potere.", "author": "Unknown"},
    {"text": "Tutto va preso con moderazione, anche la moderazione.", "author": "Oscar Wilde"},
    {"text": "L'unico posto dove si ha solidarieta' verso gli altri e' il bagno.", "author": "Unknown"},
    {"text": "Una persona creativa e' pronta a qualsiasi cosa perché sicuramente se lo e' gia' immaginata almeno una volta.", "author": "Unknown"},
    {"text": "Vorrei avere la perseveranza delle mosche.", "author": "Unknown"},
    {"text": "Sono le dieci. E' tutto chiuso qui a L'Aja. Tranne i bordelli. Quelli sono come gli ospedali.", "author": "Unknown"},
    {"text": "Dans le port d'Agadir, les lumières et la nuit. Buena Vista Social Club, du vin blanc et du poisson.", "author": "Unknown"},
    {"text": "Je voix la joie de la vie, la gentillesse et les caresses. Ça c'est pour toi, mon amour, je te le douvais et je l'ai fait. Maintenant, je suis que pour toi. Je suis libre de mes obligations, on peut se reprocher et regarder dedans. Je ne t'ai pas évite, je t'ai protégé. Et maintenant c'est que pour toi. Mon âme, je t'aime.", "author": "Unknown"},
    {"text": "Il brutto di non voler cambiare è il rischio di viversi una vita non a pieno.", "author": "Unknown"},
    {"text": "To understand people, listen to what they do not say.", "author": "Unknown"},
    {"text": "You can take my food but you cannot take my taste.", "author": "Unknown"},
    {"text": "I would kiss you! I would sleep with you! I would even marry you.", "author": "Unknown"},
    {"text": "I have so many flaws that I had to develop several skills to balance them.", "author": "Unknown"},
    {"text": "I do not understand why women do not like when a man finally manages to reflect their beauty.", "author": "Unknown"},
    {"text": "Religion is something we really need in our life, like yoga, discounts, and cookies.", "author": "Unknown"},
    {"text": "After seeing you, my concept of beauty has changed.", "author": "Unknown"},
    {"text": "If you hurt me unconsciously, that hurts, but when you want to hurt me on purpose, that does not have any effect.", "author": "Unknown"},
    {"text": "The world is a high-dimensional space. Reduce and enjoy it.", "author": "Unknown"},
    {"text": "Venice is a La Mecca for tourists, a lost homeland for locals, an academy for artists, and a multiple orgasm for beauty lovers.", "author": "Unknown"},
    {"text": "Perché come in un gioco, il personaggio a cui si vuol più bene è il mostro. Senza di lui nulla avrebbe più senso.", "author": "Unknown"},
    {"text": "I have two me in myself. One is smart, and one is stupid. The smart one has to explain the stupid one how things work and let the stupid one show off by explaining them to people.", "author": "Unknown"},
    {"text": "Non so niente, ma imparo tutto.", "author": "Unknown"},
    {"text": "Faccio tutto, ma non so niente.", "author": "Unknown"},
    {"text": "By living with three 20-year-old girls, I learned about feminism, parenthood, and 'nanana'.", "author": "Unknown"},
    {"text": "One day opossum, one day hummingbird.", "author": "Unknown"},
    {"text": "I love rough manners concealing gentle intentions.", "author": "Unknown"},
    {"text": "Sei capace di farmi sentire escluso dal niente.", "author": "Unknown"},
    {"text": "Sei una prepotenza della natura.", "author": "Unknown"},
    {"text": "Non so niente ma mi piace tutto.", "author": "Paolo Sorrentino"},
    {"text": "Quando sai tutto muori presto e solo. Sai l'indicibile.", "author": "Paolo Sorrentino"}
]

@app.route('/')
def home():
    message = "Welcome to my Flask app!"
    return render_template('index.html', message=message)

@app.route('/get_random_aphorism', methods=['GET'])
def get_random_aphorism():
    """API to get a random aphorism."""
    random_aphorism = random.choice(aphorisms)
    return jsonify(random_aphorism)

@app.route('/add_aphorism', methods=['POST'])
def add_aphorism():
    """API to add a new aphorism."""
    new_text = request.form.get('aphorism')
    new_author = request.form.get('author', 'Unknown')

    if new_text:
        aphorisms.append({"text": new_text, "author": new_author})
        return jsonify({'message': 'Aphorism added successfully!'}), 200
    return jsonify({'message': 'Invalid input.'}), 400

if __name__ == '__main__':
    app.run()
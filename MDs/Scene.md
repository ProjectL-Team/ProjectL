# Szenendesign

Hier sind ist eine Komplettübersicht, wie man Szenen in EngineL erstellt und nutzt und was man mit
ihnen erzeugen kann.

Jede Szene ist in einer XML-Datei im Unterordner `Resources/Scenes` abgelegt und wird von dort
abgerufen. Möchte man aus dem Spiel heraus eine Szene aufrufen, muss man zuerst das Szenen-Modul
importieren und dann die Szene erstellen und starten:

    import Source.EngineL.Scene as Scene

    Scene.XMLScene("Test", player).play()

Dieser Quellcode würde dann die Szene in `Resources/Scenes/Text.xml` starten. Wenn man eine Szene
startet, muss allerdings auch immer bekannt sein, wer der Spieler ist, daher ist es eigentlich am
besten, wenn man Szenen immer in Event-Handlern wie `Core.Entity.on_transfer` oder ähnlichen startet,
da der Spieler dann erstens weiß, warum die Szene jetzt startet, und zweitens, weil immer eine
Referenz zum Spieler-Objekt verfügbar ist.

Die Szenen-Dateien sind wie folgend aufgebaut:

    <?xml version='1.0' encoding='UTF-8'?>
    <scene>
        <text>"Hallo Du!"</text>
        <delay time="1500" />
        <text>"Hallo zurück!"</text>
    </scene>

Innerhalb des Wurzel-Elements sind mehrere Elemente vorhanden, die nacheinander abgearbeitet werden.
Das obere Beispiel würde zuerst `"Hallo Du!"` ausgeben, anderthalb Sekunden warten und dann `"Hallo
zurück!"` schreiben.

## verfügbare Elemente

### `<text>`

Das `<text>`-Element ist wohl das einfachste verfügbare Element einer Szene. Es fängt mit einem Tag
an und hört mit einem geschlossenen Tag auf und gibt den Text zwischen den beiden Tags aus:

    <text>foo bar!</text>

    Ausgabe:
    foo bar!

### `<delay>`

Mit `<delay>` lassen sich zeitliche Verzögerungen einbauen, um dem Spieler zum Beispiel Zeit zum
Lesen zu geben. Es benötigt nur ein Attribut: `time`. Diesem Attribut muss man die Wartezeit in
Millisekunden angeben.

    <delay time="1000" />

    Verzögerung von einer Sekunde.

### `<choice>`

Möchte man dem Spieler die Wahl über den weiteren Verlauf der Szene geben, ist das `<choice>`-Element
die richtige Wahl, sein Aufbau ist aber etwas komplizierter als der der oberen Elemente:

    <choice>
        <option text="Option 1">
            <text>Sie haben Option 1 gewählt!</text>
        </option>
        <option text="Option 2">
            <text>Sie haben Option 2 gewählt!</text>
        </option
    </choice>

Innerhalb der `<choice>`-Tags gibt man die einzelnen Optionen an, die jeweils als Attribut den Text
annehmen, der auf den Knöpfen stehen soll. Wird eine der Optionen ausgewählt, werden die Elemente
innerhalb der gewählten `<option>`-Tags ausgeführt. Sind diese abgearbeitet, fährt die Szene mit
den Elementen nach dem `<choice>`-Tags fort.

### `<transfer>`

Man kann innerhalb einer Szene auch Gegenstände verschieben, dies wird mit dem `<transfer>`-Tag
realisiert:

    <transfer subject="foo" target="bar">
        <noSubject>
            <text>Es gibt kein foo!</text>
        </noSubject>
        <noTarget>
            <text>Es gibt kein bar!</text>
        </noTarget>
        <noTransfer>
            <text>Foo kann nicht nach bar verschoben werden!</text>
        </noTransfer>
    </transfer>

Dieser Aufbau verschiebt den Gegenstand mit dem Namen "foo" auf den Gegenstand mit dem Namen "bar", nach
diesen Gegenständen wird immer weltweit gesucht, dass heißt, dass auch Gegenstände verschoben werden
können, die an einem komplett anderen Ort sind.

Natürlich kann es auch vorkommen, dass eins der beiden Gegenstände nicht gefunden wird oder der
Transfer einfach nicht möglich ist. Für diesen Fall gibt es die `<noSubject>`, `<noTarget>` und
`<noTransfer>`-Tags. Tritt ein solcher Sonderfall auf, werden die Elemente innerhalb dieser Tags
ausgeführt. Sind die Tags nicht vorhanden, obwohl sie benötigt werden, stürzt das Spiel ab.

### `<spawn>`

Es ist sogar möglich. komplett neue Gegenstände zu erstellen:

    <spawn class="Entity" target="foo">
        <noTarget>
            <text>Es gibt kein foo!</text>
        </noTarget>
    </spawn>

Dem `<spawn>`-Element wird die Klasse des neuen Gegenstandes und dessen zukünftiger Vater übergeben.
Die Klasse muss natürlich registriert sein, ist sie das nicht, stürzt das Spiel ab. Die `<noTarget>`-Tags
erfüllen auch hier den gleichen Zweck wie in `<transfer>`.

### `<changeState>`

Zu guter Letzt kann man auch Zustände von Gegenständen ändern:

    <changeState subject="foo" state="bar" value="42">
        <noSubject>
            <text>Es gibt kein foo!</text>
        </noSubject>
    </changeState>

Die Funktionsweise ähnelt den oberen Elementen sehr: Man muss das Ziel, den Status, den man ändern
möchte, und den neuen Wert angeben. Wird das Ziel nicht gefunden, werden die Elemente in `<noTarget>`
ausgeführt. Eine Besonderheit ist noch, dass der Wert sich zu einer Ganzzahl umformen lassen muss,
da ansonsten das Spiel abstürzt.
import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.CardDelegate {
    id: unknownUtterance
    skillBackgroundColorOverlay: "#000000"
    cardBackgroundOverlayColor: "#000000"

    contentItem: Rectangle {
        color: "black"

        ColumnLayout {
            anchors.fill: parent

            Mycroft.AutoFitLabel {
                id: utteranceLabel
                wrapMode: Text.Wrap
                Layout.fillWidth: true
                Layout.fillHeight: true
                font.family: "Noto Sans"
                font.weight: Font.Bold
                text: qsTr("I Heard:")
            }

            Mycroft.AutoFitLabel {
                id: unhandledUtterance
                wrapMode: Text.Wrap
                font.family: "Noto Sans"
                Layout.fillWidth: true
                Layout.fillHeight: true
                font.weight: Font.Bold
                text: sessionData.utterance
            }
        }
    }
}
 

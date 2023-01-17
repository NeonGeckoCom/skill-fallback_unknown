import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    leftPadding: 0
    rightPadding: 0
    topPadding: 0
    bottomPadding: 0

    Rectangle {
        anchors.fill: parent
        // Setting margins that need to be left for the screen edges
        anchors.margins: Mycroft.Units.gridUnit * 2

        //Setting a background dim using our primary theme / background color on top of our skillBackgroundSource image for better readability and contrast
        color: Qt.rgba(Kirigami.Theme.backgroundColor.r, Kirigami.Theme.backgroundColor.g, Kirigami.Theme.backgroundColor.b, 0.3)

        ColumnLayout {
            anchors.fill: parent
            Mycroft.AutoFitLabel {
                id: utteranceLabel
                wrapMode: Text.Wrap
                Layout.fillWidth: true
                Layout.preferredHeight: Mycroft.Units.gridUnit * 8
                font.family: "Noto Sans"
                font.weight: Font.Bold
                text: qsTr("I Heard:")
            }

            Mycroft.AutoFitLabel {
                id: unhandledUtterance
                wrapMode: Text.Wrap
                font.family: "Noto Sans"
                Layout.fillWidth: true
                Layout.preferredHeight: Mycroft.Units.gridUnit * 4
                font.weight: Font.Bold
                text: sessionData.utterance
            }
        }
    }
}
 

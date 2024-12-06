// Copyright (C) 2024 twyleg
import QtQuick 2.15

SliderSpinBox {
    id: sliderSpinBoxFading

    property alias duration: opacityAnimation.duration

    ticksOpacity: 0.0

    MouseArea {
        id: mouseArea

        anchors.fill: parent

        hoverEnabled: true
        acceptedButtons: Qt.NoButton

        onEntered: sliderSpinBoxFading.fadeIn()
        onExited: sliderSpinBoxFading.fadeOut()
    }

    PropertyAnimation {
        id: opacityAnimation

        target: sliderSpinBoxFading
        property: "ticksOpacity"
        duration: 500
    }

    function fadeIn() {
        opacityAnimation.from = sliderSpinBoxFading.ticksOpacity
        opacityAnimation.to = 1.0
        opacityAnimation.restart()
    }

    function fadeOut() {
        opacityAnimation.from = sliderSpinBoxFading.ticksOpacity
        opacityAnimation.to = 0.0
        opacityAnimation.restart()
    }
}

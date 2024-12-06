// Copyright (C) 2024 twyleg
import QtQuick 2.0

Item {
    id: sidebarAppView

    enum Alignment {
        Top,
        Bottom
    }

    default property alias data: content.data
    property alias viewProperties: properties

    anchors.fill: parent
    visible: false

    SidebarAppViewProperties {
        id: properties
    }

    Item {
        id: content

        anchors.fill: parent
        anchors.margins: 5
    }

    Component.onCompleted: {
        if(properties.background) {
            properties.background.parent = sidebarAppView
            properties.background.z = -1
            properties.background.anchors.fill = sidebarAppView
        }
    }

}

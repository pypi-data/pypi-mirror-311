// Copyright (C) 2024 twyleg
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs // No version required/possible


Item {
    id: appView

    default property alias data: content.data
    property alias content: content
    property SidebarAppView activeView
    property SidebarAppView defaultView

    signal closeViewRequested(view: SidebarAppView)

    NavigationSidebar {
        id: navigationSidebar

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left

        onActivateViewRequested: (view) => handleActivateViewRequest(view)
        onCloseViewRequested: (view) => handleCloseViewRequest(view)
    }

    Item {
        id: content

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: navigationSidebar.right
        anchors.right: parent.right
    }

    MessageDialog {
        id: closeConfirmationDialog

        property SidebarAppView pendingViewToClose

        title: "Confirm Close"
        buttons: MessageDialog.Yes | MessageDialog.No

        onAccepted: {
            if (pendingViewToClose) {
                closeView(pendingViewToClose)
            }
            pendingViewToClose = null
        }

        onRejected: {
            console.debug("Close view request canceled by the user")
            pendingViewToClose = null
        }

        function openDialog(view) {
            text = `Are you sure you want to close:<br><b>"${view.viewProperties.name}"</b>`
            pendingViewToClose = view
            open()
        }
    }

    Component.onCompleted: {
        for (var i=0; i<content.data.length; i++) {
            var child = content.data[i]
            if (child instanceof SidebarAppView) {
                var view = child
                addView(view)
            }
        }
        handleActivateViewRequest(defaultView)
    }

    function addView(view) {
        console.debug(`Adding view: name=${view.viewProperties.name}`)
        navigationSidebar.addButton(view)

        if (defaultView === null) {
            console.debug("No default view specified, promoting this view to default!")
            defaultView = view
            handleActivateViewRequest(view)
        }
    }

    function handleActivateViewRequest(view) {
        console.debug(`Handling activate view request: view=${view.viewProperties.name}`)
        if (activeView) {
            activeView.visible = false
        }
        view.visible = true
        activeView = view
        navigationSidebar.activateButton(view)
    }

    function handleCloseViewRequest(view) {
        console.debug(`Handling close view request: view=${view.viewProperties.name}`)

        if(view === defaultView) {
            console.warn("Unable to close default view")
        } else {
            if(view.viewProperties.confirmOnClose) {
                closeConfirmationDialog.openDialog(view)
            } else {
                closeView(view)
            }
        }
    }

    function closeView(view) {
        console.debug(`Closing view: view=${view.viewProperties.name}`)
        closeViewRequested(view)

        if(view === activeView) {
            handleActivateViewRequest(defaultView)
        }

        navigationSidebar.removeButton(view)
        view.destroy()
    }
}

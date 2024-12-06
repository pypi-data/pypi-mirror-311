// Copyright (C) 2024 twyleg
import QtQuick 2.15

Item {
    id: sliderSpinBoxHighlightedBackground

    property var highlights
    property list<Rectangle> highlightRectangles

    property var alignment
    property var from
    property var to

    width: parent ? parent.width : 0
    height: parent ? parent.height : 0

    onWidthChanged: updateHighlights()
    onHeightChanged: updateHighlights()
    onParentChanged: {
        tryToInheritParametersFromParent()
        updateHighlights()
    }

    onHighlightsChanged: {
        clearHighlights()
        initHighlights()
        updateHighlights()
    }

    function pointToPixel(point) {
        var sliderDelta = to - from

        if(alignment === Qt.Vertical) {
            var factor = height / sliderDelta
            return height - (point - from) * factor
        } else {
            var factor = width / sliderDelta
            return (point - from) * factor
        }
    }

    function tryToInheritParametersFromParent() {
        if (parent) {
            if (parent.alignment !== undefined && sliderSpinBoxHighlightedBackground.alignment === undefined) {
                sliderSpinBoxHighlightedBackground.alignment = Qt.binding(function() { return parent.alignment })
                console.debug(`Inherited "alignment" from parent:  ${sliderSpinBoxHighlightedBackground.alignment}`)
            }
            if (parent.from !== undefined && sliderSpinBoxHighlightedBackground.from === undefined) {
                sliderSpinBoxHighlightedBackground.from = Qt.binding(function() { return parent.from })
                console.debug(`Inherited "from" from parent:  ${sliderSpinBoxHighlightedBackground.from}`)
            }
            if (parent.to !== undefined && sliderSpinBoxHighlightedBackground.to === undefined) {
                sliderSpinBoxHighlightedBackground.to = Qt.binding(function() { return parent.to })
                console.debug(`Inherited "to" from parent:  ${sliderSpinBoxHighlightedBackground.to}`)
            }
        }
    }

    function clearHighlights() {
        for(var i=0; i<highlightRectangles.length; i++) {
            var hightlightRectangle = highlightRectangles[i]
            hightlightRectangle.destroy()
        }
        highlightRectangles = []
    }

    function updateHighlights() {

        if (highlights.length !== highlightRectangles.length) {
            return
        }

        for(var i=0; i<highlights.length; i++) {
            var highlight = highlights[i]
            var highlightRectangle = highlightRectangles[i]

            var from = highlight[0]
            var to = highlight[1]

            var pixelFrom = pointToPixel(from)
            var pixelTo = pointToPixel(to)

            if(alignment === Qt.Vertical) {
                var height = pixelFrom - pixelTo
                highlightRectangle.y = pixelFrom - height
                highlightRectangle.height = height

                highlightRectangle.anchors.left = left
                highlightRectangle.anchors.right = right
            } else if(alignment === Qt.Horizontal){
                highlightRectangle.x = pixelFrom
                highlightRectangle.width = pixelTo - pixelFrom

                highlightRectangle.anchors.top = top
                highlightRectangle.anchors.bottom = bottom
            }
        }
    }

    function initHighlights() {

        for(var i=0; i<highlights.length; i++) {
            var zone = highlights[i]
            var value = zone[2]

            var component =  Qt.createComponent("QtQuick", "Rectangle", Component.PreferSynchronous, sliderSpinBoxHighlightedBackground)
            var obj = component.createObject(sliderSpinBoxHighlightedBackground, {
                "color": value ? "green" : "red"
            })

            highlightRectangles.push(obj)
        }
    }

    Component.onCompleted: {
        initHighlights()
        updateHighlights()
    }
}

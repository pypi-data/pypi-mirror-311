// Copyright (C) 2024 twyleg
import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: doubleSpinBox

    property double value: 1.0
    property double from: 0.0
    property double to: 1.0
    property double stepSize: 0.1
    property alias editable: spinBox.editable

    property int decimals: 2
    readonly property int decimalFactor: Math.pow(10, decimals)


    SpinBox {
        id: spinBox

        from: decimalToInt(doubleSpinBox.from)
        to: decimalToInt(doubleSpinBox.to)
        stepSize: decimalToInt(doubleSpinBox.stepSize)
        value: 0

        editable: true
        anchors.fill: parent

        validator: DoubleValidator {
            bottom: Math.min(spinBox.from, spinBox.to)
            top:  Math.max(spinBox.from, spinBox.to)
            decimals: doubleSpinBox.decimals
            notation: DoubleValidator.StandardNotation
        }

        textFromValue: function(value, locale) {
            return Number(value / doubleSpinBox.decimalFactor).toLocaleString(locale, 'f', doubleSpinBox.decimals)
        }

        valueFromText: function(text, locale) {
            return Math.round(Number.fromLocaleString(locale, text) * doubleSpinBox.decimalFactor)
        }

        onValueChanged: {
            var decimalValue = intToDecimal(value)
            doubleSpinBox.update(decimalValue)
        }
    }

    onValueChanged: {
        spinBox.value = decimalToInt(value)
    }

    function decimalToInt(decimal) {
        return decimal * decimalFactor
    }

    function intToDecimal(num) {
        return num / decimalFactor
    }

    function update(newValue: double) {
        if(Math.abs(value - newValue) >= stepSize * 0.9) {
            value = newValue
        }
    }
}



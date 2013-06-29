var myModule = angular.module("createReceiptApp", [])

myModule.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

myModule.factory('receiptItemsService', function() {
    var service = {};

    service.receiptItems = [];

    service.addItem = function(name, amount) {
        var newItem = {
            name: name, 
            amount: amount 
        };
        service.receiptItems.push(newItem);
    };

    return service;
});

function ReceiptItemCtrl($scope, receiptItemsService) {
    $scope.receiptItems = receiptItemsService.receiptItems

    $scope.getSummary = function() {
        var summary = 0;
        angular.forEach($scope.receiptItems, function(item) {
            summary = summary + item.amount;
        });
        return summary;
    };

    $scope.addItem = function() {
        var name = $scope.formReceiptItemName;
        var amount = parseInt($scope.formReceiptItemAmount);
        receiptItemsService.addItem(name, amount);
        $scope.formReceiptItemName = '';
        $scope.formReceiptItemAmount = '';
        $("#formReceiptItemName").focus();
    };

    $scope.removeItem = function() {
        if(confirm('Are you sure you want to delete this item?')) {
            var index = $scope.receiptItems.indexOf(this.item);
            $scope.receiptItems.splice(index, 1);
        }
    };
};


function InvoiceItemCtrl($scope, receiptItemsService) {
    $scope.invoiceItems = [
        {name:"pay for fees", amount:30000},
        {name:"pay for fun", amount:1000},
        {name:"ballet class", amount:3000},
        {name:"piano class", amount:1000},
    ];

    $scope.copyToReceipt = function() {
        var name = this.item.name;
        var amount = this.item.amount;
        receiptItemsService.addItem(name, amount);
    };
};

var myModule = angular.module("createReceiptApp", [])

myModule.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

function ReceiptItemCtrl($scope) {
    $scope.receiptItems = [
        {name:"pay for fees", amount:10000},
        {name:"pay for fun", amount:1000},
    ];

    $scope.getSummary = function() {
        var summary = 0;
        angular.forEach($scope.receiptItems, function(item) {
            summary = summary + item.amount;
        });
        return summary;
    };

    $scope.addItem = function() {
        var newItem = {
            name: $scope.formReceiptItemName, 
            amount: parseInt($scope.formReceiptItemAmount)
        };
        $scope.receiptItems.push(newItem);
        $scope.formReceiptItemName = '';
        $scope.formReceiptItemAmount = '';
        $("#formReceiptItemName").focus();
    };

    $scope.removeItem = function() {
        if(confirm('Are you sure you want to delete this item?')) {
            var index = $scope.receiptItems.indexOf(this.item);
            $scope.receiptItems.splice(index);
        }
    };
};


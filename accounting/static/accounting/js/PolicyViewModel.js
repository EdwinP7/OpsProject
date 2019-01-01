// Reference: https://knockoutjs.com/documentation/extenders.html
ko.extenders.required = function(target, overrideMessage) {
    //add some sub-observables to our observable
    target.hasError = ko.observable();
    target.validationMessage = ko.observable();
 
    //define a function to do validation
    function validate(newValue) {
       target.hasError(newValue ? false : true);
       target.validationMessage(newValue ? "" : overrideMessage || "This field is required");
    }
 
    //initial validation
    validate(target());
 
    //validate whenever the value changes
    target.subscribe(validate);
 
    //return the original observable
    return target;
};

function PolicyViewModel(policy_id, date) {
    this.policy_id = ko.observable(policy_id).extend({ required: "Please enter a policy number" });
    this.date = ko.observable(date).extend({ required: "Please enter a date" });
}

ko.applyBindings(new PolicyViewModel(1, '2015-05-01'));
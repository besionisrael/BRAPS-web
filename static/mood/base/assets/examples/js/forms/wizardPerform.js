(function (global, factory) {
    if (typeof define === "function" && define.amd) {
      define('/forms/wizard', ['jquery', 'Site'], factory);
    } else if (typeof exports !== "undefined") {
      factory(require('jquery'), require('Site'));
    } else {
      var mod = {
        exports: {}
      };
      factory(global.jQuery, global.Site);
      global.formsWizard = mod.exports;
    }
  })(this, function (_jquery, _Site) {
    'use strict';
  
    var _jquery2 = babelHelpers.interopRequireDefault(_jquery);
  
    (0, _jquery2.default)(document).ready(function ($$$1) {
      (0, _Site.run)();
    });
  
 
    // Example Wizard Form Container
    // -----------------------------
    // http://formvalidation.io/api/#is-valid-container
    (function () {
      var defaults = Plugin.getDefaults("wizard");
      var options = _jquery2.default.extend(true, {}, defaults, {
        onInit: function onInit() {
          (0, _jquery2.default)('#exampleFormContainer').formValidation({
            framework: 'bootstrap',
            fields: {
              username: {
                validators: {
                  notEmpty: {
                    message: 'The username is required'
                  }
                }
              },
              password: {
                validators: {
                  notEmpty: {
                    message: 'The password is required'
                  }
                }
              },
              number: {
                validators: {
                  notEmpty: {
                    message: 'The credit card number is not valid'
                  }
                }
              },
              cvv: {
                validators: {
                  notEmpty: {
                    message: 'The CVV number is required'
                  }
                }
              }
            },
            err: {
              clazz: 'invalid-feedback'
            },
            control: {
              // The CSS class for valid control
              valid: 'is-valid',
  
              // The CSS class for invalid control
              invalid: 'is-invalid'
            },
            row: {
              invalid: 'has-danger'
            }
          });
        },
        validator: function validator() {
          var fv = (0, _jquery2.default)('#exampleFormContainer').data('formValidation');
  
          var $this = (0, _jquery2.default)(this);
  
          // Validate the container
          fv.validateContainer($this);
  
          var isValidStep = fv.isValidContainer($this);
          if (isValidStep === false || isValidStep === null) {
            return false;
          }
  
          return true;
        },
        onFinish: function onFinish() {
          
          document.getElementById("exampleFormContainer").submit();
        },
        buttonsAppendTo: '.panel-body'
      });
  
      (0, _jquery2.default)("#exampleWizardFormContainer").wizard(options);
    })();
  
    // Example Wizard Pager
    // --------------------------
    (function () {
      var defaults = Plugin.getDefaults("wizard");
  
      var options = _jquery2.default.extend(true, {}, defaults, {
        step: '.wizard-pane',
        templates: {
          buttons: function buttons() {
            var options = this.options;
            var html = '<div class="btn-group btn-group-sm btn-group-flat">' + '<a class="btn btn-default" href="#' + this.id + '" data-wizard="back" role="button">' + options.buttonLabels.back + '</a>' + '<a class="btn btn-success btn-outline float-right" href="#' + this.id + '" data-wizard="finish" role="button">' + options.buttonLabels.finish + '</a>' + '<a class="btn btn-default btn-outline float-right" href="#' + this.id + '" data-wizard="next" role="button">' + options.buttonLabels.next + '</a>' + '</div>';
            return html;
          }
        },
        buttonLabels: {
          next: '<i class="icon md-chevron-right" aria-hidden="true"></i>',
          back: '<i class="icon md-chevron-left" aria-hidden="true"></i>',
          finish: '<i class="icon md-check" aria-hidden="true"></i>'
        },
        onFinish: function onFinish() {
          alert('finish');
        },  
        buttonsAppendTo: '.panel-actions'
      });
  
      (0, _jquery2.default)("#exampleWizardPager").wizard(options);
    })();
  
 
  });
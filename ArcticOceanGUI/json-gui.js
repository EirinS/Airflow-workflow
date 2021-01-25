angular.module("templateCache", []).run(["$templateCache", function($templateCache) {$templateCache.put("datetime/datetime.html","<div class=\"row parameter-row\">\n    <div class=\"col-xs-6 col-md-3 col-md-offset-3 par-name-col\">\n        {{parameter.displayName}}\n    </div>\n    <div class=\"col-xs-6 col-md-3 par-value-col datetime-col\" ng-class=\"{\'has-error\': !isParameterValid}\">\n        <input ng-if=\"parameter.hasDate\" type=\"date\" ng-model=\"parameter.value\" class=\"form-control\" ng-disabled=\"parameter.disabled\">\n        <input ng-if=\"parameter.hasTime\" type=\"time\" step=\"60\" ng-model=\"parameter.value\" class=\"form-control\" ng-disabled=\"parameter.disabled\">\n        <div class=\"error-message\" ng-repeat=\"msg in parameter.message\">{{msg}}</div>\n    </div>\n</div>\n");
$templateCache.put("domains/domains.html","<div class=\"row parameter-row\">\n\n    <div class=\"col-xs-12 col-md-6 col-md-offset-3 par-name-col map-container ng-binding\" ng-class=\"{\'disabled\' : parameter.disabled}\">\n        <div style=\"width:100%;height:{{height}}\" id=\"{{parameter.dbName}}map\" ng-class=\"{\'map-has-error\' : !isParameterValid}\"></div>\n        <div class=\"error-message\" ng-repeat=\"msg in parameter.message\">{{msg}}</div>\n        <div ng-show=\"parameter.drawDomains\" ng-repeat=\"val in parameter.value.domains track by $index\">\n            Domain number {{$index+1}} - South-West: ({{val.southWest.lat | number:4}}, {{val.southWest.long | number:4}}) North-East: ({{val.northEast.lat | number:4}}, {{val.northEast.long | number:4}})<br/>\n        </div>\n        <div ng-show=\"parameter.drawMarkers\" ng-repeat=\"mark in parameter.value.markers track by $index\">\n            Marker {{$index+1}}: ({{mark.lat | number:4}}, {{mark.long | number:4}})\n        </div>\n\n    </div>\n    <div class=\"modal fade\" id=\"{{parameter.dbName}}modal\">\n        <div class=\"modal-dialog\">\n            <div class=\"modal-content\">\n                <div class=\"modal-header\">\n                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n                    <h4 class=\"modal-title\">Delete domain</h4>\n                </div>\n                <div class=\"modal-body\">\n                    <p>Do you want to delete domain number <span id=\"number\"></span><span ng-if=\"parameter.onlyNested\" id=\"lastDomain\"> and all his sub-domains</span>?</p>\n                </div>\n                <div class=\"modal-footer\">\n                    <button type=\"button\" class=\"btn btn-warning\" data-dismiss=\"modal\">No</button>\n                    <button type=\"button\" class=\"btn btn-success\">Yes</button>\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n");
$templateCache.put("float/float.html","<div class=\"row parameter-row\">\n    <div class=\"col-xs-6 col-md-3 col-md-offset-3 par-name-col\">\n        {{parameter.displayName}}\n    </div>\n    <div class=\"col-xs-6 col-md-3 par-value-col\" ng-class=\"{\'has-error\': !isParameterValid}\">\n        <input type=\"number\" step=\"1\" ng-model=\"parameter.value\" class=\"form-control\" ng-disabled=\"parameter.disabled\">\n        <div class=\"error-message\" ng-repeat=\"msg in parameter.message\">{{msg}}</div>\n    </div>\n</div>\n");
$templateCache.put("integer/integer.html","<div class=\"row parameter-row\">\n    <div class=\"col-xs-6 col-md-3 col-md-offset-3 par-name-col\">\n        {{parameter.displayName}}\n    </div>\n    <div class=\"col-xs-6 col-md-3 par-value-col\" ng-class=\"{\'has-error\': !isParameterValid}\">\n        <input type=\"number\" step=\"1\" ng-model=\"parameter.value\" class=\"form-control\" ng-disabled=\"parameter.disabled\">\n        <div class=\"error-message\" ng-repeat=\"msg in parameter.message track by $index\">{{msg}}</div>\n    </div>\n</div>\n");
$templateCache.put("json-gui/json-gui.html","<div class=\"container-fluid\" id=\"model-container\">\n    <div class=\"row\">\n        <div class=\"col-xs-12 col-md-10 groups\">\n            <div ng-repeat=\"group in data.parametersCategories\">\n                <div class=\"row group-container\">\n                    <div class=\"group-name\" id=\"group{{group.value}}\">\n                        {{group.name}}\n                    </div>\n                    <div class=\"group-parameters col-xs-12\">\n                        <div ng-repeat=\"(key, value) in hashToArray(pars)\">\n                            <integer json-input ng-if=\"pars[value].parameterCategory==group.value && pars[value].parameterType==\'integer\'\" parameter=\"pars[value]\" dependencies = \"dep[value]\"></integer>\n                            <float json-input ng-if=\"pars[value].parameterCategory==group.value && pars[value].parameterType==\'float\'\" parameter=\"pars[value]\" dependencies = \"dep[value]\"></float>\n                            <datetime json-input ng-if=\"pars[value].parameterCategory==group.value && pars[value].parameterType==\'datetime\'\" parameter=\"pars[value]\" dependencies = \"dep[value]\"></datetime>\n                            <select-parameter json-input ng-if=\"pars[value].parameterCategory==group.value && pars[value].parameterType==\'select\'\" parameter=\"pars[value]\" dependencies =\" dep[value]\"></select-parameter>\n                            <text-parameter json-input ng-if=\"pars[value].parameterCategory==group.value && pars[value].parameterType==\'text\'\" parameter=\"pars[value]\" dependencies = \"dep[value]\"></text-parameter>\n                            <domains json-input ng-if=\"pars[value].parameterCategory==group.value && pars[value].parameterType==\'domains\'\" parameter=\"pars[value]\" dependencies = \"dep[value]\"></domains>\n                            <fileupload json-input ng-if=\"pars[value].parameterCategory==group.value && pars[value].parameterType==\'fileupload\'\" parameter=\"pars[value]\" dependencies = \"dep[value]\"></fileupload>\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div class=\"col-md-2\" id=\"scrollspy\" style=\"padding-left:0px\">\n            <ul id=\"nav\" class=\"nav hidden-xs hidden-sm\" style=\"margin-top:20px;width:100%;padding-left:10px; border-left:1px solid #dedede;\">\n                <li ng-repeat=\"group in data.parametersCategories\">\n                    <a href=\"#group{{group.value}}\">{{group.name}}</a>\n                </li>\n            </ul>\n        </div>\n    </div>\n</div>\n");
$templateCache.put("fileupload/fileupload.html","<div class=\"row parameter-row\" id=\"{{parameter.dbName}}\">\n    <div class=\"col-xs-6 col-md-3 col-md-offset-3 par-name-col upload-name-col\">\n        {{parameter.displayName}}\n    </div>\n    <div class=\"col-xs-6 col-md-3 par-value-col file-container\" ng-class=\"{\'has-error\': !isParameterValid, \'disabled\' : parameter.disabled}\">\n        <!--        <div ngf-drop ngf-select ng-model=\"file\" class=\"drop-box\" ngf-drag-over-class=\"dragover\" ngf-multiple=\"true\" ngf-allow-dir=\"false\" accept=\"image/*,application/pdf\" ngf-pattern=\"\'image/*,application/pdf\'\">Drop Namelist</div>-->\n\n        <form  action=\"upload.php\" method=\"POST\" enctype=\"multipart/form-data\">\n\n            <fieldset>\n                <div>\n                    <input type=\"file\" id=\"fileselect\" name=\"fileselect[]\" multiple=\"multiple\"  style=\"visibility:hidden\"/>\n                    <div id=\"filedrag\" ng-click=\"openInput()\">Click or drop files here</div>\n                </div>\n                <div class=\"error-message\" ng-repeat=\"msg in parameter.message\">{{msg}}</div>\n                <div class=\"error-message\">\n                    <div ng-repeat=\"val in errorUpload\">{{val}}\n                    </div>\n                </div>\n                 <div class=\"success-message\" ng-show=\"parameter.value.length!=0\">\n                   Uploaded files:\n                   <ul>\n                    <li ng-repeat=\"file in parameter.value track by $index\">\n                        <span class=\"uploaded-file\">{{file.fileName}}</span>&nbsp;&nbsp;&nbsp;<span ng-if=\"!parameter.disabled\" ng-click=\"removeFile($index)\" class=\"file-unload\">Remove</span>\n                    </li>\n                  </ul>\n                </div>\n            </fieldset>\n\n        </form>\n    </div>\n    <!--\n<div class=\"modal fade\" id=\"modal\">\n<div class=\"modal-dialog\">\n<div class=\"modal-content\">\n<div class=\"modal-header\">\n<button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n<h4 class=\"modal-title\">Warning</h4>\n</div>\n<div class=\"modal-body\">\n</div>\n<div class=\"modal-footer\">\n<button type=\"button\" class=\"btn btn-warning\" data-dismiss=\"modal\">Ok</button>\n</div>\n</div>\n</div>\n</div>\n\n-->\n\n\n</div>\n");
$templateCache.put("select/select.html","<div class=\"row parameter-row\">\n    <div class=\"col-xs-6 col-md-3 col-md-offset-3 par-name-col\">\n        {{parameter.displayName}}\n    </div>\n    <div class=\"col-xs-6 col-md-3 par-value-col\" ng-class=\"{\'has-error\': !isParameterValid}\">\n        <select ng-model=\"parameter.value\" ng-options=\"option.value as option.name for option in parameter.values\" class=\"form-control\" ng-disabled=\"parameter.disabled\"></select>\n        <div class=\"error-message\" ng-repeat=\"msg in parameter.message\">{{msg}}</div>\n    </div>\n</div>\n");
$templateCache.put("text/text.html","<div class=\"row parameter-row\">\n    <div class=\"col-xs-6 col-md-3 col-md-offset-3 par-name-col\">\n        {{parameter.displayName}}\n    </div>\n    <div class=\"col-xs-6 col-md-3 par-value-col\" ng-class=\"{\'has-error\': !isParameterValid}\">\n        <textarea ng-model=\"parameter.value\" ng-disabled=\"parameter.disabled\" class=\"form-control\" style=\"resize:none\"></textarea>\n        <div class=\"error-message\" ng-repeat=\"msg in parameter.message\">{{msg}}</div>\n    </div>\n</div>\n");}]);
var directives = angular.module('json-gui', ['ngFileUpload', 'templateCache']);

directives.directive('jsonInput', function() {
  return {
  controller: ["$element", function($element) {
      this.evaluate = function(parameter, dependencies){
          var bool = true;
          this.message = [];
          if(parameter.required){
            if(parameter.value==null || typeof(parameter.value)=="undefined" || parameter.value==""){
              this.message.push("This field is required");
              bool = false;
            }
          }
          var validationFunction = new Function("return function v(parameter, dependencies){var isValid = {valid:true, message:''};"+this.isValid+" return isValid;}")();
          var validation = validationFunction(parameter, dependencies);
          if(!validation.valid){
              this.message.push(validation.message);
              bool = false;
          }
          return {message:this.message, isValid:bool};
      }
  }]
}
});

directives.directive('datetime', function() {
  return {
    restrict: 'E',
    templateUrl: 'datetime/datetime.html',
    replace: true,
    require: '^jsonInput',
    scope: {
      parameter:"=",
      dependencies:"=",
    },
    link:function(scope, elm, attr, jsonInputCtrl) {
      scope.parameter.value = new moment(scope.parameter.value).toDate();
      scope.timeValid = function(){
        // if(typeof(scope.parameter.value)==="undefined" || scope.parameter.value=="Invalid Date"){
        //   scope.parameter.message.push("Select a valid date");
        //   return false;
        // }
        return true;
      }


      scope.message = [];
      jsonInputCtrl.isValid = scope.parameter.isValid;
      scope.validationFunction = jsonInputCtrl.validationFunction;

      scope.parameter.evaluate = function() {
        scope.parameter.message = [];
        var a = jsonInputCtrl.evaluate(scope.parameter, scope.dependencies);
        for(var i=0; i<a.message.length;i++)
        scope.parameter.message.push(a.message[i]);
        var valid =  scope.timeValid();
        valid =  a.isValid && valid;
        scope.isParameterValid = valid;
        return valid;
      }

      scope.$watch('parameter.value', function(){
        scope.parameter.evaluate();
      });
    }
  };
});

directives.directive('integer', function() {
    return {
        restrict: 'E',
        templateUrl: 'integer/integer.html',
        replace: true,
        require: '^jsonInput',
        scope: {
            parameter:"=",
            dependencies:"=",
        },
        link:function(scope, elm, attr, jsonInputCtrl) {
          scope.integerValid = function(){
            if(scope.parameter.value % 1 !== 0 || scope.parameter.value ==="NaN" || typeof(scope.parameter.value) =="undefined"){
              scope.parameter.message.push("Number is not an Integer");
              return false;
            }
              return true;
          }

          scope.message = [];
          jsonInputCtrl.isValid = scope.parameter.isValid;
          scope.validationFunction = jsonInputCtrl.validationFunction;

          scope.parameter.evaluate = function() {
            scope.parameter.message = [];
            var a = jsonInputCtrl.evaluate(scope.parameter, scope.dependencies);
            for(var i=0; i<a.message.length;i++)
              scope.parameter.message.push(a.message[i]);
            var valid =  scope.integerValid();
            valid =  a.isValid && valid;
            scope.isParameterValid = valid;
            return valid;
          }

          scope.$watch('parameter.value', function(){
            scope.parameter.evaluate();
          });

        }
    };
});

directives.directive('fileupload', ["$timeout", "Upload", function($timeout, Upload) {
  return {
    restrict: 'E',
    templateUrl: 'fileupload/fileupload.html',
    replace: true,
    require: '^jsonInput',
    scope: {
      parameter:"=",
      dependencies:"=",
    },
    link:function(scope, elm, attr, jsonInputCtrl) {
      var num = scope.parameter.dbName;
      /**************** VALIDATION ******************/
      scope.fileuploadValid = function(){
        if(typeof(scope.parameter.value)=="undefined" || scope.parameter.value.length<scope.parameter.minUpload) {
          var msg = "Upload at least "+scope.parameter.minUpload;
          msg+= (scope.parameter.minUpload==1)? " file" : " files";
          scope.parameter.message.push(msg);
          return false;
        }
        return true;
      }
      /**************** EVALUATION ******************/

      scope.message = [];
      jsonInputCtrl.isValid = scope.parameter.isValid;
      scope.validationFunction = jsonInputCtrl.validationFunction;

      scope.parameter.evaluate = function() {
        scope.parameter.message = [];
        var a = jsonInputCtrl.evaluate(scope.parameter, scope.dependencies);
        for(var i=0; i<a.message.length;i++)
        scope.parameter.message.push(a.message[i]);
        var valid =  scope.fileuploadValid();
        valid =  a.isValid && valid;
        scope.isParameterValid = valid;
        return valid;
      }

      scope.$watch('parameter.value', function(){
        scope.parameter.evaluate();
      }, true);



      scope.initFileReader = function (){
        if (window.File && window.FileList && window.FileReader) {
          scope.init();
        }
      }
      // initialize
      scope.init = function() {
        scope.maxLengthByte = calculateLength(scope.parameter.maxSize);
        var form = $("#"+scope.parameter.dbName);
        var fileselect =  form.find("#fileselect")[0];
        var filedrag =  form.find("#filedrag")[0];
        //                scope.modal = form.find("#modal");

        // file select
        fileselect.addEventListener("change", scope.fileSelectHandler, false);

        // is XHR2 available?
        var xhr = new XMLHttpRequest();
        if (xhr.upload) {

          // file drop
          filedrag.addEventListener("dragover", scope.fileDragHover, false);
          filedrag.addEventListener("dragleave", scope.fileDragHover, false);
          filedrag.addEventListener("drop", scope.fileSelectHandler, false);
          filedrag.style.display = "block";

          // remove submit button
        }
      }

      scope.fileDragHover = function(e) {
        e.stopPropagation();
        e.preventDefault();
        e.target.className = (e.type == "dragover" ? "hover" : "");
      }


      scope.parseFile = function(file) {
        if(!scope.fileHasAllowedExtension(file)){
          errorUpload("This extension is not allowed. Allowed extensions are: "+scope.parameter.allowedExtensions);
          return;
        }
        if(file.size>scope.maxLengthByte) {
          errorUpload("The file named "+file.name+" is too big. The maximum dimension accepted is "+scope.parameter.maxSize+".");
          return;
        }
        if(fileAlreadyUploaded(file.name)){
          errorUpload("You already uploaded a file with name "+file.name+".");
          return;
        }
        var reader = new FileReader();
        reader.onload = function(e) {
          var paramFile = {fileName: file.name, data: e.target.result};
          $timeout(function(){scope.parameter.value.push(paramFile)});
        };
        reader.readAsDataURL(file);
        $timeout(function() {
          scope.uploadedFilesDescription.push(file);

        });


      }

      scope.fileSelectHandler = function(e) {
        scope.fileDragHover(e);
        var files = e.target.files || e.dataTransfer.files;
        if(scope.uploadedFilesDescription.length+files.length>scope.parameter.maxUpload){
          errorUpload("Reached maximum file uploads allowed ("+scope.parameter.maxUpload+").");
          return;
        }

        for (var i = 0, f; f = files[i]; i++) {
          scope.parseFile(f);
        }

      }


      scope.openInput = function(){
        if(scope.parameter.disabled) return;
        $('#'+scope.parameter.dbName).find('#fileselect').click();
      }
      var calculateLength = function(length){
        length = length.toLowerCase();
        var retLength = parseInt(length);
        if(length.indexOf("kb")>0)
        return retLength*1000;
        if(length.indexOf("mb")>0)
        return retLength*1000000;
        if(length.indexOf("gb")>0)
        return retLength*1000000000;
        return retLength;
      }
      //            scope.openModal = function(message){
      //                console.log(scope.modal[0]);
      //                scope.modal.find(".modal-body").text(message);
      //                console.log(scope.modal.find(".modal-body").text());
      //                scope.modal.modal('show');
      //                console.log("show");
      //            }

      var errorUpload = function(message) {
        $timeout(function(){scope.errorUpload.splice(0, 0, message);});
        $timeout(function(){scope.errorUpload.splice(0,1)},5000);
      }

      scope.removeFile = function(index){
        scope.parameter.value.splice(index, 1);
        scope.uploadedFilesDescription.splice(index, 1);
      }

      scope.fileHasAllowedExtension = function(file){
        var exts = scope.parameter.allowedExtensions;
        if(typeof(exts)=='undefined') return true;
        if(typeof(exts)=='string' && exts!="") return file.name.endsWith('.'+exts);
        if(Array.isArray(exts)){
          for(var i=0;i<exts.length;i++)
          if(file.name.endsWith('.'+exts[i]))
          return true;
          return false;
        }

        return true;
      }
      var fileAlreadyUploaded = function(fileName){
        for(var i=0;i<scope.parameter.value.length;i++)
          if(scope.parameter.value[i].fileName.localeCompare(fileName)==0) return true;
        return false;
      }

      scope.errorUpload = [];
      scope.uploadedFilesDescription = [];
      $timeout(function(){
        if(scope.parameter.disabled) return;
        scope.initFileReader();
      });
    }
  }



}]);

directives.directive('float', function() {
    return {
        restrict: 'E',
        templateUrl: 'float/float.html',
        replace: true,
        require: '^jsonInput',
        scope: {
            parameter:"=",
            dependencies:"=",
        },
        link:function(scope, elm, attr, jsonInputCtrl) {
            scope.floatValid = function(){
                if(typeof(scope.parameter.value) === 'undefined' || scope.parameter.value ==="NaN"){
                    scope.parameter.message.push("Number format is not valid");
                    return false;
                }
                return true;
            }
            scope.message = [];
            jsonInputCtrl.isValid = scope.parameter.isValid;
            scope.validationFunction = jsonInputCtrl.validationFunction;

            scope.parameter.evaluate = function() {
              scope.parameter.message = [];
              var a = jsonInputCtrl.evaluate(scope.parameter, scope.dependencies);
              for(var i=0; i<a.message.length;i++)
                scope.parameter.message.push(a.message[i]);
              var valid =  scope.floatValid();
              valid =  a.isValid && valid;
              scope.isParameterValid = valid;
              return valid;
            }

            scope.$watch('parameter.value', function(){
              scope.parameter.evaluate();
            });
        }
    };
});

directives.directive('jsonGui', ["$timeout", function($timeout) {
    return {
        restrict: 'E',
        templateUrl: 'json-gui/json-gui.html',
        replace: true,
        scope: {
            data:"=",
        },
        link:function(scope,elm,attr) {
          /***
             VERY STUPID WORKAROUND FOR PLUNKER. THIS LINE IS NOT PRESENT IN THE PROJECT AND IS NOT NEEDED.
           ****/
           $timeout(function(){scope.data = scope.data},1);
           /***
             END OF VERY STUPID WORKAROUND FOR PLUNKER
           ****/
            scope.pars = [];
            scope.dep=[];
            scope.buildParametersArray = function(){
              try{
                var jsonPars = scope.data.parameters;
              } catch(error){console.log(error);}
                for(var par in jsonPars){
                    scope.pars[jsonPars[par].dbName] = jsonPars[par];
                }
            }
            $timeout(function(){
                $('#nav').affix({
                    offset: {
                    }
                });
                $('body').scrollspy({ target: '#scrollspy' })
            });

            scope.buildDependencies = function(){
                var currDeps;
                for(var par in scope.pars){ // par contiene il nome del parametro
                    var obj={};
                    currDeps = scope.pars[par].dependencies;
                    for(var i=0;i<currDeps.length;i++) {
                        obj[currDeps[i]] = scope.pars[currDeps[i]];
                    }
                    scope.dep[par] = obj;
                }
            }

            scope.saveConfiguration= function(){
              console.log(scope.pars["upload"].value);
                var namelist="";
                for(var par in scope.pars){
                    // console.log(scope.pars[par]);
                    // console.log(par);

                    if(!scope.pars[par].evaluate()){
                        console.log("Error in some parameter");
                        return;
                    }
                    var functionBody = scope.buildComputingFunction(par);
                    namelist+= scope.pars[par].displayName+": "+ eval(functionBody)+";\n";
                }
                console.log(namelist);
            }

            /*
            This function is used to build two simpler object to be referred in the computedResult function: the parameter object, and the dependencies array.
            In this way, in the computedResult property of each parameter object in the json file, the current parameter and its dependencies can be referred in a simpler way.
            */
            scope.buildComputingFunction = function(par){
              var evalPrefix = "var parameter = scope.pars[par];";
              evalPrefix +=  "var dependencies = [];"
              scope.pars[par].dependencies.forEach(function(entry) {
                  evalPrefix += "dependencies['"+entry+"'] = scope.pars['"+entry+"'];";
              });
              return evalPrefix + "(function(){"+scope.pars[par].computedResult+"}())";
            };
            scope.hashToArray = function(items) {
                var result = [];
                var i = 0;
                for(item in items){
                    result[i] = item;
                    i++;
                }
                return result;
            }
            var computedResults  = function(){
              var results = [];
              var result;
              for(var par in scope.pars){
                  result = {};
                  if(!scope.pars[par].evaluate()){
                      console.log("Error in some parameter");
                      return;
                  }
                  var functionBody = scope.buildComputingFunction(par);
                   result.value = eval(functionBody);
                   result.name = scope.pars[par].dbName;
                   result.parameterType = scope.pars[par].parameterType;
                  results.push(result);
              }
              return results;
            };

            
scope.$watch(attr.data, function(data) {
  console.log("data was changed");
  console.log(attr.data);
  if(scope.data==undefined) return;
  scope.buildParametersArray();
  scope.buildDependencies();
  console.log("data is defined");
  scope.data.getComputedResults = function(){
    var results = [];
    var result;
    for(var par in scope.pars){
        result = {};
        if(!scope.pars[par].evaluate()){
            console.log("Error in some parameter");
            return;
        }
        var functionBody = scope.buildComputingFunction(par);
         result.value = eval(functionBody);
         result.name = scope.pars[par].dbName;
         result.parameterType = scope.pars[par].parameterType;
        results.push(result);
    }
    return results;
  };
}, true);


        }
    }
}]);

directives.directive('selectParameter', function() {
  return {
    restrict: 'E',
    templateUrl: 'select/select.html',
    replace: true,
    require: '^jsonInput',
    scope: {
      parameter:"=",
      dependencies:"=",
    },
    link:function(scope, elm, attr, jsonInputCtrl) {
      scope.selectValid = function(){
        return true;
      };

      scope.message = [];
      jsonInputCtrl.isValid = scope.parameter.isValid;
      scope.validationFunction = jsonInputCtrl.validationFunction;
      scope.parameter.evaluate = function() {
        scope.parameter.message = [];
        var a = jsonInputCtrl.evaluate(scope.parameter, scope.dependencies);
        for(var i=0; i<a.message.length;i++)
        scope.parameter.message.push(a.message[i]);
        var valid =  scope.selectValid();
        valid =  a.isValid && valid;
        scope.isParameterValid = valid;
        return valid;
      }

      scope.$watch('parameter.value', function(){
        scope.parameter.evaluate();
      });
    }
  };
});

directives.directive('textParameter', function() {
    return {
        restrict: 'E',
        templateUrl: 'text/text.html',
        replace: true,
        require: '^jsonInput',
        scope: {
            parameter:"=",
            dependencies:"=",
        },
        link:function(scope, elm, attr, jsonInputCtrl) {
            scope.textValid = function(){
                return true;
            }
            scope.message = [];
            jsonInputCtrl.isValid = scope.parameter.isValid;
            scope.validationFunction = jsonInputCtrl.validationFunction;

            scope.parameter.evaluate = function() {
              scope.parameter.message = [];
              var a = jsonInputCtrl.evaluate(scope.parameter, scope.dependencies);
              for(var i=0; i<a.message.length;i++)
                scope.parameter.message.push(a.message[i]);
              var valid =  scope.textValid();
              valid =  a.isValid && valid;
              scope.isParameterValid = valid;
              return valid;
            }

            scope.$watch('parameter.value', function(){
              scope.parameter.evaluate();
            });

        }
    };
});
